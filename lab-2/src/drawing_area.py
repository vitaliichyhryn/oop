import cairo
import gi
import shapes

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk


class DrawingArea(Gtk.DrawingArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_hexpand(True)
        self.set_vexpand(True)

        self.set_draw_func(self.draw)

        gesture_click = Gtk.GestureClick()
        self.add_controller(gesture_click)

        gesture_click.connect("pressed", self.on_pressed)
        gesture_click.connect("released", self.on_released)

        controller_motion = Gtk.EventControllerMotion()
        self.add_controller(controller_motion)

        controller_motion.connect("motion", self.on_motion)

        self.current_shape = None
        self.selected_shape_class = shapes.Point
        self.shapes = []

        self.mouse_pressed = False
        self.mouse_pos = (0, 0)

    def draw(self, area, context: cairo.Context, width, heigth):
        context.set_source_rgb(1, 1, 1)
        context.paint()

        context.set_source_rgb(0, 0, 0)
        context.set_line_width(3)

        for shape in self.shapes:
            shape.draw(context)

    def on_pressed(self, gesture, n, x, y):
        self.mouse_pressed = True
        self.current_shape = self.selected_shape_class(x, y)
        self.shapes.append(self.current_shape)

    def on_released(self, gesture, n, x, y):
        self.mouse_pressed = False
        self.current_shape.end_pos = (x, y)
        self.current_shape.is_drawn = True
        self.queue_draw()

    def on_motion(self, controller, x, y):
        self.mouse_pos = (x, y)
        if self.mouse_pressed:
            self.current_shape.end_pos = (x, y)
            self.queue_draw()
