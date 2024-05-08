import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter, QPixmap, QColor, QPen
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsTextItem


class Draw:

    def __init__(self, scene):
        self.scene = scene

    def image(self, device_ratio, path_svg, point_start, point_final, angle):
        renderer = QSvgRenderer(path_svg)
        image_width = 50
        aspect_ratio = renderer.defaultSize().width() / renderer.defaultSize().height()
        image_height = int(image_width / aspect_ratio)
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        renderer.render(painter)
        painter.end()

        pixmap = QPixmap.fromImage(image)
        pixmap.setDevicePixelRatio(device_ratio)

        item_img = QGraphicsPixmapItem(pixmap)
        item_img.setPos((point_start.x() + point_final.x() - pixmap.width()) / 2,
                        (point_start.y() + point_final.y() - pixmap.height()) / 2)
        item_img.setTransformOriginPoint(item_img.boundingRect().center())
        item_img.setRotation(angle)
        item_img.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.scene.addItem(item_img)

        return item_img

    def image_1(self, device_ratio, path_svg, size, point_final, angle):
        renderer = QSvgRenderer(path_svg)
        image_width = size
        aspect_ratio = renderer.defaultSize().width() / renderer.defaultSize().height()
        image_height = int(image_width / aspect_ratio)
        image = QImage(image_width, image_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        renderer.render(painter)
        painter.end()

        pixmap = QPixmap.fromImage(image)
        pixmap.setDevicePixelRatio(device_ratio)

        item_img = QGraphicsPixmapItem(pixmap)
        item_img.setPos(point_final.x() - (pixmap.width() / 2), point_final.y() - (pixmap.height() / 2))
        item_img.setTransformOriginPoint(item_img.boundingRect().center())
        item_img.setRotation(angle)
        item_img.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.scene.addItem(item_img)

        return item_img

    def line(self, x1, y1, x2, y2):
        pen = QPen()
        pen.setColor(Qt.GlobalColor.black)
        pen.setWidth(2)

        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        self.scene.addItem(line)
        return line

    def label(self, middle_point, label, angle):
        item_text = QGraphicsTextItem(str(label))
        item_text.setDefaultTextColor(QColor(0, 0, 0))

        if 0 <= angle < 69 or 291 < angle:
            item_text.setRotation(angle)
            radius = 40
            new_x = middle_point.x() + radius * math.cos(math.radians(angle - 90))
            new_y = middle_point.y() + radius * math.sin(math.radians(angle - 90))

            item_text.setPos(new_x, new_y)
            item_text.setPos(
                new_x - (item_text.boundingRect().width() / 2) * math.cos(math.radians(angle)),
                new_y - (item_text.boundingRect().width() / 2) * math.sin(math.radians(angle))
            )
        elif 111 < angle < 249:
            item_text.setRotation(angle + 180)
            radius = 15
            new_x = middle_point.x() + radius * math.cos(math.radians(angle - 90))
            new_y = middle_point.y() + radius * math.sin(math.radians(angle - 90))

            item_text.setPos(new_x, new_y)
            item_text.setPos(
                new_x + (item_text.boundingRect().width() / 2) * math.cos(math.radians(angle)),
                new_y + (item_text.boundingRect().width() / 2) * math.sin(math.radians(angle))
            )
        elif 249 <= angle <= 291:
            item_text.setRotation(0)
            radius = 23
            new_x = middle_point.x() + radius * math.cos(math.radians(angle - 55))
            new_y = middle_point.y() + radius * math.sin(math.radians(angle - 55))

            item_text.setPos(new_x, new_y)
            item_text.setPos(
                new_x - (item_text.boundingRect().width()) * math.cos(math.radians(angle + 90)),
                new_y - (item_text.boundingRect().width()) * math.sin(math.radians(angle + 90))
            )
        else:
            item_text.setRotation(angle - 90)
            radius = 20
            new_x = middle_point.x() + radius * math.cos(math.radians(angle - 130))
            new_y = middle_point.y() + radius * math.sin(math.radians(angle - 130))

            item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label1_center(self, name_tool, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setPlainText(label)
        new_x = pos_point.x() - (item_text.boundingRect().width() / 2)
        if name_tool == "VCC":
            new_y = pos_point.y() - 50
        else:
            new_y = pos_point.y() + 25
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label1(self, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setPlainText(label)
        new_x = pos_point.x()
        new_y = pos_point.y() - (item_text.boundingRect().height() * 0.7)
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label4(self, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setPlainText(label)
        new_x = pos_point.x() - (item_text.boundingRect().width() / 2)
        new_y = pos_point.y() - (50 + item_text.boundingRect().height())
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label3(self, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setPlainText(label)
        new_x = pos_point.x()
        new_y = pos_point.y() - (item_text.boundingRect().height() / 2)
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text
