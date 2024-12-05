import cairo
import math
from abc import ABC, abstractmethod


class Shape(ABC):
    def __init__(self, x1, y1, x2=None, y2=None):
        self.start_pos = (x1, y1)
        self.end_pos = (x2, y2)
        self.is_drawn = False

    @abstractmethod
    def draw(self, context): ...

    @property
    def width(self):
        return self.end_pos[0] - self.start_pos[0]

    @property
    def height(self):
        return self.end_pos[1] - self.start_pos[1]


class Point(Shape):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)

    def draw(self, context: cairo.Context):
        if self.end_pos != (None, None):
            context.arc(self.end_pos[0], self.end_pos[1], 3, 0, 2 * math.pi)
            context.fill()


class Line(Shape):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)

    def draw(self, context: cairo.Context):
        context.move_to(self.start_pos[0], self.start_pos[1])
        if self.end_pos != (None, None):
            context.line_to(self.end_pos[0], self.end_pos[1])
            context.stroke()


class Rectangle(Shape):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)

    def draw(self, context: cairo.Context):
        if self.end_pos != (None, None):
            context.rectangle(
                self.start_pos[0], self.start_pos[1], self.width, self.height
            )
            context.stroke()


class Ellipse(Shape):
    def __init__(self, x1, y1):
        super().__init__(x1, y1)

    def draw(self, context: cairo.Context):
        if self.end_pos != (None, None):
            context.save()
            context.translate(
                self.start_pos[0],
                self.start_pos[1],
            )
            if self.width != 0 and self.height != 0:
                context.scale(self.width, self.height)
            context.arc(0, 0, 1, 0, 2 * math.pi)
            context.restore()
            if self.is_drawn:
                context.set_source_rgb(1, 0, 1)
                context.fill_preserve()
                context.set_source_rgb(0, 0, 0)
                context.stroke()
            else:
                context.stroke()
