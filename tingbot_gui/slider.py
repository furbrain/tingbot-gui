import pygame
from .widget import Widget
from tingbot.graphics import _topleft_from_aligned_xy, _color
from .util import clamp


class Slider(Widget):

    """A general purpose slider widget
    Attributes:
        value: current value of the slider as a float
        max_val: maximum value that the slider can have
        min_val: minimum value that the slider can have
        step:    step value that the slider will change by if clicked
        callback: a function that accepts a float - called when the value is changed by a touch event

    Style Attributes:
        slider_line_color: color of the line
        slider_handle_color: color of the handle
    """

    def __init__(self, xy, size, align="center", parent=None, style=None,
                 max_val=1.0, min_val=0.0, step=None, callback=None, release_callback=None):
        """create a button with size and position specified by xy, size and align
        it will be a vertical slider if height is greater than width, otherwise horizontal
        max_val and min_val specify the maximum and minimum values respectively
        step specifies the step value, or 1/10 on the distance between max_val and min_val if zero or None
        callback(value) is a function to call if the value is changed
        release_callback(value) is a function to call when the slider is released
        """
        super(Slider, self).__init__(xy, size, align, parent, style)
        self.vertical = size[0] < size[1]
        self.max_val = float(max_val)
        self.min_val = float(min_val)
        if step:
            self.step = float(step)
        else:
            self.step = (max_val - min_val) / 10.0
        self.value = float(min_val)
        self.pressed = False
        self.callback = callback
        self.release_callback = release_callback

    def get_handle_size(self):
        (w, h) = self.size
        if self.vertical:
            return (w, w)
        else:
            return (h, h)

    def get_handle_position(self):
        (w, h) = self.size
        handle_size = self.get_handle_size()
        position = (self.value - self.min_val) / (self.max_val - self.min_val)
        position = clamp(0.0, 1.0, position)
                         #clip to be with max_val and min_val
        if self.vertical:
            position = (
                w / 2,
                int(h - ((h - handle_size[1]) * position) - handle_size[1] / 2))
        else:
            position = (
                int((w - handle_size[0]) * position) + handle_size[0] / 2,
                h / 2)
        return position

    def draw_groove(self):
        (w, h) = self.size
        if self.vertical:
            start = (w / 2, 0)
            end = (w / 2, h)
            width = w / 5
        else:
            start = (0, h / 2)
            end = (w, h / 2)
            width = h / 5
        pygame.draw.line(
            self.surface,
            _color(self.style.slider_line_color),
            start,
            end,
            width)

    def draw_handle(self):
        position = self.get_handle_position()
        size = self.get_handle_size()
        pygame.draw.circle(
            self.surface,
            _color(self.style.slider_handle_color),
            position,
            size[0] / 2)

    def draw(self):
        self.fill(self.style.bg_color)
        self.draw_groove()
        self.draw_handle()

    def on_touch(self, xy, action):
        handle_size = self.get_handle_size()
        if action=="down":
                handle_pos = _topleft_from_aligned_xy(
                    self.get_handle_position(),
                    "center",
                    handle_size,
                    self.parent.size)
                handle_rect = pygame.Rect(handle_pos, handle_size)
                if handle_rect.collidepoint(xy):
                    self.pressed = True
        if action in ("move","up"):
            if self.vertical:
                pos = 1.0 - \
                    float(xy[1] - handle_size[1] / 2) / (
                        self.size[1] - handle_size[1])
            else:
                pos = float(xy[0] - handle_size[0] / 2) / (
                    self.size[0] - handle_size[0])
            new_pos = self.min_val + pos * (self.max_val - self.min_val)
            new_pos = clamp(self.min_val, self.max_val, new_pos)
            if self.pressed:            
                self.value = new_pos
                if self.callback:
                    self.callback(self.value)
                self.update()
            elif action=="up":
                if new_pos>(self.value+self.step):
                    self.value +=self.step
                elif new_pos<(self.value-self.step):
                    self.value -= self.step
                else:
                    self.value = new_pos
                if self.callback:
                    self.callback(self.value)
                self.update()    
        if action in ("up","drag_up"):
            self.pressed = False
            if self.release_callback:
                self.release_callback(self.value)                                

