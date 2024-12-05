from gi.repository import Gtk
from .drawing_area import DrawingArea


@Gtk.Template(resource_path="/com/chyhryn/Lab5/gtk/shape-picker.ui")
class ShapePicker(Gtk.Box):
    __gtype_name__: str = "ShapePicker"

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
