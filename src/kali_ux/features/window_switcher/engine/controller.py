"""Coordinates recognised gestures with desktop services and GTK views."""

from __future__ import annotations

import logging

from kali_ux.features.gesture_control.router import GestureRouter

from .activator import activate_window
from .desktop import DesktopVisibilityManager
from .gestures import GestureRecognizer
from .workspaces import WorkspaceManager

log = logging.getLogger(__name__)


class SwipeSwitchController:
    def __init__(self, screen, tracker, switcher, task_view, Gdk, config, gesture_router=None):
        self.screen = screen
        self.tracker = tracker
        self.switcher = switcher
        self.task_view = task_view
        self.Gdk = Gdk
        self.config = config
        self.gesture_router = gesture_router or GestureRouter()
        self.gesture_router.set_recognizer(
            GestureRecognizer(config.show_threshold_px, config.step_px)
        )
        for action_name in (
            "switch_begin",
            "switch_move",
            "switch_commit",
            "switch_cancel",
            "workspace",
            "show_desktop",
            "task_view",
        ):
            self.gesture_router.register_action_handler(
                action_name, self._dispatch, owner="window_switcher"
            )
        self.desktop = DesktopVisibilityManager(screen, tracker)
        self.workspaces = WorkspaceManager(screen, wrap=False)
        self.switch_windows = []
        self.selected = 0

    def update_config(self, config):
        # A configuration reload must not leave a switcher overlay visible
        # after replacing the recognizer that owns its gesture lifecycle.
        if self.switch_windows:
            self.switcher.hide()
            self.switch_windows = []
        self.config = config
        self.gesture_router.set_recognizer(
            GestureRecognizer(config.show_threshold_px, config.step_px)
        )
        self.tracker.update_config(config)
        self.switcher.update_config(config)

    def handle_event(self, event):
        return self.gesture_router.handle_event(event)

    def check_timeout(self):
        return self.gesture_router.check_timeout(self.config.gesture_timeout)

    def _dispatch(self, action):
        if action.name == "switch_begin":
            self.switch_windows = self.tracker.get_switchable_windows()
            self.selected = 0
            if len(self.switch_windows) < 2:
                self.switch_windows = []
                return
            self.switcher.show(self.switch_windows, self.selected)
        elif action.name == "switch_move":
            if not self.switch_windows:
                return
            # Left advances through MRU order; right moves toward the prior item.
            delta = action.steps * (1 if action.direction == "left" else -1)
            self.selected = (self.selected + delta) % len(self.switch_windows)
            self.switcher.update_selection(self.selected)
        elif action.name == "switch_commit":
            self.switcher.hide()
            if self.switch_windows:
                target_xid = int(self.switch_windows[self.selected].get_xid())
                self.screen.force_update()
                live = {int(w.get_xid()): w for w in (self.screen.get_windows() or [])}
                target = live.get(target_xid)
                if target is not None:
                    activate_window(target, self.Gdk, log)
            self.switch_windows = []
        elif action.name == "switch_cancel":
            self.switcher.hide()
            self.switch_windows = []
        elif action.name == "workspace":
            self.task_view.hide()
            # Four-finger horizontal movement is incremental. A reversal emits
            # steps in the opposite direction, just like window selection.
            for _ in range(max(1, int(action.steps))):
                if not self.workspaces.navigate(action.direction):
                    break
            self.switch_windows = []
        elif action.name == "show_desktop":
            self.task_view.hide()
            self.desktop.show_desktop()
        elif action.name == "task_view":
            if self.desktop.has_snapshot:
                self.desktop.restore()
            else:
                self.switcher.hide()
                windows = self.tracker.get_switchable_windows()
                if windows:
                    self.task_view.show(windows)
