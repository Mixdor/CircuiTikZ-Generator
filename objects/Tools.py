class ObjTool:

    def __init__(self, name, group_name, class_name, latex, img_cover, canvas_stroke, canvas_stroke_static):
        self.name = name
        self.group = group_name
        self.class_ = class_name
        self.latex = latex
        self.img_cover = img_cover
        self.canvas_stroke = canvas_stroke
        self.canvas_stroke_static = canvas_stroke_static

    def get_name(self):
        return self.name

    def get_group(self):
        return self.group

    def get_class(self):
        return self.class_

    def get_latex(self):
        return self.latex

    def get_cover(self):
        return self.img_cover

    def get_canvas_stroke(self):
        return self.canvas_stroke

    def get_canvas_stroke_static(self):
        return self.canvas_stroke_static

    def __repr__(self):
        return f"Component(name={self.name}, group={self.group_name} class={self.class_name}, latex={self.latex} img_cover={self.img_cover}, canvas_stroke={self.canvas_stroke}, canvas_stroke_static={self.canvas_stroke_static})"

class GroupTools:
    def __init__(self, name):
        self.name = name
        self.tools = []

    def add_component(self, tool):
        self.tools.append(tool)

    def get_name(self):
        return self.name

    def size(self):
        return len(self.tools)

    def __getitem__(self, index):
        return self.tools[index]

    def __repr__(self):
        return f"Group(name={self.name}, tools={self.tools})"

class ListGroupTools:
    def __init__(self):
        self.groups = []

    def add_group(self, group):
        self.groups.append(group)

    def get_tool(self, tool_name):
        for group in self.groups:
            for tool in group.tools:
                if tool.get_name() == tool_name:
                    return tool
        return None  # No found

    def size(self):
        return len(self.groups)

    def __getitem__(self, index):
        return self.groups[index]

    def __repr__(self):
        return f"ListGroup(groups={self.groups})"
