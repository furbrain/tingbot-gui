import pygame
from ..input import HitArea
from ..graphics import _xy_subtract,_xy_add
from .widget import Widget
from .slider import Slider
from .util import clamp

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

    def update(self,upwards=True,downwards=False):
        """Call this method to redraw the widget. The widget will only be drawn if visible
        upwards: set to True to ask any parents (and their parents) to redraw themselves
        downwards: set to True to make any children  redraw themselves
        """
        if self.visible:
            if downwards:
                for child in self.children:
                    child.update(upwards=False,downwards=True)
        super(Container,self).update(upwards,downwards)
            

class Panel(Container):
    """Use this class to specify groups of widgets that can be turned on and off together"""
    def draw(self):
        """draw does not need to do anything in Panel"""
        pass

class ScrollArea(Container):
    """Use this class to specify a sub-window with (optional) scrollbars"""
    
    def __init__(self,xy,size,align="center",parent=None,canvas_size=None,vscrollbar=False,hscrollbar=False):
        super(ScrollArea,self).__init__(xy,size,align,parent)
        self.top_surface = self.surface
        self.position = [0,0]
        self.max_position = [max(0,canvas_size[0]-size[0]),max(0,canvas_size[1]-size[1])]
        self.vslider = None
        self.hslider = None
        rect = pygame.Rect(xy,size)
        if vscrollbar:
            self.vslider = Slider(xy = rect.topright, size = (10,size[1]), align = 'topright',parent=parent,change_callback=self.vslider_cb)
            self.vslider.max_val = self.max_position[1]
            self.vslider.value = self.max_position[1]
        if hscrollbar:
            self.hslider = Slider(xy = rect.bottomleft, size = (size[0],10), align = 'bottomleft',parent=parent,change_callback=self.set_x)
            self.hslider.max_val = self.max_position[0]
            self.hslider.value = 0
        self.surface = pygame.Surface(canvas_size,0,self.top_surface)
        
    def update(self,upwards=True,downwards=False):
        """Call this method to redraw the widget. The widget will only be drawn if visible
        upwards: set to True to ask any parents (and their parents) to redraw themselves
        downwards: set to True to make any children  redraw themselves
        """
        super(ScrollArea,self).update(upwards,downwards)
        if self.vslider:
            self.vslider.update(upwards=False)
        if self.hslider:
            self.hslider.update(upwards=False)

    def draw(self):           
        self.top_surface.blit(self.surface,(0,0),pygame.Rect(self.position,self.top_surface.get_size()))

    def on_touch(self,xy,action):
        #translate xy positions to account for canvas position
        super(ScrollArea,self).on_touch(_xy_add(xy,self.position),action)

    def set_x(self,value):
        value = clamp(0,self.max_position[0],int(value))
        self.position[0] = value
        if self.hslider:
            self.hslider.value = value
        self.update()

    def set_y(self,value,inverted=False):
        value = clamp(0,self.max_position[1],int(value))
        self.position[1] = int(value)
        if self.vslider:
            self.vslider.value = self.max_position[1]-value
        self.update()

    def vslider_cb(self,value):
        value = self.max_position[1]-value
        self.set_y(value)
