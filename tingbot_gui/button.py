import pygame
from functools import partial

from .widget import Widget
from tingbot.graphics import _color

class Button(Widget):

    """A Button widget
    Attributes:
        label: text on the widget
        callback: function to call when the button is pressed. No arguments taken

    Style Attributes:
        bg_color: background color
        button_inverting: does a square, inverting style of button...
        button_color: color of this button when not pressed
        button_pressed_color: color to use when button pressed
        button_rounding: rounding in pixels of button corners. use 0 for square corners
        button_text_color: color to use for text
        button_text_font: font to use (default)
        button_text_font_size: font size to use
        button_cancel_on_leave: if True (default), cancel a button press if the touch leaves
                                the button before release
    """

    def __init__(self, xy, size, align="center",
                 parent=None, style=None, label="OK", callback=None, long_click_callback=None):
        """create a button with size and position specified by xy, size and align
        it will have parent as a containing widget or will be placed directly on screen if parent is None
        use style to specify button color, activated button color, text color and font
        label: text to display on the button
        callback: a function to be called when the button is pressed
        long_click_callback: a function to be called when the button has been pressed for more than 1.5s
        """
        super(Button, self).__init__(xy, size, align, parent, style)
        self.label = label
        self.pressed = False
        self.callback = callback
        self.long_click_callback=long_click_callback
        self.click_count = 0

    def on_touch(self, xy, action):
        if action == "down":
            self.pressed = True
            self.update()
            if self.long_click_callback:
                self.create_timer(action=partial(self._long_click, self.click_count),
                                  seconds=1.0,
                                  repeating=False)
        elif action in ("up","drag","drag_up") and self.pressed:
            self.click_count += 1
            self.pressed = False
            self.update()
            if action=="up":
                if self.local_rect.collidepoint(xy) or not self.style.button_cancel_on_leave:
                    self.on_click()
        elif action == "move":
            if not self.local_rect.collidepoint(xy):
                self.click_count += 1
                
    def _long_click(self,click_count):
        if self.click_count==click_count:
            # we have been pressed for 1.0 seconds 
            # without a move outside of our box or a button release
            self.on_long_click()

    def on_click(self):
        """function called whenever button is clicked. Can be overriden in sub-classes"""
        if self.callback:
            self.callback()
            
    def on_long_click(self):
        """function called whenever button is long_clicked. Can be overriden in sub-classes"""
        if self.long_click_callback:
            self.pressed=False
            self.update()
            self.long_click_callback()

    def draw_button(self):
        (w, h) = self.size
        two_images = self.label.startswith("image:") and "|"  in self.label
        if self.style.button_inverting:
            if self.pressed and not two_images:
                self.fill(self.style.button_color)
            else:
                self.fill(self.style.bg_color)
                pygame.draw.rect(self.surface, self.style.button_color, [0, 0, w, h], 1)
        else:
            self.fill(self.style.bg_color)
            if self.pressed and not two_images:
                color = self.style.button_pressed_color
            else:
                color = self.style.button_color
            rounding = self.style.button_rounding
            # draw two cross-pieces
            self.surface.fill(
                _color(color), ((rounding, 0), (w - rounding * 2, h)))
            self.surface.fill(
                _color(color), ((0, rounding), (w, h - rounding * 2)))
            # now do circles at the edges
            coords = [(x, y) for x in (rounding, w - rounding)
                      for y in (rounding, h - rounding)]
            for pos in coords:
                pygame.draw.circle(self.surface, _color(color), pos, rounding)
            

    def draw(self):
        self.draw_button()
        if self.label.startswith("image:"):
            if self.pressed and '|' in self.label:
                image = self.label[6:].split("|")[1]
            else:
                image = self.label[6:].split("|")[0] #still works if 
            
            self.image(image)
        else:
            if self.pressed and self.style.button_inverting:
                color = self.style.bg_color
            else:
                color = self.style.button_text_color
            self.text(self.label,
                      color=color,
                      font=self.style.button_text_font,
                      font_size=self.style.button_text_font_size)
            

class ToggleButton(Button):

    """A button widget
    Attributes:
        label: text on the widget
        pressed: whether the button is currently pressed or not
        callback: function to call when the button is pressed. Passes pressed as an argument

    Style Attributes:
        bg_color: background color
        button_color: color of this button when not pressed
        button_pressed_color: color to use when button pressed
        button_rounding: rounding in pixels of button corners. use 0 for square corners
        button_text_color: color to use for text
        button_text_font: font to use (default)
        button_text_font_size: font size to use
        button_cancel_on_leave: if True (default), cancel a button press if the touch leaves
                                the button before release
    """

    def on_touch(self, xy, action):
        if action == "down":
            self.pressed = not self.pressed
        elif action in ("up","drag_up"):
            if (self.local_rect.collidepoint(xy) or not self.style.button_cancel_on_leave) and action=="up":
                if self.callback:
                    self.callback(self.pressed)
            else:
                self.pressed = not self.pressed  # revert to previous state if touch moves out of the button before release
        self.update()
