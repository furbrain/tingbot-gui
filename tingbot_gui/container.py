import pygame
from tingbot.input import HitArea, touch
from tingbot.graphics import _xy_subtract, screen
from tingbot import main_run_loop
from .style import get_default_style
from .widget import Widget


class Container(Widget):

    """This is a base class for both Panels and ScrollAreas
    This implements container which can hold and keep track of other widgets and allows you
    to easily draw or hide all contained widgets and also manageds any incoming inputs"""

    def __init__(self, xy, size, align="center", parent=None, style=None):
        """Initialise this container. It creates it's own subsurface for drawing on
        xy, size and align specify the position of the widget
        style specifies any look and appearance needed
        if this widget will live in a sub-container, such as ScrollArea, specify this with parent
        otherwise it will be attached to the main screen
        xy is relative to the parent widget (or screen)
        """
        super(Container, self).__init__(xy, size, align, parent, style)
        self.children = []
        self.hit_areas = []
        self.active_hit_areas = []

    def add_child(self, widget):
        """Add a child widget to this container"""
        self.children.append(widget)
        offset = widget.surface.get_offset()
        rect = pygame.Rect(offset, widget.size)
        self.hit_areas.append(HitArea(rect, widget._touch))

    def remove_child(self, widget):
        """Remove a specified child from this widget"""
        self.hit_areas[:] = [
            x for x in self.hit_areas if x.callback.__self__ is not widget]
        self.active_hit_areas[:] = [
            x for x in self.active_hit_areas if x.callback.__self__ is not widget]
        self.children.remove(widget)

    def remove_all(self):
        """Remove all children from this widget"""
        self.children[:] = []
        self.hit_areas[:] = []

    def on_touch(self, xy, action):
        """distribute touch events to relevant widgets, offset relative to each widget"""
        if action == 'down':
            for hit_area in self.hit_areas:
                if hit_area.rect.collidepoint(xy):
                    self.active_hit_areas.append(hit_area)
                    pos = _xy_subtract(xy, hit_area.rect.topleft)
                    hit_area.callback(pos, 'down')
        elif action in ('move', 'drag', 'up', 'drag_up'):
            for hit_area in self.active_hit_areas:
                pos = _xy_subtract(xy, hit_area.rect.topleft)
                hit_area.callback(pos, action)
        if action in ('up','drag_up'):
            self.active_hit_areas[:] = []

    def update(self, upwards=True, downwards=False):
        """Call this method to redraw the widget. The widget will only be drawn if visible
        upwards: set to True to ask any parents (and their parents) to redraw themselves
        downwards: set to True to make any children  redraw themselves
        """
        if self.is_visible():
            if downwards:
                for child in self.children:
                    child.update(upwards=False, downwards=True)
            self.draw()
        if upwards:
            self.parent.update()
            
    def resize(self,size):
        """resize this container to the specified size
        will raise an error if this would cut off any child widgets"""
        #check we can safely resize...
        child_rects = [x.rect for x in self.children]
        all_widgets = pygame.Rect(0,0,0,0).unionall(child_rects)
        if not pygame.Rect((0,0),size).contains(all_widgets):
            raise ValueError("resized container would be smaller than child widgets"+repr(size)+repr(all_widgets))
        self.init_size = size
        self.surface = self._create_surface()
        for child in self.children:
            child.resurface(self.surface)

class Panel(Container):

    """Use this class to specify groups of widgets that can be turned on and off together

    Style Attributes:
        bg_color: background color"""

    def draw(self):
        """ no action needed on draw"""
        pass

    def update(self, upwards=True, downwards=False):
        # clear contents before drawing
        if self.is_visible() and downwards:
            self.fill(self.style.bg_color)
        super(Panel, self).update(upwards, downwards)


class RootWidget(Container):

    def __init__(self):
        self.children = []
        self.hit_areas = []
        self.active_hit_areas = []
        self.xy = (0, 0)
        self.init_size = (320, 240)
        self.visible = True
        self.style = get_default_style()
        touch((0, 0), (320, 240), "topleft")(self._touch)

    def _create_surface(self):
        return screen.surface

    def draw(self):
        pass

    def is_visible(self):   
        return self.visible
    
    def run_loop(self):
        return main_run_loop
        
    def update(self, upwards=True, downwards=False):
        if self.visible:
            if downwards:
                for child in self.children:
                    child.update(upwards=False, downwards=True)
            self.draw()

    def get_abs_position(self):
        return (0, 0)
        
    


root = RootWidget()


def get_root_widget():
    return root
