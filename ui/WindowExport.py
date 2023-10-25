import pyperclip
from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QTextEdit, QPushButton
from components.LatexGenerator import LatexGenerator
from settings.Settings import Settings


class WindowExport(QWidget):
    def __init__(self, draws_list, base_path):
        super().__init__()
        self.setWindowTitle('Generated')
        self.setGeometry(150, 150, 350, 500)
        self.latexGen = LatexGenerator()
        self.aux_settings = Settings(base_path)

        self.draw_list = draws_list
        self.dic_settings = self.aux_settings.get_settings()

        self.layout = QVBoxLayout()
        self.widget_layout = QWidget(self)
        self.widget_layout.setLayout(self.layout)

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(False)
        self.text_area.setText(self.latexGen.get_latex_full(self.draw_list, self.dic_settings))

        self.copy = QPushButton("Copy")
        self.copy.clicked.connect(self.clipboard)

        self.layout.addWidget(self.text_area)
        self.layout.addWidget(self.copy)

        self.setLayout(self.layout)

    def clipboard(self):

        pyperclip.copy(self.text_area.toPlainText())
