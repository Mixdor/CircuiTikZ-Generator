import math

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QColor, QPen, QPixmap, QPainter, QImage
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPixmapItem, QGraphicsTextItem

pen = QPen(Qt.black, 1.5, Qt.SolidLine)


def calculate_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1

    radians = math.atan2(delta_y, delta_x)
    angle = math.degrees(radians)
    angle = (angle + 360) % 360

    return angle


class Drawable:

    def get_point(self, x, y):

        point_radio = 5
        point_mouse = QGraphicsEllipseItem(x - point_radio, y - point_radio, 2 * point_radio, 2 * point_radio)
        point_mouse.setBrush(Qt.red)

        return point_mouse

    def draw_line_with_image(self, scene, device_ratio, start_point, final_point, path_svg, label_component):

        items_added = []

        middle_point = QPointF(
            (start_point.x() + final_point.x()) / 2,
            (start_point.y() + final_point.y()) / 2
        )
        magnitude = math.sqrt(
            math.pow((final_point.x() - start_point.x()), 2) +
            math.pow(final_point.y() - start_point.y(), 2)
        )
        angle = calculate_angle(start_point.x(), start_point.y(), final_point.x(), final_point.y())

        component = QPointF(
            (final_point.x() - start_point.x()) / magnitude,
            (final_point.y() - start_point.y()) / magnitude
        )

        line_top = self.get_line(
            scene,
            start_point.x(),
            start_point.y(),
            middle_point.x() - 25 * component.x(),
            middle_point.y() - 25 * component.y()
        )

        line_button = self.get_line(
            scene,
            middle_point.x() + 25 * component.x(),
            middle_point.y() + 25 * component.y(),
            final_point.x(),
            final_point.y()
        )

        item_img = self.get_image(
            scene,
            device_ratio,
            path_svg,
            start_point,
            final_point,
            angle
        )

        item_label = self.get_label(
            scene,
            middle_point,
            label_component,
            angle
        )

        items_added.append(line_top)
        items_added.append(item_img)
        items_added.append(item_label)
        items_added.append(line_button)

        return items_added

    def draw_line(self, scene, start_point, end_point):
        items_added = []

        item_line = self.get_line(
            scene, 
            start_point.x(), start_point.y(),
            end_point.x(), end_point.y()
        )
        items_added.append(item_line)

        return items_added

    def get_line(self, scene, x1, y1, x2, y2):
        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        scene.addItem(line)
        return line

    def get_label(self, scene, middle_point, label, angle):
        item_text = QGraphicsTextItem()
        item_text.setPlainText(label)
        item_text.setRotation(angle)
        radius = 40
        new_x = middle_point.x() + radius * math.cos(math.radians(angle - 90))
        new_y = middle_point.y() + radius * math.sin(math.radians(angle - 90))

        item_text.setPos(new_x, new_y)
        item_text.setPos(
            new_x - (item_text.boundingRect().width() / 2) * math.cos(math.radians(angle)),
            new_y - (item_text.boundingRect().width() / 2) * math.sin(math.radians(angle))
        )
        scene.addItem(item_text)
        return item_text

    def get_image(self, scene, device_ratio, path_svg, point_start, point_final, angle):
        renderer = QSvgRenderer(path_svg)
        image_width = 50
        aspect_ratio = renderer.defaultSize().width() / renderer.defaultSize().height()
        image_height = int(image_width / aspect_ratio)
        image = QImage(image_width, image_height, QImage.Format_ARGB32)
        image.fill(Qt.TransparentMode)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.Antialiasing, True)
        renderer.render(painter)
        painter.end()

        pixmap = QPixmap.fromImage(image)
        pixmap.setDevicePixelRatio(device_ratio)

        item_img = QGraphicsPixmapItem(pixmap)
        item_img.setPos((point_start.x() + point_final.x() - pixmap.width()) / 2,
                        (point_start.y() + point_final.y() - pixmap.height()) / 2)
        item_img.setTransformOriginPoint(item_img.boundingRect().center())
        item_img.setRotation(angle)
        item_img.setTransformationMode(Qt.SmoothTransformation)
        scene.addItem(item_img)

        return item_img

    def draw_grid(self, scene):

        cell_size = 50
        canvas_width = 2000
        canvas_height = 2000

        grid_color = QColor(0, 0, 0, 35)  # RGB + Alfa (transparency)
        brush = QPen(grid_color)

        for y in range(0, canvas_height, cell_size):
            line = QGraphicsLineItem(0, y, canvas_width, y)
            line.setPen(brush)
            scene.addItem(line)

        for x in range(0, canvas_width, cell_size):
            line = QGraphicsLineItem(x, 0, x, canvas_height)
            line.setPen(brush)
            scene.addItem(line)
