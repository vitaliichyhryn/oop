import cairo
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, GObject
from . import shapes


@Gtk.Template(resource_path="/com/chyhryn/Lab3/gtk/drawing-area.ui")
class DrawingArea(Gtk.DrawingArea):
    __gtype_name__: str = "DrawingArea"

    picked_shape_name: GObject.Property = GObject.Property(
        type=str,
        default="Олівець",
    )

    @property
    def picked_shape(self) -> type[shapes.Shape]:
        match self.picked_shape_name:
            case "Олівець":
                return shapes.Pencil
            case "Лінія":
                return shapes.Line
            case "Прямокутник":
                return shapes.Rectangle
            case "Еліпс":
                return shapes.Ellipse
            case _:
                raise Exception(f"Invalid shape name: {self.picked_shape_name}")

    @property
    def is_drawing(self) -> bool:
        return self.current_shape is not None

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.set_draw_func(self.draw)

        gesture_click: Gtk.GestureClick = Gtk.GestureClick()
        self.add_controller(gesture_click)

        gesture_click.connect("pressed", self.on_pressed)
        gesture_click.connect("released", self.on_released)

        controller_motion: Gtk.EventControllerMotion = Gtk.EventControllerMotion()
        self.add_controller(controller_motion)

        controller_motion.connect("motion", self.on_motion)

        self.current_shape: shapes.Shape | None = None
        self.cache_surface: cairo.ImageSurface | None = None

    def draw(self, area, context: cairo.Context, width: float, height: float) -> None:
        if (
            not self.cache_surface
            or self.cache_surface.get_width() != width
            or self.cache_surface.get_height() != height
        ):
            old_cache_surface = self.cache_surface
            self.cache_surface = cairo.ImageSurface(cairo.Format.ARGB32, width, height)
            cache_context: cairo.Context = cairo.Context(self.cache_surface)
            cache_context.set_source_rgb(1.0, 1.0, 1.0)
            cache_context.paint()

            if old_cache_surface is not None:
                cache_context.set_source_surface(old_cache_surface, 0, 0)
                cache_context.paint()

        context.set_source_surface(self.cache_surface, 0, 0)
        context.paint()

        if self.is_drawing:
            draw_context: cairo.Context = (
                cairo.Context(self.cache_surface)
                if self.current_shape.is_stroked
                else context
            )
            draw_context.set_source_rgb(0.0, 0.0, 0.0)
            draw_context.set_line_width(3.0)
            self.current_shape.draw(draw_context)

            if self.current_shape.is_stroked:
                self.current_shape = None
                context.set_source_surface(self.cache_surface, 0, 0)
                context.paint()

    def on_pressed(self, gesture: Gtk.GestureClick, n: int, x: float, y: float) -> None:
        self.current_shape = self.picked_shape((x, y), (x, y))

    def on_released(
        self, gesture: Gtk.GestureClick, n: int, x: float, y: float
    ) -> None:
        self.current_shape.is_stroked = True
        self.queue_draw()

    def on_motion(
        self, controller: Gtk.EventControllerMotion, x: float, y: float
    ) -> None:
        if self.is_drawing:
            self.current_shape.end_pos = (x, y)
            self.queue_draw()
