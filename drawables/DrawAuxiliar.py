from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem


class DrawAuxiliar:

    def __init__(self, canvas):
        self.canvas = canvas
        self.scene = canvas.scene

    def draw_grid(self):

        cell_size = 50
        canvas_width = 2000
        canvas_height = 2000

        grid_color = QColor(0, 0, 0, 35)  # RGB + Alfa (transparency)
        brush = QPen(grid_color)

        for y in range(0, canvas_height, cell_size):
            line = QGraphicsLineItem(0, y, canvas_width, y)
            line.setPen(brush)
            self.scene.addItem(line)

        for x in range(0, canvas_width, cell_size):
            line = QGraphicsLineItem(x, 0, x, canvas_height)
            line.setPen(brush)
            self.scene.addItem(line)

    def create_mouse_point(self, x, y):

        point_radio = 4
        point = QGraphicsEllipseItem(x - point_radio, y - point_radio, 2 * point_radio, 2 * point_radio)
        point.setBrush(QColor(219, 103, 37))
        self.scene.addItem(point)

        return point

    def remove_point_cursor(self):
        if self.canvas.mouse_point:
            self.scene.removeItem(self.canvas.mouse_point)
            self.canvas.mouse_point = None
