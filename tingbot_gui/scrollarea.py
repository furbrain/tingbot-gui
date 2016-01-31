import math
import pygame

from .container import Panel, Container
from .slider import Slider
from .util import clamp
from tingbot.graphics import _xy_subtract, _xy_add


class VirtualPanel(Panel):

    """This class implements a virtual panel"""

    def __init__(self, size, parent, style):
        super(VirtualPanel, self).__init__((0, 0), size, "topleft", parent, style)
        self.init_size = size

    def _create_surface(self):
        return pygame.Surface(self.init_size, 0, self.parent.surface)

    def get_abs_position(self):
        if hasattr(self.parent, "position"):
            return _xy_subtract(self.parent.get_abs_position(), self.parent.position)
        else: #pragma: no cover can't think of any way to test this currently
            super(VirtualPanel, self).get_abs_position()


class ViewPort(Container):

    """the viewport is a container that only has one child, a VirtualPanel"""

    def __init__(self, xy, size, align="center", parent=None, style=None,
                 canvas_size=None, vslider=None, hslider=None):
        super(ViewPort, self).__init__(xy, size, align, parent, style)
        self.panel = VirtualPanel(canvas_size, self, style)
        self.resize_canvas(canvas_size)
        self.set_sliders(vslider,hslider)
        self.dragging = False
        
    def distance(self,a,b):
        """return a distance between two points, but only consider an axis if there is
        a corresponding slider"""
        if self.vslider:
            if self.hslider:
                return math.hypot(a[0]-b[0],a[1]-b[1])
            else:
                return abs(a[1]-b[1])
        elif self.hslider:
            return abs(a[0]-b[1])
        else:
            return 0
            
    def set_sliders(self, vslider, hslider):
        self.vslider = vslider
        self.hslider = hslider
        if self.vslider:
            self.vslider.max_val = self.max_position[1]
            self.vslider.value = self.max_position[1]
            self.vslider.change_callback = self.vslider_cb
        if self.hslider:
            self.hslider.max_val = self.max_position[0]
            self.hslider.change_callback = self.set_x

    def resize_canvas(self,canvas_size):
        self.position = [0, 0]
        self.max_position = [
            max(0, canvas_size[0] - self.init_size[0]), max(0, canvas_size[1] - self.init_size[1])]
        self.panel.resize(canvas_size)
    
    def set_x(self, value):
        value = clamp(0, self.max_position[0], int(value))
        self.position[0] = value
        if self.hslider:
            self.hslider.value = value
        self.update()

    def set_y(self, value):
        value = clamp(0, self.max_position[1], int(value))
        self.position[1] = int(value)
        if self.vslider:
            self.vslider.value = self.max_position[1] - value
        self.update()

    def vslider_cb(self, value):
        value = self.max_position[1] - value
        self.set_y(value)

    def on_touch(self, xy, action):
        if action=="down":
            self.drag_origin = xy
        if action=="move":
            if self.dragging:
                if self.hslider:
                    self.set_x(self.drag_offset[0]-xy[0])
                if self.vslider:
                    self.set_y(self.drag_offset[1]-xy[1])
                action="drag"
            else:
                if self.distance(xy,self.drag_origin)>15:
                    self.dragging=True
                    self.drag_offset = _xy_add(self.position,self.drag_origin)
        if action in ("up","drag_up"):
            if self.dragging:
                action="drag_up"
                self.dragging = False               
        # translate xy positions to account for panel position, and pass on to
        # the panel for processing
        self.panel.on_touch(_xy_add(xy, self.position), action)

    def draw(self):
        self.fill(self.style.bg_color)
        self.surface.blit(self.panel.surface, (0,0), pygame.Rect(self.position, self.size))

    def resize(self,size):
        """resize this container to the specified size"""
        self.init_size = size
        self.surface = self._create_surface()
             

class ScrollArea(Container):

    """Use this class to specify a sub-window with (optional) scrollbars
    style: specify the style of your sliders
    canvas_size: specify the size of the underlying window

    Style Attributes:
        scrollbar_width: width of the scrollbars
        slider_line_color: color of the line
        slider_handle_color: color of the handle
    """

    def __init__(self, xy, size, align="center",
                 parent=None, style=None, canvas_size=None):
        if canvas_size is None:
            raise ValueError("canvas_size must be specified")
        super(ScrollArea, self).__init__(xy, size, align, parent, style)
        self.vslider = None
        self.hslider = None
        self.viewport = ViewPort((0, 0), size,
                                 align=align,
                                 parent=self,
                                 style=self.style,
                                 canvas_size=canvas_size,
                                 vslider=self.vslider,
                                 hslider=self.hslider)
        self.resize_canvas(canvas_size)

    def resize_canvas(self, canvas_size):
        """creates vertical and horizontal sliders if needed"""
        rect = pygame.Rect((0, 0), self.size)
        vscrollbar = False
        hscrollbar = False
        if canvas_size[0] > rect.right:
            rect.height -= self.style.scrollbar_width
            hscrollbar = True
        if canvas_size[1] > rect.bottom:
            rect.width -= self.style.scrollbar_width
            vscrollbar = True
        if canvas_size[0] > rect.right and not hscrollbar:
            rect.height -= self.style.scrollbar_width
            hscrollbar = True
        if vscrollbar and not self.vslider:
            self.vslider = Slider(
                xy=rect.topright,
                size=(
                    self.style.scrollbar_width,
                    rect.bottom),
                align = 'topleft',
                parent=self,
                style=self.style)
        elif self.vslider and not vscrollbar:
            self.remove_child(self.vslider)
            self.vslider = None
        if hscrollbar and not self.hslider:
            self.hslider = Slider(
                xy=rect.bottomleft,
                size=(rect.right,
                      self.style.scrollbar_width),
                align = 'topleft',
                parent=self,
                style=self.style)
        elif self.hslider and not hscrollbar:
            self.remove_child(self.hslider)
            self.hslider = None
        self.viewport.resize(rect.size)
        self.viewport.resize_canvas(canvas_size)
        self.viewport.set_sliders(self.vslider,self.hslider)
        self.update(downwards=True)
        
    def update(self, upwards=True, downwards=False):
        """Call this method to redraw the widget. The widget will only be drawn if visible
        upwards: set to True to ask any parents (and their parents) to redraw themselves
        downwards: set to True to make any children  redraw themselves
        """
        super(ScrollArea, self).update(upwards, downwards)
        if self.visible:
            if self.vslider:
                self.vslider.update(upwards=False)
            if self.hslider:
                self.hslider.update(upwards=False)

    def draw(self):
        # all drawing functions are provided by this classes children
        pass

    @property
    def scrolled_area(self):
        return self.viewport.panel
