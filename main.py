import sys
from PyQt5.QtWidgets import QApplication
from ui.Window import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.setGeometry(100, 100, 800, 600)
    mainWindow.setWindowTitle("CircuiTikZ Generator")
    mainWindow.show()
    sys.exit(app.exec_())
