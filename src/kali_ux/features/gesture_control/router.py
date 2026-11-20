"""In-process gesture routing with one recognizer and explicit ownership.

The router deliberately accepts a recognizer by interface rather than importing
one from a feature package. This keeps gesture acquisition/recognition
replaceable while allowing the active feature to own a complete gesture
lifecycle (including incremental updates and cancellation).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class Gesture:
    """Legacy completed-gesture value retained for existing integrations."""

    fingers: int
    direction: str
    phase: str = "end"
    distance: float = 0.0


class Recognizer(Protocol):
    """Minimal interface required by the shared router."""

    def handle(self, event: Any) -> list[Any]: ...

    def check_timeout(self, timeout_seconds: float) -> list[Any]: ...

    def reset(self) -> None: ...


@dataclass(frozen=True)
class _ActionHandler:
    owner: str
    callback: Callable[[Any], None]


class GestureRouter:
    """Route normalized input through one recognizer to one feature owner.

    ``register``/``dispatch`` preserve the original end-only routing contract.
    New integrations should inject a recognizer and use
    ``register_action_handler`` plus ``handle_event``. The first recognised
    action claims the gesture for its owner; subsequent actions from that
    gesture cannot be delivered to a different feature.
    """

    _TERMINAL_ACTIONS = frozenset(
        {"switch_commit", "switch_cancel", "task_view", "show_desktop"}
    )

    def __init__(self, recognizer: Recognizer | None = None):
        self._handlers: dict[tuple[int, str], Callable[[Gesture], None]] = {}
        self._action_handlers: dict[str, _ActionHandler] = {}
        self._recognizer = recognizer
        self._enabled = False
        self._active_owner: str | None = None
        self._active_fingers: int | None = None

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        value = bool(value)
        if self._enabled and not value:
            self._reset_lifecycle()
        self._enabled = value

    @property
    def active_owner(self) -> str | None:
        """Return the owner of the currently recognised gesture, if any."""
        return self._active_owner

    def set_recognizer(self, recognizer: Recognizer) -> None:
        if recognizer is None:
            raise TypeError("recognizer must not be None")
        self._reset_lifecycle()
        self._recognizer = recognizer

    def register(self, fingers: int, direction: str, handler: Callable[[Gesture], None]) -> None:
        """Register a legacy handler for a completed direction gesture."""
        key = (int(fingers), str(direction))
        if key in self._handlers:
            raise ValueError(f"Gesture already registered: {key}")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._handlers[key] = handler

    def register_action_handler(
        self,
        action_name: str,
        handler: Callable[[Any], None],
        *,
        owner: str,
    ) -> None:
        """Register one feature handler for a recognised action name."""
        action_name = str(action_name).strip()
        owner = str(owner).strip()
        if not action_name or not owner:
            raise ValueError("action_name and owner must not be empty")
        if action_name in self._action_handlers:
            raise ValueError(f"Action already registered: {action_name}")
        if not callable(handler):
            raise TypeError("handler must be callable")
        self._action_handlers[action_name] = _ActionHandler(owner, handler)

    def unregister_action_handler(self, action_name: str) -> bool:
        """Remove a handler; release its ownership if it owns the active gesture."""
        entry = self._action_handlers.pop(action_name, None)
        if entry is None:
            return False
        if self._active_owner == entry.owner:
            self._active_owner = None
        return True

    def dispatch(self, event: Gesture) -> bool:
        """Dispatch a legacy completed gesture when routing is enabled."""
        if not self.enabled or event.phase not in ("end", "cancel"):
            return False
        handler = self._handlers.get((event.fingers, event.direction))
        if not handler:
            return False
        handler(event)
        return True

    def handle_event(self, event: Any) -> list[Any]:
        """Recognise and route one normalized begin/update/end event."""
        if not self.enabled or self._recognizer is None:
            return []

        kind = getattr(event, "kind", None)
        fingers = getattr(event, "fingers", None)
        previous_fingers = self._active_fingers
        actions = self._recognizer.handle(event)
        for action in actions:
            self._dispatch_action(action)

        # A fresh BEGIN closes the previous sequence only after any cancellation
        # action returned by the recognizer has reached its current owner.
        if kind == "begin":
            self._active_owner = None
            self._active_fingers = int(fingers) if fingers is not None else None
        elif kind == "end":
            self._active_owner = None
            self._active_fingers = None
        elif kind == "update" and previous_fingers is not None and fingers != previous_fingers:
            self._active_owner = None
            self._active_fingers = None

        return actions

    def check_timeout(self, timeout_seconds: float) -> list[Any]:
        """Ask the recognizer to expire an unfinished gesture and route its actions."""
        if not self.enabled or self._recognizer is None:
            return []
        actions = self._recognizer.check_timeout(timeout_seconds)
        for action in actions:
            self._dispatch_action(action)
        if getattr(self._recognizer, "fingers", None) == 0:
            self._active_owner = None
            self._active_fingers = None
        return actions

    def _dispatch_action(self, action: Any) -> bool:
        name = getattr(action, "name", None)
        entry = self._action_handlers.get(name)
        if entry is None:
            return False
        if self._active_owner is None:
            self._active_owner = entry.owner
        if self._active_owner != entry.owner:
            return False
        try:
            entry.callback(action)
        finally:
            if name in self._TERMINAL_ACTIONS:
                self._active_owner = None
        return True

    def _reset_lifecycle(self) -> None:
        if self._recognizer is not None:
            reset = getattr(self._recognizer, "reset", None)
            if callable(reset):
                reset()
        self._active_owner = None
        self._active_fingers = None
