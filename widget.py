import pygame
from ..graphics import Surface,screen,_topleft_from_aligned_xy
from ..input import touch

class Widget(Surface):
    def __init__(self,xy,size,align="center",parent=None):
        """Initialise this widget. It creates it's own subsurface for drawing on
        xy, size and align specify the position of the widget
        if this widget will live in a sub-container, such as ScrollArea, specify this with parent
        otherwise it will be attached to the main screen
        xy is relative to the parent widget (or screen)
        """
        if parent:
            self.parent = parent
        else:
            self.parent = screen
        self.xy = _topleft_from_aligned_xy(xy,align,size,self.parent.size)
        self.surface = self.parent.surface.subsurface(pygame.Rect(self.xy,size))
        self.visible = True
        if hasattr(parent,'touch'):
            parent.touch((0,0),size,"topleft",self)(self._touch)
        else:
            touch((0,0),size,"topleft",self)(self._touch)
            
    def _touch(self):
        if self.visible:
            self.on_touch()
            
    def on_touch(self,xy,action):
        """Override this method for any widgets that respond to touch events"""
        pass
        
    def update(self):
        """call this method to redraw the widget. The widget will only be drawn if visible
        do not override it"""
        if self.visible:
            self.draw()
        
    def draw(self):
        """Override this method for all derived widgets"""
        raise NotImplementedError
        
