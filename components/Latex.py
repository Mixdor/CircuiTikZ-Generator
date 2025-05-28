import math

from PyQt6.QtCore import QPoint, QPointF

from objects.Components import ObjScales


class Latex:

    def __init__(self):
        super().__init__()
        self.cell_size = 50

    def get_one_pin(self, start_point:QPointF, final_point:QPointF, latex:str, label:str):
        draws = []
        x1 = str(start_point.x() / self.cell_size)
        y1 = str(start_point.y() / self.cell_size)
        x2 = str(final_point.x() / self.cell_size)
        y2 = str(final_point.y() / self.cell_size)

        draw_text = '\\draw(' + x1 + ",-" + y1 + ')to(' + x2 + ',-' + y2 + ') ' + latex + '{' + label + '}' + ';'
        draws.append(draw_text)

        return draws

    def get_two_pin(self, name_tool:str, start_point:QPointF, final_point:QPointF, latex:str, label:str):
        draws = []
        x1 = str(start_point.x() / self.cell_size)
        y1 = str(start_point.y() / self.cell_size)
        x2 = str(final_point.x() / self.cell_size)
        y2 = str(final_point.y() / self.cell_size)

        if name_tool == 'Ramp Oscilloscope':
            draws.append('\\ctikzset{bipoles/oscope/waveform=ramps}')
        elif name_tool == 'Sin Oscilloscope':
            draws.append('\\ctikzset{bipoles/oscope/waveform=sin}')
        elif name_tool == 'Square Oscilloscope':
            draws.append('\\ctikzset{bipoles/oscope/waveform=square}')
        elif name_tool == 'Triangle Oscilloscope':
            draws.append('\\ctikzset{bipoles/oscope/waveform=triangle}')
        elif name_tool == 'Lissajous Oscilloscope':
            draws.append('\\ctikzset{bipoles/oscope/waveform=lissajous}')
        elif name_tool == 'Zero Oscilloscope':
            draws.append('\\ctikzset{bipoles/oscope/waveform=zero}')
        elif name_tool == 'None Oscilloscope':
            draws.append('\\ctikzset{bipoles/oscope/waveform=none}')

        scale = ",/tikz/circuitikz/bipoles/length=1.1cm"
        if latex=="short":
            scale = ""

        draw_text = f"\\draw[{latex}={{{label}}}{scale}]({x1},-{y1})to({x2},-{y2});"
        #draw_text = '\\draw[' + latex + '={' + label + '}](' + x1 + ",-" + y1 + ')to(' + x2 + ',-' + y2 + ');'
        draws.append(draw_text)

        return draws

    def get_transistor(self, id_node:int, point:QPointF, latex:str, label:str, rotation:float, scales:ObjScales):

        draws = []
        node = 'Q' + str(id_node)

        cx = point.x() / self.cell_size
        cy = point.y() / self.cell_size

        angle = rotation
        if scales.x_scale == -1:
            angle = (360 - angle) % 360
        if scales.y_scale == -1:
            angle = (180 - angle) % 360
        if angle < 0:
            angle = angle + (90 * 4)

        radian = angle * (math.pi / 180)

        top_x = (point.x() / self.cell_size)
        top_y = (point.y() / self.cell_size) - 0.5
        top_x_ = cx + (math.cos(radian) * (top_x - cx)) - (math.sin(radian) * (top_y - cy))
        top_y_ = cy + (math.sin(radian) * (top_x - cx)) + (math.cos(radian) * (top_y - cy))

        button_x = (point.x() / self.cell_size)
        button_y = (point.y() / self.cell_size) + 0.5

        button_x_ = cx + (math.cos(radian) * (button_x - cx)) - (math.sin(radian) * (button_y - cy))
        button_y_ = cy + (math.sin(radian) * (button_x - cx)) + (math.cos(radian) * (button_y - cy))


        if latex.__contains__('mos'):
            draw_properties = '\\ctikzset{tripoles/mos style/arrows}'
            draws.append(draw_properties)

        if (latex.__contains__('npn') or latex.__contains__('nigbt') or latex.__contains__('nmos')
                or latex.__contains__('hemt') or latex.__contains__('nfet')):
            conf = ['C', 'B', 'E']
        else:
            conf = ['E', 'B', 'C']

        #label_cord : str
        cord = {0.0:"west", 90.0:"north", -270.0:"north", 180.0:"east", -180.0:"east", 270.0:"south", -90.0:"south"}
        label_cord = self.calculate_position_label(rotation, scales.x_scale, scales.y_scale)

        draw_node = f"\\draw node[{latex},scale=0.59,xscale={scales.x_scale},yscale={scales.y_scale},rotate={rotation*-1}]({node}) at ({str(cx)},-{str(cy)}) {{}} node[anchor={label_cord},scale=0.9] at ({node}.text){{{label}}};"
        draw_line_top = f"\\draw[short]({node}.{conf[0]})to({str(top_x_)},-{str(top_y_)});"
        draw_line_button = f"\\draw[short]({node}.{conf[2]})to({str(button_x_)},-{str(button_y_)});"


        draws.append(draw_node)
        draws.append(draw_line_top)
        draws.append(draw_line_button)

        return draws

    def get_transformer(self, id_node:int, point:QPointF, latex:str, label:str):

        draws = []
        node = 'Q' + str(id_node)
        x = str(point.x() / self.cell_size)
        y = str(point.y() / self.cell_size)

        draw_node = '\\draw (' + x + ",-" + y + ') ' + latex + '(' + node + ')' + '{' + label + '}' + ';'
        draws.append(draw_node)

        return draws

    def get_amplifier(self, id_node:int, x:float, y:float, latex:str, label:str):

        draws = []
        node = 'Q' + str(id_node)

        x_int = x / self.cell_size
        x = str((x / self.cell_size) + 0.22)
        y = str(y / self.cell_size)

        draw_node = '\\draw (' + x + ",-" + y + ') ' + latex + '(' + node + ')' + '{' + label + '}' + ';'
        draw_out = '\\draw[short](' + node + '.out)to(+' + str(x_int+1.5) + ', -' + y + ');'

        draws.append(draw_node)
        draws.append(draw_out)

        return draws

    def full_generete(self, draw_list, settings):

        generated = ""

        if settings['wrap_in_figure'] == 1:
            generated = generated + "\\begin{figure}[h]" + "\n"
            generated = generated + "\\centering" + "\n"

        if settings['american_style_components'] == 1:
            generated = generated + "\\begin{circuitikz}[american]" + "\n"
        else:
            generated = generated + "\\begin{circuitikz}" + "\n"

        for i in range(len(draw_list)):
            draw_sublist = draw_list[i]
            for j in range(len(draw_sublist)):
                generated = generated + draw_sublist[j] + "\n"

        generated = generated + "\\end{circuitikz}" + "\n"

        if settings['wrap_in_figure'] == 1:
            generated = generated + "\\end{figure}" + "\n"

        return generated

    def calculate_position_label(self, rotation:float, split_x:float, split_y:float) -> str:

        angle = (90 + rotation) % 360

        if split_x == -1:
            angle = (360 - angle) % 360
        if split_y == -1:
            angle = (180 - angle) % 360
        if angle < 0:
            angle = angle + (90 * 4)

        dic_cord = {
            0.0 : "south",
            90.0: "west",
            180.0: "north",
            270.0: "east"
        }

        return dic_cord.get(angle, "Unknow")
