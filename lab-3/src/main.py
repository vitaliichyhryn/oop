import sys
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, Gio
from .window import Window


class Application(Adw.Application):
    def __init__(self) -> None:
        super().__init__(
            application_id="com.chyhryn.Lab3",
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

    def do_activate(self) -> None:
        win = self.props.active_window
        if not win:
            win = Window(application=self)
        win.present()


def main(version) -> int:
    app = Application()
    return app.run(sys.argv)
