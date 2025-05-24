from objects.Components import ObjComponent


class ObjEvent:

    def __init__(self, id_event:int, type_event:int, component_before:ObjComponent, component:ObjComponent):
        self.id_event = id_event
        self.type_event = type_event
        self.component_before = component_before
        self.component = component

    def __repr__(self):
        return f"ObjEvent(id_event={self.id_event}, type_event={self.type_event}, comp_before={self.component_before}, comp={self.component})"