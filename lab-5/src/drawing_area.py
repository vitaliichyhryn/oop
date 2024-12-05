import cairo
import gi

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Gtk, GObject
from .shapes import *
from .singleton import singleton

@singleton
@Gtk.Template(resource_path="/com/chyhryn/Lab5/gtk/drawing-area.ui")
class DrawingArea(Gtk.DrawingArea):
    __gtype_name__: str = "DrawingArea"

    picked_shape_name = GObject.Property(
        type=str,
        default="Крапка",
    )
    
    stroked = GObject.Signal("stroked")

    def shape_from_name(self, shape_name) -> type[Shape]:
        match shape_name:
            case "Крапка":
                return Dot
            case "Лінія":
                return Line
            case "Лінія з кружками":
                return LineWithCircles
            case "Прямокутник":
                return Rectangle
            case "Куб":
                return Cube
            case "Еліпс":
                return Ellipse
            case _:
                raise Exception(f"Invalid shape name: {self.shape_name}")
    
    @property
    def picked_shape(self) -> type[Shape]:
        return self.shape_from_name(self.picked_shape_name)
    
    @property
    def is_drawing(self) -> bool:
        return self.current_shape is not None
    
    @property
    def table(self) -> list[dict[str, str]]:
        keys = ["Фігура", "Початкова точка", "Кінцева точка"]
        table = [{key : None for key in keys}]
        
        for shape in self.shapes:
            start_pos = f"({shape.start_pos[0]:.3f}, {shape.start_pos[1]:.3f})"
            end_pos = f"({shape.end_pos[0]:.3f}, {shape.end_pos[1]:.3f})"
            
            shape_values = [shape.name, start_pos, end_pos]
            table.append(dict(zip(keys, shape_values)))
        
        return table
        
    @table.setter
    def table(self, table) -> None:
        keys = list(table[0].keys())
        self.shapes = []
        self.selected_shape = None
        
        for entry in table[1:]:
            shape_name = entry[keys[0]]
            start_pos = tuple(map(float, entry[keys[1]].strip("()").split(", ")))
            end_pos = tuple(map(float, entry[keys[2]].strip("()").split(", ")))
            
            shape_class = self.shape_from_name(shape_name)
            shape = shape_class(start_pos, end_pos)
            
            shape.is_stroked = True
            if isinstance(shape, Ellipse):
                shape.is_filled = True
            self.shapes.append(shape)
        
        self.queue_draw()
        self.stroked.emit()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        
        self.set_draw_func(self.draw)

        gesture_click = Gtk.GestureClick()
        self.add_controller(gesture_click)

        gesture_click.connect("pressed", self.on_pressed)
        gesture_click.connect("released", self.on_released)

        controller_motion = Gtk.EventControllerMotion()
        self.add_controller(controller_motion)

        controller_motion.connect("motion", self.on_motion)

        self.current_shape: Shape | None = None
        self.selected_shape: Shape | None = None
        self.shapes: list[Shape] = []

    def draw(self, area, context: cairo.Context, width: float, height: float) -> None:
        context.set_source_rgb(1, 1, 1)
        context.paint()

        context.set_source_rgb(0, 0, 0)
        context.set_line_width(3)

        for shape in self.shapes:
            if shape is self.selected_shape:
                continue
            if not shape.is_stroked:
                shape.draw_preview(context)
            else:
                shape.draw(context)
        
        if self.selected_shape:
            self.selected_shape.draw(context)
            self.selected_shape.draw_selection(context)

    def on_pressed(self, gesture: Gtk.GestureClick, n: int, x: float, y: float) -> None:
        self.current_shape = self.picked_shape((x, y), (x, y))
        self.shapes.append(self.current_shape)

    def on_released(
        self, gesture: Gtk.GestureClick, n: int, x: float, y: float
    ) -> None:
        self.current_shape.is_stroked = True
        if isinstance(self.current_shape, Ellipse):
            self.current_shape.is_filled = True
        self.stroked.emit()
        self.current_shape = None
        self.queue_draw()

    def on_motion(
        self, controller: Gtk.EventControllerMotion, x: float, y: float
    ) -> None:
        if self.is_drawing:
            self.current_shape.end_pos = (x, y)
            self.queue_draw()

