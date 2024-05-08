from objects.ObjEvent import ObjEvent


class History:

    def __init__(self):

        self.list_undo = []
        self.list_redo = []

    def new_event_undo(self, type_event, component, latex):
        event = ObjEvent(
            len(self.list_undo),
            type_event,
            component,
            latex
        )
        self.list_undo.append(event)

    def new_event_redo(self, type_event, component, latex):
        event = ObjEvent(
            len(self.list_redo),
            type_event,
            component,
            latex
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
                latex = last_event.latex

                for item in component:
                    canvas.scene.addItem(item)

                canvas.draw_added.append(latex)
                canvas.components_added.append(component)

                self.new_event_redo(1, last_event.component, last_event.latex)

            elif last_event.type_event == 1:
                component = last_event.component
                for item in component:
                    canvas.scene.removeItem(item)
                index_delete = canvas.components_added.index(component)
                canvas.draw_added.pop(index_delete)
                canvas.components_added.remove(component)

                self.new_event_redo(0, last_event.component, last_event.latex)

            self.list_undo.remove(last_event)

    def redo(self, canvas):

        if self.list_redo:

            last_event = self.list_redo[-1]

            if last_event.type_event == 0:

                component = last_event.component
                latex = last_event.latex

                for item in component:
                    canvas.scene.addItem(item)

                canvas.draw_added.append(latex)
                canvas.components_added.append(component)

                self.new_event_undo(1, last_event.component, last_event.latex)

            elif last_event.type_event == 1:
                component = last_event.component
                for item in component:
                    canvas.scene.removeItem(item)
                index_delete = canvas.components_added.index(component)
                canvas.draw_added.pop(index_delete)
                canvas.components_added.remove(component)

                self.new_event_undo(0, last_event.component, last_event.latex)

            self.list_redo.remove(last_event)
