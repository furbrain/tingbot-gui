# -*- coding: utf-8 -*-
import pygame
from functools import partial

from .dialog import ModalWindow, MessageBox
from .button import Button
from .container import Panel
from .statictext import StaticText
from .widget import Widget
from tingbot.graphics import _xy_from_align

class KbButton(Button):
    def __init__(self, xy, size, parent, keys, style,):
        super(KbButton,self).__init__(xy,size,"topleft",parent,style)
        self.keys = keys
        
    def draw(self):
        self.label = self.keys[self.parent.layout]
        super(KbButton,self).draw()
        
    def on_click(self):
        self.parent.text.add_letter(self.label)
        
class LayoutButton(KbButton):
    def on_click(self):
        new_layout = self.transitions[self.parent.layout]
        self.parent.set_layout(new_layout)

class ShiftButton(LayoutButton):
    transitions = {0:1,1:0,2:3,3:2}

class AlnumButton(LayoutButton):
    transitions = {0:2,1:2,2:0,3:0}
    
class OkButton(StaticText):
    def on_touch(self, xy, action):
        if action=="up":
            self.parent.close(self.parent.text.string)
        
class CancelButton(StaticText):
    def on_touch(self, xy, action):
        if action=="up":
            self.parent.close(None)
            
class KbText(Widget):
    def __init__(self, xy, size, align, parent, style, text=u""):
        super(KbText,self).__init__(xy, size, align, parent, style)
        self.string = text
        self.cursor_pos = len(text)
        
    def draw(self):
        self.fill(self.style.bg_color)
        self.fill(self.style.keyboard_box_bg_color)
        pygame.draw.rect(self.surface,self.style.keyboard_text_color,self.local_rect,1)
        pos = _xy_from_align('left', self.size)
        pos = (pos[0]+9,pos[1])
        self.offsets = self.text(self.string,
              xy=pos,
              color=self.style.keyboard_text_color,
              align='left',
              font=self.style.keyboard_text_font,
              font_size=self.style.keyboard_text_size)
        x = sum(self.offsets[:self.cursor_pos])+9
        y1 = (self.size[1] - self.style.keyboard_text_size)//2
        y2 = (self.size[1] + self.style.keyboard_text_size)//2
        pygame.draw.line(self.surface,self.style.keyboard_text_color,(x,y1),(x,y2))
                  
    def add_letter(self,letter):
        self.string = self.string+letter
        self.cursor_pos += len(letter)
        self.update()
        
    def del_letter(self):
        if self.cursor_pos > 0:
            self.string  = self.string[:self.cursor_pos-1] + self.string[self.cursor_pos:]
            self.cursor_pos -= 1
            self.update()

                  
class Keyboard(ModalWindow):
    keys = [(u'qwertyuiop', u'asdfghjkl', u'zxcvbnm'), 
            (u'QWERTYUIOP', u'ASDFGHJKL', u'ZXCVBNM'), 
            (u'1234567890', u'-/:;()£&@', u'.,?!\'"`'), 
            (u'[]{}#%^*+=', u'_\|~<>€$¥', u'.,?!\'"·')]
    def __init__(self,title,text=u"",style=None,callback=None):
        super(Keyboard, self).__init__((0,0), (320,240), "topleft", style, callback=callback)
        
        self.text = KbText((7,46), (307,36), 'topleft', self, self.style, text)
        self.layout = 0

        #create all our buttons
        cancel_button = CancelButton((16,23), (60,24), "left", self, self.style, "Cancel", "left")
        ok_button = OkButton((304,23), (60,24), "right", self, self.style, "OK", "right")
        self.title = StaticText((160,23),(160,24),"center",self,self.style,title,"center")
        for row,x,y in zip(zip(*self.keys),(7,22,53),(0,33,66)):
            for i,letter in enumerate(zip(*row)):
                KbButton((x+i*31,105+y),(28,28),self,letter,self.style)
        space_bar = Button((73,105+99),(175,28),"topleft",self,self.style,"space",callback=partial(self.text.add_letter,' '))
        shift = ShiftButton((7,105+66),(34,28),self,"ABCD",self.style)
        alnum = AlnumButton((7,105+99),(61,28),self,"1234",self.style)
        delete = Button((314,105+66),(34,28),"topright",self,self.style,'<',callback=self.text.del_letter)
        enter = Button((314,105+99),(28,28),"topright",self,self.style,'/',callback=self.new_line)
        emoji = Button((253,105+99),(28,28),"topleft",self,self.style,'@',callback=self.emoji)
        self.set_layout(0)
                
    def set_layout(self,layout):    
        self.layout = layout
        self.update(downwards=True)
                
    def add_letter(self,letter):
        print letter
        
    def del_letter(self):
        print "del"
        
    def new_line(self):
        print "NL"
        
    def emoji(self):
        MessageBox(message="Emojiiiiis!")
        
