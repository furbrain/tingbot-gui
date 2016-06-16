Dialog windows
==============

Dialog windows are modal - this means that only the specified window is active while it is open
This is particularly useful for alert boxes and also pop-up menus

.. py:class:: Dialog(xy=None, size=None, align="center", style=None, \
                          buttons=None, message="", cancellable=True, callback=None)

    Base: :class:`Container`

    Dialog is a base class you can use to create your own dialogs. You will need to
    override the draw method. Call close to make the dialog disappear

    :param xy: position that the dialog will be drawn
    :param size: size of the dialog
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Style style: :ref:`style <Styles>` for this dialog. If None, the dialog will have the default style
    :param bool cancellable: If true, then the dialog can be closed by clicking outside its area. Any callback
                             specified will be passed None as it's argument
    :param callable callback: A callback that will be called when the dialog is closed, one argument is
                              passed, which is whatever the close method is called with.
    
    :Attributes:
        - *cancellable* -- If true, then the dialog can be closed by clicking outside its area. Any callback
          specified will be passed None as it's argument
        - *callback* -- A callback that will be called when the dialog is closed, one argument is
          passed, which is whatever the close method is called with. See :ref:`Callbacks` for more
          
 
    :Style Attributes:
        - *scrollbar_width* -- width of the scrollbars
        - *slider_line_color* -- color of the line
        - *slider_handle_color* -- color of the handle

    .. py:method:: close(self, ret_value=None)
        
        :param ret_value: value to be returned to the callback function

        Close this modal window and return ret_value to the callback function



.. py:class:: MessageBox(xy=None, size=None, align="center", style=None,\
                         buttons=None, message="", cancellable=True, callback=None)

    Base: :class:`Dialog`

    A MessageBox allows you to alert the user to simple events, and also ask simple Yes/No type questions
    
    :param xy: position that the dialog will be drawn (in the centre if None)
    :param size: size of the dialog, (280x200 if None)
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Style style: :ref:`style <Styles>` for this MessageBox. If None, the MessageBox will have the default style
    :param buttons: A list of labels for buttons to be shown. Three can be displayed with the default window size
                     and button size. Defaults to ["OK"] if None
    :param string message: Text to display in the MessageBox
    :param bool cancellable: If true, then the MessageBox can be closed by clicking outside its area. Any callback
                             specified will be passed None as it's argument
    :param callable callback: A callback that will be called when the MessageBox is closed, one argument is
                              passed, which is the label of the button that was pressed (or None if cancelled)
                     
    :Attributes:
        - *cancellable* -- If true, then the MessageBox can be closed by clicking outside its area. Any callback
          specified will be passed None as it's argument
        - *callback* -- A callback that will be called when the MessageBox is closed, one argument is
          passed, which is the label of the button that was pressed (or None if cancelled) See :ref:`Callbacks` for more

    :Style Attribute:
        - *bg_color* -- background color
        - *button_color* -- color of buttons when not pressed
        - *button_pressed_color* -- color to use when button pressed
        - *button_rounding* -- rounding in pixels of button corners. use 0 for square corners
        - *button_text_color* -- color to use for button text
        - *button_text_font* -- font to use (default font if None)
        - *button_text_font_size* -- font size to use
        - *messagebox_button_size* -- size to use for buttons
        - *statictext_color* -- color to use for message text
        - *statictext_font* -- font to use (default font if None)
        - *statictext_font_size* -- font size to use

    :Example:
        .. code-block:: python
            :caption: Find out if the user likes cheese

                def cb(name,value=None):
                    print name, value

                gui.MessageBox(message="Do you like cheese?",
                               buttons=["Yes","No","Maybe"],
                               cancellable=False,
                               callback = lambda x:cb("Cheese?",x))
    
.. py:class:: PopupMenu(xy, style=None, cancellable=True, menu_items=None, button_size=None)

    Base: :class:`Dialog`
    
    A PopupMenu (also known as a context menu) allows you to present the user with a menu 
    
    :param xy: position for the topleft of the menu. However, the menu may be adjusted so that it fits
               on the screen. If the menu is so long that it cannot fit on the screen, a scrollbar 
               will be provided
    :param Style style: :ref:`style <Styles>` for this PopupMenu. If None, the PopupMenu will have the default style
    :param bool cancellable: If true, then the PopupMenu can be closed by clicking outside its area.
    :param menu_items: is a list of the form [(label,callback)...], one for each entry in the menu. 
                       callback takes no arguments and will be called if that menu item selected.
    :param button_size: a size parameter for each button in the popupmenu. If none, button_size will be taken
                        from the style.
                     
    :Attributes:
        None                 
                        
    :Style Attributes:
        - *bg_color* -- background color
        - *button_pressed_color* -- color to use when menu item pressed
        - *button_text_color* -- color to use for text
        - *button_text_font* -- font to use (default)
        - *button_text_font_size* -- font size to use
        - *popup_bg_color* -- color for the background of the popup
        - *popupmenu_button_size* -- default size for the menu items
        
    :Example:
        .. code-block:: python
            :caption: Bring up a Popup prompting to Open or Save

                def open_fn():
                    print "open"
                    
                def save_fn():
                    print "save"
                    
                gui.PopupMenu((160,100), menu_items = [("Open",open_fn), ("Save",save_fn)])
                        
