import pygame
from .dialog import ModalWindow
from .scrollarea import ScrollArea
from .button import Button
from .style import get_default_style


class PopupMenu(ModalWindow):

    """A popupmenu"""

    def __init__(self, xy, style=None, cancellable=True,  
                 menu_items=None, button_size=None):
        if style is None:
            style = get_default_style()
        if button_size == None:
            button_size = style.popupmenu_button_size
        list_size = (button_size[0], button_size[1] * len(menu_items))
        #make sure popupmenu is completely within screen area
        menu_window = pygame.Rect(xy,list_size)
        print menu_window
        if list_size[1]>240:
            menu_window.width += style.scrollbar_width
        print menu_window
        
        menu_window.clamp_ip((0,0),(320,240))
        print menu_window
        menu_window = menu_window.clip((0,0),(320,240))
        print menu_window
        
        super(PopupMenu, self).__init__(xy=menu_window.topleft, 
                                        size=menu_window.size, 
                                        align="topleft", style=style,
                                        cancellable=cancellable)
        self.menu_items = menu_items
        #create_scroller
        scroller = ScrollArea(
            (0, 0), size=menu_window.size, align="topleft",
            style=self.style,
            parent=self,
            canvas_size=list_size)

        # populate popupmenu
        for i, (label, item_callback) in enumerate(menu_items):
            but = PopupButton(
                xy=(0, i * self.style.popupmenu_button_size[1]),
                size = button_size,
                align = "topleft",
                parent = scroller.scrolled_area,
                style = self.style,
                label = label,
                callback = self.make_callback(label, item_callback))
        self.update(downwards=True)

    def make_callback(self, label, callback):
        return lambda: self.button_press(label, callback)

    def button_press(self, label, item_callback):
        self.close()
        if item_callback:
            item_callback()


class PopupButton(Button):

    """A button specialised for use in popup menus"""

    def draw(self):
        if self.pressed:
            self.fill(self.style.button_pressed_color)
        else:
            self.fill(self.style.popup_bg_color)
        self.text(self.label,
                  xy=(5, self.size[1] / 2),
                  align = "left",
                  color=self.style.button_text_color,
                  font = self.style.button_text_font,
                  font_size = self.style.button_text_font_size)
