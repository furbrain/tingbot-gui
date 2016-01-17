from .dialog import ModalWindow
from .button import Button
from .style import get_default_style


class PopupMenu(ModalWindow):

    """A popupmenu"""

    def __init__(self, xy, align="center", style=None,
                 cancellable=True, callback=None, menu_items=None):
        if style is None:
            style = get_default_style()
        size = (
            style.popupmenu_button_size[0],
            style.popupmenu_button_size[1] * len(menu_items))
        super(
            PopupMenu,
            self).__init__(
            xy,
            size,
            align,
            style,
            cancellable,
            callback)
        self.menu_items = menu_items

        # populate popupmenu
        for i, (label, callback) in enumerate(menu_items):
            but = PopupButton(
                xy=(0, i * self.style.popupmenu_button_size[1]),
                size = self.style.popupmenu_button_size,
                align = "topleft",
                parent = self,
                style = self.style,
                label = label,
                callback = self.make_callback(label, callback))
        self.update(downwards=True)

    def make_callback(self, label, callback):
        return lambda: self.button_press(label, callback)

    def button_press(self, label, callback):
        self.close()
        if callback:
            callback()
        if self.callback:
            self.callback(label)


class PopupButton(Button):

    """A button specialised for use in popup menus"""

    def draw(self):
        if self.pressed:
            self.fill(self.style.button_pressed_color)
        else:
            self.fill(self.style.dropdown_bg_color)
        self.text(self.label,
                  xy=(5, self.size[1] / 2),
                  align = "left",
                  color=self.style.button_text_color,
                  font = self.style.button_text_font,
                  font_size = self.style.button_text_font_size)
