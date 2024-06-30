import copy

from objects.ObjComponent import ObjComponent
from objects.ObjEvent import ObjEvent


class History:

    def __init__(self):

        self.list_undo = []
        self.list_redo = []

    def new_event_undo(self, type_event, component_before, component):
        event = ObjEvent(
            len(self.list_undo),
            type_event,
            component_before,
            component
        )
        self.list_undo.append(event)

    def new_event_redo(self, type_event, component_before, component):
        event = ObjEvent(
            len(self.list_redo),
            type_event,
            component_before,
            component
        )
        self.list_redo.append(event)

    def delete_event_undo(self, event):
        self.list_undo.remove(event)

    def delete_event_redo(self, event):
        self.list_redo.remove(event)

    def undo(self, canvas):
        if self.list_undo:

            last_event = self.list_undo[-1]

            if last_event.type_event == 0:
                component = last_event.component

                for item in component.drawables:
                    canvas.scene.addItem(item)

                canvas.components.append(component)

                self.new_event_redo(1, None, component)

            elif last_event.type_event == 1:
                component = last_event.component
                for item in component.drawables:
                    canvas.scene.removeItem(item)

                canvas.components.remove(component)

                self.new_event_redo(0, None, component)

            elif last_event.type_event == 2:
                component_before = last_event.component_before
                component = last_event.component

                component_after = ObjComponent(
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

                self.new_event_redo(2, component_after, component)

                for item in component.drawables:
                    canvas.scene.removeItem(item)

                for item in component_before.drawables:
                    canvas.scene.addItem(item)

                index = canvas.components.index(component)

                canvas.components[index].num = component_before.num
                canvas.components[index].name = component_before.name
                canvas.components[index].group_name = component_before.group_name
                canvas.components[index].class_name = component_before.class_name
                canvas.components[index].seed_latex = component_before.seed_latex
                canvas.components[index].middle_point = component_before.middle_point
                canvas.components[index].angle = component_before.angle
                canvas.components[index].positions = component_before.positions
                canvas.components[index].label = component_before.label
                canvas.components[index].drawables = component_before.drawables
                canvas.components[index].latex = component_before.latex

            self.list_undo.remove(last_event)

    def redo(self, canvas):

        if self.list_redo:

            last_event = self.list_redo[-1]

            if last_event.type_event == 0:

                component = last_event.component

                for item in component.drawables:
                    canvas.scene.addItem(item)

                canvas.components.append(component)
                self.new_event_undo(1, None, component)

            elif last_event.type_event == 1:
                component = last_event.component
                for item in component.drawables:
                    canvas.scene.removeItem(item)

                canvas.components.remove(component)

                self.new_event_undo(0, None, component)

            elif last_event.type_event == 2:
                component_after = last_event.component_before
                component = last_event.component

                component_before = ObjComponent(
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

                self.new_event_undo(2, component_before, component)

                for item in component.drawables:
                    canvas.scene.removeItem(item)

                for item in component_after.drawables:
                    canvas.scene.addItem(item)

                index = canvas.components.index(component)

                canvas.components[index].num = component_after.num
                canvas.components[index].name = component_after.name
                canvas.components[index].group_name = component_after.group_name
                canvas.components[index].class_name = component_after.class_name
                canvas.components[index].seed_latex = component_after.seed_latex
                canvas.components[index].middle_point = component_after.middle_point
                canvas.components[index].angle = component_after.angle
                canvas.components[index].positions = component_after.positions
                canvas.components[index].label = component_after.label
                canvas.components[index].drawables = component_after.drawables
                canvas.components[index].latex = component_after.latex

            self.list_redo.remove(last_event)
