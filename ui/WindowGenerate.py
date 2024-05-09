import pyperclip
from PyQt6.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QTextEdit, QPushButton, QDialog, QHBoxLayout
from components.Latex import Latex


class WindowGenerate(QDialog):
    def __init__(self, draws_list):
        super().__init__()
        self.setWindowTitle('Generated')
        self.setGeometry(150, 150, 350, 500)
        self.latexGen = Latex()

        self.draw_list = draws_list
        self.dic_settings = {
            'wrap_in_figure': 0,
            'american_style_components': 0
        }

        self.layout = QVBoxLayout()
        self.widget_layout = QWidget(self)
        self.widget_layout.setLayout(self.layout)

        layout_settings1 = QHBoxLayout()
        self.layout.addLayout(layout_settings1)

        check_figure = QCheckBox("Wrap in Figure")
        check_figure.stateChanged.connect(self.figure_change)
        check_style_american = QCheckBox("American Style")
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

        pyperclip.copy(self.text_area.toPlainText())

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
