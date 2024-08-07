from PyQt6.QtCore import QPoint


class Latex:

    def __init__(self):
        super().__init__()
        self.cell_size = 50

    def get_one_pin(self, start_point, final_point, latex, label):
        draws = []
        x1 = str(start_point.x() / self.cell_size)
        y1 = str(start_point.y() / self.cell_size)
        x2 = str(final_point.x() / self.cell_size)
        y2 = str(final_point.y() / self.cell_size)

        draw_text = '\\draw(' + x1 + ",-" + y1 + ')to(' + x2 + ',-' + y2 + ') ' + latex + '{' + label + '}' + ';'
        draws.append(draw_text)

        return draws

    def get_two_pin(self, name_tool, start_point, final_point, latex, label):
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
        draw_text = '\\draw[' + latex + '={' + label + '}](' + x1 + ",-" + y1 + ')to(' + x2 + ',-' + y2 + ');'
        draws.append(draw_text)

        return draws

    def get_transistor(self, id_node, point, latex, label):
        draws = []
        node = 'Q' + str(id_node)
        top = QPoint(point.x(), point.y() - 1)
        top_x = (point.x() / self.cell_size)
        top_y = (point.y() / self.cell_size) - 0.5
        button = QPoint(point.x(), point.y() + 1)
        button_x = (point.x() / self.cell_size)
        button_y = (point.y() / self.cell_size) + 0.5

        x = str(point.x() / self.cell_size)
        y = str(point.y() / self.cell_size)

        if latex.__contains__('mos'):
            draw_properties = '\\ctikzset{tripoles/mos style/arrows}'
            draws.append(draw_properties)

        if (latex.__contains__('npn') or latex.__contains__('nigbt') or latex.__contains__('nmos')
                or latex.__contains__('hemt') or latex.__contains__('nfet')):
            conf = ['C', 'B', 'E']
        else:
            conf = ['E', 'B', 'C']

        draw_node = '\\draw(' + x + ",-" + y + ') ' + latex + '(' + node + ')' + '{' + label + '}' + ';'
        draw_line_top = '\\draw[short](' + node + '.' + conf[0] + ')to(' + str(top_x) + ',-' + str(top_y) + ');'
        draw_line_button = '\\draw[short](' + node + '.' + conf[2] + ')to(' + str(button_x) + ',-' + str(
            button_y) + ');'

        draws.append(draw_node)
        draws.append(draw_line_top)
        draws.append(draw_line_button)

        return draws

    def get_transformer(self, id_node, point, latex, label):

        draws = []
        node = 'Q' + str(id_node)
        x = str(point.x() / self.cell_size)
        y = str(point.y() / self.cell_size)

        draw_node = '\\draw (' + x + ",-" + y + ') ' + latex + '(' + node + ')' + '{' + label + '}' + ';'
        draws.append(draw_node)

        return draws

    def get_amplifier(self, id_node, x, y, latex, label):

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
