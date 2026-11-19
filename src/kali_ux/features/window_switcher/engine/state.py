"""Pure gesture state machine; intentionally independent of GTK."""
from dataclasses import dataclass
from enum import Enum, auto
import time


class State(Enum):
    IDLE = auto()
    PENDING = auto()
    ACTIVE = auto()


@dataclass(frozen=True)
class GestureEvent:
    kind: str
    fingers: int = 0
    dx: float = 0.0
    dy: float = 0.0
    cancelled: bool = False
    timestamp: float | None = None


@dataclass
class StateResult:
    show_overlay: bool = False
    overlay_visible: bool = False
    hide_overlay: bool = False
    selected_index: int = 0
    activate_id: int | None = None
    reset_snapshot: bool = False


class GestureStateMachine:
    def __init__(self, config):
        self.config = config
        self.state = State.IDLE
        self.snapshot = []
        self.selected = 0
        self.acc = 0.0
        self.last_step = 0
        self.started_at = None
        self.overlay_visible = False

    def update_config(self, config):
        self.config = config

    def _reset(self):
        self.state = State.IDLE
        self.snapshot = []
        self.selected = 0
        self.acc = 0.0
        self.last_step = 0
        self.started_at = None
        self.overlay_visible = False

    def handle(self, event: GestureEvent, windows=None):
        if event.kind == "begin":
            if event.fingers != self.config.fingers or self.state != State.IDLE:
                return StateResult()
            self.snapshot = list(windows or [])
            if len(self.snapshot) < 2:
                self._reset()
                return StateResult()
            self.state = State.PENDING
            self.selected = 0
            self.acc = 0.0
            self.last_step = 0
            self.started_at = event.timestamp if event.timestamp is not None else time.monotonic()
            return StateResult()

        if event.kind == "update":
            if self.state == State.IDLE:
                return StateResult()
            self.acc += event.dx
            if self.state == State.PENDING:
                if abs(self.acc) < self.config.show_threshold_px:
                    return StateResult()
                self.state = State.ACTIVE
                self.overlay_visible = True
                # Include the movement that crossed the display threshold.
                # Otherwise a fast initial swipe can open the overlay while
                # leaving the selection behind the user's actual movement.
                step = int(self.acc / self.config.step_px)
                delta = step - self.last_step
                if delta:
                    direction = -1 if self.config.invert_direction else 1
                    self.selected = (self.selected - delta * direction) % len(self.snapshot)
                self.last_step = step
                return StateResult(show_overlay=True, overlay_visible=True,
                                   selected_index=self.selected)
            step = int(self.acc / self.config.step_px)
            delta = step - self.last_step
            if delta:
                direction = -1 if self.config.invert_direction else 1
                self.selected = (self.selected - delta * direction) % len(self.snapshot)
                self.last_step = step
            return StateResult(overlay_visible=True, selected_index=self.selected)

        if event.kind == "end":
            if self.state == State.IDLE:
                return StateResult()
            if event.cancelled:
                was_visible = self.overlay_visible
                self._reset()
                return StateResult(hide_overlay=was_visible, reset_snapshot=True)
            chosen = None
            was_visible = self.state == State.ACTIVE
            if was_visible and self.snapshot:
                chosen = self.snapshot[self.selected]
            elif abs(self.acc) >= self.config.flick_min_px and self.snapshot:
                direction = -1 if self.config.invert_direction else 1
                index = 1 if self.acc < 0 else -1
                chosen = self.snapshot[(index * direction) % len(self.snapshot)]
            self._reset()
            return StateResult(hide_overlay=was_visible, activate_id=chosen,
                               reset_snapshot=True)
        return StateResult()

    def check_timeout(self, now=None):
        if self.state == State.IDLE or self.started_at is None:
            return StateResult()
        current = now if now is not None else time.monotonic()
        if current - self.started_at <= self.config.gesture_timeout:
            return StateResult()
        was_visible = self.overlay_visible
        self._reset()
        return StateResult(hide_overlay=was_visible, reset_snapshot=True)
