import cairo
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(
        self, start_pos: tuple[float, float], end_pos: tuple[float, float]
    ) -> None:
        self.start_pos: tuple[float, float] = start_pos
        self.end_pos: tuple[float, float] = end_pos
        self.is_stroked: bool = False

    @abstractmethod
    def draw(self, context) -> None: ...

    def draw_anchors(self, context) -> None:
        context.set_line_width(1.0)
        context.arc(self.start_pos[0], self.start_pos[1], 3, 0.0, 2.0 * math.pi)
        context.stroke()
        if self.start_pos != self.end_pos:
            context.arc(self.end_pos[0], self.end_pos[1], 3, 0.0, 2.0 * math.pi)
            context.stroke()
        context.set_line_width(3.0)

    @property
    def width(self) -> float:
        return self.end_pos[0] - self.start_pos[0]

    @property
    def height(self) -> float:
        return self.end_pos[1] - self.start_pos[1]


class Pencil(Shape):
    def __init__(
        self, start_pos: tuple[float, float], end_pos: tuple[float, float]
    ) -> None:
        super().__init__(start_pos, end_pos)
        self.path: cairo.Path | None = None

    def draw(self, context: cairo.Context) -> None:
        context.arc(self.start_pos[0], self.start_pos[1], 1.5, 0.0, 2.0 * math.pi)
        if self.start_pos != self.end_pos:
            context.arc(self.end_pos[0], self.end_pos[1], 1.5, 0.0, 2.0 * math.pi)
        context.fill()

        if self.path is None:
            context.move_to(self.start_pos[0], self.start_pos[1])
            context.line_to(self.end_pos[0], self.end_pos[1])
            self.path = context.copy_path()
        else:
            context.append_path(self.path)
            context.line_to(self.end_pos[0], self.end_pos[1])
            self.path = context.copy_path()
        context.stroke()


class Line(Shape):
    def __init__(
        self, start_pos: tuple[float, float], end_pos: tuple[float, float]
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        if not self.is_stroked:
            self.draw_anchors(context)
        context.move_to(self.start_pos[0], self.start_pos[1])
        context.line_to(self.end_pos[0], self.end_pos[1])
        context.stroke()


class Rectangle(Shape):
    def __init__(
        self, start_pos: tuple[float, float], end_pos: tuple[float, float]
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        if not self.is_stroked:
            self.draw_anchors(context)
        context.rectangle(self.start_pos[0], self.start_pos[1], self.width, self.height)
        context.stroke()


class Ellipse(Shape):
    pink: tuple[float, float, float] = (1.0, 0.75, 0.8)

    def __init__(
        self, start_pos: tuple[float, float], end_pos: tuple[float, float]
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        if not self.is_stroked:
            self.draw_anchors(context)
        context.save()
        context.translate(
            self.start_pos[0],
            self.start_pos[1],
        )
        if self.width != 0.0 and self.height != 0.0:
            context.scale(self.width, self.height)
        context.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
        context.restore()
        if self.is_stroked:
            context.set_source_rgb(*self.pink)
            context.fill_preserve()
            context.set_source_rgb(0.0, 0.0, 0.0)
        context.stroke()
