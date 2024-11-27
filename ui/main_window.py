from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import NamedTuple

from ghettoblaster.controller.logger import Logger
from ghettoblaster.controller.maya_cmds import get_project_dir
from ghettoblaster.controller.playblast import Playblast, PlayblastRenderer
from ghettoblaster.ui.playblast_widget import PlayblastWidget
from ghettoblaster.ui.settings_widget import SettingsWidget
from ghettoblaster.ui.toolbar import Toolbar
from ghettoblaster.ui.version import get_version
from maya import OpenMayaUI
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from Qt.QtCompat import wrapInstance
from Qt.QtCore import Qt
from Qt.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSplitter,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


def get_maya_main_window():
    main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QMainWindow)


class PlayblastWidgets(NamedTuple):
    playblast: PlayblastWidget
    settings: SettingsWidget


class MainWindow(MayaQWidgetDockableMixin, QWidget):
    win_instance = None

    ROOT_PATH = Path(__file__).parent.parent
    LOGS = ROOT_PATH / "logs"
    LOGGING_PATH = LOGS / f"{datetime.now().date()}.log"

    def __init__(self, parent=None):
        super().__init__(parent)
        self._widgets: list[PlayblastWidgets] = []

        self.setWindowTitle(f"Ghettoblaster - {get_version()}")
        self.setWindowFlag(Qt.WindowType.Window)

        MainWindow.LOGS.mkdir(exist_ok=True)
        Logger.write_to_file(MainWindow.LOGGING_PATH)
        Logger.set_propagate(False)
        Logger.info("starting Ghettoblaster...")

        self.init_widgets()
        self.init_layouts()
        self.init_signals()

        self.resize(700, 525)
        self.add_playblast()

    @classmethod
    def show_window(cls) -> MainWindow:
        if not cls.win_instance:
            cls.win_instance = MainWindow(parent=get_maya_main_window())
            cls.win_instance.show(dockable=True)
        elif cls.win_instance.isHidden():
            cls.win_instance.show(dockable=True)
        else:
            cls.win_instance.showNormal()

        cls.win_instance.update_widgets()
        return cls.win_instance

    def init_widgets(self):
        self.playblast_btn = QPushButton("Playblast")
        self.toolbar = Toolbar(40)

        self.pb_scroll_widget = QWidget()
        self.pb_scroll_area = QScrollArea()
        self.pb_scroll_area.setWidget(self.pb_scroll_widget)
        self.pb_scroll_area.setFocusPolicy(Qt.NoFocus)
        self.pb_scroll_area.setWidgetResizable(True)

        self.s_scroll_widget = QWidget()
        self.s_scroll_area = QScrollArea()
        self.s_scroll_area.setWidget(self.s_scroll_widget)
        self.s_scroll_area.setFocusPolicy(Qt.NoFocus)
        self.s_scroll_area.setWidgetResizable(True)

        self.settings_stack = QStackedWidget()

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.pb_scroll_area)
        self.splitter.addWidget(self.s_scroll_area)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

    def init_layouts(self):
        self.playblast_layout = QVBoxLayout(self.pb_scroll_widget)
        self.playblast_layout.setAlignment(Qt.AlignTop)
        self.playblast_layout.addWidget(self.toolbar)
        self.playblast_layout.setContentsMargins(0, 0, 0, 0)
        self.playblast_layout.setSpacing(5)

        self.settings_layout = QVBoxLayout(self.s_scroll_widget)
        self.settings_layout.addWidget(self.settings_stack)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.splitter)
        self.main_layout.addWidget(self.playblast_btn)
        self.main_layout.addWidget(self.progress)

    def init_signals(self):
        self.toolbar.add_btn.clicked.connect(self.add_playblast)
        self.toolbar.duplicate_btn.clicked.connect(self.duplicate_playblast)
        self.toolbar.check_all_btn.clicked.connect(self.check_all_playblasts)
        self.toolbar.uncheck_all_btn.clicked.connect(self.uncheck_all_playblasts)
        self.toolbar.reload_btn.clicked.connect(self.update_widgets)
        self.toolbar.save_btn.clicked.connect(self.save)
        self.toolbar.load_btn.clicked.connect(self.load)
        self.playblast_btn.clicked.connect(self.render_playblast)

    def add_playblast(self, playblast=None) -> PlayblastWidgets:
        if not playblast:
            playblast = Playblast(id=len(self._widgets))

        pw = PlayblastWidget(playblast)
        sw = SettingsWidget(playblast)

        sw.name_changed.connect(lambda x: pw.name.setText(x))
        pw.name.setText(playblast.name)
        pw.clicked.connect(lambda: self.set_current_widget(sw, pw))
        pw.delete.connect(self.remove_playblast)

        self.playblast_layout.addWidget(pw)
        self.settings_stack.addWidget(sw)

        self.set_current_widget(sw, pw)
        widgets = PlayblastWidgets(pw, sw)
        self._widgets.append(widgets)

        return widgets

    def set_current_widget(self, sw: SettingsWidget, pw: PlayblastWidget) -> None:
        self.settings_stack.setCurrentWidget(sw)

        for i in self._widgets:
            i.playblast.toggle_checked(toggle=False)

        pw.toggle_checked(toggle=True)

    def render_playblast(self):
        pb: list[Playblast] = [
            i.playblast.playblast
            for i in self._widgets
            if i.playblast.checkbox.isChecked()
        ]

        renderer = PlayblastRenderer(pb, lambda u: self.progress.setValue(u))
        renderer.batch_maya_render()

    def remove_playblast(self, pbw: PlayblastWidget):
        for i in self._widgets:
            if i.playblast != pbw:
                continue

            self._widgets.remove(i)
            self.main_layout.removeWidget(pbw)
            self.settings_stack.removeWidget(i.settings)
            pbw.deleteLater()
            i.settings.deleteLater()

            if len(self._widgets) == 1:
                w = self._widgets[0]
                self.set_current_widget(w.settings, w.playblast)

            return

    def check_all_playblasts(self):
        for i in self._widgets:
            i.playblast.checkbox.setChecked(True)

    def uncheck_all_playblasts(self):
        for i in self._widgets:
            i.playblast.checkbox.setChecked(False)

    def duplicate_playblast(self):
        playblast = [
            p.settings.playblast for p in self._widgets if p.playblast.is_clicked
        ][0].clone()

        playblast.name = f"{playblast.name} copy"
        self.add_playblast(playblast=playblast)

    def update_widgets(self):
        for i in self._widgets:
            i.settings.update_cameras()
            i.settings.update_render_layers()

    def save(self):
        file, _ = QFileDialog.getSaveFileName(
            self,
            "Save Ghettoblaster Config",
            filter="JSON (*.json)",
            dir=get_project_dir(),
        )
        if not file:
            return

        playblasts = [p.settings.playblast.serialize() for p in self._widgets]
        data = {"playblasts": playblasts}

        with open(file, "w") as f:
            f.write(json.dumps(data))

    def load(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Save Ghettoblaster Config", dir=get_project_dir()
        )
        if not file:
            return

        with open(file, "r") as f:
            data = json.load(f)

        playblasts = [Playblast.deserialize(p) for _, v in data.items() for p in v]
        for p in playblasts:
            self.add_playblast(p)
