from PyQt6.QtCore import Qt, QPoint, QRectF, QPointF
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem, \
    QGraphicsTextItem

from auxiliar.Calculate import Calculate
from components.ComponentsRemover import ComponentsRemover
from components.ComponentsSelector import ComponentsSelector
from components.Latex import Latex
from drawables.Draw import Draw
from drawables.DrawAuxiliar import DrawAuxiliar
from drawables.DrawComponent import DrawComponent
from objects.Components import ObjComponent, ObjScales
from objects.Tools import ObjTool
from ui.Resources import Resources


def contain_item(drawables, item):
    if item in drawables:
        return drawables
    return []


class Canvas(QGraphicsView):

    def __init__(self, cord, tool_selected, components, label_component,
                 button_label_edit, button_delete, button_flip_horizontal,
                 button_flip_vertical, button_rotate_no_clock, button_rotate_clock,
                 manager_components, history):
        super().__init__()

        self.resources = Resources()
        self.setBackgroundBrush(self.resources.get_color_canvas())
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMouseTracking(True)

        self.current_label = label_component
        self.button_label_edit = button_label_edit
        self.button_flip_horizontal = button_flip_horizontal
        self.button_flip_vertical = button_flip_vertical
        self.button_rotate_no_clock = button_rotate_no_clock
        self.button_rotate_clock = button_rotate_clock
        self.button_delete = button_delete

        # Inicializar el punto del mouse como None
        self.mouse_point = None

        self.draw_component = DrawComponent(self.scene)
        self.draw_auxiliar = DrawAuxiliar(self)
        self.draw = Draw(self.scene)
        self.calculate = Calculate()
        self.latex_gen = Latex()
        self.cell_size = 50

        self.cord = cord
        self.tool : ObjTool = tool_selected
        self.components : list[ObjComponent]= components

        self.components_selector = ComponentsSelector()
        self.components_remover = ComponentsRemover(history)
        self.manager_components = manager_components

        self.current_tool_shadow = None
        self.rect_select = None
        self.start_point = None
        self.end_point = None

        # Dibujar la cuadrícula de fondo
        self.draw_auxiliar.draw_grid()

        # Definir los límites de zoom
        self.min_scale = 0.6
        self.max_scale = 1.5
        self.space_pressed = False

        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        horizontal_scrollbar = self.horizontalScrollBar()
        vertical_scrollbar = self.verticalScrollBar()
        horizontal_scrollbar.valueChanged.connect(self.scroll_value_changed)
        vertical_scrollbar.valueChanged.connect(self.scroll_value_changed)

        # self.setRenderHint(QPainter.RenderHint.Antialiasing)

    def leaveEvent(self, event):
        self.cord.setText("")
        self.draw_auxiliar.remove_point_cursor()
        self.draw_auxiliar.remove_shadow()

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor

        current_scale = self.transform().m11()
        if self.min_scale < current_scale * factor < self.max_scale:
            self.scale(factor, factor)

    def keyPressEvent(self, event):

        if event.key() == Qt.Key.Key_Space:
            self.space_pressed = True

    def keyReleaseEvent(self, event):

        if event.key() == Qt.Key.Key_Space:
            self.space_pressed = False

        if event.key() == Qt.Key.Key_Delete:
            self.components_remover.delete_selected(self)

    def mousePressEvent(self, event):

        if self.dragMode() == QGraphicsView.DragMode.NoDrag:
            real_pos = self.mapToScene(event.pos())

            cord_x = round((real_pos.x() / self.cell_size) * 2) / 2
            cord_y = round((real_pos.y() / self.cell_size) * 2) / 2

            self.start_point = QPoint(
                int(cord_x * self.cell_size),
                int(cord_y * self.cell_size))
            self.end_point = QPoint(
                int(cord_x * self.cell_size),
                int(cord_y * self.cell_size))

        if event.button() == Qt.MouseButton.LeftButton and self.space_pressed:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.draw_auxiliar.remove_point_cursor()
            self.draw_auxiliar.remove_shadow()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        if self.dragMode() == QGraphicsView.DragMode.NoDrag:

            real_pos = self.mapToScene(event.pos())

            cord_x = round((real_pos.x() / self.cell_size) * 2) / 2
            cord_y = round((real_pos.y() / self.cell_size) * 2) / 2

            self.end_point = QPoint(
                int(cord_x * self.cell_size),
                int(cord_y * self.cell_size))

            name_class = self.tool.class_

            if name_class == 'None':

                self.components_selector.unselect(self)

                pos = self.mapToScene(event.pos())
                item = self.scene.itemAt(pos, self.transform())

                if item:
                    if not isinstance(item, QGraphicsTextItem):
                        select_component = None
                        for component in self.components:
                            selected_drawables = contain_item(component.draws, item)
                            if len(selected_drawables) > 0:
                                select_component = component

                        if select_component is not None:
                            self.components_selector.select(self, select_component)

            if self.start_point:

                if name_class == 'Traceable_Final':
                    path_svg = self.tool.canvas_stroke
                    self.manager_components.create_traceable_final(self, path_svg)

                if name_class == 'Traceable':
                    self.manager_components.create_traceable(self)

            if name_class == 'Transistor':
                path_svg = self.tool.canvas_stroke
                self.manager_components.create_transistor(self, self.end_point, path_svg)

            if name_class == 'Amplifier':
                path_svg = self.tool.canvas_stroke
                self.manager_components.create_amplifier(self, path_svg)

            if name_class == 'Transformer':
                path_svg = self.tool.canvas_stroke
                self.manager_components.create_transformer(self, path_svg)

        if self.dragMode() == QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)

        self.start_point = None

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.setMouseTracking(True)

        if self.dragMode() == QGraphicsView.DragMode.NoDrag:

            if self.tool.name != 'Select':
                self.cell_size = 50
                pos = self.mapToScene(event.pos())

                cord_x = round((pos.x() / self.cell_size) * 2) / 2
                cord_y = round((pos.y() / self.cell_size) * 2) / 2

                self.cord.setText("Coordinates: [" + str(cord_x) + "," + str(cord_y) + "]")

                x = cord_x * self.cell_size
                y = cord_y * self.cell_size
                name_class = self.tool.class_
                path_svg = self.tool.canvas_stroke

                self.draw_auxiliar.remove_point_cursor()
                self.draw_auxiliar.remove_shadow()

                if self.start_point:

                    if name_class == 'Traceable':

                        difference = self.calculate.difference(self.start_point, QPointF(x, y))

                        if difference > 40 or self.tool.name == 'Wire':

                            if self.tool.name != 'Wire':
                                self.current_tool_shadow = self.draw_component.two_pins(
                                    self.scene, self.devicePixelRatio(),
                                    self.start_point, QPointF(x, y),
                                    self.tool.canvas_stroke, self.tool.canvas_stroke_static, '',
                                    self.resources.get_color_shadow()
                                )
                            else:
                                self.current_tool_shadow = self.draw_component.two_pins_no_img(
                                    self.scene, self.start_point, QPointF(x, y),
                                    '', self.resources.get_color_shadow()
                                )

                    elif name_class == 'Traceable_Final':
                        self.current_tool_shadow = self.draw_component.one_pins(
                            self.devicePixelRatio(),
                            self.start_point, QPointF(x, y),
                            self.tool, '',
                            self.resources.get_color_shadow()
                        )

                elif name_class == 'Amplifier':
                    self.current_tool_shadow = self.draw.image_with_height(
                        self.devicePixelRatio(), path_svg,
                        125, 100, x, y, 0, self.resources.get_color_shadow()
                    )
                elif name_class == 'Transformer':
                    self.current_tool_shadow = self.draw.image_1(
                        self.devicePixelRatio(), path_svg,
                        100, QPointF(x, y), 0, self.resources.get_color_shadow()
                    )
                elif name_class == 'Transistor':
                    self.current_tool_shadow = self.draw.image(
                        self.devicePixelRatio(), path_svg, QPointF(x, y), QPointF(x, y),
                        0, self.resources.get_color_shadow(), ObjScales(1, 1)
                    )
                else:
                    self.mouse_point = self.draw_auxiliar.create_mouse_point(x, y)

        super().mouseMoveEvent(event)

    def scroll_value_changed(self):
        self.draw_auxiliar.remove_point_cursor()
        self.draw_auxiliar.remove_shadow()

    def enterEvent(self, event):
        self.setFocus()

    def set_tool(self, new_tool):
        self.tool = new_tool
