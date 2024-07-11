from __future__ import annotations
from pathlib import Path
from typing import Callable, Optional
import time

from ghettoblaster.controller.data_classes import Resolution
from ghettoblaster.controller import maya_cmds
from ghettoblaster.controller.logger import Logger
import cv2


RESOLUTIONS = (
    Resolution("HD_2160", 3840, 2160),
    Resolution("HD_1080", 1920, 1080),
    Resolution("HD_720", 1280, 720),
    Resolution("HD_540", 960, 540),
    Resolution("Custom", 0, 0),
)
KEYWORDS = ("<Scene>", "<Camera>", "<Layer>")
QUALITIES = {"High": "mp4v", "Medium": "X264"}
FRAME_RANGES = ("Time Slider", "Custom")


class Playblast:
    resolutions = RESOLUTIONS
    keywords = KEYWORDS
    qualities = QUALITIES
    frame_ranges = FRAME_RANGES

    def __init__(self, id: int) -> None:
        self.id = id
        self.frame_range_name = "Time Slider"
        self.start_frame = 0
        self.end_frame = 0
        self.filename = ""
        self.filename_field = "<Scene>/<Scene>_<Camera>"
        self.output_field = ""
        self.format = "image"
        self.resolution = "HD_1080"
        self.width = 1920
        self.height = 1080
        self.show_ornaments = False
        self.offscreen = False
        self.overscan = False
        self.camera = "persp"
        self.name = f"Playblast {self.id}"
        self.render_layer = "defaultRenderLayer"
        self.quality = "High"
        self.delete_images = False

    @property
    def cameras(self) -> list[str]:
        return maya_cmds.get_all_cameras()

    @property
    def frame_rate(self) -> float:
        return maya_cmds.get_frame_rate()

    @property
    def render_layers(self) -> list[str]:
        return maya_cmds.get_render_layers()

    def get_resolution_by_name(self, name: str) -> Optional[Resolution]:
        for i in self.resolutions:
            if not (name == i.name):
                continue

            return i

    def get_resolution_by_value(self, x: int, y: int) -> Optional[Resolution]:
        for i in self.resolutions:
            if x != i.x or y != i.y:
                continue

            return i

    def get_frame_range_by_name(self, name: str) -> tuple[int, int]:
        if name == "Time Slider":
            start, end = maya_cmds.get_frame_range()
            return start, end
        elif name == "Custom":
            return self.start_frame, self.end_frame

        return 0, 0

    def clone(self) -> Playblast:
        pb = Playblast(self.id)

        for k, v in self.__dict__.items():
            pb.__dict__[k] = v

        return pb


class PlayblastRenderer:
    def __init__(self, playblasts: list[Playblast], update_progress: Callable) -> None:
        self.playblasts = playblasts
        self.update_progress = update_progress

    def batch_maya_render(self):
        self.update_progress(0)
        for i, p in enumerate(self.playblasts, start=1):
            start_time = time.perf_counter()
            Logger.info(f"Starting Playblast for {p.name}")
            self.maya_render(p)
            self.video_render(p)
            stop_time = time.perf_counter()
            Logger.info(
                f"Finished Playblast for {p.name} in {stop_time - start_time:.2f}s"
            )
            self.update_progress(int((i / len(self.playblasts)) * 100))

    def maya_render(self, pb: Playblast):
        maya_cmds.set_active_camera(pb.camera)
        maya_cmds.set_render_layer(pb.render_layer)
        maya_cmds.set_camera_overscan(pb.camera, pb.overscan)
        maya_cmds.render_playblast(pb)

    def video_render(self, pb: Playblast):
        path = Path(pb.filename)
        folder = path.parent
        filename = path.stem
        videoname = f"{folder / filename}.mp4"

        all_files = [
            file for file in folder.glob("*.jpg") if file.stem.startswith(filename)
        ]
        all_files.sort(key=lambda x: x.stem)

        fourcc = cv2.VideoWriter_fourcc(*QUALITIES[pb.quality])
        video = cv2.VideoWriter(videoname, fourcc, pb.frame_rate, (pb.width, pb.height))

        if pb.delete_images:
            for i in all_files:
                video.write(cv2.imread(str(i)))
                i.unlink()
        else:
            for i in all_files:
                video.write(cv2.imread(str(i)))

        cv2.destroyAllWindows()
        video.release()
