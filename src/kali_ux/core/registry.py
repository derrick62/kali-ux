"""Static feature registry; intentionally not a third-party plugin loader."""
from dataclasses import dataclass
from typing import Callable
@dataclass(frozen=True)
class Feature:
    key: str
    title: str
    description: str
    status: str
    requires: tuple[str, ...] = ()
FEATURES = (
 Feature('window_switcher','SwipeSwitch','Gesture-driven MRU window switching and desktop actions','integrated',('X11','GTK3','libwnck')),
 Feature('gesture_control','Gesture Control','Normalized gesture routing and conflict reporting','foundation',('gesture provider',)),
 Feature('window_overview','Task View','Overview of open windows with selection and dismissal','integrated',('X11','GTK3')),
 Feature('snap_assist','Snap Assist','Native window placement presets and snap suggestions','foundation',('X11','xfwm4')),
 Feature('clipboard_history','Clipboard History','Bounded local history with explicit persistence controls','foundation',('X11','xclip')),
 Feature('quick_panel','Quick Panel','Shortcuts to existing XFCE controls','foundation',('XFCE',)),
 Feature('focus_tools','Focus Tools','Optional do-not-disturb and focus session controls','foundation',('XFCE',)),
 Feature('launcher','Application Launcher','Desktop-entry search and launch','foundation',()),
 Feature('window_peek','Window Peek','Best-effort window preview capability','foundation',('X11 compositor',)),
 Feature('layout_memory','Layout Memory','Save and restore best-effort window geometry','foundation',('X11','wmctrl')),
)
