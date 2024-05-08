from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCheckBox
from settings.Settings import Settings


class WindowSettings(QWidget):
    def __init__(self, base_path):
        super().__init__()
        self.setWindowTitle("settings")
        self.setGeometry(150, 150, 270, 100)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.aux_settings = Settings(base_path)

        check_figure = QCheckBox("Wrap in Figure")
        check_figure.stateChanged.connect(self.figure_change)
        check_style_american = QCheckBox("American Style Components")
        check_style_american.stateChanged.connect(self.american_change)

        self.settings = self.aux_settings.get_settings()
        wrap_in_figure = self.settings['wrap_in_figure']
        american_style = self.settings['american_style_components']

        if wrap_in_figure == 1:
            check_figure.setCheckState(Qt.CheckState.Checked)

        if american_style == 1:
            check_style_american.setCheckState(Qt.CheckState.Checked)

        done = QPushButton('Done', self)
        done.clicked.connect(self.on_button_done)

        self.layout.addWidget(check_figure)
        self.layout.addWidget(check_style_american)
        self.layout.addWidget(done)

    def on_button_done(self):

        keys = list(self.settings.keys())
        values = list(self.settings.values())

        self.aux_settings.save_Settings(keys, values)

        self.close()

    def figure_change(self, state):
        if state:
            self.settings['wrap_in_figure'] = 1
        else:
            self.settings['wrap_in_figure'] = 0

    def american_change(self, state):
        if state:
            self.settings['american_style_components'] = 1
        else:
            self.settings['american_style_components'] = 0
