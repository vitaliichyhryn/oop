from gi.repository import Adw, Gtk, Gio

from .sign_up import SignUpWindow

@Gtk.Template(resource_path='/com/chyhryn/Project/gtk/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'
    
    sign_up_button: Gtk.Button = Gtk.Template.Child()
    toolbar_view: Adw.ToolbarView = Gtk.Template.Child()
    box: Gtk.Box = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_action("sign_up", self.on_sign_up)
        self.user_data_box = None
    
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
    
    def on_sign_up(self, action, button):
        sign_up_win = SignUpWindow(self)
        sign_up_win.present()
        sign_up_win.connect("close-request", lambda *_: self.sign_up_button.set_sensitive(True))
        self.sign_up_button.set_sensitive(False)
        
