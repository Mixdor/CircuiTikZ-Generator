import math

from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QImage, QPainter, QPixmap, QColor, QPen, QFont, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsColorizeEffect


class Draw:

    def __init__(self, scene):
        self.font = QFont("Times New Roman", 14)
        self.scene = scene

    def image(self, device_ratio, path_svg, point_start, point_final, angle, color):
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

        if color != Qt.GlobalColor.black:
            colorize_effect = QGraphicsColorizeEffect()
            colorize_effect.setColor(color)
            item_img.setGraphicsEffect(colorize_effect)

        self.scene.addItem(item_img)

        return item_img

    def image_1(self, device_ratio, path_svg, size, point_final, angle, color):
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

        if color != Qt.GlobalColor.black:
            colorize_effect = QGraphicsColorizeEffect()
            colorize_effect.setColor(color)
            item_img.setGraphicsEffect(colorize_effect)

        self.scene.addItem(item_img)

        return item_img

    def image_with_height(self, device_ratio, path_svg, img_with, img_height, final_x, final_y, angle, color):

        renderer = QSvgRenderer(path_svg)
        aspect_ratio = renderer.defaultSize().width() / renderer.defaultSize().height()
        image = QImage(img_with, img_height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.transparent)

        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        renderer.render(painter)
        painter.end()

        pixmap = QPixmap.fromImage(image)
        pixmap.setDevicePixelRatio(device_ratio)

        item_img = QGraphicsPixmapItem(pixmap)
        item_img.setPos((final_x+13) - (pixmap.width() / 2), final_y - (pixmap.height() / 2))
        item_img.setTransformOriginPoint(item_img.boundingRect().center())
        item_img.setRotation(angle)
        item_img.setTransformationMode(Qt.TransformationMode.SmoothTransformation)

        if color != Qt.GlobalColor.black:
            colorize_effect = QGraphicsColorizeEffect()
            colorize_effect.setColor(color)
            item_img.setGraphicsEffect(colorize_effect)

        self.scene.addItem(item_img)

        return item_img

    def line(self, x1, y1, x2, y2, color):

        pen = QPen()
        pen.setColor(color)
        pen.setWidth(2)

        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(pen)
        self.scene.addItem(line)
        return line

    def label(self, middle_point, label, angle):

        item_text = QGraphicsTextItem(str(label))
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setFont(self.font)

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

    def label_center_horizontal(self, name_tool, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setFont(self.font)
        item_text.setPlainText(label)
        new_x = pos_point.x() - (item_text.boundingRect().width() / 2)
        if name_tool == "VCC":
            new_y = pos_point.y() - 50
        else:
            new_y = pos_point.y() + 25
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label_center(self, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setFont(self.font)
        item_text.setPlainText(label)
        new_x = pos_point.x() - (item_text.boundingRect().width() / 2)
        new_y = pos_point.y() - (item_text.boundingRect().height() / 2)
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label1(self, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setFont(self.font)
        item_text.setPlainText(label)
        new_x = pos_point.x()
        new_y = pos_point.y() - (item_text.boundingRect().height() * 0.7)
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label_transistor(self, pos_point:QPointF, label:str, rotation:float):

        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setFont(self.font)
        item_text.setPlainText(label)

        new_x = 0
        new_y = 0

        #item_text.setRotation(rotation)

        if rotation==0:
            new_x = pos_point.x()
            new_y = pos_point.y() - (item_text.boundingRect().height() / 2)
        elif rotation==90 or rotation==-270:
            new_x = pos_point.x() - (item_text.boundingRect().width() / 2)
            new_y = pos_point.y()
        elif rotation==180 or rotation==-180:
            new_x = pos_point.x() - item_text.boundingRect().width()
            new_y = pos_point.y() - (item_text.boundingRect().height() / 2)
        elif rotation==270 or rotation==-90:
            new_x = pos_point.x() - (item_text.boundingRect().width() / 2)
            new_y = pos_point.y() - item_text.boundingRect().height()

        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text

    def label_transformer(self, pos_point, label):
        item_text = QGraphicsTextItem()
        item_text.setDefaultTextColor(QColor(0, 0, 0))
        item_text.setFont(self.font)
        item_text.setPlainText(label)
        new_x = pos_point.x() - (item_text.boundingRect().width() / 2)
        new_y = pos_point.y() - (50 + item_text.boundingRect().height())
        item_text.setPos(new_x, new_y)

        self.scene.addItem(item_text)
        return item_text
