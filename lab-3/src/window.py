from gi.repository import Adw, Gtk, Gio
from .drawing_area import DrawingArea
from .shape_picker import ShapePicker


@Gtk.Template(resource_path="/com/chyhryn/Lab3/gtk/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__: str = "Window"

    drawing_area: DrawingArea = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        pick_shape = Gio.PropertyAction(
            name="pick_shape",
            object=self.drawing_area,
            property_name="picked_shape_name",
        )

        self.add_action(pick_shape)
