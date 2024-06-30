import os
import re

from objects.ObjTool import ObjTool


class TxtToComponents:
    def __init__(self, base_path):
        self.base_path = base_path

    def get_groups(self):
        path = os.path.join(self.base_path, 'list_components.txt')
        with open(path, 'r') as file:
            content = file.read()

            list_groups = content.split("</group>")
            list_groups.remove("")

        return list_groups

    def get_components(self, group_str):

        list_components = []

        lines = group_str.split("\n")
        lines = [elemento for elemento in lines if elemento != ""]
        lines.remove(lines[0])

        for i in range(lines.__len__()):
            match = re.search("\[.+]", lines[i]).group()
            match = match.replace("[", "")
            match = match.replace("]", "")
            list_components.append(match)

        return list_components

    def get_group_name(self, group_str):
        lines = group_str.split("\n")
        lines.remove("")
        line_tag = lines[0]
        match = re.search("\".+\"", line_tag).group()
        match = match.replace("\"", "")

        return match

    def get_tools_for_group(self, group_str, name_group):
        list_components = []

        lines = group_str.split("\n")
        lines = [elemento for elemento in lines if elemento != ""]
        lines.remove(lines[0])

        for i in range(lines.__len__()):
            list_components.append(
                ObjTool(
                    name=self.get_name(lines[i]),
                    group_name=name_group,
                    class_name=self.get_name_class(lines[i]),
                    image=self.get_image(lines[i]),
                    image_static=self.get_image_static(lines[i]),
                    latex=self.get_latex(lines[i])
                )
            )

        return list_components

    def get_name(self, text_line):

        name_tool = re.search(r'\[[a-zA-Z0-9\s]+]', text_line).group()
        name_tool = name_tool.replace("[", "")
        name_tool = name_tool.replace("]", "")

        return name_tool

    def get_name_class(self, text_line):

        text = re.search(r'(<class>)(.+)(</class>)', text_line, re.UNICODE).group()
        text = text.replace("<class>", "")
        text = text.replace("</class>", "")

        return text

    def get_image(self, text_line):

        text = re.search(r'(<img>)(.+)(</img>)', text_line)

        if text is not None:
            text = text.group()
            text = text.replace("<img>", "")
            text = text.replace("</img>", "")
            path = os.path.join(self.base_path, text)

        else:
            path = ''

        return path

    def get_image_static(self, text_line):

        text = re.search(r'(<img_static>)(.+)(</img_static>)', text_line)
        if text is not None:
            text = text.group()
            text = text.replace("<img_static>", "")
            text = text.replace("</img_static>", "")

            path = os.path.join(self.base_path, text)

        else:
            path = ''

        return path

    def get_latex(self, text_line):

        text = re.search(r'((<latex>)(.+)(</latex>))', text_line).group()
        text = text.replace("<latex>", "")
        text = text.replace("</latex>", "")

        return text
