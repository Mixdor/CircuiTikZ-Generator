from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *

from components.ObjTool import ObjTool
from ui.MainCanvas import Canvas
from components.Components import Components
from ui.WindowExport import WindowExport
from ui.WindowSettings import WindowSettings


class MainWindow(QMainWindow):
    def __init__(self, base_path):
        super().__init__()
        self.base_path = base_path
        self.setMouseTracking(True)

        self.botones = []
        self.obj_tools = []
        self.tool_selected = ObjTool("Select", "Basic", 0, "", "")
        self.components_added = []
        self.components_deleted = []
        self.draw_added = []
        self.draw_deleted = []

        shortcut_undo = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Z), self)
        shortcut_undo.activated.connect(self.on_undo)
        shortcut_redo = QShortcut(QKeySequence(Qt.CTRL + Qt.SHIFT + Qt.Key_Z), self)
        shortcut_redo.activated.connect(self.on_redo)

        layout = QHBoxLayout()

        layout_tools = QVBoxLayout()
        widget_layout_tools = QWidget(self)
        widget_layout_tools.setLayout(layout_tools)
        widget_layout_tools.setFixedWidth(250)
        layout.addWidget(widget_layout_tools)

        layout_scroll_area = QVBoxLayout()
        layout_scroll_area.setAlignment(Qt.AlignTop)

        new_components = Components(self.base_path)

        list_groups_components = new_components.get_groups()

        # Agregar contenido al layout
        for i in range(list_groups_components.__len__()):

            group_str = list_groups_components[i]
            name = new_components.get_name_group(group_str)
            label_name = QLabel(name)
            layout_scroll_area.addWidget(label_name)

            current_tools = new_components.get_tools_for_group(group_str, name)

            for k in range(current_tools.__len__()):
                tool = current_tools[k]
                self.obj_tools.append(tool)
                button = QPushButton(tool.name)
                button.clicked.connect(self.on_button_click)

                if tool.name == "Select":
                    button.setStyleSheet("background-color: lightblue; color: black;")

                self.botones.append(button)
                layout_scroll_area.addWidget(button)

        # Crear un área de desplazamiento y configurar el layout dentro de ella
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Permitir que el widget contenido cambie de tamaño
        scroll_content = QWidget()
        scroll_content.setLayout(layout_scroll_area)
        scroll_area.setWidget(scroll_content)

        layout_tools.addWidget(scroll_area)

        layout_canvas_properties = QVBoxLayout()
        widget_canvas_properties = QWidget(self)
        widget_canvas_properties.setLayout(layout_canvas_properties)
        layout.addWidget(widget_canvas_properties)

        layout_properties = QHBoxLayout()
        widget_layout_properties = QWidget(self)
        widget_layout_properties.setFixedHeight(48)
        widget_layout_properties.setLayout(layout_properties)

        layout_properties.addWidget(QLabel("Component label"))
        self.label_component = QTextEdit()
        layout_properties.addWidget(self.label_component)

        label_cord = QLabel("Coordinates: [0,0]")
        layout_tools.addWidget(label_cord)

        layout_export = QHBoxLayout()
        widget_layout_export = QWidget(self)
        widget_layout_export.setLayout(layout_export)
        layout_export.setContentsMargins(0, 0, 0, 0)
        layout_tools.addWidget(widget_layout_export)

        button_export = QPushButton("Generate", self)
        button_export.clicked.connect(self.show_export)
        button_settings_export = QPushButton("(%)", self)
        button_settings_export.setFixedWidth(30)
        button_settings_export.clicked.connect(self.show_setting)

        layout_export.addWidget(button_export)
        layout_export.addStrut(1)
        layout_export.addWidget(button_settings_export)

        layout_canvas_properties.addWidget(widget_layout_properties)
        self.canvas = Canvas(
            label_cord,
            self.tool_selected,
            self.components_added,
            self.draw_added,
            self.label_component
            )
        self.canvas_scene = self.canvas.scene
        layout_canvas_properties.addWidget(self.canvas)

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def on_button_click(self):
        button = self.sender()
        # Este método se llamará cuando se haga clic en el botón
        list_buttons = self.botones
        for i in range(list_buttons.__len__()):
            list_buttons[i].setStyleSheet("")

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
            button.setStyleSheet("background-color: lightblue; color: black;")
        else:
            button.setStyleSheet("background-color: lightblue; color: black;")

    def show_export(self):
        self.window_export = WindowExport(self.draw_added, self.base_path)
        self.window_export.show()

    def show_setting(self):
        self.window_setting = WindowSettings(self.base_path)
        self.window_setting.show()

    def on_undo(self):
        if self.components_added:
            list_remove = self.components_added[-1]
            for i in range(list_remove.__len__()):
                self.canvas_scene.removeItem(list_remove[i])
            self.components_deleted.append(self.components_added[-1])
            self.components_added.remove(self.components_added[-1])

            self.draw_deleted.append((self.draw_added[-1]))
            self.draw_added.remove(self.draw_added[-1])

    def on_redo(self):
        if self.components_deleted:
            list_add = self.components_deleted[-1]
            for i in range(list_add.__len__()):
                self.canvas_scene.addItem(list_add[i])
            self.components_added.append(self.components_deleted[-1])
            self.components_deleted.remove(self.components_deleted[-1])

            self.draw_added.append(self.draw_deleted[-1])
            self.draw_deleted.remove(self.draw_deleted[-1])
