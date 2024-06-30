
class ObjEvent:

    def __init__(self, id_event, type_event, component_before, component):
        self.id_event = id_event
        self.type_event = type_event
        self.component_before = component_before
        self.component = component

    @property
    def id_event(self):
        return self._id_event

    @id_event.setter
    def id_event(self, new_id_event):
        self._id_event = new_id_event

    @property
    def type_event(self):
        return self._type_event

    @type_event.setter
    def type_event(self, new_type_event):
        self._type_event = new_type_event

    @property
    def component_before(self):
        return self._component_before

    @component_before.setter
    def component_before(self, new_component_before):
        self._component_before = new_component_before

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, new_component):
        self._component = new_component
