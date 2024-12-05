from gi.repository import Adw, Gtk
from .table import Table

@Gtk.Template(resource_path='/com/chyhryn/Object2/gtk/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'
    
    toolbar_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    def show_points(self, points: list[tuple[int, int]]):
        table = [{"Точка": "0", "Координати": "(0, 0)"}] + [
            {"Точка": str(num), "Координати": str(point)}
            for num, point in enumerate(points, 1)
        ]
        table = Table(table)
        self.toolbar_view.set_content(table)
