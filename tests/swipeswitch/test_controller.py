from types import SimpleNamespace

from kali_ux.features.window_switcher.engine.events import GestureEvent
from kali_ux.features.window_switcher.engine.controller import SwipeSwitchController


class _Tracker:
    def update_config(self, _config):
        pass


class _Switcher:
    def update_config(self, _config):
        pass


class _TaskView:
    def __init__(self):
        self.hide_count = 0

    def hide(self):
        self.hide_count += 1


class _WorkspaceRecorder:
    def __init__(self):
        self.directions = []

    def navigate(self, direction):
        self.directions.append(direction)
        return True


def test_four_finger_workspace_steps_are_dispatched_incrementally():
    task_view = _TaskView()
    config = SimpleNamespace(show_threshold_px=20, step_px=40, gesture_timeout=3.0)
    controller = SwipeSwitchController(
        object(), _Tracker(), _Switcher(), task_view, None, config
    )
    workspaces = _WorkspaceRecorder()
    controller.workspaces = workspaces
    controller.gesture_router.enabled = True

    controller.handle_event(GestureEvent("begin", 4))
    controller.handle_event(GestureEvent("update", 4, dx=-130))
    controller.handle_event(GestureEvent("end", 4))

    assert workspaces.directions == ["left", "left", "left"]
    assert task_view.hide_count == 1
