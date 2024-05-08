from PyQt6.QtCore import Qt, QPoint, QRectF
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsLineItem, \
    QGraphicsTextItem

from components.Latex import Latex
from drawables.DrawAuxiliar import DrawAuxiliar
from drawables.DrawComponent import DrawComponent


def contain_item(components_added, item):
    for sublist in components_added:
        if item in sublist:
            return sublist
    return []


class Canvas(QGraphicsView):

    def __init__(self, cord, tool_selected, components_added, draw_added, label_component, button_delete, manager_components):
        super().__init__()

        self.setBackgroundBrush(QColor(255, 255, 255))
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMouseTracking(True)
        self.id_node = 0

        self.current_label = label_component
        self.button_delete = button_delete

        # Inicializar el punto del mouse como None
        self.mouse_point = None

        self.draw_component = DrawComponent(self.scene)
        self.draw_auxiliar = DrawAuxiliar(self)
        self.latex_gen = Latex()
        self.cell_size = 50

        self.cord = cord
        self.tool = tool_selected
        self.components_added = components_added
        self.draw_added = draw_added

        self.manager_components = manager_components

        self.component_selected = []

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
            self.manager_components.delete_selected()

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

            number_pins = self.tool.number_pins

            if number_pins == 0:

                self.manager_components.unselected()

                pos = event.pos()
                item = self.itemAt(pos)

                if item:
                    component = contain_item(self.components_added, item)
                    if len(component) > 0:

                        rec_select_x = 2000
                        rec_select_y = 2000
                        point_final_x = 0
                        point_final_y = 0

                        for item_comp in component:

                            if not isinstance(item_comp, QGraphicsTextItem):
                                if isinstance(item_comp, QGraphicsLineItem):
                                    if item_comp.boundingRect().x() < rec_select_x:
                                        rec_select_x = item_comp.boundingRect().x()
                                    if item_comp.boundingRect().y() < rec_select_y:
                                        rec_select_y = item_comp.boundingRect().y()

                                    point_comp_x = item_comp.boundingRect().x() + item_comp.boundingRect().width()
                                    point_comp_y = item_comp.boundingRect().y() + item_comp.boundingRect().height()

                                else:
                                    if item_comp.x() < rec_select_x:
                                        rec_select_x = item_comp.x()
                                    if item_comp.y() < rec_select_y:
                                        rec_select_y = item_comp.y()

                                    point_comp_x = item_comp.x() + item_comp.boundingRect().width()
                                    point_comp_y = item_comp.y() + item_comp.boundingRect().height()

                                if point_comp_x > point_final_x:
                                    point_final_x = point_comp_x
                                if point_comp_y > point_final_y:
                                    point_final_y = point_comp_y

                        self.rect_select = QGraphicsRectItem(
                            QRectF(
                                rec_select_x,
                                rec_select_y,
                                point_final_x - rec_select_x,
                                point_final_y - rec_select_y
                            )
                        )
                        self.rect_select.setBrush(Qt.GlobalColor.transparent)
                        pen = self.rect_select.pen()
                        pen.setStyle(Qt.PenStyle.DotLine)
                        pen.setColor(QColor('#DB6725'))
                        pen.setWidth(2)
                        self.rect_select.setPen(pen)

                        self.scene.addItem(self.rect_select)
                        self.component_selected = component
                        self.button_delete.setEnabled(True)

            if number_pins == 1:
                path_svg = self.tool.image
                self.manager_components.create_one_pins(path_svg)

            if number_pins == 2:
                self.manager_components.create_two_pins()

            if number_pins == 3:
                path_svg = self.tool.image
                self.manager_components.create_three_pins(path_svg)

            if number_pins == 4:
                path_svg = self.tool.image
                self.manager_components.create_four_pins(path_svg)

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
