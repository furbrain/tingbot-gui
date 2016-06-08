# -*- coding: utf-8 -*-
from functools import partial
from .dialog import ModalWindow
from .button import Button
from .container import Panel

class KbButton(Button):
    def __init__(self, xy, size, parent, keys, style):
        super(KbButton,self).__init__(xy,size,"topleft",parent,style)
        self.keys = keys
        
    def draw(self):
        self.label = self.keys[self.parent.layout]
        super(KbButton,self).draw()
        
    def on_click(self):
        self.parent.add_letter(self.label)

class Keyboard(ModalWindow):
    keys = [(u'qwertyuiop', u'asdfghjkl', u'zxcvbnm'), 
            (u'QWERTYUIOP', u'ASDFGHJKL', u'ZXCVBNM'), 
            (u'1234567890', u'-/:;()£&@', u'.,?!\'"`'), 
            (u'[]{}#%^*+=', u'_\|~<>€$¥', u'.,?!\'"·')]
    def __init__(self,title,text="",style=None,callback=None):
        super(Keyboard, self).__init__((0,0), (320,240), "topleft", style, callback=callback)
        self.title = title
        self.text = text
        self.layout = 0
        self.panels = [Panel((0,105),(320,135),"topleft",self,self.style) for x in range(4)]
        for row,x,y in zip(zip(*self.keys),(7,22,53),(0,33,66)):
            for i,letter in enumerate(zip(*row)):
                print i,letter
                KbButton((x+i*31,105+y),(28,28),self,letter,self.style)
        self.set_layout(3)
                
    def set_layout(self,layout):    
        self.layout = layout
        self.update(downwards=True)
                
    def add_letter(self,letter):
        print letter
        
    def draw(self):
        for panel in self.panels:
            panel.draw()
        
