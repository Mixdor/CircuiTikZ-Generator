from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QWidget, QLabel, QPushButton, QHBoxLayout


class WindowNewVersion(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle('New Version Available')
        self.setGeometry(150, 150, 300, 100)

        self.layout = QVBoxLayout()
        self.widget_layout = QWidget(self)
        self.widget_layout.setLayout(self.layout)

        self.description = QLabel('It is recommended to download the new version\nto enjoy the latest features and bug '
                                  'fixes.')
        self.description.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.description)

        self.layout_button = QHBoxLayout()
        self.layout.addLayout(self.layout_button)

        self.button = QPushButton('Download')
        self.button.setFixedWidth(150)
        self.button.clicked.connect(self.web_sourceforge)
        self.layout_button.addWidget(self.button)

        self.setLayout(self.layout)

    def web_sourceforge(self):
        url = QUrl('https://sourceforge.net/projects/circuitikz-generator/')
        QDesktopServices.openUrl(url)
        self.accept()
