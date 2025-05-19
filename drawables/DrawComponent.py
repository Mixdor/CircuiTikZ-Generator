import math

from PyQt6.QtCore import QPointF, Qt

from auxiliar.Calculate import Calculate
from drawables.Draw import Draw


class DrawComponent:

    def __init__(self, scene):
        self.scene = scene
        self.draw = Draw(self.scene)
        self.calculate = Calculate()

    def one_pins(self, device_ratio, start_point, final_point, tool, label_component, color):

        items_added = []

        item_line = self.draw.line(
            start_point.x(), start_point.y(),
            final_point.x(), final_point.y(),
            color
        )

        item_img = self.draw.image_1(
            device_ratio,
            tool.get_canvas_stroke(),
            50,
            final_point,
            90,
            color
        )

        if tool.get_group() == 'Power Supplies':
            item_label = self.draw.label_center_horizontal(
                tool.get_name(),
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

    def two_pins(self, scene, device_ratio, start_point, final_point, path_svg, image_static, label_component, color):

        items_added = []

        middle_point = self.calculate.middle_point(start_point, final_point)
        magnitude = self.calculate.magnitude(start_point, final_point)
        angle = self.calculate.angle(magnitude, start_point, final_point)
        component = self.calculate.component(magnitude, start_point, final_point)

        line_top = self.draw.line(
            start_point.x(),
            start_point.y(),
            middle_point.x() - 25 * component.x(),
            middle_point.y() - 25 * component.y(),
            color
        )

        line_button = self.draw.line(
            middle_point.x() + 25 * component.x(),
            middle_point.y() + 25 * component.y(),
            final_point.x(),
            final_point.y(),
            color
        )

        item_img = self.draw.image(
            device_ratio,
            path_svg,
            start_point,
            final_point,
            angle,
            color
        )

        item_label = self.draw.label(
            middle_point,
            label_component,
            angle
        )

        if image_static != '':
            item_img_static = self.draw.image(
                device_ratio,
                image_static,
                start_point,
                final_point,
                0,
                color
            )
            items_added.append(item_img_static)

        items_added.append(line_top)
        items_added.append(item_img)
        items_added.append(item_label)
        items_added.append(line_button)

        return items_added

    def two_pins_no_img(self, scene, start_point, final_point, label_component, color):

        items_added = []

        middle_point = self.calculate.middle_point(start_point, final_point)
        magnitude = self.calculate.magnitude(start_point, final_point)
        angle = self.calculate.angle(magnitude, start_point, final_point)

        item_line = self.draw.line(
            start_point.x(),
            start_point.y(),
            final_point.x(),
            final_point.y(),
            color
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
            0,
            Qt.GlobalColor.black
        )

        item_label = self.draw.label_transistor(final_point, label_component)

        items_added.append(item_img)
        items_added.append(item_label)

        return items_added

    def transformer(self, scene, device_ratio, final_point, path_svg, label_component):

        items_added = []

        item_img = self.draw.image_1(
            device_ratio,
            path_svg,
            100,
            final_point,
            0,
            Qt.GlobalColor.black
        )

        item_label = self.draw.label_transformer(final_point, label_component)

        items_added.append(item_img)
        items_added.append(item_label)

        return items_added

    def amplifier(self, scene, device_ratio, final_point, path_svg, label_component):

        items_added = []

        item_img = self.draw.image_with_height(
            device_ratio,
            path_svg,
            125,
            100,
            final_point.x(),
            final_point.y(),
            0,
            Qt.GlobalColor.black
        )

        item_label = self.draw.label_transformer(final_point, label_component)

        items_added.append(item_img)
        items_added.append(item_label)

        return items_added

    def line(self, start_point, end_point, color):
        items_added = []

        item_line = self.draw.line(
            start_point.x(), start_point.y(),
            end_point.x(), end_point.y(),
            color
        )
        items_added.append(item_line)

        return items_added
