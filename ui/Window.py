from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QSize
from PyQt6.QtGui import QKeySequence, QShortcut, QIcon, QDesktopServices
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import *

from auxiliar.SourceForge import SourceForge
from components.ComponentsCreator import ComponentsCreator
from components.ComponentsEditor import ComponentsEditor
from components.ComponentsRemover import ComponentsRemover
from components.ComponentsSelector import ComponentsSelector
from components.History import History
from components.TxtToComponents import TxtToComponents
from drawables.DrawComponent import DrawComponent
from objects.Tools import ObjTool
from ui.MainCanvas import Canvas
from ui.Resources import Resources
from ui.WindowGenerate import WindowGenerate
from ui.WindowNewVersion import WindowNewVersion


class MainWindow(QMainWindow):
    def __init__(self, base_path):
        super().__init__()

        self.resources = Resources()

        self.base_path = base_path
        self.setMouseTracking(True)

        self.botones = []
        self.group_buttons = []
        self.obj_tools : list[ObjTool] = []

        self.components = []

        xml_to_tools = TxtToComponents(self.base_path)
        list_groups_tools = xml_to_tools.parse_xml_to_objects()
        self.tool_selected = list_groups_tools.get_tool("Select")

        shortcut_undo = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Key.Key_Z), self)
        shortcut_undo.activated.connect(self.on_undo2)
        shortcut_redo = QShortcut(QKeySequence(Qt.Modifier.CTRL | Qt.Modifier.SHIFT | Qt.Key.Key_Z), self)
        shortcut_redo.activated.connect(self.on_redo2)

        screen_width = QApplication.primaryScreen().size().width()
        desired_width = int(screen_width * 0.19)

        layout = QHBoxLayout()

        layout_tools = QVBoxLayout()
        widget_layout_tools = QWidget(self)
        widget_layout_tools.setLayout(layout_tools)
        widget_layout_tools.setFixedWidth(desired_width)
        layout.addWidget(widget_layout_tools)

        self.name_app = QLabel('CircuiTikZ Generator v0.9')
        self.name_app.setStyleSheet("font-size: 11pt; font-weight: bold")
        self.name_app.setContentsMargins(0, 0, 0, 11)
        layout_tools.addWidget(self.name_app)
        print(f'::: {self.name_app.text()} :::')

        layout_search = QHBoxLayout()
        layout_tools.addLayout(layout_search)

        self.searchField = QLineEdit()
        self.searchField.setPlaceholderText('Search tool...')
        self.searchField.textChanged.connect(self.handle_search_changed)
        layout_search.addWidget(self.searchField)

        self.btn_clear_search = QPushButton("")
        self.btn_clear_search.setIcon(QIcon(f'{self.resources.get_path()}/backspace.svg'))
        self.btn_clear_search.setEnabled(False)
        self.btn_clear_search.setFixedWidth(28)
        self.btn_clear_search.clicked.connect(self.clear_search)
        layout_search.addWidget(self.btn_clear_search)

        layout_scroll_area = QVBoxLayout()
        layout_scroll_area.setAlignment(Qt.AlignmentFlag.AlignTop)


        for i in range(list_groups_tools.size()):

            group_tool = list_groups_tools[i]
            name_group = group_tool.name

            label_name = QLabel(name_group)
            layout_scroll_area.addWidget(label_name)
            self.group_buttons.append(label_name)

            colum = 3
            content_button_aux = []

            for k in range(group_tool.size()):

                tool = group_tool[k]
                self.obj_tools.append(tool)

                button = QPushButton()
                button.setFixedWidth(int((214-(6*colum))/colum))
                button.setToolTip(tool.name)
                button.setIcon(QIcon(tool.img_cover))
                button.setIconSize(QSize(45, 45))
                button.setStyleSheet(f'background-color: {self.resources.get_hex_deactivate()}; color: black;')

                button.clicked.connect(self.on_button_click)

                if tool.name == "Select":
                    button.setStyleSheet(f'background-color: {self.resources.get_hex_active()}; color: black;')

                self.botones.append(button)
                content_button_aux.append(button)

                if (k+1) % colum == 0:
                    self.layout_tools_aux(content_button_aux, layout_scroll_area)

            if len(content_button_aux) != 0:
                self.layout_tools_aux(content_button_aux, layout_scroll_area)

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

        layout_properties.addWidget(QLabel('Label'))
        self.label_component = QLineEdit()
        self.label_component.setFixedHeight(28)
        self.label_component.setEnabled(False)
        self.label_component.returnPressed.connect(self.handle_component_label)
        layout_properties.addWidget(self.label_component)

        self.button_label_edit = QPushButton(QIcon(f'{self.resources.get_path()}/edit.svg'), '')
        self.button_label_edit.setToolTip("Edit Label")
        self.button_label_edit.setEnabled(False)
        self.button_label_edit.clicked.connect(self.handle_component_label)
        layout_properties.addWidget(self.button_label_edit)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout_properties.addItem(spacer)

        self.button_flip_horizontal = QPushButton(QIcon(f'{self.resources.get_path()}/flip_horizontal.svg'), '')
        self.button_flip_horizontal.setToolTip("Flip Horizontal")
        self.button_flip_horizontal.setEnabled(False)
        # self.button_flip_horizontal.clicked.connect(self.handle_component)
        layout_properties.addWidget(self.button_flip_horizontal)

        self.button_flip_vertical = QPushButton(QIcon(f'{self.resources.get_path()}/flip_vertical.svg'), '')
        self.button_flip_vertical.setToolTip("Flip Vertical")
        self.button_flip_vertical.setEnabled(False)
        # self.button_flip_vertical.clicked.connect(self.handle_component)
        layout_properties.addWidget(self.button_flip_vertical)

        self.button_rotate_no_clock = QPushButton(QIcon(f'{self.resources.get_path()}/rotate_left.svg'), '')
        self.button_rotate_no_clock.setToolTip("Rotate 90° Counter-Clockwise")
        self.button_rotate_no_clock.setEnabled(False)
        self.button_rotate_no_clock.clicked.connect(self.rotate_counter_clockwise)
        layout_properties.addWidget(self.button_rotate_no_clock)

        self.button_rotate_clock = QPushButton(QIcon(f'{self.resources.get_path()}/rotate_rigth.svg'), '')
        self.button_rotate_clock.setToolTip("Rotate 90° Clockwise")
        self.button_rotate_clock.setEnabled(False)
        self.button_rotate_clock.clicked.connect(self.rotate_clockwise)
        layout_properties.addWidget(self.button_rotate_clock)

        spacer2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout_properties.addItem(spacer2)

        self.button_delete = QPushButton(QIcon(f'{self.resources.get_path()}/delete.svg'), '')
        self.button_delete.setToolTip("Delete")
        self.button_delete.setEnabled(False)
        self.button_delete.clicked.connect(self.delete_component)
        layout_properties.addWidget(self.button_delete)

        spacer3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout_properties.addItem(spacer3)

        self.svg_widget = QSvgWidget(parent=self)
        self.svg_widget.setFixedSize(40, 40)
        self.svg_widget.setStyleSheet(
            'background-color: white; color: white; border: 1.5px solid #DB6725; border-radius: 3px;'
        )
        self.svg_widget.load(self.tool_selected.img_cover)
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

        button_donate = QPushButton(QIcon(f'{self.resources.get_path()}/ko-fi-icon.svg'), ' Donate ', self)
        button_donate.clicked.connect(self.show_kofi)

        # button_about = QPushButton(QIcon(f'{self.resources.get_path()}/info.svg'), '', self)
        # button_about.setFixedWidth(30)
        # button_about.clicked.connect(self.show_win_about)

        layout_donate.addWidget(button_donate)
        # layout_donate.addStrut(1)
        # layout_donate.addWidget(button_about)

        layout_canvas_properties.addWidget(widget_layout_properties)
        self.history = History()

        self.components_selector = ComponentsSelector()
        self.components_creator = ComponentsCreator(self.history)
        self.components_remover = ComponentsRemover(self.history)
        self.components_editor = ComponentsEditor(self.history)

        self.canvas = Canvas(
            label_cord,
            self.tool_selected,
            self.components,
            self.label_component,
            self.button_label_edit,
            self.button_delete,
            self.button_flip_horizontal,
            self.button_flip_vertical,
            self.button_rotate_no_clock,
            self.button_rotate_clock,
            self.components_creator,
            self.history)

        self.canvas_scene = self.canvas.scene
        self.components_creator.canvas = self.canvas
        self.components_creator.draw_component = DrawComponent(self.canvas.scene)
        self.components_editor.draw_component = DrawComponent(self.canvas.scene)
        layout_canvas_properties.addWidget(self.canvas)

        self.hilo = MiHilo(self.name_app.text())
        self.hilo.finished.connect(self.show_winversion)
        self.hilo.start()

        widget = QWidget(self)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def handle_search_changed(self, input_text):

        if self.searchField.text() != '':
            self.btn_clear_search.setEnabled(True)
        else:
            self.btn_clear_search.setEnabled(False)

        for button in self.botones:
            button.setVisible(True)
        for group in self.group_buttons:
            group.setVisible(False)

        text = str(input_text).lower()

        for button in self.botones:
            if not button.toolTip() == 'Select':
                title = button.toolTip().lower()
                if not title.__contains__(text):
                    button.setVisible(False)

        for button in self.botones:
            if button.isVisible():

                for tool in self.obj_tools:
                    if tool.name == button.toolTip():
                        for label in self.group_buttons:
                            if label.text() == tool.group_name:
                                label.setVisible(True)

    def clear_search(self):
        self.searchField.setText("")

    def on_button_click(self):

        self.components_selector.unselect(self.canvas)

        button = self.sender()

        list_buttons = self.botones
        for i in range(list_buttons.__len__()):
            list_buttons[i].setStyleSheet(f'background-color: {self.resources.get_hex_deactivate()}; color: black;')

        current_tool = None

        for j in range(self.obj_tools.__len__()):
            if self.obj_tools[j].name == button.toolTip():
                current_tool = self.obj_tools[j]

        if self.tool_selected != current_tool:

            self.tool_selected = ObjTool(
                name=current_tool.name,
                group_name=current_tool.group,
                class_name=current_tool.class_,
                latex=current_tool.latex,
                img_cover=current_tool.img_cover,
                canvas_stroke=current_tool.canvas_stroke,
                canvas_stroke_static=current_tool.canvas_stroke_static,
            )

            self.canvas.set_tool(self.tool_selected)
            self.svg_widget.load(self.tool_selected.img_cover)

            button.setStyleSheet(f'background-color: {self.resources.get_hex_active()}; color: black;')
        else:
            button.setStyleSheet(f'background-color: {self.resources.get_hex_active()}; color: black;')

    def handle_component_label(self):
        if self.canvas.component_selected:
            self.components_editor.label(self.canvas, self.canvas.current_label.text())

    def rotate_clockwise(self):
        if self.canvas.component_selected:
            self.components_editor.rotation(self.canvas, 90)

    def rotate_counter_clockwise(self):
        if self.canvas.component_selected:
            self.components_editor.rotation(self.canvas, -90)

    def delete_component(self):
        if self.canvas.component_selected:
            self.components_remover.delete_selected(self.canvas)

    def show_generate_latex(self):
        self.components_selector.unselect(self.canvas)
        dialog = WindowGenerate(self.components)
        dialog.move(self.frameGeometry().topLeft() + self.rect().center() - dialog.rect().center())
        dialog.exec()

    def show_web(self):
        self.components_selector.unselect(self.canvas)
        url = QUrl('https://mixdor.github.io/circuitikz-generator.github.io/')
        QDesktopServices.openUrl(url)

    def show_kofi(self):
        self.components_selector.unselect(self.canvas)
        url = QUrl('https://github.com/sponsors/Mixdor')
        QDesktopServices.openUrl(url)

    def show_winversion(self, version_available):

        if version_available:
            dialog = WindowNewVersion()
            dialog.move(self.frameGeometry().topLeft() + self.rect().center() - dialog.rect().center())
            dialog.exec()

    def on_undo2(self):

        self.components_selector.unselect(self.canvas)
        self.history.undo(self.canvas)

    def on_redo2(self):

        self.components_selector.unselect(self.canvas)
        self.history.redo(self.canvas)

    def layout_tools_aux(self, button_list, layout_scrollable):

        colum_box = QHBoxLayout()
        colum_box.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_scrollable.addLayout(colum_box)

        for btn_aux in button_list:
            colum_box.addWidget(btn_aux)

        button_list.clear()


class MiHilo(QThread):
    finished = pyqtSignal(bool)

    def __init__(self, name_app):
        super().__init__()
        self.name_app = name_app

    def run(self):

        sourceforge = SourceForge()
        update_available = sourceforge.check_version(self.name_app)
        self.finished.emit(update_available)
