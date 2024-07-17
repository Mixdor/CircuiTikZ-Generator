import math

from PyQt6.QtCore import QPointF


class Calculate:

    def __init__(self):
        super().__init__()

    def middle_point(self, start_point, final_point):

        middle_point = QPointF(
            (start_point.x() + final_point.x()) / 2,
            (start_point.y() + final_point.y()) / 2
        )
        return middle_point

    def magnitude(self, start_point, final_point):

        magnitude = math.sqrt(
            math.pow((final_point.x() - start_point.x()), 2) +
            math.pow(final_point.y() - start_point.y(), 2)
        )
        return magnitude

    def difference(self, start_point, final_point):

        x1 = start_point.x()
        y1 = start_point.y()
        x2 = final_point.x()
        y2 = final_point.y()

        difference = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))
        return difference

    def angle(self, magnitude, start_point, final_point):

        x1 = start_point.x()
        y1 = start_point.y()
        x2 = final_point.x()
        y2 = final_point.y()

        if magnitude != 0:
            delta_x = x2 - x1
            delta_y = y2 - y1

            radians = math.atan2(delta_y, delta_x)
            angle = math.degrees(radians)
            angle = (angle + 360) % 360
        else:
            angle = 90

        return angle

    def component(self, magnitude, start_point, final_point):

        if magnitude == 0:
            component = QPointF(
                (final_point.x() - start_point.x()),
                (final_point.y() - start_point.y())
            )
        else:
            component = QPointF(
                (final_point.x() - start_point.x()) / magnitude,
                (final_point.y() - start_point.y()) / magnitude
            )
        return component