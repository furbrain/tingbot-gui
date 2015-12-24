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
        if hasattr(self.parent,'touch'):
            self.parent.touch(self.xy,size,"topleft")(self.on_touch)
        else:
            touch(self.xy,self.size,"topleft")(self.on_touch)
            
    def on_touch(self,xy,action):
        """Override this method for any widgets that respond to touch events"""
        pass
        
    def draw(self):
        """Override this method for all derived widgets"""
        raise NotImplementedError
        
