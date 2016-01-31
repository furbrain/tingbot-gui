from functools import partial

class NoteBook(object):

    """A NoteBook container - this uses a series of toggle button that allows the user
    to select between various views.

    Attributes:
        selected: the currently selected button

    Style Attributes: none
    """

    def __init__(self, pairs, callback=None):
        """Create a notebook
        pairs: a list of the form [(button1,panel1), (button2,panel2)]. The controlled widgets should all occupy the
               same screen real estate
        callback: a callback to be called whenever the selected panel changes. It is passed two arguments, the 
                  newly selected button and the selected panel.

        Example:
            but1 = gui.ToggleButton((30,30),(60,60),label="1")
            but2 = gui.ToggleButton((30,100),(60,60),label="2")
            but3 = gui.ToggleButton((30,170),(60,60),label="3")
            panel1 = gui.Panel((0,70),(320,170))
            panel2 = gui.Panel((0,70),(320,170))
            panel3 = gui.Panel((0,70),(320,170))

            nb = NoteBook([(but1,panel1), (but2,panel2), (but3,panel3)])
        """
        self.pairs = dict(pairs)
        self.callback = callback
        # hide all widgets apart from the first one
        first_but, first_widget = pairs[0]
        first_but.pressed = True
        first_widget.visible = True
        first_widget.update(upwards=False, downwards=True)
        first_but.update()
        self._selected = first_but
        for button, widget in pairs[1:]:
            button.pressed = False
            widget.visible = False

        # set button callbacks
        for button, widget in pairs:
            button.callback = partial(self.button_pressed,button)

    def button_pressed(self, button, dummy):
        self.selected = button

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, button):
        self._selected = button
        for but, widg in self.pairs.items():
            if but == button:
                but.pressed = True
                widg.visible = True
                widg.update(upwards=False, downwards=True)
            else:
                but.pressed = False
                widg.visible = False
                but.update()
        if self.callback:
            self.callback(button,self.pairs[button])
