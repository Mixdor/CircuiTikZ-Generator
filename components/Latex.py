from PyQt6.QtCore import QPoint


class Latex:

    def get_one_pin(self, start_point, final_point, latex, label):
        draws = []
        x1 = str(start_point.x())
        y1 = str(start_point.y())
        x2 = str(final_point.x())
        y2 = str(final_point.y())

        draw_text = '\\draw (' + x1 + ",-" + y1 + ')to(' + x2 + ',-' + y2 + ') ' + latex + '{' + label + '}' + ';'
        draws.append(draw_text)

        return draws

    def get_two_pin(self, start_point, final_point, latex, label):
        draws = []
        x1 = str(start_point.x())
        y1 = str(start_point.y())
        x2 = str(final_point.x())
        y2 = str(final_point.y())

        draw_text = '\\draw (' + x1 + ",-" + y1 + ')to[' + latex + '={' + label + '}] (' + x2 + ',-' + y2 + ');'
        draws.append(draw_text)

        return draws

    def get_transistor(self, id_node, point, latex, label):
        draws = []
        node = 'Q' + str(id_node + 1)
        top = QPoint(point.x(), point.y() - 1)
        button = QPoint(point.x(), point.y() + 1)
        middle = QPoint(point.x() - 1, point.y())
        x = str(point.x())
        y = str(point.y())

        if latex.__contains__('mos'):
            draw_properties = '\\ctikzset{tripoles/mos style/arrows}'
            draws.append(draw_properties)

        if (latex.__contains__('npn') or latex.__contains__('nigbt') or latex.__contains__('nmos')
                or latex.__contains__('hemt') or latex.__contains__('nfet')):
            conf = ['C', 'B', 'E']
        else:
            conf = ['E', 'B', 'C']

        draw_node = '\\draw (' + x + ",-" + y + ') ' + latex + '(' + node + ')' + '{' + label + '}' + ';'
        draw_line_top = '\\draw (' + node + '.' + conf[0] + ') to[short] (' + str(top.x()) + ',-' + str(top.y()) + ');'
        draw_line_middle = '\\draw (' + node + '.' + conf[1] + ') to[short] (' + str(middle.x()) + ',-' + str(
            middle.y()) + ');'
        draw_line_button = '\\draw (' + node + '.' + conf[2] + ') to[short] (' + str(button.x()) + ',-' + str(
            button.y()) + ');'

        draws.append(draw_node)
        draws.append(draw_line_top)
        draws.append(draw_line_middle)
        draws.append(draw_line_button)

        return draws

    def get_transformer(self, id_node, point, latex, label):

        draws = []
        node = 'Q' + str(id_node + 1)
        x = str(point.x())
        y = str(point.y())

        draw_node = '\\draw (' + x + ",-" + y + ') ' + latex + '(' + node + ')' + '{' + label + '}' + ';'
        draws.append(draw_node)

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
