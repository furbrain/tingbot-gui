import pygame
from tingbot.run_loop import Timer
from tingbot.graphics import Surface, Image, screen, _topleft_from_aligned_xy, _xy_add, _font, _color
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

        if self.is_visible():
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
    
    @property
    def local_rect(self):
        return pygame.Rect((0,0),self.init_size)
        
    def run_loop(self):
        return self.parent.run_loop()
        
    def create_timer(self,action, seconds, repeating=True):
        timer = Timer(action=action, period=seconds, repeating=repeating, next_fire_time=None)
        self.run_loop().schedule(timer)
        return timer
        
    def is_visible(self):
        return self.parent.is_visible() and self.visible
        
    def resurface(self,surface):
        """attach this widget to a new surface (used when a virtual panel changes size)"""
        self.surface = surface.subsurface(self.rect)
        
    def text(self, string, xy=None, size=None, color='grey', align='center', font=None, font_size=32, antialias=None):
        """
        render text to a specific area, will adjust font size to try and fit text into specified size
        returns a list of offsets for each letter
        """
        string = unicode(string)
        if size is None:
            size = self.size
        if antialias is None:
            antialias

        for x in reversed(range(font_size*3/4,font_size)):
            font_obj, antialias= _font(font, x, antialias)
            rendered_size = font_obj.size(string)
            if (size[0]>rendered_size[0]) and (size[1]>rendered_size[1]):
                break
        else: # no break
            # couldn't fit with just font size shrinking. Try clipping and put an ellipsis on the end
            for x in range(3,len(string)):
                temp_string = string[:-x]+u'...'
                rendered_size = font_obj.size(temp_string)
                if (size[0]>rendered_size[0]): #success!
                    string = temp_string
                    break
        text_image = Image(surface=font_obj.render(string, antialias, _color(color)))

        self.image(text_image, xy, align=align)
        if string:
            total = 0
            result = []
            for metric in font_obj.metrics(string):
                total+=metric[4]
                result.append(total)
            return result
        else:
            return []
