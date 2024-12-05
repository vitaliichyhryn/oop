from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/chyhryn/Lab6/gtk/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'

    point_num_entry: Gtk.Entry = Gtk.Template.Child()
    x_low_entry: Gtk.Entry = Gtk.Template.Child()
    x_up_entry: Gtk.Entry = Gtk.Template.Child()
    y_low_entry: Gtk.Entry = Gtk.Template.Child()
    y_up_entry: Gtk.Entry = Gtk.Template.Child()
    
    @property
    def point_num(self) -> int:
        return int(self.point_num_entry.get_buffer().get_text())
        
    @property
    def x_low(self) -> int:
        return int(self.x_low_entry.get_buffer().get_text())
        
    @property
    def x_up(self) -> int:
        return int(self.x_up_entry.get_buffer().get_text())
        
    @property
    def y_low(self) -> int:
        return int(self.y_low_entry.get_buffer().get_text())
    
    @property
    def y_up(self) -> int:
        return int(self.y_up_entry.get_buffer().get_text())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
