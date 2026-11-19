"""Pre-created GTK3 switcher overlay."""
import logging
from gi.repository import Pango

log = logging.getLogger(__name__)

DARK_CSS = """
window#swipeswitch-overlay { background-color: rgba(12, 15, 22, 0.88); }
.frame { background-color: rgba(28, 33, 45, 0.96); border: 1px solid rgba(255,255,255,0.10); border-radius: 16px; padding: 14px; }
.card { background-color: rgba(255,255,255,0.055); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px; min-width: 132px; min-height: 106px; }
.card.selected { background-color: rgba(55,112,220,0.24); border: 2px solid #6ea8ff; }
.title { color: #f3f5f8; font-size: 12px; }
.icon { color: #dce6f5; font-size: 28px; }
"""
LIGHT_CSS = """
window#swipeswitch-overlay { background-color: rgba(25,30,40,0.55); }
.frame { background-color: rgba(245,247,250,0.98); border: 1px solid #d6dce5; border-radius: 16px; padding: 14px; }
.card { background-color: #fff; border: 1px solid #dce2ea; border-radius: 12px; padding: 12px; min-width: 132px; min-height: 106px; }
.card.selected { background-color: #e5efff; border: 2px solid #2878e8; }
.title { color: #18202c; font-size: 12px; }
.icon { color: #315b91; font-size: 28px; }
"""


class SwitcherOverlay:
    def __init__(self, Gtk, Gdk, config):
        self.Gtk, self.Gdk, self.config = Gtk, Gdk, config
        self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
        self.window.set_name("swipeswitch-overlay")
        self.window.set_title("swipeswitch-overlay")
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)
        self.window.set_accept_focus(False)
        self.window.set_focus_on_map(False)
        self.window.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.window.set_app_paintable(True)
        self.window.connect("draw", self._draw_fallback)
        self.css = Gtk.CssProvider()
        self.screen = Gdk.Screen.get_default()
        self._apply_css()
        self.outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.outer.set_halign(Gtk.Align.CENTER)
        self.outer.set_valign(Gtk.Align.CENTER)
        self.frame = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.frame.get_style_context().add_class("frame")
        self.outer.pack_start(self.frame, True, True, 0)
        self.window.add(self.outer)
        self.cards, self.windows, self.selected = [], [], 0
        self.window.hide()

    def _apply_css(self):
        css = LIGHT_CSS if self.config.theme == "light" else DARK_CSS
        try:
            self.css.load_from_data(css.encode())
            self.Gtk.StyleContext.add_provider_for_screen(
                self.screen, self.css, self.Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        except Exception:
            log.exception("Could not apply overlay CSS")

    def update_config(self, config):
        self.config = config
        self._apply_css()

    def _draw_fallback(self, widget, cr):
        try:
            if not self.Gdk.Screen.get_default().is_composited():
                cr.set_source_rgb(0.055, 0.065, 0.09)
                cr.paint()
        except Exception:
            pass
        return False

    def show(self, windows, selected_index=0):
        self.windows, self.selected = list(windows), selected_index
        self._rebuild()
        self.window.show_all()
        self.window.present()
        self.window.set_keep_above(True)
        self._center_on_primary()

    def _center_on_primary(self):
        try:
            display = self.Gdk.Display.get_default()
            monitor = display.get_primary_monitor() or display.get_monitor(0)
            geo = monitor.get_geometry()
            width = min(760, geo.width - 60)
            height = min(190, geo.height - 60)
            self.window.set_default_size(width, height)
            self.window.move(geo.x + (geo.width-width)//2, geo.y + (geo.height-height)//2)
        except Exception:
            self.window.set_position(self.Gtk.WindowPosition.CENTER)

    def _rebuild(self):
        for child in self.frame.get_children():
            self.frame.remove(child)
        self.cards = []
        for index, window in enumerate(self.windows):
            card = self.Gtk.Box(orientation=self.Gtk.Orientation.VERTICAL, spacing=8)
            card.set_halign(self.Gtk.Align.CENTER)
            context = card.get_style_context()
            context.add_class("card")
            if index == self.selected:
                context.add_class("selected")
            icon = window.get_icon()
            if icon is not None:
                image = self.Gtk.Image.new_from_pixbuf(icon)
                image.set_pixel_size(40)
                card.pack_start(image, True, True, 0)
            else:
                fallback = self.Gtk.Label(label="▣")
                fallback.get_style_context().add_class("icon")
                card.pack_start(fallback, True, True, 0)
            title = self.Gtk.Label(label=(window.get_name() or "Untitled window")[:34])
            title.set_ellipsize(Pango.EllipsizeMode.END)
            title.set_max_width_chars(20)
            title.get_style_context().add_class("title")
            card.pack_start(title, False, False, 0)
            self.frame.pack_start(card, False, False, 0)
            self.cards.append(card)
        self.frame.show_all()

    def update_selection(self, selected_index):
        if not self.cards:
            return
        selected_index %= len(self.cards)
        if selected_index == self.selected:
            return
        self.cards[self.selected].get_style_context().remove_class("selected")
        self.selected = selected_index
        self.cards[self.selected].get_style_context().add_class("selected")

    def hide(self):
        self.window.hide()
