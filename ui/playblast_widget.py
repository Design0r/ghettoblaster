from __future__ import annotations

from ghettoblaster.controller.playblast import Playblast
from ghettoblaster.ui.buttons import IconButton
from Qt.QtCore import Qt, Signal
from Qt.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QWidget,
)


class PlayblastWidget(QWidget):
    clicked = Signal()
    delete = Signal(QWidget)

    def __init__(self, playblast: Playblast, parent=None):
        super().__init__(parent)
        self.playblast = playblast
        self.is_clicked = False
        self.base_style = "border-radius: 5px; IconButton{padding: 5px};"
        self.clicked_style = (
            f"{self.base_style} background-color: rgb(235, 177, 52); color: #000"
        )
        self.unclicked_style = (
            f"{self.base_style} background: rgb(40,40,40); color: #fff"
        )
        self.setStyleSheet(self.unclicked_style)
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.init_widgets()
        self.init_layouts()
        self.init_signals()

    def init_widgets(self):
        self.checkbox = QCheckBox(checked=True)
        self.name = QLabel("Playblast Name")
        self.delete_btn = IconButton((25, 25))
        self.delete_btn.setStyleSheet(
            """
        IconButton::hover {
            background-color: rgb(128,128,128);
        }
        """
        )
        self.delete_btn.set_icon(":icons/tabler-icon-trash.png", (20, 20))

    def init_layouts(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignLeft)
        self.main_layout.addWidget(self.checkbox)
        self.main_layout.addWidget(self.name)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.delete_btn)

    def init_signals(self):
        self.delete_btn.clicked.connect(lambda: self.delete.emit(self))

    def toggle_checked(self, toggle=None):
        if toggle is True:
            self.setStyleSheet(self.clicked_style)
            self.is_clicked = True
            return
        elif toggle is False:
            self.setStyleSheet(self.unclicked_style)
            self.is_clicked = False
            return

        state = self.clicked
        if state is True:
            self.setStyleSheet(self.unclicked_style)
            self.is_clicked = False
            return
        elif toggle is False:
            self.setStyleSheet(self.clicked_style)
            self.is_clicked = True
            return

    def mousePressEvent(self, event) -> None:
        self.clicked.emit()
        return super().mousePressEvent(event)
