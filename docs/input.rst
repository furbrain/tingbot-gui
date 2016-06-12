Input
=====

There are two widgets that can be used to enter text, and one dialog

.. py:class:: Keyboard(label, text="", style=None, callback=None)

    Base: :class:`ModalWindow`
    
    This dialog box allows you to enter text using an on-screen keyboard. It has
    lower case, upper case, number and symbols screen. There is a button to add emojis,
    but it is not currently functional
    
    :param label: Text to display at the top of the dialog e.g. "Username"
    :param text: Text to put in the box for editing e.g. "JohnSmith4001"
    :param Style style: :ref:`style <Styles>` for this keyboard. If None, the keyboard will have the default style
    :param callable callback: Function to call when the keyboard is exited. It will be passed a single variable
                              which is the completed string (or None if cancel is pressed)

    :Attributes:
        - *callback* -- Function to call when the keyboard is exited. It will be passed a single variable
          which is the completed string (or None if cancel is pressed). See :ref:`Callbacks` for more information
    
    :Style Attributes:
        - *bg_color* -- background color
        - *textentry_bg_color* -- color of text entry box
        - *textentry_text_color* -- color to use for text
        - *textentry_text_font* -- font to use (default)
        - *textentry_text_font_size* -- font size to use
        - *button_color* -- color of the buttons when not pressed
        - *button_inverting* -- if True, the buttons will use bg_color for text and button_text_color for background
          when pressed. If False, will use button_pressed_color as background color when pressed
        - *button_pressed_color* -- color to use when buttons pressed
        - *button_rounding* -- rounding in pixels of button corners when button_inverting is False. use 0 for square corners
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *statictext_color* -- color to use for text at top of screen (i.e. Cancel, Title, Ok)
        - *statictext_font* -- font to use (default)
        - *statictext_font_size* -- font size to use

    :Example:
        .. code-block:: python

            def cb(text):
                print text

            Keyboard("Text", "Happy World!", callback=cb)


        .. image:: images/Keyboard.png
        
.. py:class:: TextEntry(xy, size, align="center", parent=None, style=None, label="", text="", callback=None)

    Base: :class:`Button`
    
    A Text entry widget - shows as a box with text inside it. Clicking on the box will bring up a keyboard to
    enter new text.

    :param xy: position that the TextEntry will be drawn
    :param size: size of the TextEntry
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this TextEntry. If None, TextEntry will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this TextEntry. If None, the TextEntry will have the default style
    :param label: title for the Keyboard when it is shown
    :param string: text to display in the TextEntry
    :param callable callback: Function to call when the string is changed. It will be passed a single variable
                              which is the new string.
                              
    :Attributes:
        - *label* -- title for the Keyboard when it is shown
        - *string* -- current text of the TextEntry
        - *callback* -- Function to call when the string is changed. It will be passed a single variable
          which is the new string. See :ref:`Callbacks` for more information
          
    :Style Attributes:
        - *bg_color* -- background color
        - *textentry_bg_color* -- color of TextEntry box
        - *textentry_text_color* -- color to use for text
        - *textentry_text_font* -- font to use (default)
        - *textentry_text_font_size* -- font size to use
        
.. py:class:: PasswordEntry(xy, size, align="center", parent=None, style=None, label="", text="", callback=None)

    Base: :class:`TextEntry`
    
    A Password entry widget - shows as a box with a series of dots (•) inside it. Clicking on the box will bring up a keyboard to
    enter new text (but the current text will not be displayed). Ideal for where you don't want a passerby to see any passwords.

    :param xy: position that the TextEntry will be drawn
    :param size: size of the TextEntry
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this TextEntry. If None, TextEntry will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this TextEntry. If None, the TextEntry will have the default style
    :param label: title for the Keyboard when it is shown
    :param string: text to display in the TextEntry
    :param callable callback: Function to call when the string is changed. It will be passed a single variable
                              which is the new string.
                              
    :Attributes:
        - *label* -- title for the Keyboard when it is shown
        - *string* -- current text of the TextEntry
        - *callback* -- Function to call when the string is changed. It will be passed a single variable
          which is the new string. See :ref:`Callbacks` for more information
          
    :Style Attributes:
        - *bg_color* -- background color
        - *textentry_bg_color* -- color of TextEntry box
        - *textentry_text_color* -- color to use for text
        - *textentry_text_font* -- font to use (default)
        - *textentry_text_font_size* -- font size to use
        
    

   

