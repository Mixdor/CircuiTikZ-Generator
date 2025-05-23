from components.ComponentsSelector import ComponentsSelector
from objects.Components import ObjComponent


class ComponentsRemover:

    def __init__(self, history):
        super().__init__()

        self.history = history
        self.components_selector = ComponentsSelector()

    def delete_selected(self, canvas):

        if canvas.component_selected:
            self.delete_component(canvas)
            self.components_selector.unselect(canvas)

    def delete_component(self, canvas):

        component : ObjComponent = canvas.component_selected

        for draw in component.draws:
            canvas.scene.removeItem(draw)

        self.history.new_event_undo(0, None, component)
        canvas.components.remove(component)
