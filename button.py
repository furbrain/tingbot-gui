import pygame
from .widget import Widget


class Button(Widget):
    """A button widget
    Attributes:
        but_text: text on the widget
        bg_color: background color
        text_color: text color
        active_color: colour of button while being pressed
        callback: function to call when the button is pressed. No arguments taken
    """
    def __init__(self, xy, size, align="center", parent=None, style=None, but_text="OK", callback=None):
        """create a button with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        use style to specify button color, activated button color, text color and font
        but_text: text to display on the button
        callback: a function to be called when the button is pressed
        """
        super(Button,self).__init__(xy,size,align,parent,style)
        self.but_text = but_text
        self.pressed = False
        self.callback = callback
        
    def on_touch(self,xy,action):
        if action=="down":
            self.pressed = True
        elif action=="up":
            self.pressed = False
            if pygame.Rect((0,0),self.size).collidepoint(xy):
                if self.callback:
                    self.callback()
        self.update()
        
    def draw(self):
        if self.pressed:
            self.fill(self.active_color)
        else:
            self.fill(self.bg_color)
        self.text(self.but_text,color=self.text_color)
