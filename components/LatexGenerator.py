class LatexGenerator:

    def getDrawOnePin(self, start_point, final_point, latex, label):
        x1 = str(start_point.x())
        y1 = str(start_point.y())
        x2 = str(final_point.x())
        y2 = str(final_point.y())

        draw_text = '\\draw (' + x1 + ",-" + y1 + ')to(' + x2 + ',-' + y2 + ') ' + latex + '{' + label + '}' + ';'

        return draw_text

    def getDrawTwoPin(self, start_point, final_point, latex, label):
        x1 = str(start_point.x())
        y1 = str(start_point.y())
        x2 = str(final_point.x())
        y2 = str(final_point.y())

        draw_text = '\\draw (' + x1 + ",-" + y1 + ')to[' + latex + '=' + label + '] (' + x2 + ',-' + y2 + ');'

        return draw_text

    def get_latex_full(self, draw_list, settings):

        generated = ""

        if settings['wrap_in_figure'] == 1:
            generated = generated + "\\begin{figure}[h]" + "\n"
            generated = generated + "\\centering" + "\n"

        if settings['american_style_components'] == 1:
            generated = generated + "\\begin{circuitikz}[american]" + "\n"
        else:
            generated = generated + "\\begin{circuitikz}" + "\n"

        for i in range(draw_list.__len__()):
            generated = generated + draw_list[i] + "\n"

        generated = generated + "\\end{circuitikz}" + "\n"

        if settings['wrap_in_figure'] == 1:
            generated = generated + "\\end{figure}" + "\n"

        return generated
