import os
import sys

from PyQt6 import QtGui
from PyQt6.QtGui import QGuiApplication, QColor, QPalette


class Resources:

    def __init__(self):
        self.main_path = None
        self.pathResources = None
        self.color_active = None
        self.color_deactivate = None

        if hasattr(sys, '_MEIPASS'):
            # Ruta a la carpeta donde se extrajeron los archivos empaquetados
            self.main_path = sys._MEIPASS
        else:
            # Ruta al directorio del script principal si la aplicación no está empaquetada
            self.main_path = os.path.dirname(os.path.abspath(__file__))
            self.main_path = os.path.dirname(self.main_path)

        if QGuiApplication.styleHints().colorScheme() == QGuiApplication.styleHints().colorScheme().Dark:
            self.color_active = '#DB6725'
            self.color_deactivate = '#996845'
        else:
            self.color_active = '#DB6725'
            self.color_deactivate = '#D9A178'

    def get_active(self):
        return self.color_active

    def get_deactivate(self):
        return self.color_deactivate

    def apply_theme(self, window):

        palette = window.palette()

        if QGuiApplication.styleHints().colorScheme() == QGuiApplication.styleHints().colorScheme().Dark:
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor('#2F2721'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor('#EEC4B2'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor('#5E564F'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor('#E5E3E1'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor('#742B02'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor('#F4DED1'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor('#DB6725'))

            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor('#2F2721'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor('#EEC4B2'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, QColor('#5E564F'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor('#E5E3E1'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, QColor('#742B02'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor('#F4DED1'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor('#DB6725'))
        else:
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, QColor('#F4DED1'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, QColor('#742B02'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, QColor('#EEC4B2'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, QColor('#191C1E'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, QColor('#DF7E48'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, QColor('#2F2721'))
            palette.setColor(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, QColor('#DB6725'))

            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, QColor('#F4DED1'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, QColor('#742B02'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, QColor('#EEC4B2'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, QColor('#191C1E'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, QColor('#DF7E48'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, QColor('#2F2721'))
            palette.setColor(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, QColor('#DB6725'))

        window.setPalette(palette)

    def get_icon_app(self):

        path_icon = os.path.join(self.main_path, 'images/logo_app.svg')
        return QtGui.QIcon(path_icon)

    def get_path(self):

        if QGuiApplication.styleHints().colorScheme() == QGuiApplication.styleHints().colorScheme().Dark:
            self.pathResources = os.path.join(self.main_path, 'images/basic_dark/')
        else:
            self.pathResources = os.path.join(self.main_path, 'images/basic_light/')

        return self.pathResources
