# -*- coding: utf-8 -*-
import pygame

from tingbot.graphics import _xy_from_align

from .keyboard import Keyboard
from .button import Button

class TextEntry(Button):
    """Create a TextEntry - this displays a line of text in a box. Clicking on it fires up a keyboard
    that allows the user to enter text"""
    def __init__(self, xy, size, align="center",
                 parent=None, style=None, label="", text="", callback=None):
        super(TextEntry,self).__init__(xy, size, align, parent, style, label, callback)
        self.string = text
    
    def draw_box(self):
        self.fill(self.style.bg_color)
        self.fill(self.style.keyboard_box_bg_color)
        pygame.draw.rect(self.surface,self.style.keyboard_text_color,self.local_rect,1)
    
    
    def draw_text(self):
        pos = _xy_from_align('left', self.size)
        pos = (pos[0]+9,pos[1])
        self.text(self.string,
              xy=pos,
              color=self.style.keyboard_text_color,
              align='left',
              font=self.style.keyboard_text_font,
              font_size=self.style.keyboard_text_size)    

    def draw(self):
        self.draw_box()
        self.draw_text()
        
    def on_click(self):
        Keyboard(self.label, self.string, self.style, self.text_entered)
        
    def text_entered(self,text):
        if text is not None:
            self.string = text
            self.update()
            if self.callback:
                self.callback(text)
                
class PasswordEntry(TextEntry):
    """this displays a line of obfuscated characters, for use when entering passwords"""
    
    def draw_text(self):
        pos = _xy_from_align('left', self.size)
        pos = (pos[0]+9,pos[1])
        self.text(u'•'*len(self.string),
              xy=pos,
              color=self.style.keyboard_text_color,
              align='left',
              font=self.style.keyboard_text_font,
              font_size=self.style.keyboard_text_size)    

    def on_click(self):
        Keyboard(self.label, '', self.style, self.text_entered)

