Widgets
=======

There are several different elements that can be used in an interface, known as widgets

.. py:class:: Widget(xy, size, align = "center", parent = None)

    This is the base class for all other widgets, but should not be directly used. All other widgets
    will have the methods listed below. You can make your own widgets by sub-classing this one. You
    will need to override the draw method, and possibly the on_touch method
        
    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    
    :Attributes:
        - *visible* -- True if the widget is to be displayed. Widget will be hidden if false
        - *surface* -- A pygame surface that corresponds to the widgets area - use this in the draw method
    
    .. py:method:: on_touch(self,xy,action)
        
        Override this method for any widgets that respond to touch events
        
        :param xy: position of the touch
        :param action: one of "up", "down", "move"
        
    .. py:method:: update(self,upwards=True,downwards=False)
    
        Call this method to redraw the widget. The widget will only be drawn if visible
        
        :param upwards: set to True to ask any parents (and their parents) to redraw themselves
        :param downwards: set to True to make any children  redraw themselves
        
    .. py:method:: draw(self)
    
        Called when the widget needs to draw itself. Override this method for all derived widgets    
        
        
.. py:class:: Button(xy, size, align="center", parent=None, style=None, label="OK", callback=None)

    Base: :class:`Widget`

    A simple button control

    :param xy: position that the button will be drawn
    :param size: size of the button
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this button. If None, button will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this button. If None, the button will have the default style
    :param label: Text to display on button
    :param callable callback: function to call when the button is pressed. It should not take any arguments
    
    :Attributes:
        - *label* -- Text to be displayed on the button.
        - *callback* -- Function to be called when button is clicked. No arguments passed. 
          See :ref:`Callbacks` for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *button_color* -- color of this button when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use
    
.. py:class:: ToggleButton(xy, size, align="center", parent=None, style=None, label="OK", callback=None)

    Base: :class:`Widget`

    A button which can be in an on or off state
    
    :param xy: position that the button will be drawn
    :param size: size of the button
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this button. If None, button will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this button. If None, the button will have the default style
    :param label: Text to display on button
    :param callable callback: function to call when the button is pressed. It should accept a single boolean value
    
    :Attributes:
        - *label* -- Text to be displayed on the button.
        - *pressed* -- Current state of the button. True if pressed, False if not
        - *callback* -- Function to be called when button is clicked. A boolean value is passed which is the current state of the button.
          See :ref:`Callbacks` for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *button_color* -- color of this button when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use

.. py:class:: StaticText(xy, size, align="center", parent=None, style=None, label="", text_align="center")

    Base: :class:`Widget`

    A static text control

    :param xy: position that the text widget will be drawn
    :param size: size of the area for text
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this text. If None, text will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this text. If None, the text will have the default style
    :param label: Text to display
    :param text_align: alignment of text within the widget
    
    :Attributes:
         - *label* -- text
         - *text_align* -- alignment of the text

    :Style Attributes:
        - *bg_color* -- background color
        - *statictext_color* -- color to use for text
        - *statictext_font* -- font to use (default)
        - *statictext_font_size* -- font size to use
        
.. py:class:: Slider(xy, size, align = "center", parent = None, style = None, max_val=1.0, min_val=0.0, step = None, change_callback=None)

    Base: :class:`Widget`
    
    A sliding control to allow selection from a range of values
    
    :param xy: position that the slider will be drawn
    :param size: size of the slider
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this slider. If None, slider will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this slider. If None, the slider will have the default style
    :param float max_val: maximum value for the slider
    :param float min_val: minimum value for the slider
    :param step: amount to jump by when clicked outside the slider handle. Defaults to one tenth of ``max_val-min_val``
    :param callable change_callback: function called when the slider is moved. Passed a float which is the sliders new value
    
    :Attributes:
        - *value* -- Current value of the slider
        - *change_callback* -- Function to be called when the slider is moved. A single float is passed. 
          See :ref:`Callbacks` for more information

    :Style Attributes:
        - *bg_color* -- background color
        - *slider_line_color* -- color of the line
        - *slider_handle_color* -- color of the handle

