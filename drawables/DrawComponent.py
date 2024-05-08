import math

from PyQt6.QtCore import QPointF

from drawables.Draw import Draw


def calculate_angle(x1, y1, x2, y2):
    delta_x = x2 - x1
    delta_y = y2 - y1

    radians = math.atan2(delta_y, delta_x)
    angle = math.degrees(radians)
    angle = (angle + 360) % 360

    return angle


class DrawComponent:

    def __init__(self, scene):
        self.scene = scene
        self.draw = Draw(self.scene)

    def one_pins(self, device_ratio, start_point, final_point, tool, label_component):

        items_added = []

        item_line = self.draw.line(
            start_point.x(),
            start_point.y(),
            final_point.x(),
            final_point.y()
        )

        item_img = self.draw.image_1(
            device_ratio,
            tool.image,
            50,
            final_point,
            90
        )

        if tool.name_class == "Power Supplies":
            item_label = self.draw.label1_center(
                tool.name,
                final_point,
                label_component
            )
            items_added.append(item_label)
        else:
            item_label = self.draw.label1(
                final_point,
                label_component
            )
            items_added.append(item_label)

        items_added.append(item_line)
        items_added.append(item_img)

        return items_added

    def two_pins(self, scene, device_ratio, start_point, final_point, path_svg, label_component):

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

        if magnitude == 0:
            component = QPointF(
                (final_point.x() - start_point.x()),
                (final_point.y() - start_point.y())
            )
            angle = 90
        else:
            component = QPointF(
                (final_point.x() - start_point.x()) / magnitude,
                (final_point.y() - start_point.y()) / magnitude
            )

        line_top = self.draw.line(
            start_point.x(),
            start_point.y(),
            middle_point.x() - 25 * component.x(),
            middle_point.y() - 25 * component.y()
        )

        line_button = self.draw.line(
            middle_point.x() + 25 * component.x(),
            middle_point.y() + 25 * component.y(),
            final_point.x(),
            final_point.y()
        )

        item_img = self.draw.image(
            device_ratio,
            path_svg,
            start_point,
            final_point,
            angle
        )

        item_label = self.draw.label(
            middle_point,
            label_component,
            angle
        )

        items_added.append(line_top)
        items_added.append(item_img)
        items_added.append(item_label)
        items_added.append(line_button)

        return items_added

    def two_pins_no_img(self, scene, start_point, final_point, label_component):

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

        if magnitude == 0:
            angle = 90

        item_line = self.draw.line(
            start_point.x(),
            start_point.y(),
            final_point.x(),
            final_point.y()
        )

        item_label = self.draw.label(
            middle_point,
            label_component,
            angle
        )

        items_added.append(item_line)
        items_added.append(item_label)

        return items_added

    def transistor(self, scene, device_ratio, final_point, path_svg, label_component):

        items_added = []

        item_img = self.draw.image(
            device_ratio,
            path_svg,
            final_point,
            final_point,
            0
        )

        line_top = self.draw.line(
            final_point.x(), final_point.y() - 50,
            final_point.x(), final_point.y() - 25
        )

        line_button = self.draw.line(
            final_point.x(), final_point.y() + 50,
            final_point.x(), final_point.y() + 25
        )

        line_middle = self.draw.line(
            final_point.x() - 50, final_point.y(),
            final_point.x() - 25, final_point.y()
        )

        item_label = self.draw.label3(final_point, label_component)

        items_added.append(item_img)
        items_added.append(line_top)
        items_added.append(line_middle)
        items_added.append(line_button)
        items_added.append(item_label)

        return items_added

    def transformer(self, scene, device_ratio, final_point, path_svg, label_component):

        items_added = []

        item_img = self.draw.image_1(
            device_ratio,
            path_svg,
            100,
            final_point,
            0
        )

        item_label = self.draw.label4(final_point, label_component)

        items_added.append(item_img)
        items_added.append(item_label)

        return items_added

    def line(self, start_point, end_point):
        items_added = []

        item_line = self.draw.line(
            start_point.x(), start_point.y(),
            end_point.x(), end_point.y()
        )
        items_added.append(item_line)

        return items_added
