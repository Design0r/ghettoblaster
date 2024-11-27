from ghettoblaster.ui.buttons import IconButton
from ghettoblaster.ui.separator import VLine
from Qt.QtCore import Qt
from Qt.QtWidgets import QHBoxLayout, QWidget


class Toolbar(QWidget):
    def __init__(self, thickness: int, parent=None):
        super().__init__(parent)
        self.thickness = thickness

        self.setFixedHeight(self.thickness)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(
            """
            QWidget{
                background-color: rgb(38,38,38);
                color: rgb(255,255,255);
            }

            QPushButton{
                background-color: none;
                border-radius: 5px;
            }

            QPushButton::hover{
                background-color: rgb(235, 177, 52);
            }

            QPushButton::checked{
                background-color: rgb(235, 177, 52);
            }
            """
        )
        self.init_widgets()
        self.init_layouts()
        self.init_signals()

    def init_widgets(self):
        b = (30, 30)
        i = (20, 20)
        self.add_btn = IconButton(b)
        self.add_btn.set_icon(":icons/tabler-icon-file-plus.png", i)
        self.add_btn.setToolTip("Add new playblast layer")
        self.duplicate_btn = IconButton(b)
        self.duplicate_btn.set_icon(":icons/tabler-icon-copy.png", i)
        self.duplicate_btn.setToolTip("Duplicate selected playblast layer")
        self.check_all_btn = IconButton(b)
        self.check_all_btn.set_icon(":icons/tabler-icon-file-check.png", i)
        self.check_all_btn.setToolTip("Check all playblast layers")
        self.uncheck_all_btn = IconButton(b)
        self.uncheck_all_btn.set_icon(":icons/tabler-icon-file-x.png", i)
        self.uncheck_all_btn.setToolTip("Uncheck all playblast layers")
        self.reload_btn = IconButton(b)
        self.reload_btn.set_icon(":icons/tabler-icon-reload.png", i)
        self.reload_btn.setToolTip("Refresh camera and render layer lists")
        self.save_btn = IconButton(b)
        self.save_btn.set_icon(":icons/device-floppy.png", i)
        self.save_btn.setToolTip("Save Playblast")
        self.load_btn = IconButton(b)
        self.load_btn.set_icon(":icons/folder-open.png", i)
        self.load_btn.setToolTip("Load Playblast")

    def init_layouts(self) -> None:
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.addWidget(self.add_btn)
        self.main_layout.addWidget(self.duplicate_btn)
        self.main_layout.addWidget(self.check_all_btn)
        self.main_layout.addWidget(self.uncheck_all_btn)
        self.main_layout.addWidget(VLine())
        self.main_layout.addWidget(self.reload_btn)
        self.main_layout.addWidget(VLine())
        self.main_layout.addWidget(self.save_btn)
        self.main_layout.addWidget(self.load_btn)
        self.main_layout.addStretch()

    def init_signals(self):
        pass

    def add_widgets(self, widgets: list[QWidget]):
        for widget in widgets:
            self.main_layout.addWidget(widget)
        self.main_layout.addStretch()
