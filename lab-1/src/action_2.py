import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, Adw


class Dialog(Adw.AlertDialog):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)

        self.parent = app

        scale = Gtk.Scale(
            adjustment=Gtk.Adjustment(value=50, lower=1, upper=100, step_increment=1),
            digits=0,
            draw_value=True,
        )
        self.set_extra_child(scale)

        self.add_response(id="cancel", label="Відміна")
        self.add_response(id="confirm", label="Так")

        self.choose(parent=self.parent.win, callback=self.on_response_selected)

    def on_response_selected(self, _, result):
        response = self.choose_finish(result)
        scale = self.get_extra_child()

        if response == "confirm":
            scale_value = int(scale.get_value())
            self.parent.win.label.set_label(str(scale_value))


def action_2(app):
    dialog = Dialog(app)
