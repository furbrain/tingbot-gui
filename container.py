import pygame
from .widget import Widget
from ..input import HitArea
from ..graphics import _xy_subtract

class Container(Widget):
    """This is a base class for both Panels and ScrollAreas
    This implements container which can hold and keep track of other widgets and allows you
    to easily draw or hide all contained widgets and also manageds any incoming inputs"""
    def __init__(self,xy,size,align="center",parent=None):
        """Initialise this container. It creates it's own subsurface for drawing on
        xy, size and align specify the position of the widget
        if this widget will live in a sub-container, such as ScrollArea, specify this with parent
        otherwise it will be attached to the main screen
        xy is relative to the parent widget (or screen)
        """
        super(Container,self).__init__(xy,size,align,parent)
        self.children = []
        self.hit_areas = []
        self.active_hit_areas = []
        
    def register(self,widget):
        self.children.append(widget)
        
    def touch(self,widget):
        offset = widget.surface.get_offset()
        rect = pygame.Rect(offset,widget.size)
        self.hit_areas.append(HitArea(rect,widget._touch))

    def on_touch(self,xy,action):
        """distribute touch events to relevant widgets, offset relative to each widget"""
        if action=='down':
            for hit_area in self.hit_areas:
                if hit_area.rect.collidepoint(xy):
                    self.active_hit_areas.append(hit_area)
                    pos = _xy_subtract(xy,hit_area.rect.topleft)
                    hit_area.callback(pos,'down')
        elif action in ('move','up'):
            for hit_area in self.active_hit_areas:
                pos = _xy_subtract(xy,hit_area.rect.topleft)
                hit_area.callback(pos, action)
        if action=='up':
            self.active_hit_areas[:] = []

    def update(self):
        if self.visible:
            for child in self.children:
                child.update()

class Panel(Container):
    """Use this class to specify groups of widgets that can be turned on and off together"""
    pass

