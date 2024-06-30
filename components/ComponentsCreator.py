import os

from auxiliar.Calculate import Calculate
from components.ComponentsSelector import ComponentsSelector
from components.Latex import Latex
from objects.ObjComponent import ObjComponent


class ComponentsCreator:

    def __init__(self, history):

        self.draw_component = None
        self.components_selector = ComponentsSelector()
        self.latex = Latex()
        self.calculate = Calculate()
        self.history = history

    def create_traceable_final(self, canvas, path_svg):

        tool = canvas.tool
        start_point = canvas.start_point
        end_point = canvas.end_point
        current_label = canvas.current_label.text()

        if os.path.exists(path_svg):
            draw_comp = self.draw_component.one_pins(
                canvas.devicePixelRatio(),
                start_point, end_point,
                tool,
                canvas.current_label.text()
            )
        else:
            draw_comp = self.draw_component.line(start_point, end_point)
        canvas.update()

        latex_comp = self.latex.get_one_pin(
            start_point / canvas.cell_size,
            end_point / canvas.cell_size,
            tool.latex,
            current_label)

        new_comp = ObjComponent(
            num=len(canvas.components) + 1,
            name=tool.name,
            group_name=tool.group_name,
            class_name=tool.class_name,
            seed_latex=tool.latex,
            middle_point=self.calculate.middle_point(start_point, end_point),
            angle=self.calculate.angle(
                magnitude=self.calculate.magnitude(start_point, end_point),
                start_point=start_point,
                final_point=end_point
            ),
            positions=[start_point, end_point],
            label=current_label,
            drawables=draw_comp,
            latex=latex_comp
        )

        canvas.components.append(new_comp)

        self.history.new_event_undo(1, None, new_comp)
        self.history.list_redo.clear()

    def create_traceable(self, canvas):

        tool = canvas.tool
        start_point = canvas.start_point
        end_point = canvas.end_point
        current_label = canvas.current_label.text()

        if start_point != end_point:

            if tool.name != 'Wire':
                draw_comp = self.draw_component.two_pins(
                    canvas.scene, canvas.devicePixelRatio(),
                    start_point, end_point,
                    tool.image, tool.image_static, current_label
                )
            else:
                draw_comp = self.draw_component.two_pins_no_img(
                    canvas.scene,
                    start_point, end_point,
                    current_label
                )
            canvas.update()

            latex_comp = self.latex.get_two_pin(
                tool.name,
                start_point / canvas.cell_size,
                end_point / canvas.cell_size,
                tool.latex,
                current_label)

            new_comp = ObjComponent(
                num=len(canvas.components)+1,
                name=tool.name,
                group_name=tool.group_name,
                class_name=tool.class_name,
                seed_latex=tool.latex,
                middle_point=self.calculate.middle_point(start_point, end_point),
                angle=self.calculate.angle(
                    magnitude=self.calculate.magnitude(start_point, end_point),
                    start_point=start_point,
                    final_point=end_point
                ),
                positions=[start_point, end_point],
                label=current_label,
                drawables=draw_comp,
                latex=latex_comp
            )

            canvas.components.append(new_comp)

            self.history.new_event_undo(1, None, new_comp)
            self.history.list_redo.clear()

    def create_transistor(self, canvas, path_svg):
        if os.path.exists(path_svg):

            tool = canvas.tool
            point = canvas.end_point
            current_label = canvas.current_label.text()

            draw_comp = self.draw_component.transistor(
                canvas.scene, canvas.devicePixelRatio(), canvas.end_point,
                path_svg, canvas.current_label.text()
            )

            canvas.update()

            latex_comp = self.latex.get_transistor(
                len(canvas.components) + 1,
                point / canvas.cell_size,
                tool.latex,
                current_label
            )

            new_comp = ObjComponent(
                num=len(canvas.components) + 1,
                name=tool.name,
                group_name=tool.group_name,
                class_name=tool.class_name,
                seed_latex=tool.latex,
                middle_point=point,
                angle=0,
                positions=[point],
                label=current_label,
                drawables=draw_comp,
                latex=latex_comp
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

            latex_comp = self.latex.get_transformer(
                len(canvas.components) + 1,
                point / canvas.cell_size,
                tool.latex,
                current_label
            )

            new_comp = ObjComponent(
                num=len(canvas.components) + 1,
                name=tool.name,
                group_name=tool.group_name,
                class_name=tool.class_name,
                seed_latex=tool.latex,
                middle_point=point,
                angle=0,
                positions=[point],
                label=current_label,
                drawables=draw_comp,
                latex=latex_comp
            )

            canvas.components.append(new_comp)

            self.history.new_event_undo(1, None, new_comp)
            self.history.list_redo.clear()

        else:
            print("No found image")
