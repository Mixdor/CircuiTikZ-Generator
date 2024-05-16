import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication

from ui.Resources import Resources
from ui.Window import MainWindow

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setHighDpiScaleFactorRoundingPolicy(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.Round)
    app.setStyle('fusion')

    resources = Resources()
    resources.apply_theme(app)

    app.setWindowIcon(resources.get_icon_app())

    mainWindow = MainWindow(resources.main_path)
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.showMaximized()
    mainWindow.setWindowTitle("CircuiTikZ Generator")
    mainWindow.show()
    app.exec()
