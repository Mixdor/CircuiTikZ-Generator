from PyQt6.QtCore import QRectF, Qt
from PyQt6.QtWidgets import QGraphicsTextItem, QGraphicsLineItem, QGraphicsRectItem

from objects.Components import ObjComponent
from ui.Resources import Resources


class ComponentsSelector:

    def __init__(self):
        super().__init__()
        self.resources = Resources()

    def unselect(self, canvas):

        if canvas.rect_select:
            canvas.scene.removeItem(canvas.rect_select)
            canvas.rect_select = None
            canvas.component_selected = None
            canvas.button_delete.setEnabled(False)
            canvas.button_label_edit.setEnabled(False)
            canvas.current_label.setEnabled(False)
            canvas.current_label.setText('')

            canvas.button_flip_horizontal.setEnabled(False)
            canvas.button_flip_vertical.setEnabled(False)
            canvas.button_rotate_no_clock.setEnabled(False)
            canvas.button_rotate_clock.setEnabled(False)

    def select(self, canvas, component:ObjComponent):

        rec_select_x = 2000
        rec_select_y = 2000
        point_final_x = 0
        point_final_y = 0

        select_drawables = component.draws

        for item_comp in select_drawables:

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

        canvas.rect_select = QGraphicsRectItem(
            QRectF(
                rec_select_x,
                rec_select_y,
                point_final_x - rec_select_x,
                point_final_y - rec_select_y
            )
        )
        canvas.rect_select.setBrush(Qt.GlobalColor.transparent)
        pen = canvas.rect_select.pen()
        pen.setStyle(Qt.PenStyle.DotLine)
        pen.setColor(self.resources.get_color_shadow())
        pen.setWidth(2)
        canvas.rect_select.setPen(pen)

        canvas.scene.addItem(canvas.rect_select)
        canvas.component_selected = component
        canvas.button_delete.setEnabled(True)
        canvas.button_label_edit.setEnabled(True)
        canvas.current_label.setEnabled(True)

        comp_class = component.built_tool.class_
        if comp_class == "Transistor":
            canvas.button_flip_horizontal.setEnabled(True)
            canvas.button_flip_vertical.setEnabled(True)
            canvas.button_rotate_no_clock.setEnabled(True)
            canvas.button_rotate_clock.setEnabled(True)

        for draw in canvas.component_selected.draws:
            if isinstance(draw, QGraphicsTextItem):
                canvas.current_label.setText(draw.toPlainText())
