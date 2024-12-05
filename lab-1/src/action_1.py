import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw


class Dialog(Adw.AlertDialog):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.parent = app

        entry = Gtk.Entry()
        self.set_extra_child(entry)

        self.add_response(id="cancel", label="Відміна")
        self.add_response(id="confirm", label="Так")

        self.choose(parent=self.parent.win, callback=self.on_response_selected)

    def on_response_selected(self, _, result):
        response = self.choose_finish(result)
        entry = self.get_extra_child()

        if response == "confirm":
            entry_text = entry.get_text()
            self.parent.win.label.set_label(entry_text)


def action_1(app):
    dialog = Dialog(app)
