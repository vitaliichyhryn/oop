from gi.repository import Adw, Gtk, Gio

from .sign_up import SignUpDialog

@Gtk.Template(resource_path='/com/chyhryn/Project/gtk/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'
    
    toolbar_view: Adw.ToolbarView = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_action("sign_up", self.on_sign_up)
    
    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)
    
    def on_sign_up(self, action, button):
        sign_up_dialog = SignUpDialog()
        sign_up_dialog.present()
        
