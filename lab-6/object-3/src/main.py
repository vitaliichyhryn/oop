
import sys, gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gio, Adw
from .window import Window
from .dbus_interface import DBusInterface


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.chyhryn.Object3',
                         flags=Gio.ApplicationFlags.DEFAULT_FLAGS)
        
    def do_startup(self):
        Adw.Application.do_startup(self)
        self.create_action('quit', lambda *_: self.quit(), ['<primary>q'])

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.present()
        
        interface = DBusInterface(self)

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
    

def main(version):
    app = Application()
    return app.run(sys.argv)
