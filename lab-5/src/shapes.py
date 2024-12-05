import cairo
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    preview_dash_sequence: list[float] = [5, 5]

    def __init__(
        self,
        start_pos: tuple[float, float],
        end_pos: tuple[float, float],
    ) -> None:
        self.start_pos: tuple[float, float] = start_pos
        self.end_pos: tuple[float, float] = end_pos
        self.is_stroked: bool = False
        self.is_filled: bool = False

    @abstractmethod
    def draw(self, context) -> None: ...
    
    @property
    @abstractmethod
    def name(self) -> str: ...
    
    def draw_selection(self, context: cairo.Context):
        context.save()
        
        blue = (0.0, 0.5, 1.0, 0.25)
        context.set_source_rgba(*blue)
        context.set_line_width(12)
        
        fill_state = self.is_filled
        self.is_filled = False if self.is_filled else fill_state
        self.draw(context)
        self.is_filled = fill_state
        
        context.restore()
    
    def draw_preview(self, context: cairo.Context):
        context.save()
        context.set_dash(self.preview_dash_sequence)
        self.draw(context)
        context.restore()
    
    @property
    def width(self) -> float:
        return self.end_pos[0] - self.start_pos[0]

    @property
    def height(self) -> float:
        return self.end_pos[1] - self.start_pos[1]


class Dot(Shape):
    def __init__(
        self,
        start_pos: tuple[float, float],
        end_pos: tuple[float, float],
    ) -> None:
        super().__init__(start_pos, end_pos)
        self.path: cairo.Path | None = None

    def draw(self, context: cairo.Context) -> None:
        context.arc(self.end_pos[0], self.end_pos[1], 3, 0.0, 2.0 * math.pi)
        context.fill_preserve()
        context.stroke()
    
    @property
    def name(self) -> str:
        return "Крапка"


class Line(Shape):
    def __init__(
        self,
        start_pos: tuple[float, float],
        end_pos: tuple[float, float],
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        context.move_to(self.start_pos[0], self.start_pos[1])
        context.line_to(self.end_pos[0], self.end_pos[1])
        context.stroke()
    
    @property
    def name(self) -> str:
        return "Лінія"

class Rectangle(Shape):
    def __init__(
        self,
        start_pos: tuple[float, float],
        end_pos: tuple[float, float],
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        context.rectangle(self.start_pos[0], self.start_pos[1], self.width, self.height)
        context.stroke()
    
    @property
    def name(self) -> str:
        return "Прямокутник"


class Ellipse(Shape):
    def __init__(
        self,
        start_pos: tuple[float, float],
        end_pos: tuple[float, float],
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        context.save()
        context.translate(
            self.start_pos[0],
            self.start_pos[1],
        )
        if self.width != 0.0 and self.height != 0.0:
            context.scale(self.width, self.height)
        context.arc(0.0, 0.0, 1.0, 0.0, 2.0 * math.pi)
        context.restore()
        
        if self.is_filled:
            context.save()
            pink = (1.0, 0.75, 0.8)
            context.set_source_rgb(*pink)
            context.fill_preserve()
            context.restore()
        
        context.stroke()
    
    @property
    def name(self) -> str:
        return "Еліпс"

class LineWithCircles(Line, Ellipse):
    def __init__(
        self,
        start_pos: tuple[float, float],
        end_pos: tuple[float, float],
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        Line.draw(self, context)

        temp_end_pos: tuple[float, float] = self.end_pos
        self.end_pos = (self.start_pos[0] + 5, self.start_pos[1] + 5)
        Ellipse.draw(self, context)
        self.end_pos = temp_end_pos

        temp_start_pos: tuple[float, float] = self.start_pos
        self.start_pos = self.end_pos
        self.end_pos = (self.start_pos[0] + 5, self.start_pos[1] + 5)
        Ellipse.draw(self, context)
        self.start_pos = temp_start_pos
        self.end_pos = temp_end_pos
    
    @property
    def name(self) -> str:
        return "Лінія з кружками"

class Cube(Line, Rectangle):
    def __init__(
        self,
        start_pos: tuple[float, float],
        end_pos: tuple[float, float],
    ) -> None:
        super().__init__(start_pos, end_pos)

    def draw(self, context: cairo.Context) -> None:
        temp_end_pos: tuple[float, float] = self.end_pos
        self.end_pos = (
            (self.start_pos[0] * 1 / 3 + self.end_pos[0] * 2 / 3),
            (self.start_pos[1] * 1 / 3 + self.end_pos[1] * 2 / 3),
        )
        Rectangle.draw(self, context)
        back_vertices = [
            (self.start_pos),
            (self.start_pos[0], self.end_pos[1]),
            (self.end_pos[0], self.start_pos[1]),
            (self.end_pos),
        ]
        self.end_pos = temp_end_pos

        temp_start_pos: tuple[float, float] = self.start_pos
        self.start_pos = (
            (self.start_pos[0] * 2 / 3 + self.end_pos[0] * 1 / 3),
            (self.start_pos[1] * 2 / 3 + self.end_pos[1] * 1 / 3),
        )
        Rectangle.draw(self, context)
        front_vertices = [
            (self.start_pos),
            (self.start_pos[0], self.end_pos[1]),
            (self.end_pos[0], self.start_pos[1]),
            (self.end_pos),
        ]
        self.start_pos = temp_start_pos

        for back_vertice, front_vertice in zip(back_vertices, front_vertices):
            self.start_pos = back_vertice
            self.end_pos = front_vertice
            Line.draw(self, context)
        self.start_pos = temp_start_pos
        self.end_pos = temp_end_pos
    
    @property
    def name(self) -> str:
        return "Куб"
