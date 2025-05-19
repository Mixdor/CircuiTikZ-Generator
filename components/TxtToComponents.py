import xml.etree.ElementTree as ET
import os
import re

from objects.Tools import ObjTool, GroupTools, ListGroupTools


class TxtToComponents:

    def __init__(self, base_path):

        self.base_path = base_path

    def parse_xml_to_objects(self):

        xml_path = os.path.join(self.base_path, 'list_components.xml')
        tree = ET.parse(xml_path)
        root = tree.getroot()
        list_group = ListGroupTools()

        for group_tool in root.findall('group'):

            name_group = group_tool.attrib['name']
            class_group = group_tool.attrib['class']
            group = GroupTools(name_group)

            for tool in group_tool.findall('tool'):

                name = tool.attrib['name']
                class_tool = tool.attrib.get('class')
                latex = tool.attrib['latex']
                cover = tool.findtext('img_cover')
                stroke = tool.findtext('canvas_stroke')
                stroke_static = tool.findtext('canvas_stroke_static')

                class_ = class_group
                if class_tool:
                    class_ = class_tool

                component = ObjTool(
                    name=name,
                    group_name=name_group,
                    class_name=class_,
                    latex=latex,
                    img_cover=cover,
                    canvas_stroke=stroke,
                    canvas_stroke_static=stroke_static,
                )
                group.add_component(component)

            list_group.add_group(group)

        return list_group
