import gi
import shapes

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw
from drawing_area import DrawingArea


class Window(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_default_size(800, 800)

        toolbar_view = Adw.ToolbarView()
        self.set_content(toolbar_view)

        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)

        window_title = Adw.WindowTitle(title="Лабораторна робота №2")
        header_bar.set_title_widget(window_title)

        self.drawing_area = DrawingArea()
        toolbar_view.set_content(self.drawing_area)

        list_model = Gtk.StringList()
        shapes = ["Крапка", "Лінія", "Прямокутник", "Еліпс"]
        for shape in shapes:
            list_model.append(shape)
        drop_down = Gtk.DropDown.new(list_model)
        drop_down.connect("notify::selected-item", self.on_selected_shape)
        header_bar.pack_end(drop_down)

    def on_selected_shape(self, drop_down, _):
        shape_dict = {
            "Крапка": shapes.Point,
            "Лінія": shapes.Line,
            "Прямокутник": shapes.Rectangle,
            "Еліпс": shapes.Ellipse,
        }
        selected_item_label = drop_down.get_selected_item().get_string()
        self.drawing_area.selected_shape_class = shape_dict.get(selected_item_label)
