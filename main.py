import os
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from ui.Window import MainWindow

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        # Ruta a la carpeta donde se extrajeron los archivos empaquetados
        base_path = sys._MEIPASS
    else:
        # Ruta al directorio del script principal si la aplicación no está empaquetada
        base_path = os.path.dirname(os.path.abspath(__file__))
    app = QApplication(sys.argv)

    path_icon = os.path.join(base_path, 'images/IconApp.png')
    app.setWindowIcon(QtGui.QIcon(path_icon))

    mainWindow = MainWindow(base_path)
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.setWindowTitle("CircuiTikZ Generator")
    mainWindow.show()
    sys.exit(app.exec_())
