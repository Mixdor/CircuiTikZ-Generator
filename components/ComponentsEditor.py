import copy

from PyQt6.QtWidgets import QGraphicsTextItem

from components.Latex import Latex
from drawables.Draw import Draw
from objects.Components import ObjComponent, ObjScales


class ComponentsEditor:

    def __init__(self, history):
        super().__init__()

        self.history = history
        self.draw_component = None

    def label(self, canvas, input_text:str):

        drawer = Draw(canvas.scene)
        component : ObjComponent = canvas.component_selected

        if component:

            before_component = self.create_deep_copy(component)
            
            for draw in component.draws:

                if isinstance(draw, QGraphicsTextItem):

                    component.label = input_text

                    if component.built_tool.class_ == 'Simple_Node':

                        if component.built_tool.group == 'Power Supplies' or component.built_tool.group == 'Grounds':
                            item_label = drawer.label_center_horizontal(
                                name_tool=component.built_tool.name,
                                pos_point=component.positions.middle_point,
                                label=input_text
                            )
                        else:
                            item_label = drawer.label1(
                                pos_point=component.positions.middle_point,
                                label=input_text
                            )

                        component.draws.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.draws.append(item_label)

                    elif component.built_tool.class_ == 'Traceable':

                        item_label = drawer.label(
                            component.positions.middle_point,
                            input_text,
                            component.rotation
                        )

                        component.draws.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.draws.append(item_label)

                    elif component.built_tool.class_ == 'Transistor':

                        item_label = drawer.label_transistor(
                            pos_point=component.positions.middle_point,
                            label=input_text,
                            rotation=component.rotation,
                            scales=component.scales
                        )

                        component.draws.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.draws.append(item_label)

                    elif component.built_tool.class_ == 'Amplifier':

                        item_label = drawer.label_center(
                            pos_point=component.positions.middle_point,
                            label=input_text
                        )

                        component.draws.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.draws.append(item_label)

                    elif component.built_tool.class_ == 'Transformer':

                        item_label = drawer.label_transformer(
                            pos_point=component.positions.middle_point,
                            label=input_text
                        )

                        component.draws.remove(draw)
                        canvas.scene.removeItem(draw)
                        component.draws.append(item_label)

                    else:
                        print("Number pins not found")

            if component != before_component:
                self.history.new_event_undo(2, before_component, component)

    def rotation(self, canvas, rotation:int):

        drawer = Draw(canvas.scene)
        component : ObjComponent = canvas.component_selected


        sentido = component.scales.x_scale * component.scales.y_scale
        if sentido > 0:
            new_rotation = component.rotation + rotation
        else:
            new_rotation = component.rotation - rotation

        if new_rotation==360 or new_rotation==-360:
            new_rotation = 0

        if component:

            before_component = self.create_deep_copy(component)

            draw_comp = self.draw_component.transistor(
                canvas.scene, canvas.devicePixelRatio(), component.positions.middle_point,
                component.built_tool.canvas_stroke, new_rotation, canvas.current_label.text(),
                component.scales
            )

            for draw in component.draws:
                canvas.scene.removeItem(draw)

            component.draws.clear()
            component.draws = draw_comp
            component.rotation = new_rotation

            if component != before_component:
                self.history.new_event_undo(2, before_component, component)


    def change_scales(self, canvas, scales:ObjScales):

        component: ObjComponent = canvas.component_selected

        new_scale_x = component.scales.x_scale * scales.x_scale
        new_scale_y = component.scales.y_scale * scales.y_scale

        new_scales = ObjScales(new_scale_x, new_scale_y)

        if component:

            before_component = self.create_deep_copy(component)

            draw_comp = self.draw_component.transistor(
                canvas.scene, canvas.devicePixelRatio(), component.positions.middle_point,
                component.built_tool.canvas_stroke, component.rotation, canvas.current_label.text(),
                new_scales
            )

            for draw in component.draws:
                canvas.scene.removeItem(draw)

            component.draws.clear()
            component.draws = draw_comp
            component.scales = new_scales

            if component != before_component:
                self.history.new_event_undo(2, before_component, component)


    def create_deep_copy(self, component) -> ObjComponent:

        return ObjComponent(
            num=copy.copy(component.num),
            built_tool=copy.copy(component.built_tool),
            positions=copy.copy(component.positions),
            rotation=copy.copy(component.rotation),
            scales=copy.copy(component.scales),
            label=copy.copy(component.label),
            colors=copy.copy(component.colors),
            draws=copy.copy(component.draws),
        )