.. py:class:: DropDown(xy, size, align="center", parent=None, style=None, values=None, callback=None)

    Base: :class:`Widget`

    A widget that displays its current value, and shows a pop-up menu when clicked, allowing the
    useer to select a new value from a preset list
    
    :param xy: position that the checkbox will be drawn
    :param size: size of the checkbox
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this checkbox. If None, checkbox will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this checkbox. If None, the checkbox will have the default style
    :param values: a list of (label,data), one for each menu item
    :param callable callback: callback is a function to be called when the selected
                              item is changed. It is passed two arguments, label and data.

    :Attributes:
        - *values* -- a list of (label,data), one for each menu item
        - *selected* -- currently selected menu item as a tuple (label,data)
        - *callback* -- callback is a function to be called when the selected
          item is changed. It is passed two arguments, label and data.
          The label is the new label for the control and data is any
          associated data (if no data was passed in the constructor,
          then data will be None)
            
    :Style Attributes:
        - *bg_color* -- background color
        - *button_color* -- color of this button when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use
        - *popup_bg_color* -- color for the background of the popup

       
.. py:class:: CheckBox(xy, size, align="center", parent=None, style=None, label="OK", callback=None)

    Base: :class:`Widget`

    A checkbox control

    :param xy: position that the checkbox will be drawn
    :param size: size of the checkbox
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this checkbox. If None, checkbox will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this checkbox. If None, the checkbox will have the default style
    :param label: Text to display
    :param callable callback: function to call when the button is pressed. Is passed True if checkbox ticked, False otherwise
    
    :Attributes:
        - *label* -- Text to be displayed.
        - *value* -- Current status of the checkbox - True for checked, False for unchecked
        - *callback* -- Function to be called when the checkbox is clicked. 
          Is passed True if checkbox ticked, False otherwise
          See :ref:`Callbacks` for more information
        
    :Style Attributes:
        - *bg_color* -- background color
        - *checkbox_color* -- color of the checkbox
        - *checkbox_text_color* -- color to use for text
        - *checkbox_text_font* -- font to use (default)
        - *checkbox_text_font_size* -- font size to use


        
Radio Buttons
-------------

Radio buttons are similar to checkboxes, but only one in a group can be selected at any
one time. As they need to be part of a group, a :class:`RadioButton` cannot exist by itself - it
needs to be part of a :class:`RadioGroup`.
        
.. code-block:: python
    :caption: Example: create a set of radiobuttons
    
    group = gui.RadioGroup()
    radio1 = gui.RadioButton((100,80),(200,20),label="Radio 1",value=1,group=group)
    radio2 = gui.RadioButton((100,110),(200,20),label="Radio 2",value=2,group=group)
    radio3 = gui.RadioButton((100,140),(200,20),label="Radio 3",value=3,group=group)

.. py:class:: RadioGroup(callback = None)

    Base: object
    
    A group of RadioButtons
    
    :param callable callback: function to call when one of the radio buttons is pressed. Will be passed
                              two arguments - first is the buttons label, second is it's value
                              
    :Attributes:
        - *selected* -- Currently selected RadioButton
                                  
.. py:class:: RadioButton(xy, size, align="center", parent=None, style=None, label="", value=None, group=None, callback=None)

    Base: :class:`Widget`

    A radio button control

    :param xy: position that the radio button will be drawn
    :param size: size of the radio button
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this radio button. If None, radio button will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this radio button. If None, the radio button will have the default style
    :param label: Text to display
    :param value: Value for this RadioButton, set to label if not specified
    :param RadioGroup group: RadioGroup that this Button will be part of.
    :param callable callback: function to call when the button is pressed. It should not take any arguments
    
    :Attributes:
        - *label* -- text to displayed
        - *value* -- data associated with this radio button
        - *pressed* -- whether this radio button is pressed or not
        - *callback* -- function to call when the radio button is pressed. It should not take any arguments
          See :ref:`Callbacks` for more information
                        
    :Style Attributes:
        - *bg_color* -- background color
        - *radiobutton_color* -- color of the RadioButton
        - *radiobutton_text_color* -- color to use for text
        - *radiobutton_text_font* -- font to use (default)
        - *radiobutton_text_font_size* -- font size to use
       
