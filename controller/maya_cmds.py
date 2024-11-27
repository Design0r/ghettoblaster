from pathlib import Path

from maya import cmds

TIME_CONVERSION = {
    "game": 15,
    "film": 24,
    "pal": 25,
    "ntsc": 30,
    "show": 48,
    "palf": 50,
    "ntscf": 60,
}


def get_scene_name() -> str:
    path = Path(cmds.file(query=True, sceneName=True))
    return path.stem


def get_active_camera() -> str:
    active_Editor = cmds.playblast(activeEditor=True)
    camera = cmds.modelEditor(active_Editor, query=True, camera=True)

    return camera.split("|")[-1]


def get_activte_render_layer() -> str:
    return cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)


def get_all_cameras() -> list[str]:
    cam_shapes = cmds.ls(cameras=True)
    transforms = [cmds.listRelatives(i, parent=True)[0] for i in cam_shapes]
    return transforms


def get_frame_range() -> tuple[int, int]:
    start = cmds.playbackOptions(query=True, minTime=True)
    end = cmds.playbackOptions(query=True, maxTime=True)

    return int(start), int(end)


def set_active_camera(camera_name: str):
    panel = cmds.playblast(activeEditor=True)

    cmds.modelEditor(panel, edit=True, camera=camera_name)


def get_frame_rate() -> float:
    frame_rate = cmds.currentUnit(query=True, time=True)
    return TIME_CONVERSION[frame_rate]


def get_render_layers() -> list[str]:
    return cmds.ls(type="renderLayer")


def set_render_layer(name: str) -> None:
    cmds.editRenderLayerGlobals(currentRenderLayer=name)


def set_camera_overscan(camera: str, value: bool) -> None:
    cmds.setAttr(f"{camera}.displayResolution", value)


def render_playblast(pb) -> None:
    actView = cmds.playblast(activeEditor=True)
    cmds.modelEditor(actView, e=1, allObjects=False)
    cmds.modelEditor(actView, e=1, polymeshes=True)
    cmds.modelEditor(actView, e=1, particleInstancers=True)
    cmds.modelEditor(actView, e=1, particleInstancers=True)
    cmds.modelEditor(actView, e=1, pluginShapes=True)

    cmds.playblast(
        startTime=pb.start_frame,
        endTime=pb.end_frame,
        filename=pb.filename,
        widthHeight=(pb.width, pb.height),
        format=pb.format,
        compression="jpg",
        offScreen=pb.offscreen,
        showOrnaments=pb.show_ornaments,
        viewer=False,
        quality=100,
        percent=100,
        forceOverwrite=True,
    )
    cmds.modelEditor(actView, e=1, allObjects=True)


def get_project_dir() -> str:
    return cmds.workspace(q=True, rootDirectory=True)
