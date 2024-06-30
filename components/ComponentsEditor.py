import copy

from PyQt6.QtWidgets import QGraphicsTextItem

from components.Latex import Latex
from drawables.Draw import Draw
from objects.ObjComponent import ObjComponent


class ComponentsEditor:

    def __init__(self, history):
        super().__init__()
        self.history = history
        self.latex = Latex()

    def label(self, canvas, input_text):

        drawer = Draw(canvas.scene)
        component = canvas.component_selected

        if component:

            before_component = ObjComponent(
                num=copy.copy(component.num),
                name=copy.copy(component.name),
                group_name=copy.copy(component.group_name),
                class_name=copy.copy(component.class_name),
                seed_latex=copy.copy(component.seed_latex),
                middle_point=copy.copy(component.middle_point),
                angle=copy.copy(component.angle),
                positions=copy.copy(component.positions),
                label=copy.copy(component.label),
                drawables=copy.copy(component.drawables),
                latex=copy.copy(component.latex)
            )

            for draw in component.drawables:
                if isinstance(draw, QGraphicsTextItem):

                    component.label = input_text

                    if component.class_name == 'Traceable_Final':

                        if component.group_name == 'Power Supplies':
                            item_label = drawer.label1_center(
                                name_tool=component.name,
                                pos_point=component.positions[1],
                                label=input_text
                            )
                        else:
                            item_label = drawer.label1(
                                pos_point=component.positions[1],
                                label=input_text
                            )

                        component.drawables.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.drawables.append(item_label)

                        new_latext = self.latex.get_one_pin(
                            start_point=component.positions[0] / canvas.cell_size,
                            final_point=component.positions[1] / canvas.cell_size,
                            latex=component.seed_latex,
                            label=input_text
                        )

                        component.latex = new_latext

                    elif component.class_name == 'Traceable':

                        item_label = drawer.label(
                            component.middle_point,
                            input_text,
                            component.angle
                        )

                        component.drawables.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.drawables.append(item_label)

                        new_latext = self.latex.get_two_pin(
                            component.name,
                            start_point=component.positions[0] / canvas.cell_size,
                            final_point=component.positions[1] / canvas.cell_size,
                            latex=component.seed_latex,
                            label=input_text
                        )
                        component.latex = new_latext

                    elif component.class_name == 'Transistor':

                        item_label = drawer.label_transistor(
                            pos_point=component.middle_point,
                            label=input_text
                        )

                        component.drawables.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.drawables.append(item_label)

                        new_latext = self.latex.get_transistor(
                            id_node=component.num,
                            point=component.middle_point / canvas.cell_size,
                            latex=component.seed_latex,
                            label=input_text
                        )
                        component.latex = new_latext

                    elif component.class_name == 'Transformer':

                        item_label = drawer.label_transformer(
                            pos_point=component.middle_point,
                            label=input_text
                        )

                        component.drawables.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.drawables.append(item_label)

                        new_latext = self.latex.get_transformer(
                            id_node=component.num,
                            point=component.middle_point / canvas.cell_size,
                            latex=component.seed_latex,
                            label=input_text
                        )
                        component.latex = new_latext

                    else:
                        print("Number pins not found")

            if component != before_component:
                self.history.new_event_undo(2, before_component, component)

