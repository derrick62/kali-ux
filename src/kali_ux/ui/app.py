"""Interactive GTK3 dashboard for the Kali UX prototype.

All desktop mutations are explicit user actions. The UI does not elevate privileges,
change xfwm4 configuration, or start an input listener automatically.
"""

from __future__ import annotations

import json

from kali_ux.core.config import load_config, write_default_config
from kali_ux.core.paths import CONFIG_HOME
from kali_ux.diagnostics.report import build_report
from kali_ux.features.clipboard_history.service import ClipboardHistory
from kali_ux.features.focus_tools.service import FocusMode
from kali_ux.features.launcher.service import ApplicationLauncher
from kali_ux.features.layout_memory.service import LayoutMemory
from kali_ux.features.quick_panel.actions import ACTIONS, open_action
from kali_ux.features.snap_assist.service import SnapService
from kali_ux.features.window_switcher.engine.activator import activate_window
from kali_ux.features.window_switcher.engine.task_view import TaskView
from kali_ux.platform.commands import start_command
from kali_ux.platform.gtk import load_gtk3


def _gtk():
    return load_gtk3()


class KaliUXWindow:
    def __init__(self, Gtk, Gdk, GLib, Pango, Wnck):
        self.Gtk, self.Gdk, self.GLib, self.Pango, self.Wnck = Gtk, Gdk, GLib, Pango, Wnck
        self.config = load_config()
        clipboard_config = self.config.get("clipboard", {})
        self.clipboard = ClipboardHistory(
            max_items=clipboard_config.get("max_items", 50),
            max_item_bytes=clipboard_config.get("max_item_bytes", 65536),
        )
        self.focus = FocusMode()
        self.layouts = LayoutMemory()
        self.launcher = ApplicationLauncher()
        self.snap = SnapService()
        self.window = Gtk.Window(title="Kali UX · Desktop Control Center")
        self.window.set_default_size(1000, 720)
        self.window.set_border_width(18)
        self.window.connect("destroy", Gtk.main_quit)
        self._style()
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        self.window.add(root)
        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        title = Gtk.Label()
        title.set_markup(
            '<span size="xx-large" weight="bold">Kali UX</span>  '
            '<span alpha="65%">Desktop Control Center</span>'
        )
        title.set_halign(Gtk.Align.START)
        header.pack_start(title, True, True, 0)
        status = Gtk.Button(label="System status")
        status.connect("clicked", self.show_diagnostics)
        header.pack_end(status, False, False, 0)
        root.pack_start(header, False, False, 0)
        subtitle = Gtk.Label(
            label="A unified set of thoughtful desktop interactions for XFCE on X11."
        )
        subtitle.set_halign(Gtk.Align.START)
        subtitle.get_style_context().add_class("muted")
        root.pack_start(subtitle, False, False, 0)

        self.notebook = Gtk.Notebook()
        root.pack_start(self.notebook, True, True, 0)
        self._build_home()
        self._build_windows()
        self._build_clipboard()
        self._build_launcher()
        self._build_productivity()
        self._build_settings()
        footer = Gtk.Label(
            label=(
                "Prototype · X11 / XFCE · Window manager remains xfwm4 · "
                "No background listeners started automatically"
            )
        )
        footer.get_style_context().add_class("muted")
        footer.set_halign(Gtk.Align.START)
        root.pack_start(footer, False, False, 0)
        self.window.show_all()
        self.clipboard_backend = self.Gtk.Clipboard.get(self.Gdk.SELECTION_CLIPBOARD)
        self.clipboard_backend.connect("owner-change", self._clipboard_changed)

    def _style(self):
        css = self.Gtk.CssProvider()
        css.load_from_data(b"""
            window { background: #171b24; color: #edf1f7; }
            notebook, notebook > header { background: #202633; }
            notebook tab { padding: 10px 16px; }
            button { padding: 8px 12px; border-radius: 8px; }
            entry, textview, treeview { background: #242c3a; color: #edf1f7; }
            .panel {
                background: #202735;
                border: 1px solid #354154;
                border-radius: 12px;
                padding: 16px;
            }
            .muted { color: #aab5c5; }
            .metric { font-size: 24px; font-weight: bold; }
        """)
        self.Gtk.StyleContext.add_provider_for_screen(
            self.Gdk.Screen.get_default(), css, self.Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _page(self, name):
        box = self.Gtk.Box(orientation=self.Gtk.Orientation.VERTICAL, spacing=12)
        box.set_border_width(16)
        self.notebook.append_page(box, self.Gtk.Label(label=name))
        return box

    def _button(self, parent, label, callback, *args):
        b = self.Gtk.Button(label=label)
        b.connect("clicked", lambda *_: callback(*args))
        parent.pack_start(b, False, False, 0)
        return b

    def _card(self, parent, title, description):
        box = self.Gtk.Box(orientation=self.Gtk.Orientation.VERTICAL, spacing=7)
        box.get_style_context().add_class("panel")
        heading = self.Gtk.Label()
        heading.set_markup(f"<b>{title}</b>")
        heading.set_halign(self.Gtk.Align.START)
        body = self.Gtk.Label(label=description)
        body.set_line_wrap(True)
        body.set_halign(self.Gtk.Align.START)
        body.get_style_context().add_class("muted")
        box.pack_start(heading, False, False, 0)
        box.pack_start(body, False, False, 0)
        parent.pack_start(box, False, False, 0)
        return box

    def _build_home(self):
        page = self._page("Overview")
        self._card(
            page,
            "Your desktop, brought together",
            "Use the tabs to switch windows, arrange your workspace, search applications, "
            "manage clipboard history and access common XFCE settings.",
        )
        grid = self.Gtk.Grid(column_spacing=12, row_spacing=12)
        page.pack_start(grid, False, False, 0)
        items = [
            ("Window switching", "Open the SwipeSwitch interface", self.start_swipeswitch),
            ("Task View", "See and select open windows", self.show_task_view),
            ("Snap Assist", "Arrange the active window", lambda: self.notebook.set_current_page(1)),
            (
                "Application launcher",
                "Find and launch applications",
                lambda: self.notebook.set_current_page(3),
            ),
            (
                "Clipboard history",
                "Review recent copied text",
                lambda: self.notebook.set_current_page(2),
            ),
            ("Diagnostics", "Check desktop capabilities", self.show_diagnostics),
        ]
        for i, (name, desc, cb) in enumerate(items):
            card = self.Gtk.Button()
            content = self.Gtk.Box(orientation=self.Gtk.Orientation.VERTICAL, spacing=6)
            h = self.Gtk.Label()
            h.set_markup(f"<b>{name}</b>")
            h.set_halign(self.Gtk.Align.START)
            d = self.Gtk.Label(label=desc)
            d.set_line_wrap(True)
            d.set_halign(self.Gtk.Align.START)
            content.pack_start(h, False, False, 0)
            content.pack_start(d, False, False, 0)
            card.add(content)
            card.connect("clicked", lambda _b, f=cb: f())
            grid.attach(card, i % 2, i // 2, 1, 1)

    def _build_windows(self):
        page = self._page("Windows")
        self._card(
            page,
            "Window overview and snapping",
            "Task View uses libwnck to inspect windows. Snap presets request geometry "
            "changes through wmctrl; xfwm4 remains authoritative.",
        )
        row = self.Gtk.Box(spacing=8)
        page.pack_start(row, False, False, 0)
        self._button(row, "Open Task View", self.show_task_view)
        self._button(row, "Refresh window list", self.refresh_windows)
        self.window_list = self.Gtk.ListBox()
        self.window_list.set_selection_mode(self.Gtk.SelectionMode.NONE)
        scroll = self.Gtk.ScrolledWindow()
        scroll.set_min_content_height(170)
        scroll.add(self.window_list)
        page.pack_start(scroll, True, True, 0)
        self.refresh_windows()
        self._card(
            page,
            "Snap Assist",
            "Choose a layout for the currently active window. Display work-area and "
            "multi-monitor calibration will be refined during live desktop testing.",
        )
        snapgrid = self.Gtk.Grid(column_spacing=8, row_spacing=8)
        page.pack_start(snapgrid, False, False, 0)
        presets = [
            "left",
            "right",
            "top",
            "bottom",
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
        ]
        for i, p in enumerate(presets):
            b = self.Gtk.Button(label=p.replace("-", " ").title())
            b.connect("clicked", lambda _b, preset=p: self.snap_active(preset))
            snapgrid.attach(b, i % 4, i // 4, 1, 1)

    def _screen(self):
        """Return the active window monitor's usable work area when possible."""
        display = self.Gdk.Display.get_default()
        x = y = 0
        wnck_screen = self.Wnck.Screen.get_default()
        active = wnck_screen.get_active_window() if wnck_screen else None
        if active is not None:
            wx, wy, ww, wh = active.get_geometry()
            x, y = wx + max(0, ww // 2), wy + max(0, wh // 2)
        monitor = display.get_monitor_at_point(x, y) if display else None
        if monitor:
            rect = (
                monitor.get_workarea()
                if hasattr(monitor, "get_workarea")
                else monitor.get_geometry()
            )
            return rect.x, rect.y, rect.width, rect.height
        screen = self.Gdk.Screen.get_default()
        if screen is None:
            return 0, 0, 0, 0
        if screen.get_n_monitors() > 0:
            rect = screen.get_monitor_workarea(0)
            return rect.x, rect.y, rect.width, rect.height
        return 0, 0, screen.get_width(), screen.get_height()

    def snap_active(self, preset):
        x, y, w, h = self._screen()
        ok = self.snap.snap_active(preset, w, h, x, y)
        self.notify(
            "Snap request sent."
            if ok
            else "Snap failed. Check that wmctrl is installed and an active X11 window exists."
        )

    def _window_objects(self):
        screen = self.Wnck.Screen.get_default()
        if not screen:
            return []
        screen.force_update()
        return [
            w
            for w in screen.get_windows()
            if not w.is_skip_tasklist() and w.get_window_type() == self.Wnck.WindowType.NORMAL
        ]

    def refresh_windows(self):
        for child in self.window_list.get_children():
            self.window_list.remove(child)
        for win in self._window_objects():
            row = self.Gtk.ListBoxRow()
            box = self.Gtk.Box(spacing=10)
            box.set_border_width(6)
            label = self.Gtk.Label(label=win.get_name() or "Untitled")
            label.set_halign(self.Gtk.Align.START)
            activate = self.Gtk.Button(label="Activate")
            activate.connect(
                "clicked",
                lambda _b, w=win: (w.activate(self.Gdk.CURRENT_TIME), self.window.present()),
            )
            box.pack_start(label, True, True, 0)
            box.pack_end(activate, False, False, 0)
            row.add(box)
            self.window_list.add(row)
        self.window_list.show_all()

    def show_task_view(self):
        try:
            if not hasattr(self, "task_view"):
                self.task_view = TaskView(
                    self.Gtk, self.Gdk, self.Pango, lambda w: activate_window(w, self.Gdk)
                )
            self.task_view.show(self._window_objects())
        except Exception as exc:
            self.notify(f"Task View unavailable: {exc}")

    def _build_clipboard(self):
        page = self._page("Clipboard")
        self._card(
            page,
            "Private clipboard history",
            "Recent text is held in memory only. Password-like content is not "
            "automatically detectable; pause capture before copying secrets. "
            "History is cleared when this application exits.",
        )
        bar = self.Gtk.Box(spacing=8)
        page.pack_start(bar, False, False, 0)
        self.capture_toggle = self.Gtk.CheckButton(label="Capture copied text during this session")
        self.capture_toggle.set_active(False)
        bar.pack_start(self.capture_toggle, False, False, 0)
        self._button(bar, "Clear history", self.clear_clipboard)
        self.clip_query = self.Gtk.Entry()
        self.clip_query.set_placeholder_text("Search clipboard history…")
        page.pack_start(self.clip_query, False, False, 0)
        self.clip_query.connect("changed", lambda *_: self.render_clipboard())
        self.clip_list = self.Gtk.ListBox()
        self.clip_scroll = self.Gtk.ScrolledWindow()
        self.clip_scroll.add(self.clip_list)
        page.pack_start(self.clip_scroll, True, True, 0)
        self.render_clipboard()

    def _clipboard_changed(self, clipboard, _event):
        if self.capture_toggle.get_active():
            # The asynchronous request avoids blocking GTK while another app
            # provides clipboard data over X11.
            clipboard.request_text(self._clipboard_text_received, None)

    def _clipboard_text_received(self, _clipboard, value, _user_data):
        if not self.capture_toggle.get_active() or not value:
            return
        self.clipboard.add(value)
        self.render_clipboard()

    def render_clipboard(self):
        if not hasattr(self, "clip_list"):
            return
        for child in self.clip_list.get_children():
            self.clip_list.remove(child)
        query = self.clip_query.get_text() if hasattr(self, "clip_query") else ""
        for item in self.clipboard.search(query):
            row = self.Gtk.ListBoxRow()
            box = self.Gtk.Box(spacing=8)
            box.set_border_width(8)
            text = self.Gtk.Label(label=item.text[:240].replace("\n", " ↵ "))
            text.set_line_wrap(True)
            text.set_halign(self.Gtk.Align.START)
            copy = self.Gtk.Button(label="Copy")
            copy.connect(
                "clicked",
                lambda _b, value=item.text: self.Gtk.Clipboard.get(
                    self.Gdk.SELECTION_CLIPBOARD
                ).set_text(value, -1),
            )
            box.pack_start(text, True, True, 0)
            box.pack_end(copy, False, False, 0)
            row.add(box)
            self.clip_list.add(row)
        self.clip_list.show_all()

    def clear_clipboard(self):
        self.clipboard.clear()
        self.render_clipboard()

    def _build_launcher(self):
        page = self._page("Applications")
        self._card(
            page,
            "Application launcher",
            "Search installed XDG desktop entries. Applications are launched through "
            "the desktop environment, without shell evaluation.",
        )
        self.app_search = self.Gtk.SearchEntry()
        self.app_search.set_placeholder_text("Search applications…")
        page.pack_start(self.app_search, False, False, 0)
        self.app_list = self.Gtk.ListBox()
        scroll = self.Gtk.ScrolledWindow()
        scroll.add(self.app_list)
        page.pack_start(scroll, True, True, 0)
        self.app_search.connect("search-changed", lambda *_: self.render_apps())
        self.render_apps()

    def render_apps(self):
        for child in self.app_list.get_children():
            self.app_list.remove(child)
        query = self.app_search.get_text()
        for entry in self.launcher.search(query)[:80]:
            row = self.Gtk.ListBoxRow()
            box = self.Gtk.Box(spacing=8)
            box.set_border_width(6)
            label = self.Gtk.Label(label=entry.name)
            label.set_halign(self.Gtk.Align.START)
            launch = self.Gtk.Button(label="Launch")
            launch.connect("clicked", lambda _b, e=entry: self.launch_app(e))
            box.pack_start(label, True, True, 0)
            box.pack_end(launch, False, False, 0)
            row.add(box)
            self.app_list.add(row)
        self.app_list.show_all()

    def launch_app(self, entry):
        if not self.launcher.launch(entry):
            self.notify(
                f"Could not start {entry.name}. Check that gio is installed and "
                "the desktop entry is valid."
            )
        else:
            self.notify(f"Launch requested: {entry.name}")

    def _build_productivity(self):
        page = self._page("Productivity")
        self._card(
            page,
            "Focus mode",
            "Temporarily request XFCE notification do-not-disturb. The previous "
            "value is restored when you disable it in this session.",
        )
        row = self.Gtk.Box(spacing=8)
        page.pack_start(row, False, False, 0)
        self._button(row, "Enable focus mode", self.enable_focus)
        self._button(row, "Restore notifications", self.disable_focus)
        self._card(
            page,
            "Quick Settings",
            "Open the existing XFCE settings applications rather than "
            "reimplementing system controls.",
        )
        grid = self.Gtk.Grid(column_spacing=8, row_spacing=8)
        page.pack_start(grid, False, False, 0)
        for i, key in enumerate(ACTIONS):
            b = self.Gtk.Button(label=key.title())
            b.connect(
                "clicked",
                lambda _b, k=key: self.notify(
                    "Launch requested."
                    if open_action(k)
                    else f"Could not start {k} settings; check optional packages."
                ),
            )
            grid.attach(b, i % 3, i // 3, 1, 1)
        self._card(
            page,
            "Layout memory",
            "Save current window geometry under a name, then request restoration "
            "later. This is best-effort and cannot guarantee exact monitor/workspace recovery.",
        )
        entry = self.Gtk.Entry()
        entry.set_placeholder_text("Layout name")
        page.pack_start(entry, False, False, 0)
        self.layout_name = entry
        row2 = self.Gtk.Box(spacing=8)
        page.pack_start(row2, False, False, 0)
        self._button(row2, "Save current layout", self.capture_layout)
        self._button(row2, "Restore selected layout", self.restore_layout)
        self.layout_combo = self.Gtk.ComboBoxText()
        page.pack_start(self.layout_combo, False, False, 0)
        self.refresh_layouts()

    def enable_focus(self):
        self.notify(
            "Focus mode enabled."
            if self.focus.enable()
            else "Could not enable focus mode; XFCE notification property may be unavailable."
        )

    def disable_focus(self):
        self.notify(
            "Previous notification setting restored."
            if self.focus.disable()
            else "No saved focus-mode state to restore."
        )

    def capture_layout(self):
        ok = self.layouts.capture(self.layout_name.get_text())
        self.refresh_layouts()
        self.notify(
            "Layout saved." if ok else "Could not save layout; check wmctrl and the layout name."
        )

    def refresh_layouts(self):
        self.layout_combo.remove_all()
        for name in self.layouts.names():
            self.layout_combo.append_text(name)

    def restore_layout(self):
        name = self.layout_combo.get_active_text()
        count = self.layouts.restore(name) if name else 0
        self.notify(f"Requested geometry restoration for {count} window(s).")

    def _build_settings(self):
        page = self._page("Settings")
        self._card(
            page,
            "Gesture integration",
            "Gesture routing is intentionally not enabled automatically. SwipeSwitch "
            "can start its own listener when explicitly launched. Before enabling a "
            "shared provider, verify device ownership, permissions and conflicts "
            "with existing gesture tools.",
        )
        self._button(page, "Start SwipeSwitch listener", self.start_swipeswitch)
        self._button(page, "Open configuration folder", self.open_config_folder)
        self._button(
            page,
            "Create default configuration",
            lambda: self.notify(f"Configuration: {write_default_config()}"),
        )
        self._button(page, "Show implementation status", self.show_status)
        self._card(
            page,
            "Privacy controls",
            "Clipboard capture is opt-in and memory-only. No clipboard content is "
            "logged or persisted. Window capture is not implemented. No telemetry is collected.",
        )

    def open_config_folder(self):
        try:
            CONFIG_HOME.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            self.notify(f"Could not create the configuration folder: {exc}")
            return
        result = start_command(["xdg-open", str(CONFIG_HOME)])
        if not result.started:
            self.notify(
                "Could not open the configuration folder; check that xdg-open is installed."
            )

    def start_swipeswitch(self):
        result = start_command(["kali-ux-swipeswitch"])
        if not result.started:
            self.notify("Could not start SwipeSwitch. Check that its command is installed.")
            return
        self.notify("SwipeSwitch launch requested. Check its logs if the listener does not start.")

    def show_diagnostics(self, *_):
        self._dialog("System diagnostics", json.dumps(build_report(), indent=2))

    def show_status(self):
        self._dialog(
            "Implementation status",
            "Kali UX prototype\n\n"
            "Working interfaces: dashboard, window list, Task View, eight snap presets, "
            "in-memory clipboard history, application search/launch, XFCE quick settings, "
            "focus mode and layout snapshots.\n\n"
            "Requires live validation: touchpad listener permissions and arbitration, "
            "multi-monitor work areas, focus restoration, compositor behaviour and "
            "XFCE notification settings.\n\n"
            "Not implemented: compositor-aware window screenshots, Wayland backend, "
            "persistent clipboard history, automatic gesture-provider configuration.",
        )

    def _dialog(self, title, content):
        dialog = self.Gtk.Dialog(
            title=title, transient_for=self.window, flags=self.Gtk.DialogFlags.MODAL
        )
        dialog.add_button("Close", self.Gtk.ResponseType.CLOSE)
        view = self.Gtk.TextView()
        view.set_editable(False)
        view.set_monospace(True)
        view.get_buffer().set_text(content)
        scroll = self.Gtk.ScrolledWindow()
        scroll.set_size_request(760, 480)
        scroll.add(view)
        dialog.get_content_area().pack_start(scroll, True, True, 8)
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def notify(self, message):
        dialog = self.Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=self.Gtk.MessageType.INFO,
            buttons=self.Gtk.ButtonsType.OK,
            text=message,
        )
        dialog.run()
        dialog.destroy()


def main():
    Gdk, GLib, Gtk, Pango, Wnck = _gtk()
    _window = KaliUXWindow(Gtk, Gdk, GLib, Pango, Wnck)
    Gtk.main()
    return 0
