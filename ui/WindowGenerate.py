from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QTextEdit, QPushButton, QDialog, QHBoxLayout, QApplication

from components.Latex import Latex
from objects.Components import ObjComponent


class WindowGenerate(QDialog):

    def __init__(self, components:list[ObjComponent]):
        super().__init__()
        self.setWindowTitle('Generated')
        self.setGeometry(150, 150, 350, 500)
        self.latexGen = Latex()

        self.draw_list : list[str] = []

        for component in components:

            latex = None

            if component.built_tool.class_ == 'Traceable_Final':

                latex = self.latexGen.get_one_pin(
                    start_point=component.positions.start_point,
                    final_point=component.positions.end_point,
                    latex=component.built_tool.latex,
                    label=component.label
                )

            elif component.built_tool.class_ == 'Traceable':

                latex = self.latexGen.get_two_pin(
                    component.built_tool.name,
                    start_point=component.positions.start_point,
                    final_point=component.positions.end_point,
                    latex=component.built_tool.latex,
                    label=component.label
                )

            elif component.built_tool.class_ == 'Transistor':

                latex = self.latexGen.get_transistor(
                    id_node=component.num,
                    point=component.positions.middle_point,
                    latex=component.built_tool.latex,
                    label=component.label,
                    rotation=component.rotation
                )

            elif component.built_tool.class_ == 'Amplifier':

                latex = self.latexGen.get_amplifier(
                    id_node=component.num,
                    x=component.positions.middle_point.x(),
                    y=component.positions.middle_point.y(),
                    latex=component.built_tool.latex,
                    label=component.label
                )

            elif component.built_tool.class_ == 'Transformer':

                latex = self.latexGen.get_transformer(
                    id_node=component.num,
                    point=component.positions.middle_point,
                    latex=component.built_tool.latex,
                    label=component.label
                )

            else:
                print("Number pins not found")

            if latex:
                self.draw_list.append(latex)

        self.dic_settings = {
            'wrap_in_figure': 0,
            'american_style_components': 1
        }

        self.layout = QVBoxLayout()
        self.widget_layout = QWidget(self)
        self.widget_layout.setLayout(self.layout)

        layout_settings1 = QHBoxLayout()
        self.layout.addLayout(layout_settings1)

        check_figure = QCheckBox("Wrap in Figure")
        check_figure.stateChanged.connect(self.figure_change)
        check_style_american = QCheckBox("American Style")
        check_style_american.setCheckState(Qt.CheckState.Checked)
        check_style_american.stateChanged.connect(self.american_change)

        layout_settings1.addWidget(check_figure)
        layout_settings1.addWidget(check_style_american)

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setText(self.latexGen.full_generete(self.draw_list, self.dic_settings))

        self.copy = QPushButton("Copy")
        self.copy.clicked.connect(self.clipboard)

        self.layout.addWidget(self.text_area)
        self.layout.addWidget(self.copy)

        self.setLayout(self.layout)

    def clipboard(self):

        QApplication.clipboard().setText(self.text_area.toPlainText())

    def figure_change(self, state):
        if state:
            self.dic_settings['wrap_in_figure'] = 1
            self.text_area.setText(self.latexGen.full_generete(self.draw_list, self.dic_settings))
        else:
            self.dic_settings['wrap_in_figure'] = 0
            self.text_area.setText(self.latexGen.full_generete(self.draw_list, self.dic_settings))

    def american_change(self, state):
        if state:
            self.dic_settings['american_style_components'] = 1
            self.text_area.setText(self.latexGen.full_generete(self.draw_list, self.dic_settings))
        else:
            self.dic_settings['american_style_components'] = 0
            self.text_area.setText(self.latexGen.full_generete(self.draw_list, self.dic_settings))
