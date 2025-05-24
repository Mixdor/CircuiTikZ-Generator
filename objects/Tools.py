from __future__ import annotations

class ObjTool:

    def __init__(self, name:str, group_name:str, class_name:str, latex:str,
                 img_cover:str, canvas_stroke:str, canvas_stroke_static:str):

        self.name : str = name
        self.group : str = group_name
        self.class_ : str = class_name
        self.latex : str = latex
        self.img_cover : str = img_cover
        self.canvas_stroke : str = canvas_stroke
        self.canvas_stroke_static : str = canvas_stroke_static

    def __repr__(self):
        return f"Component(name={self.name}, group={self.group} class={self.class_}, latex={self.latex} img_cover={self.img_cover}, canvas_stroke={self.canvas_stroke}, canvas_stroke_static={self.canvas_stroke_static})"


class GroupTools:
    def __init__(self, name:str):
        self.name : str = name
        self.tools : list[ObjTool] = []

    def add_component(self, tool):
        self.tools.append(tool)

    def size(self) -> int:
        return len(self.tools)

    def __getitem__(self, index:int) -> ObjTool:
        return self.tools[index]

    def __repr__(self):
        return f"Group(name={self.name}, tools={self.tools})"


class ListGroupTools:
    def __init__(self):
        self.groups : list[GroupTools] = []

    def add_group(self, group:GroupTools):
        self.groups.append(group)

    def get_tool(self, tool_name:str) -> ObjTool | None:
        for group in self.groups:
            for tool in group.tools:
                if tool.name == tool_name:
                    return tool
        return None  # No found

    def size(self) -> int:
        return len(self.groups)

    def __getitem__(self, index:int) -> GroupTools:
        return self.groups[index]

    def __repr__(self):
        return f"ListGroup(groups={self.groups})"
