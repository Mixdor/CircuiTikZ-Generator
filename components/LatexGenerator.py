class LatexGenerator:

    def getDraw(self, point_initial, point_final, latex, text_aux):
        x1 = str(point_initial.x())
        y1 = str(point_initial.y())
        x2 = str(point_final.x())
        y2 = str(point_final.y())

        draw_text = '\\draw (' + x1 + ",-" + y1 + ')to[' + latex + '=' + text_aux + '] (' + x2 + ',-' + y2 + ');'

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
