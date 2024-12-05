import sys
import gi

gi.require_version("Adw", "1")

from gi.repository import Adw
from window import Window


class Application(Adw.Application):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def window(self):
        return self.get_active_window()

    def do_activate(self) -> None:
        window: Adw.Window = Window(application=self)
        window.present()


def main() -> None:
    application = Application()
    return application.run(sys.argv)


if __name__ == "__main__":
    main()
