from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPen
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsEllipseItem

from ui.Resources import Resources


class DrawAuxiliar:

    def __init__(self, canvas):
        self.resources = Resources()
        self.canvas = canvas
        self.scene = canvas.scene

    def draw_grid(self):

        interpolated = False
        cell_size = 50
        cell_size_dotted = 25
        canvas_width = 2000
        canvas_height = 2000

        grid_color = QColor(0, 0, 0, 35)  # RGB + Alfa (transparency)
        brush = QPen(grid_color)
        brush_dotted = QPen(grid_color)
        brush_dotted.setStyle(Qt.PenStyle.DashLine)

        for i in range(0, canvas_height, cell_size):
            line = QGraphicsLineItem(0, i, canvas_width, i)
            line.setPen(brush)
            self.scene.addItem(line)
            line = QGraphicsLineItem(i, 0, i, canvas_height)
            line.setPen(brush)
            self.scene.addItem(line)

        for i in range(0, canvas_height, cell_size_dotted):
            if interpolated:
                line = QGraphicsLineItem(0, i, canvas_width, i)
                line.setPen(brush_dotted)
                self.scene.addItem(line)
                line = QGraphicsLineItem(i, 0, i, canvas_height)
                line.setPen(brush_dotted)
                self.scene.addItem(line)

            interpolated = not interpolated

    def create_mouse_point(self, x, y):

        point_radio = 4
        point = QGraphicsEllipseItem(x - point_radio, y - point_radio, 2 * point_radio, 2 * point_radio)
        point.setBrush(self.resources.get_color_shadow())
        self.scene.addItem(point)

        return point

    def remove_point_cursor(self):
        if self.canvas.mouse_point:
            self.scene.removeItem(self.canvas.mouse_point)
            self.canvas.mouse_point = None

    def remove_shadow(self):
        if self.canvas.current_tool_shadow:
            if isinstance(self.canvas.current_tool_shadow, list):
                for item in self.canvas.current_tool_shadow:
                    self.scene.removeItem(item)
            else:
                self.scene.removeItem(self.canvas.current_tool_shadow)
            self.canvas.current_tool_shadow = None
