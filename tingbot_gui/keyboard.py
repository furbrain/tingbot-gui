# -*- coding: utf-8 -*-
import os
from functools import partial

import pygame

from .dialog import Dialog, message_box
from .button import Button
from .container import Panel
from .statictext import StaticText
from .widget import Widget
from tingbot.graphics import _xy_from_align

def get_image_location(name,inverted=False):
    directory = os.path.dirname(__file__)
    text = "image:"
    if inverted:
        text += os.path.join(directory,'images',name)+"_inv.png"
        text += "|"
        text += os.path.join(directory,'images',name)+".png"
    else:
        text += os.path.join(directory,'images',name)+".png"
        text += "|"
        text += os.path.join(directory,'images',name)+"_inv.png"
    return text
    

class KbButton(Button):
    def __init__(self, xy, size, parent, keys, style):
        super(KbButton,self).__init__(xy,size,"topleft",parent,style)
        self.style = style.copy()
        self.style.button_cancel_on_leave = False
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
    """A widget to display text with a cursor"""
    def __init__(self, xy, size, align, parent, style, text=u""):
        super(KbText,self).__init__(xy, size, align, parent, style)
        self.string = text
        self.cursor_pos = len(text)
        
    def draw(self):
        self.fill(self.style.bg_color)
        self.fill(self.style.textentry_bg_color)
        pygame.draw.rect(self.surface,self.style.textentry_text_color,self.local_rect,1)
        pos = _xy_from_align('left', self.size)
        pos = (pos[0]+9,pos[1])
        self.offsets = self.text(self.string,
              xy=pos,
              color=self.style.textentry_text_color,
              align='left',
              font=self.style.textentry_text_font,
              font_size=self.style.textentry_text_size)    
        if self.cursor_pos:
            x = self.offsets[self.cursor_pos-1]+9
        else:
            x = 9
        y1 = (self.size[1] - self.style.textentry_text_size)//2
        y2 = (self.size[1] + self.style.textentry_text_size)//2
        pygame.draw.line(self.surface,self.style.textentry_text_color,(x,y1),(x,y2))
                  
    def add_letter(self,letter):
        self.string = self.string[:self.cursor_pos]+letter+self.string[self.cursor_pos:]
        self.cursor_pos += len(letter)
        self.update()
        
    def del_letter(self):
        if self.cursor_pos > 0:
            self.string  = self.string[:self.cursor_pos-1] + self.string[self.cursor_pos:]
            self.cursor_pos -= 1
            self.update()
            
    def on_touch(self, xy, action):
        x = xy[0]
        for i,offset in enumerate(self.offsets):
            if (x-9) < offset:
                self.cursor_pos=i
                break
            else:
                self.cursor_pos = len(self.string)
        self.update()

                  
class KeyboardPanel(Panel):
    keys = [(u'qwertyuiop', u'asdfghjkl', u'zxcvbnm'), 
            (u'QWERTYUIOP', u'ASDFGHJKL', u'ZXCVBNM'), 
            (u'1234567890', u'-/:;()£&@', u'.,?!\'"`'), 
            (u'[]{}#%^*+=', u'_\|~<>€$¥', u'.,?!\'"·')]
    def __init__(self,label,text=u"", parent=None, style=None):
        super(KeyboardPanel, self).__init__((0,0), (320,240), "topleft", parent, style)
        self.text = KbText((7,46), (307,36), 'topleft', self, self.style, text)
        self.layout = 0
        #find image files
        shift_images = get_image_location("shift")
        inverted_shift_images = get_image_location("shift", inverted=True)
        del_images = get_image_location("del")
        enter_images = get_image_location("enter")
        smiley_images = get_image_location("smiley")
        style14 = self.style.copy(button_text_font_size=14)
        style13 = self.style.copy(button_text_font_size=13)
        style12 = self.style.copy(button_text_font_size=12, statictext_font_size=12)
        
        #create all our buttons
        cancel_button = CancelButton((16,23), (60,24), "left", self, style12, "Cancel", "left")
        ok_button = OkButton((304,23), (60,24), "right", self, style12, "OK", "right")
        self.title = StaticText((160,23),(160,24),"center",self,style12,label,"center")
        for row,x,y in zip(zip(*self.keys),(7,22,53),(0,33,66)):
            for i,letter in enumerate(zip(*row)):
                KbButton((x+i*31,105+y),(28,28),self,letter,style14)
        space_bar = Button((73,105+99),(175,28),"topleft",self,style13,"space",callback=partial(self.text.add_letter,' '))
        shift_labels = [shift_images, inverted_shift_images, u'#+=', u'123']
        shift = ShiftButton((7,105+66),(34,28),self,shift_labels,style13)
        alnum = AlnumButton((7,105+99),(61,28),self,['@123','@123','abc','abc'],style13)
        delete = Button((314,105+66),(34,28),"topright",self,self.style,del_images,callback=self.text.del_letter)
        enter = Button((314,105+99),(28,28),"topright",self,self.style,enter_images,callback=self.new_line)
        emoji = Button((253,105+99),(28,28),"topleft",self,self.style,smiley_images,callback=self.emoji)
        self.set_layout(0)
                
    def set_layout(self,layout):    
        self.layout = layout
        self.update(downwards=True)
                
    def new_line(self):
        self.close(self.text.string)
        
    def emoji(self):
        message_box(message="Sorry, no emoji's yet")
        
    def close(self,value=None):
        self.parent.close(value)
        
class Keyboard(Dialog):
    def __init__(self, label, text=u"", style=None, callback=None):
        super(Keyboard, self).__init__((0,0), (320,240), "topleft", style, callback=callback)
        panel = KeyboardPanel(label, text, self, style)
        
def show_keyboard(label, text=u"", style=None):
    return Keyboard(label,text,style).run()
        
