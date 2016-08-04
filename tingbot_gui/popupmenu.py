from functools import partial
import pygame
from .dialog import Dialog
from .scrollarea import ScrollArea
from .button import Button
from .style import get_default_style


class PopupMenu(Dialog):

    """A popupmenu that is displayed on top of the screen"""

    def __init__(self, xy, style=None, cancellable=True,  
                 menu_items=None, button_size=None):
        """Create a popupmenu with its top left at position xy
        style specifies the style of the object (default style if None)
        If cancellable is true then the menu can be dismissed by 
            clicking outside of it.
        menu_items is a list of the form [(label,callback)...]
            callback takes no arguments
        button_size is the size for each menu_item (as per style if not
            specified.
        
        If the menu is too big to it on the screen at xy, it will
        be moved so that it does fit. If it is too big to fit on
        the screen at any position it will be given appropriate
        scroll bars
        """
        if style is None:
            style = get_default_style()
        if button_size == None:
            button_size = style.popupmenu_button_size
        list_size = (button_size[0], button_size[1] * len(menu_items))
        #make sure popupmenu is completely within screen area
        menu_window = pygame.Rect(xy,list_size)
        if list_size[1]>240:
            menu_window.width += style.scrollbar_width
        
        menu_window.clamp_ip((0,0),(320,240))
        menu_window = menu_window.clip((0,0),(320,240))
        super(PopupMenu, self).__init__(xy=menu_window.topleft, 
                                        size=menu_window.size, 
                                        align="topleft", style=style,
                                        cancellable=cancellable)
        self.menu_items = menu_items
        #create_scroller
        scroller = ScrollArea(
            (0, 0), size=menu_window.size, align="topleft",
            style=self.style,
            parent=self.panel,
            canvas_size=list_size)

        # populate popupmenu
        button_class = self.style.popupmenu_button_class or PopupButton
        for i, (label, item_callback) in enumerate(menu_items):
            but = button_class(
                xy=(0, i * button_size[1]),
                size = button_size,
                align = "topleft",
                parent = scroller.scrolled_area,
                style = self.style,
                label = label,
                callback = partial(self.button_press, label, item_callback))
        self.update(downwards=True)

    def button_press(self, label, item_callback):
        self.close(label)
        if item_callback:
            item_callback()

def popup_menu(xy, style=None, cancellable=True, menu_items=None, button_size=None):
    return PopupMenu(xy, style, cancellable, menu_items, button_size).run()

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
