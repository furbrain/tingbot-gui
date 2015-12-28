import pygame
from .widget import Widget


class Button(Widget):
    def __init__(self, xy, size, align="center", parent=None, text="OK", bg_color="blue", text_color="white", active_color="aqua", callback=None):
        """create a button with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        bg_color: background color
        text_color: text color
        active_color: colour of button while being pressed
        callback: a function to be called when the button is pressed
        """
        super(Button,self).__init__(xy,size,align,parent)
        self.but_text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.active_color = active_color
        self.pressed = False
        self.callback = callback
        
    def on_touch(self,xy,action):
        if action=="down":
            self.pressed = True
        elif action=="up":
            self.pressed = False
            if pygame.Rect(self.xy,self.size).collidepoint(xy):
                if self.callback:
                    self.callback()
        self.draw()
        
    def draw(self):
        if self.pressed:
            self.fill(self.active_color)
        else:
            self.fill(self.bg_color)
        self.text(self.but_text,color=self.text_color)
