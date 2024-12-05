import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import GLib, Gtk, Gio, Adw, Gdk
from .window import Window
from .objects import Object


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.chyhryn.Lab6',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        self.create_action('run', self.on_run_action)
        
        self.connection = Gio.bus_get_sync(Gio.BusType.SESSION)
        
        self.object_2 = Object(
            name="com.chyhryn.Object2",
            object_path = "/com/chyhryn/Object2",
            interface_name = "com.chyhryn.Object2Interface",
            connection = self.connection,
        )
        
        self.object_3 = Object(
            name="com.chyhryn.Object3",
            object_path = "/com/chyhryn/Object3",
            interface_name = "com.chyhryn.Object3Interface",
            connection = self.connection,
        )

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = Window(application=self)
        self.win.present()
    
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
    
    def on_run_action(self, *args):
        if not self.object_2.is_active:
            self.object_2.activate()
        
        parameters = GLib.Variant(
            "(iiiii)",
            [
                self.win.point_num,
                self.win.x_low,
                self.win.x_up,
                self.win.y_low, 
                self.win.y_up
            ]
        )
        self.object_2.call_method("Initialize", parameters)
        
        if not self.object_3.is_active:
            self.object_3.activate()
        
        self.object_3.call_method("Initialize")

    def do_shutdown(self):
        if self.object_2.is_active:
            self.object_2.shutdown()
        if self.object_3.is_active:
            self.object_3.shutdown()
        
        Adw.Application.do_shutdown(self)


def main(version):
    app = Application()
    return app.run(sys.argv)
