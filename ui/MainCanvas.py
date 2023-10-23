import os

from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene

from components.Drawable import Drawable
from components.LatexGenerator import LatexGenerator



def remove_point_cursor(self):
    if self.mouse_point:
        self.scene.removeItem(self.mouse_point)
        self.mouse_point = None


class Canvas(QGraphicsView):

    def __init__(self, cord, tool_selected, components_added, draw_added, label_component):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setMouseTracking(True)

        self.current_label = label_component

        self.drawable = Drawable()
        self.latex_gen = LatexGenerator()
        self.cell_size = 50

        self.cord = cord
        self.tool = tool_selected
        self.components_added = components_added
        self.draw_added = draw_added

        self.start_point = None
        self.end_point = None

        # Dibujar la cuadrícula de fondo
        self.drawable.draw_grid(self.scene)

        # Inicializar el punto del mouse como None
        self.mouse_point = None

        # Definir los límites de zoom
        self.min_scale = 0.6
        self.max_scale = 1.5
        self.space_pressed = False

        self.setDragMode(QGraphicsView.NoDrag)

        horizontal_scrollbar = self.horizontalScrollBar()
        vertical_scrollbar = self.verticalScrollBar()
        horizontal_scrollbar.valueChanged.connect(self.scroll_value_changed)
        vertical_scrollbar.valueChanged.connect(self.scroll_value_changed)

    def leaveEvent(self, event):
        self.cord.setText("")
        remove_point_cursor(self)

    def wheelEvent(self, event):
        factor = 1.2
        if event.angleDelta().y() < 0:
            factor = 1.0 / factor

        # Aplicar el zoom dentro de los límites
        current_scale = self.transform().m11()
        if self.min_scale < current_scale * factor < self.max_scale:
            self.scale(factor, factor)

    def keyPressEvent(self, event):
        # Detectar si la tecla de espacio está presionada
        if event.key() == Qt.Key_Space:
            self.space_pressed = True

    def keyReleaseEvent(self, event):
        # Detectar si la tecla de espacio se ha soltado
        if event.key() == Qt.Key_Space:
            self.space_pressed = False

    def mousePressEvent(self, event):

        if self.dragMode() == QGraphicsView.NoDrag:
            real_pos = self.mapToScene(event.pos())

            self.start_point = QPoint(
                round(real_pos.x() / self.cell_size) * self.cell_size,
                round(real_pos.y() / self.cell_size) * self.cell_size)
            self.end_point = QPoint(
                round(real_pos.x() / self.cell_size) * self.cell_size,
                round(real_pos.y() / self.cell_size) * self.cell_size)

        if event.button() == Qt.LeftButton and self.space_pressed:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            remove_point_cursor(self)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):

        if self.dragMode() == QGraphicsView.NoDrag:

            real_pos = self.mapToScene(event.pos())
            self.end_point = QPoint(
                round(real_pos.x() / self.cell_size) * self.cell_size,
                round(real_pos.y() / self.cell_size) * self.cell_size)

            number_pins = self.tool.number_pins

            if number_pins == 0:
                print("Select Tool")

            if number_pins == 1:
                path_svg = self.tool.image
                if os.path.exists(path_svg):
                    comp = self.drawable.canvas_one_pins(
                        self.scene, self.devicePixelRatio(),
                        self.start_point, self.end_point,
                        self.tool,
                        self.current_label.toPlainText()
                    )
                else:
                    comp = self.drawable.draw_line(self.scene, self.start_point, self.end_point)
                self.update()

                draw = self.latex_gen.getDrawOnePin(
                    self.start_point / self.cell_size,
                    self.end_point / self.cell_size,
                    self.tool.latex,
                    self.current_label.toPlainText())

                self.draw_added.append(draw)
                self.components_added.append(comp)

            if number_pins == 2:
                path_svg = self.tool.image

                if os.path.exists(path_svg):
                    comp = self.drawable.canvas_two_pins(
                        self.scene, self.devicePixelRatio(),
                        self.start_point, self.end_point,
                        path_svg, self.current_label.toPlainText()
                    )
                else:
                    comp = self.drawable.draw_line(self.scene, self.start_point, self.end_point)
                self.update()

                draw = self.latex_gen.getDrawTwoPin(
                    self.start_point/self.cell_size,
                    self.end_point/self.cell_size,
                    self.tool.latex,
                    self.current_label.toPlainText())

                self.draw_added.append(draw)
                self.components_added.append(comp)

            if number_pins == 3:
                print(number_pins)

        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.setDragMode(QGraphicsView.NoDrag)

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.setMouseTracking(True)

        if self.dragMode() == QGraphicsView.NoDrag:
            self.cell_size = 50
            pos = self.mapToScene(event.pos())

            cord_x = round(pos.x() / self.cell_size)
            cord_y = round(pos.y() / self.cell_size)

            self.cord.setText("Coordinates: [" + str(cord_x) + "," + str(cord_y) + "]")

            x = cord_x * self.cell_size
            y = cord_y * self.cell_size

            remove_point_cursor(self)

            self.mouse_point = self.drawable.get_point(x, y)
            self.scene.addItem(self.mouse_point)

        super().mouseMoveEvent(event)

    def scroll_value_changed(self, value):
        remove_point_cursor(self)

    def enterEvent(self, event):
        self.setFocus()

    def set_tool(self, new_tool):
        self.tool = new_tool
