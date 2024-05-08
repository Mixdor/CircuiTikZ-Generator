import os
import sys

from PyQt6 import QtGui
from PyQt6.QtGui import QIcon, QPalette
from PyQt6.QtWidgets import QApplication
from ui.Window import MainWindow
from ui.Resources import Resources

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyle('fusion')

    resources = Resources()
    resources.apply_theme(app)

    app.setWindowIcon(resources.get_icon_app())

    mainWindow = MainWindow(resources.main_path)
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.setWindowTitle("CircuiTikZ Generator")
    mainWindow.show()
    app.exec()
