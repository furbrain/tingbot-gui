# -*- coding: utf-8 -*-
import pygame

from tingbot.graphics import _xy_from_align

from .keyboard import Keyboard
from .button import Button

class TextEntry(Button):
    """Create a TextEntry - this displays a line of text in a box. Clicking on it fires up a keyboard
    that allows the user to enter text"""
    def __init__(self, xy, size, align="center",
                 parent=None, style=None, label="", string="", callback=None):
        super(TextEntry,self).__init__(xy, size, align, parent, style, label, callback)
        self.string = string
    
    def draw_box(self):
        self.fill(self.style.bg_color)
        self.fill(self.style.textentry_bg_color)
        pygame.draw.rect(self.surface,self.style.textentry_text_color,self.local_rect,1)
    
    
    def draw_text(self,text):
        pos = _xy_from_align('left', self.size)
        pos = (pos[0]+9,pos[1])
        self.text(text,
              xy=pos,
              color=self.style.textentry_text_color,
              align='left',
              font=self.style.textentry_text_font,
              font_size=self.style.textentry_text_size)    

    def draw(self):
        self.draw_box()
        self.draw_text(self.string)
        
    def on_click(self):
        Keyboard(self.label, self.string, self.style, self.text_entered).run()
        
    def text_entered(self,text):
        if text is not None:
            self.string = text
            self.update()
            if self.callback:
                self.callback(text)
                
class PasswordEntry(TextEntry):
    """this displays a line of obfuscated characters, for use when entering passwords"""
    
    def draw(self):
        self.draw_box()
        self.draw_text(u'•'*len(self.string))
    
    def on_click(self):
        Keyboard(self.label, '', self.style, self.text_entered).run()

