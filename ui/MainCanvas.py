from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem, \
    QGraphicsTextItem

from components.ComponentsRemover import ComponentsRemover
from components.ComponentsSelector import ComponentsSelector
from components.Latex import Latex
from drawables.DrawAuxiliar import DrawAuxiliar
from drawables.DrawComponent import DrawComponent


def contain_item(drawables, item):
    if item in drawables:
        return drawables
    return []


class Canvas(QGraphicsView):

    def __init__(self, cord, tool_selected, components, label_component,
                 button_label_edit, button_delete, manager_components, history):
        super().__init__()

        self.setBackgroundBrush(QColor(255, 255, 255))
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMouseTracking(True)

        self.current_label = label_component
        self.button_label_edit = button_label_edit
        self.button_delete = button_delete

        # Inicializar el punto del mouse como None
        self.mouse_point = None

        self.draw_component = DrawComponent(self.scene)
        self.draw_auxiliar = DrawAuxiliar(self)
        self.latex_gen = Latex()
        self.cell_size = 50

        self.cord = cord
        self.tool = tool_selected
        self.components = components

        self.components_selector = ComponentsSelector()
        self.components_remover = ComponentsRemover(history)
        self.manager_components = manager_components

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

            self.start_point = QPoint(
                round(real_pos.x() / self.cell_size) * self.cell_size,
                round(real_pos.y() / self.cell_size) * self.cell_size)
            self.end_point = QPoint(
                round(real_pos.x() / self.cell_size) * self.cell_size,
                round(real_pos.y() / self.cell_size) * self.cell_size)

        if event.button() == Qt.MouseButton.LeftButton and self.space_pressed:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
            self.draw_auxiliar.remove_point_cursor()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        if self.dragMode() == QGraphicsView.DragMode.NoDrag:

            real_pos = self.mapToScene(event.pos())
            self.end_point = QPoint(
                round(real_pos.x() / self.cell_size) * self.cell_size,
                round(real_pos.y() / self.cell_size) * self.cell_size)

            name_class = self.tool.class_name

            if name_class == 'None':

                self.components_selector.unselect(self)

                pos = event.pos()
                item = self.itemAt(pos)

                if item:
                    select_component = None
                    for component in self.components:
                        selected_drawables = contain_item(component.drawables, item)
                        if len(selected_drawables) > 0:
                            select_component = component

                    if select_component is not None:
                        self.components_selector.select(self, select_component)

            if name_class == 'Traceable_Final':
                path_svg = self.tool.image
                self.manager_components.create_traceable_final(self, path_svg)

            if name_class == 'Traceable':
                self.manager_components.create_traceable(self)

            if name_class == 'Transistor':
                path_svg = self.tool.image
                self.manager_components.create_transistor(self, path_svg)

            if name_class == 'Transformer':
                path_svg = self.tool.image
                self.manager_components.create_transformer(self, path_svg)

        if self.dragMode() == QGraphicsView.DragMode.ScrollHandDrag:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.setMouseTracking(True)

        if self.dragMode() == QGraphicsView.DragMode.NoDrag:

            if self.tool.name != 'Select':
                self.cell_size = 50
                pos = self.mapToScene(event.pos())

                cord_x = round(pos.x() / self.cell_size)
                cord_y = round(pos.y() / self.cell_size)

                self.cord.setText("Coordinates: [" + str(cord_x) + "," + str(cord_y) + "]")

                x = cord_x * self.cell_size
                y = cord_y * self.cell_size

                self.draw_auxiliar.remove_point_cursor()
                self.mouse_point = self.draw_auxiliar.create_mouse_point(x, y)

        super().mouseMoveEvent(event)

    def scroll_value_changed(self):
        self.draw_auxiliar.remove_point_cursor()

    def enterEvent(self, event):
        self.setFocus()

    def set_tool(self, new_tool):
        self.tool = new_tool
