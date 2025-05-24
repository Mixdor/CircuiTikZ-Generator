import copy

from objects.Components import ObjComponent
from objects.ObjEvent import ObjEvent


class History:

    def __init__(self):

        self.list_undo : list[ObjEvent] = []
        self.list_redo : list[ObjEvent] = []

    def new_event_undo(self, type_event:int, component_before:ObjComponent|None, component:ObjComponent):
        event = ObjEvent(
            len(self.list_undo),
            type_event,
            component_before,
            component
        )
        self.list_undo.append(event)

    def new_event_redo(self, type_event:int, component_before:ObjComponent|None, component:ObjComponent):
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

                for item in component.draws:
                    canvas.scene.addItem(item)

                canvas.components.append(component)

                self.new_event_redo(1, None, component)

            elif last_event.type_event == 1:
                component = last_event.component
                for item in component.draws:
                    canvas.scene.removeItem(item)

                canvas.components.remove(component)

                self.new_event_redo(0, None, component)

            elif last_event.type_event == 2:
                component_before = last_event.component_before
                component = last_event.component

                component_after = ObjComponent(
                    num = copy.copy(component.num),
                    built_tool = copy.copy(component.built_tool),
                    positions = copy.copy(component.positions),
                    rotation = copy.copy(component.rotation),
                    scales = copy.copy(component.scales),
                    label = copy.copy(component.label),
                    colors = copy.copy(component.colors),
                    draws = copy.copy(component.draws),
                )

                self.new_event_redo(2, component_after, component)

                for item in component.draws:
                    canvas.scene.removeItem(item)

                for item in component_before.draws:
                    canvas.scene.addItem(item)

                index = canvas.components.index(component)

                canvas.components[index].num = component_before.num
                canvas.components[index].built_tool = component_before.built_tool
                canvas.components[index].positions = component_before.positions
                canvas.components[index].rotation = component_before.rotation
                canvas.components[index].scales = component_before.scales
                canvas.components[index].label = component_before.label
                canvas.components[index].colors = component_before.colors
                canvas.components[index].draws = component_before.draws

            self.list_undo.remove(last_event)

        print(f"Undo:{self.list_undo}")
        print(f"Redo:{self.list_redo}")

    def redo(self, canvas):

        if self.list_redo:

            last_event = self.list_redo[-1]

            if last_event.type_event == 0:

                component = last_event.component

                for item in component.draws:
                    canvas.scene.addItem(item)

                canvas.components.append(component)
                self.new_event_undo(1, None, component)

            elif last_event.type_event == 1:
                component = last_event.component
                for item in component.draws:
                    canvas.scene.removeItem(item)

                canvas.components.remove(component)

                self.new_event_undo(0, None, component)

            elif last_event.type_event == 2:
                component_after = last_event.component_before
                component = last_event.component

                component_before = ObjComponent(
                    num = copy.copy(component.num),
                    built_tool = copy.copy(component.built_tool),
                    positions = copy.copy(component.positions),
                    rotation = copy.copy(component.rotation),
                    scales = copy.copy(component.scales),
                    label = copy.copy(component.label),
                    colors = copy.copy(component.colors),
                    draws = copy.copy(component.draws),
                )

                self.new_event_undo(2, component_before, component)

                for item in component.draws:
                    canvas.scene.removeItem(item)

                for item in component_after.draws:
                    canvas.scene.addItem(item)

                index = canvas.components.index(component)

                canvas.components[index].num = component_after.num
                canvas.components[index].built_tool = component_after.built_tool
                canvas.components[index].positions = component_after.positions
                canvas.components[index].rotation = component_after.rotation
                canvas.components[index].scales = component_after.scales
                canvas.components[index].label = component_after.label
                canvas.components[index].colors = component_after.colors
                canvas.components[index].draws = component_after.draws

            self.list_redo.remove(last_event)

        print(f"Undo:{self.list_undo}")
        print(f"Redo:{self.list_redo}")
