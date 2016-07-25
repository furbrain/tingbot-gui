from functools import partial

import pygame.draw
from tingbot.graphics import _color
from .button import Button
from .popupmenu import PopupMenu


class DropDown(Button):

    """A widget that displays its current value, and shows a pop-up menu when clicked, allowing the
    useer to select a new value from a preset list
    
    Attributes:
        values: a list of (label,data), one for each menu item
        selected: currently selected menu item as a tuple (label,data)
        callback: callback is a function to be called when the selected
            item is changed. It is passed two arguments label and data.
            The label is the new label for the control and data is any
            associated data (if no data was passed in the constructor,
            then data will be None)
            
    Style Attributes:
        bg_color
        button_color
        button_pressed_color
        button_text_color
        button_text_font
        button_text_font_size
        popup_bg_color
    """    
    def __init__(self, xy, size, align="center",
                 parent=None, style=None, values=None, callback=None):
        """ create a DropDown control with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        use style to specify it's appearance
        values is a list of labels with optional associated data items
        callback is a function to be called when the selected item is changed. It is passed two arguments
            label and data. The label is the new label for the control and data is any associated data
            (if no data was passed in the constructor, then data will be None) """
        super(DropDown, self).__init__(xy, size, align, parent,
                                       style, '', callback)
        self.values = []
        for value in values:
            if isinstance(value, basestring):
                self.values.append((value, None))
            elif hasattr(value, "__getitem__"):
                self.values.append(value)
            else:
                self.values.append((value, None))
        self.selected = self.values[0]

    def draw(self):
        (w, h) = self.size
        self.draw_button()
        triangle_size = self.style.button_text_font_size / 2
        self.text(self.selected[0],
                  xy=(5, h / 2),
                  size = (w-10-triangle_size,h),
                  align="left",
                  color=self.style.button_text_color,
                  font=self.style.button_text_font,
                  font_size=self.style.button_text_font_size)
        triangle_points = ((w-5, (h-triangle_size) / 2),
                           (w - 5 - triangle_size/2, (h+triangle_size) / 2),
                           (w - 5 - triangle_size, (h-triangle_size) / 2))
        pygame.draw.polygon(self.surface,
                            _color(self.style.button_text_color),
                            triangle_points)


    def on_click(self):
        # calculate size of dropdown and size of canvas needed
        items = [(label, partial(self.value_selected,(label,value))) for label,value in self.values]
        menu = PopupMenu(self.get_abs_position(), style=self.style, menu_items=items, button_size=self.size).run()

    def value_selected(self, value_pair):
        if value_pair:
            self.selected = value_pair
        self.update()
        if self.callback:
            self.callback(value_pair[0],value_pair[1])
