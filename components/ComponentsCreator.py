import os

from PyQt6.QtCore import Qt

from auxiliar.Calculate import Calculate
from components.ComponentsSelector import ComponentsSelector
from components.Latex import Latex
from objects.Components import ObjComponent, ObjPosition, ObjScales, ObjColors
from objects.Tools import ObjTool


class ComponentsCreator:

    def __init__(self, history):

        self.draw_component = None
        self.components_selector = ComponentsSelector()
        self.latex = Latex()
        self.calculate = Calculate()
        self.history = history

    def create_simple_node(self, canvas, path_svg):

        tool = canvas.tool
        end_point = canvas.end_point
        current_label = canvas.current_label.text()
        draw_comp = None

        if os.path.exists(path_svg):

            draw_comp = self.draw_component.one_pins(
                canvas.devicePixelRatio(),
                end_point,
                tool,
                canvas.current_label.text(),
                Qt.GlobalColor.black
            )

            canvas.update()


        # obj_position = ObjPosition(
        #     start_point=start_point,
        #     middle_point=self.calculate.middle_point(start_point, end_point),
        #     end_point=end_point
        # )

        # angle = self.calculate.angle(
        #     magnitude=self.calculate.magnitude(start_point, end_point),
        #     start_point=start_point,
        #     final_point=end_point
        # )

        new_comp = ObjComponent(
            num=len(canvas.components) + 1,
            built_tool=tool,
            positions=ObjPosition(None, end_point, None),
            rotation=0,
            scales=ObjScales(1, 1),
            label=current_label,
            colors=ObjColors("black", ""),
            draws=draw_comp
        )

        canvas.components.append(new_comp)

        self.history.new_event_undo(1, None, new_comp)
        self.history.list_redo.clear()

    def create_traceable(self, canvas):

        tool : ObjTool = canvas.tool
        start_point = canvas.start_point
        end_point = canvas.end_point
        current_label = canvas.current_label.text()

        difference = self.calculate.difference(start_point, end_point)

        if difference > 40 or tool.name == 'Wire':

            if tool.name != 'Wire':
                draw_comp = self.draw_component.two_pins(
                    canvas.scene, canvas.devicePixelRatio(),
                    start_point, end_point,
                    tool.canvas_stroke, tool.canvas_stroke_static, current_label,
                    Qt.GlobalColor.black
                )
            else:
                draw_comp = self.draw_component.two_pins_no_img(
                    canvas.scene,
                    start_point, end_point,
                    current_label,
                    Qt.GlobalColor.black
                )
            canvas.update()

            obj_position = ObjPosition(
                start_point = start_point,
                middle_point = self.calculate.middle_point(start_point, end_point),
                end_point = end_point
            )

            angle = self.calculate.angle(
                magnitude=self.calculate.magnitude(start_point, end_point),
                start_point=start_point,
                final_point=end_point
            )

            new_comp = ObjComponent(
                num = len(canvas.components) + 1,
                built_tool = tool,
                positions = obj_position,
                rotation = angle,
                scales = ObjScales(1,1),
                label = current_label,
                colors = ObjColors("black", ""),
                draws = draw_comp
            )

            canvas.components.append(new_comp)

            self.history.new_event_undo(1, None, new_comp)
            self.history.list_redo.clear()

    def create_transistor(self, canvas, point, path_svg):
        if os.path.exists(path_svg):

            tool = canvas.tool
            current_label = canvas.current_label.text()

            draw_comp = self.draw_component.transistor(
                canvas.scene, canvas.devicePixelRatio(), canvas.end_point,
                path_svg, 0, canvas.current_label.text(), ObjScales(1.0, 1.0)
            )

            canvas.update()

            new_comp = ObjComponent(
                num=len(canvas.components) + 1,
                built_tool=tool,
                positions=ObjPosition(None, point, None),
                rotation=0,
                scales=ObjScales(1, 1),
                label=current_label,
                colors=ObjColors("black", ""),
                draws=draw_comp
            )

            canvas.components.append(new_comp)

            self.history.new_event_undo(1, None, new_comp)
            self.history.list_redo.clear()

        else:
            print("No found image")

    def create_amplifier(self, canvas, path_svg):

        if os.path.exists(path_svg):

            tool = canvas.tool
            point = canvas.end_point
            current_label = canvas.current_label.text()

            draw_comp = self.draw_component.amplifier(
                canvas.scene, canvas.devicePixelRatio(), canvas.end_point,
                path_svg, canvas.current_label.text(),
            )

            canvas.update()

            new_comp = ObjComponent(
                num=len(canvas.components) + 1,
                built_tool=tool,
                positions=ObjPosition(None, point, None),
                rotation=0,
                scales=ObjScales(1, 1),
                label=current_label,
                colors=ObjColors("black", ""),
                draws=draw_comp
            )

            canvas.components.append(new_comp)

            self.history.new_event_undo(1, None, new_comp)
            self.history.list_redo.clear()

        else:
            print("No found image")

    def create_transformer(self, canvas, path_svg):
        if os.path.exists(path_svg):

            tool = canvas.tool
            point = canvas.end_point
            current_label = canvas.current_label.text()

            draw_comp = self.draw_component.transformer(
                canvas.scene, canvas.devicePixelRatio(),
                point, path_svg, current_label
            )

            canvas.update()

            new_comp = ObjComponent(
                num=len(canvas.components) + 1,
                built_tool=tool,
                positions=ObjPosition(None, point, None),
                rotation=0,
                scales=ObjScales(1, 1),
                label=current_label,
                colors=ObjColors("black", ""),
                draws=draw_comp
            )

            canvas.components.append(new_comp)

            self.history.new_event_undo(1, None, new_comp)
            self.history.list_redo.clear()

        else:
            print("No found image")
