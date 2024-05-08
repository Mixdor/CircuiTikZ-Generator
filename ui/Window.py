import threading

from PyQt6.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut, QIcon, QDesktopServices
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import *

from auxiliar.SourceForge import SourceForge
from components.ComponentsManager import ComponentsManager
from components.History import History
from drawables.DrawComponent import DrawComponent
from objects.ObjTool import ObjTool
from components.TxtToComponents import TxtToComponents
from ui.MainCanvas import Canvas
from ui.WindowGenerate import WindowGenerate
from ui.Resources import Resources
from ui.WindowNewVersion import WindowNewVersion


class MainWindow(QMainWindow):
    def __init__(self, base_path):
        super().__init__()
        self.showMaximized()

        # self.setWindowIcon(QtGui.QIcon('images/araña2.png'))
        self.resources = Resources()

        self.base_path = base_path
        self.setMouseTracking(True)

        self.botones = []
        self.obj_tools = []
        self.tool_selected = ObjTool("Select", "Basic", 0, 'images/components_svg/arrow_selector.svg', '')
        self.components_added = []
        self.components_deleted = []
        self.draw_added = []
        self.draw_deleted = []

        shortcut_undo = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Z), self)
        shortcut_undo.activated.connect(self.on_undo2)
        shortcut_redo = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_Z), self)
        shortcut_redo.activated.connect(self.on_redo2)

        layout = QHBoxLayout()

        layout_tools = QVBoxLayout()
        widget_layout_tools = QWidget(self)
        widget_layout_tools.setLayout(layout_tools)
        widget_layout_tools.setFixedWidth(250)
        layout.addWidget(widget_layout_tools)

        self.name_app = QLabel('CircuiTikZ Generator v0.5')
        self.name_app.setStyleSheet("font-size: 11pt; font-weight: bold")
        self.name_app.setContentsMargins(0, 0, 0, 11)
        layout_tools.addWidget(self.name_app)
        print(f'::: {self.name_app.text()} :::')

        layout_scroll_area = QVBoxLayout()
        layout_scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)

        txt_to_components = TxtToComponents(self.base_path)

        list_groups_components = txt_to_components.get_groups()

        # Agregar contenido al layout
        for i in range(list_groups_components.__len__()):

            group_str = list_groups_components[i]
            name = txt_to_components.get_name_group(group_str)
            label_name = QLabel(name)
            layout_scroll_area.addWidget(label_name)

            current_tools = txt_to_components.get_tools_for_group(group_str, name)

            for k in range(current_tools.__len__()):
                tool = current_tools[k]
                self.obj_tools.append(tool)
                button = QPushButton(tool.name)
                button.setStyleSheet(f'background-color: {self.resources.color_deactivate}; color: black;')
                button.clicked.connect(self.on_button_click)

                if tool.name == "Select":
                    button.setStyleSheet(f'background-color: {self.resources.color_active}; color: black;')

                self.botones.append(button)
                layout_scroll_area.addWidget(button)

        # Crear un área de desplazamiento y configurar el layout dentro de ella
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Permitir que el widget contenido cambie de tamaño
        scroll_content = QWidget()
        scroll_content.setLayout(layout_scroll_area)
        scroll_area.setWidget(scroll_content)

        layout_tools.addWidget(scroll_area)

        layout_canvas_properties = QVBoxLayout()
        layout_canvas_properties.setContentsMargins(11, 0, 11, 11)
        widget_canvas_properties = QWidget(self)
        widget_canvas_properties.setLayout(layout_canvas_properties)
        layout.addWidget(widget_canvas_properties)

        layout_properties = QHBoxLayout()
        layout_properties.setContentsMargins(0, 0, 0, 0)
        widget_layout_properties = QWidget(self)
        widget_layout_properties.setFixedHeight(64)
        widget_layout_properties.setLayout(layout_properties)

        layout_properties.addWidget(QLabel('Component label'))
        self.label_component = QTextEdit()
        self.label_component.setFixedHeight(28)

        layout_properties.addWidget(self.label_component)

        self.button_delete = QPushButton(QIcon(f'{self.resources.get_path()}/delete.svg'), '')
        self.button_delete.setEnabled(False)
        self.button_delete.clicked.connect(self.delete_component)
        layout_properties.addWidget(self.button_delete)

        self.svg_widget = QSvgWidget(parent=self)
        self.svg_widget.setFixedSize(40, 40)
        self.svg_widget.setStyleSheet(
            'background-color: white; color: white; border: 1.5px solid #742B02; border-radius: 3px;'
        )
        self.svg_widget.load(self.tool_selected.get_image())
        layout_properties.addWidget(self.svg_widget)

        label_cord = QLabel("Coordinates: [0,0]")
        layout_tools.addWidget(label_cord)

        layout_export = QHBoxLayout()
        widget_layout_export = QWidget(self)
        widget_layout_export.setLayout(layout_export)
        layout_export.setContentsMargins(0, 0, 0, 0)
        layout_tools.addWidget(widget_layout_export)

        button_export = QPushButton("Generate", self)
        button_export.clicked.connect(self.show_generate_latex)
        button_web = QPushButton(QIcon(f'{self.resources.get_path()}/link_web.svg'), '', self)
        button_web.setFixedWidth(30)
        button_web.clicked.connect(self.show_web)

        layout_export.addWidget(button_export)
        layout_export.addStrut(1)
        layout_export.addWidget(button_web)

        layout_donate = QHBoxLayout()
        widget_layout_donate = QWidget(self)
        widget_layout_donate.setLayout(layout_donate)
        layout_donate.setContentsMargins(0, 0, 0, 0)
        layout_tools.addWidget(widget_layout_donate)

        button_donate = QPushButton(QIcon(f'{self.resources.get_path()}/ko-fi-icon.svg'), ' Support me ', self)
        button_donate.clicked.connect(self.show_kofi)

        # button_about = QPushButton(QIcon(f'{self.resources.get_path()}/info.svg'), '', self)
        # button_about.setFixedWidth(30)
        # button_about.clicked.connect(self.show_win_about)

        layout_donate.addWidget(button_donate)
        # layout_donate.addStrut(1)
        # layout_donate.addWidget(button_about)

        layout_canvas_properties.addWidget(widget_layout_properties)
        self.history = History()
        self.manager_components = ComponentsManager(self.history)
        self.canvas = Canvas(
            label_cord,
            self.tool_selected,
            self.components_added,
            self.draw_added,
            self.label_component,
            self.button_delete,
            self.manager_components)
        self.canvas_scene = self.canvas.scene
        self.manager_components.canvas = self.canvas
        self.manager_components.draw_component = DrawComponent(self.canvas.scene)
        layout_canvas_properties.addWidget(self.canvas)

        self.hilo = MiHilo(self.name_app.text())
        self.hilo.finished.connect(self.show_winversion)
        self.hilo.start()

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def on_button_click(self):

        self.manager_components.unselected()

        button = self.sender()

        list_buttons = self.botones
        for i in range(list_buttons.__len__()):
            list_buttons[i].setStyleSheet(f'background-color: {self.resources.color_deactivate}; color: black;')

        current_tool = None

        for j in range(self.obj_tools.__len__()):
            if self.obj_tools[j].name == button.text():
                current_tool = self.obj_tools[j]

        if self.tool_selected != current_tool:

            self.tool_selected = ObjTool(
                current_tool.name, current_tool.name_class,
                current_tool.number_pins,
                current_tool.image, current_tool.latex)

            self.canvas.set_tool(self.tool_selected)

            self.svg_widget.load(self.tool_selected.get_image())

            button.setStyleSheet(f'background-color: {self.resources.color_active}; color: black;')
        else:
            button.setStyleSheet(f'background-color: {self.resources.color_active}; color: black;')

    def delete_component(self):
        if self.canvas.component_selected:
            self.manager_components.delete_selected()

    def show_generate_latex(self):
        self.manager_components.unselected()
        dialog = WindowGenerate(self.draw_added, self.base_path)
        dialog.move(self.frameGeometry().topLeft() + self.rect().center() - dialog.rect().center())
        dialog.exec()

    def show_web(self):
        self.manager_components.unselected()
        url = QUrl('https://mixdor.github.io/circuitikz-generator.github.io/')
        QDesktopServices.openUrl(url)

    def show_kofi(self):
        self.manager_components.unselected()
        url = QUrl('https://ko-fi.com/mixdor')
        QDesktopServices.openUrl(url)

    def show_winversion(self, version_available):

        if version_available:
            dialog = WindowNewVersion()
            dialog.move(self.frameGeometry().topLeft() + self.rect().center() - dialog.rect().center())
            dialog.exec()

    def on_undo2(self):

        self.manager_components.unselected()
        self.history.undo(self.canvas)

    def on_redo2(self):

        self.manager_components.unselected()
        self.history.redo(self.canvas)


class MiHilo(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, name_app):
        super().__init__()
        self.name_app = name_app

    def run(self):

        sourceforge = SourceForge()
        update_available = sourceforge.check_version(self.name_app)
        self.finished.emit(update_available)
