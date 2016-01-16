import pygame.draw
from tingbot.graphics import _color
from .button import Button
from .dialog import ModalWindow
from .scrollarea import ScrollArea
from .popupmenu import PopupButton

class DropDown(Button):
    """A widget that displays its current value, and shows a pop-up menu when clicked, allowing the
    useer to select a new value from a preset list"""
    
    def __init__(self,xy,size,align="center",parent=None,style=None,values=None,callback=None):
        """ Creates a dropdown with preselected values"""
        super(DropDown,self).__init__(xy,size,align,parent,style,'',callback)
        self.values = []
        for value in values:
            if isinstance(value,basestring):
                self.values.append((value,value))
            elif hasattr(value,"__getitem__"):
                self.values.append(value)
            else:
                self.values.append((value,value))
                    
        self.selected = self.values[0]
        

    def draw(self):
        (w,h) = self.size
        self.draw_button()
        
        self.text(self.selected[0],
                  xy = (5,h/2),
                  align = "left",  
                  color=self.style.button_text_color,
                  font = self.style.button_text_font,
                  font_size = self.style.button_text_font_size)
        triangle_size = self.style.button_text_font_size/2
        triangle_points = ((w-5,(h-triangle_size)/2),
                           (w-5-(triangle_size/2),(h+triangle_size)/2),
                           (w-5-triangle_size,(h-triangle_size)/2))
        pygame.draw.polygon(self.surface, _color(self.style.button_text_color), triangle_points)
        
    def make_cb(self,dlg,label,value):
        #make a callback to attach to a button
        def cb():
            return dlg.close((label,value))
        return cb
            
    def on_click(self):
        #calculate size of dropdown and size of canvas needed
        (w,h) = self.size
        (x,y) = self.get_abs_position()
        list_size = (w,h*len(self.values))
        if list_size[1]>240:
            pos = (x,0)
            size = (min(320,w+self.style.scrollbar_width),240)
        elif list_size[1] > (240-y):
            pos = (x,240-list_size[1])
            size = list_size
        else:
            pos = (x,y)
            size = list_size
            
        self.dlg = ModalWindow(pos,size,align="topleft",style=self.style,callback=self.value_selected)
        scroller = ScrollArea((0,0),size,align="topleft",style=self.style,parent=self.dlg,canvas_size=list_size)
        
        for i in range(len(self.values)):
            button = PopupButton((0,i*h),(w,h),align="topleft",
                                    style=self.style,
                                    label=self.values[i][0],
                                    parent=scroller.scrolled_area,
                                    callback = self.make_cb(self.dlg,self.values[i][0],self.values[i][1]))
        self.dlg.update(downwards=True,upwards=False)
        self.dlg.update()
        
        
    def value_selected(self,value_pair):
        if value_pair:
            self.selected = value_pair
        del self.dlg
        self.update()
        if self.callback:
            self.callback()
        

