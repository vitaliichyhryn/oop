import sys
import gi

gi.require_version("Adw", "1")

from gi.repository import Gio, Adw
from window import Window
from action_1 import action_1
from action_2 import action_2


class App(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.create_action("action_1", self.on_action_1)
        self.create_action("action_2", self.on_action_2)

    @property
    def win(self):
        return self.get_active_window()

    def do_activate(self):
        win = Window(application=self)
        win.present()

    def create_action(self, name, callback):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)

    def on_action_1(self, *_args):
        action_1(self)

    def on_action_2(self, *_args):
        action_2(self)


def main():
    app = App()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
