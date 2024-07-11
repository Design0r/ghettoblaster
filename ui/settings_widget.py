from PySide2.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QAbstractSpinBox,
    QLineEdit,
    QHBoxLayout,
    QWidget,
    QComboBox,
    QGroupBox,
    QVBoxLayout,
    QSpinBox,
    QFileDialog,
)
from PySide2.QtCore import Qt, Signal
from ghettoblaster.ui.keyword_linedit import KeywordLineedit
from ghettoblaster.ui.buttons import IconButton
from ghettoblaster.controller.playblast import Playblast
from ghettoblaster.controller import maya_cmds


class SettingsWidget(QWidget):
    name_changed = Signal(str)

    def __init__(self, playblast: Playblast, parent=None):
        super().__init__(parent)
        self.playblast = playblast

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.init_widgets()
        self.init_layouts()
        self.init_signals()

        self.init_state()

    def init_widgets(self):
        # Widget Settings
        self.playblast_name = QLineEdit()

        # Output Settings
        self.file_preview = QLineEdit()
        self.file_preview.setReadOnly(True)

        self.file_name = KeywordLineedit(self.playblast.keywords)
        self.file_name.setText(self.playblast.filename_field)

        self.output_path = QLineEdit(self.playblast.output_field)

        self.browser = IconButton((25, 25))
        self.browser.set_icon(":icons/tabler-icon-folder-open.png", (20, 20))

        self.quality = QComboBox()
        self.quality.addItems(self.playblast.qualities)

        self.delete_images = QCheckBox()

        # Playblast Settings
        self.camera = QComboBox()
        self.camera.setMinimumWidth(200)
        self.camera.addItems(self.playblast.cameras)

        self.render_layer = QComboBox()
        self.render_layer.setMinimumWidth(200)
        self.render_layer.addItems(self.playblast.render_layers)

        self.resolution_box = QComboBox()
        self.resolution_box.setMinimumWidth(200)
        self.resolution_box.addItems([i.name for i in self.playblast.resolutions])
        self.res_x = QSpinBox()
        self.res_x.setMaximum(999999)
        self.res_x.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.res_y = QSpinBox()
        self.res_y.setMaximum(999999)
        self.res_y.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.frame_range_box = QComboBox()
        self.frame_range_box.addItems(self.playblast.frame_ranges)
        self.frame_range_box.setMinimumWidth(200)
        self.frame_start = QSpinBox()
        self.frame_start.setMaximum(999999)
        self.frame_start.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.frame_end = QSpinBox()
        self.frame_end.setMaximum(999999)
        self.frame_end.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.show_ornaments = QCheckBox()
        self.render_offscreen = QCheckBox()
        self.overscan = QCheckBox()

        self.playblast_box = QGroupBox("Layer Name")
        self.output_box = QGroupBox("Output Settings")
        self.settings_box = QGroupBox("Playblast Settings")

    def init_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.settings_form_layout = QFormLayout(self.settings_box)
        self.output_form_layout = QFormLayout(self.output_box)
        self.playblast_form_layout = QFormLayout(self.playblast_box)

        self.output_layout = QHBoxLayout()
        self.output_layout.addWidget(self.output_path)
        self.output_layout.addWidget(self.browser)

        self.res_layout = QHBoxLayout()
        self.res_layout.addWidget(self.resolution_box)
        self.res_layout.addWidget(self.res_x)
        self.res_layout.addWidget(self.res_y)

        self.frame_layout = QHBoxLayout()
        self.frame_layout.addWidget(self.frame_range_box)
        self.frame_layout.addWidget(self.frame_start)
        self.frame_layout.addWidget(self.frame_end)

        self.output_form_layout.addRow("File Preview", self.file_preview)
        self.output_form_layout.addRow("File Name", self.file_name)
        self.output_form_layout.addRow("Output Path", self.output_layout)
        self.output_form_layout.addRow("Quality", self.quality)
        self.output_form_layout.addRow("Delete Image Sequence", self.delete_images)

        self.settings_form_layout.addRow("Camera", self.camera)
        self.settings_form_layout.addRow("Render Layer", self.render_layer)
        self.settings_form_layout.addRow("Resolution", self.res_layout)
        self.settings_form_layout.addRow("Frame Range", self.frame_layout)
        self.settings_form_layout.addRow("Show Ornaments", self.show_ornaments)
        self.settings_form_layout.addRow("Render Offscreen", self.render_offscreen)
        self.settings_form_layout.addRow("Overscan", self.overscan)

        self.playblast_form_layout.addRow("Name", self.playblast_name)

        self.main_layout.addWidget(self.playblast_box)
        self.main_layout.addWidget(self.output_box)
        self.main_layout.addWidget(self.settings_box)
        self.main_layout.addStretch()

    def init_signals(self):
        self.browser.clicked.connect(self.browse_folder)
        self.playblast_name.textChanged.connect(self.set_playblast_name)
        self.resolution_box.currentTextChanged.connect(self.set_resolution_value)
        self.res_x.valueChanged.connect(self.set_resolution_name)
        self.res_y.valueChanged.connect(self.set_resolution_name)
        self.frame_range_box.currentTextChanged.connect(self.set_frame_range_value)
        self.frame_start.valueChanged.connect(self.set_frame_range_name)
        self.frame_end.valueChanged.connect(self.set_frame_range_name)
        self.file_name.textChanged.connect(self.update_file_preview)
        self.render_offscreen.toggled.connect(self.set_offscreen)
        self.show_ornaments.toggled.connect(self.set_ornaments)
        self.overscan.toggled.connect(self.set_overscan)
        self.camera.currentTextChanged.connect(self.set_camera)
        self.output_path.textChanged.connect(self.change_output_path)
        self.quality.currentTextChanged.connect(self.set_quality)
        self.render_layer.currentTextChanged.connect(self.set_render_layer)
        self.delete_images.toggled.connect(self.set_delete_images)

    def init_state(self):
        self.playblast_name.setText(self.playblast.name)
        self.quality.setCurrentText(self.playblast.quality)
        self.render_layer.setCurrentText(self.playblast.render_layer)

        self.output_path.setText(self.playblast.output_field)

        self.resolution_box.setCurrentText(self.playblast.resolution)
        self.set_resolution_value(self.playblast.resolution)

        self.set_frame_range_value(self.playblast.frame_range_name)

        self.update_file_preview(self.playblast.name)

        self.camera.setCurrentText(self.playblast.camera)
        self.set_camera(self.playblast.camera)

        self.show_ornaments.setChecked(self.playblast.show_ornaments)
        self.render_offscreen.setChecked(self.playblast.offscreen)
        self.overscan.setChecked(self.playblast.overscan)
        self.delete_images.setChecked(self.playblast.delete_images)

    def set_delete_images(self, value: bool) -> None:
        self.playblast.delete_images = value

    def set_render_layer(self, layer: str) -> None:
        self.playblast.render_layer = layer
        self.update_file_preview(self.file_name.text())

    def set_quality(self, quality: str) -> None:
        self.playblast.quality = quality

    def set_playblast_name(self, name: str):
        self.name_changed.emit(name)
        self.playblast.name = name

    def set_camera(self, camera: str):
        self.playblast.camera = camera
        self.update_file_preview(self.file_name.text())

    def set_offscreen(self, value: bool):
        self.playblast.offscreen = value

    def set_ornaments(self, value: bool):
        self.playblast.show_ornaments = value

    def set_overscan(self, value: bool):
        self.playblast.overscan = value

    def update_file_preview(self, file_name: str):
        fn = self.eval_file_name(file_name)
        self.file_preview.setText(fn)
        self.playblast.filename_field = file_name
        self.playblast.filename = f"{self.output_path.text()}/{fn}"

    def eval_file_name(self, file_name: str) -> str:
        scene = maya_cmds.get_scene_name()
        camera = self.camera.currentText()
        layer = self.render_layer.currentText()

        replaced = (
            file_name.replace("<Scene>", scene)
            .replace("<Layer>", layer)
            .replace("<Camera>", camera)
        )

        return replaced

    def set_resolution_value(self, name: str):
        res = self.playblast.get_resolution_by_name(name)
        if not res:
            return

        self.playblast.width = res.x
        self.playblast.height = res.y
        self.playblast.resolution = name

        self.res_x.blockSignals(True)
        self.res_y.blockSignals(True)
        self.res_x.setValue(res.x)
        self.res_y.setValue(res.y)
        self.res_x.blockSignals(False)
        self.res_y.blockSignals(False)

    def set_resolution_name(self, *args) -> None:
        curr_x, curr_y = self.res_x.value(), self.res_y.value()
        res = self.playblast.get_resolution_by_value(curr_x, curr_y)

        self.resolution_box.blockSignals(True)
        if not res:
            self.resolution_box.setCurrentText("Custom")
            self.playblast.resolution = "Custom"
        else:
            self.resolution_box.setCurrentText(res.name)
            self.playblast.resolution = res.name
        self.resolution_box.blockSignals(False)

    def set_frame_range_value(self, name: str) -> None:
        frame_range = self.playblast.get_frame_range_by_name(name)
        if not frame_range:
            return

        start, end = frame_range

        self.playblast.start_frame = start
        self.playblast.end_frame = end
        self.playblast.frame_range_name = name

        self.frame_start.blockSignals(True)
        self.frame_end.blockSignals(True)
        self.frame_range_box.blockSignals(True)
        self.frame_range_box.setCurrentText(name)
        self.frame_start.setValue(start)
        self.frame_end.setValue(end)
        self.frame_start.blockSignals(False)
        self.frame_end.blockSignals(False)
        self.frame_range_box.blockSignals(False)

    def set_frame_range_name(self, *args) -> None:
        start, end = self.frame_start.value(), self.frame_end.value()
        self.playblast.start_frame = start
        self.playblast.end_frame = end
        time_start, time_end = self.playblast.get_frame_range_by_name("Time Slider")

        if time_start == start and time_end == end:
            state = "Time Slider"
        else:
            state = "Custom"

        self.playblast.frame_range_name = state
        self.frame_range_box.blockSignals(True)
        self.frame_range_box.setCurrentText(state)
        self.frame_range_box.blockSignals(False)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if not folder:
            return
        self.output_path.setText(folder)
        self.playblast.output_field = folder
        self.playblast.filename = (
            f"{self.output_path.text()}/{self.file_preview.text()}"
        )

    def change_output_path(self, text: str):
        self.playblast.output_field = text

    def update_cameras(self) -> None:
        curr = self.camera.currentText()

        self.camera.blockSignals(True)

        self.camera.clear()
        new_cams = self.playblast.cameras
        self.camera.addItems(new_cams)
        if curr in new_cams:
            self.camera.setCurrentText(curr)

        self.playblast.camera = self.camera.currentText()
        self.camera.blockSignals(False)

    def update_render_layers(self) -> None:
        curr = self.render_layer.currentText()

        self.render_layer.blockSignals(True)

        self.render_layer.clear()
        new_layers = self.playblast.render_layers
        self.render_layer.addItems(new_layers)
        if curr in new_layers:
            self.render_layer.setCurrentText(curr)
        self.playblast.render_layer = self.render_layer.currentText()

        self.render_layer.blockSignals(False)
