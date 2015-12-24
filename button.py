import pygame
from .widget import Widget


class Button(Widget):
    def __init__(self, xy, size, align="center", parent=None, text="OK", bg_color="black", text_color="white", active_color="red", callback=None):
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
