import os

from drawables.DrawComponent import DrawComponent
from components.Latex import Latex


class ComponentsManager:

    def __init__(self, history):

        self.canvas = None
        self.draw_component = None
        self.latex = Latex()
        self.history = history

    def delete_selected(self):

        if self.canvas.component_selected:
            self.delete_component(self.canvas.component_selected)
            self.unselected()

    def delete_component(self, component):

        for item in component:
            self.canvas.scene.removeItem(item)
        index_delete = self.canvas.components_added.index(component)
        self.history.new_event_undo(0, component, self.canvas.draw_added[index_delete])
        self.canvas.draw_added.pop(index_delete)
        self.canvas.components_added.remove(component)

    def unselected(self):

        if self.canvas.rect_select:
            self.canvas.scene.removeItem(self.canvas.rect_select)
            self.canvas.rect_select = None
            self.canvas.component_selected = None
            self.canvas.button_delete.setEnabled(False)

    def create_one_pins(self, path_svg):

        if os.path.exists(path_svg):
            draw_comp = self.draw_component.one_pins(
                self.canvas.devicePixelRatio(),
                self.canvas.start_point, self.canvas.end_point,
                self.canvas.tool,
                self.canvas.current_label.toPlainText()
            )
        else:
            draw_comp = self.draw_component.line(self.canvas.start_point, self.canvas.end_point)
        self.canvas.update()

        latex_comp = self.latex.get_one_pin(
            self.canvas.start_point / self.canvas.cell_size,
            self.canvas.end_point / self.canvas.cell_size,
            self.canvas.tool.latex,
            self.canvas.current_label.toPlainText())

        self.canvas.draw_added.append(latex_comp)
        self.canvas.components_added.append(draw_comp)

        self.history.new_event_undo(1, draw_comp, latex_comp)
        self.history.list_redo.clear()

    def create_two_pins(self):

        if self.canvas.start_point != self.canvas.end_point:

            if self.canvas.tool.get_name() != 'Wire':
                draw_comp = self.draw_component.two_pins(
                    self.canvas.scene, self.canvas.devicePixelRatio(),
                    self.canvas.start_point, self.canvas.end_point,
                    self.canvas.tool.image, self.canvas.current_label.toPlainText()
                )
            else:
                draw_comp = self.draw_component.two_pins_no_img(
                    self.canvas.scene,
                    self.canvas.start_point, self.canvas.end_point,
                    self.canvas.current_label.toPlainText()
                )
            self.canvas.update()

            latex_comp = self.latex.get_two_pin(
                self.canvas.start_point / self.canvas.cell_size,
                self.canvas.end_point / self.canvas.cell_size,
                self.canvas.tool.latex,
                self.canvas.current_label.toPlainText())

            self.canvas.draw_added.append(latex_comp)
            self.canvas.components_added.append(draw_comp)

            self.history.new_event_undo(1, draw_comp, latex_comp)
            self.history.list_redo.clear()

    def create_three_pins(self, path_svg):
        if os.path.exists(path_svg):
            draw_comp = self.draw_component.transistor(
                self.canvas.scene, self.canvas.devicePixelRatio(), self.canvas.end_point,
                path_svg, self.canvas.current_label.toPlainText()
            )

            self.canvas.update()

            latex_comp = self.latex.get_transistor(
                self.canvas.id_node,
                self.canvas.end_point / self.canvas.cell_size,
                self.canvas.tool.latex,
                self.canvas.current_label.toPlainText()
            )
            self.canvas.id_node += 1

            self.canvas.draw_added.append(latex_comp)
            self.canvas.components_added.append(draw_comp)

            self.history.new_event_undo(1, draw_comp, latex_comp)
            self.history.list_redo.clear()

        else:
            print("No found image")

    def create_four_pins(self, path_svg):
        if os.path.exists(path_svg):
            draw_comp = self.draw_component.transformer(
                self.canvas.scene, self.canvas.devicePixelRatio(), self.canvas.end_point,
                path_svg, self.canvas.current_label.toPlainText()
            )

            self.canvas.update()

            latex_comp = self.latex.get_transformer(
                self.canvas.id_node,
                self.canvas.end_point / self.canvas.cell_size,
                self.canvas.tool.latex,
                self.canvas.current_label.toPlainText()
            )
            self.canvas.id_node += 1

            self.canvas.draw_added.append(latex_comp)
            self.canvas.components_added.append(draw_comp)

            self.history.new_event_undo(1, draw_comp, latex_comp)
            self.history.list_redo.clear()

        else:
            print("No found image")
