import pygame
from tingbot.graphics import Surface, screen, _topleft_from_aligned_xy, _xy_add
from .style import get_default_style


class Widget(Surface):

    def __init__(self, xy, size, align="center", parent=None, style=None):
        """Initialise this widget. It creates it's own subsurface for drawing on
        xy, size and align specify the position of the widget
        if this widget will live in a sub-container, such as ScrollArea, specify this with parent
        otherwise it will be attached to the main screen
        xy is relative to the parent widget (or screen)
        style is an instance of Style to specify the appearance of the widget
        """
        if parent:
            self.parent = parent
        else:
            from .container import get_root_widget
            self.parent = get_root_widget()
        if style:
            self.style = style
        else:
            self.style = get_default_style()
        self.xy = _topleft_from_aligned_xy(xy, align, size, self.parent.size)
        self.visible = True
        self.init_size = size
        self.parent.add_child(self)

    def _create_surface(self):
        return self.parent.surface.subsurface(pygame.Rect(self.xy, self.init_size))

    def _touch(self, xy, action):
        if self.visible:
            self.on_touch(xy, action)

    def on_touch(self, xy, action):
        """Override this method for any widgets that respond to touch events"""
        pass

    def update(self, upwards=True, downwards=False):
        """Call this method to redraw the widget. The widget will only be drawn if visible
        upwards: set to True to ask any parents (and their parents) to redraw themselves
        downwards: set to True to make any children  redraw themselves
        """

        if self.visible:
            self.draw()
        if upwards:
            self.parent.update()
        screen.needs_update = True

    def draw(self):
        """Override this method for all derived widgets"""
        raise NotImplementedError

    def get_abs_position(self):
        return _xy_add(self.parent.get_abs_position(), self.xy)
        
    @property
    def rect(self):
        return pygame.Rect(self.xy,self.init_size)
        
    def resurface(self,surface):
        """attach this widget to a new surface (used when a virtual panel changes size)"""
        self.surface = surface.subsurface(self.rect)
