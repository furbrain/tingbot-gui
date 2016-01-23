Containers
==========

Containers can be used to group widgets together. ScrollAreas can be used to access more widgets than can fit
on the screen otherwise. 

.. py:class:: Container

    Base: :class:`Widget`

    A base class for ScrollAreas and Panels
    
    .. py:method: add_child(self,widget)
    
        :param Widget widget: The widget to be added to this container
    
        Adds a widget to this container. This should rarely be called as the widget will call this itself 
        on initiation
        
    .. py:method: remove_child(self,widget)
    
        :param Widget widget: The widget to be added to this container
        
        Remove a widget from this container
        
    .. py:method: remove_all(self)
    
        Removes all widgets from the container
        
.. py:class:: Panel

    Base: :class:`Container`

    Panel class, allows you to collect together various widgets and turn on or off as needed

.. py:class:: ScrollArea(xy,size,align="center",parent=None,style = None,canvas_size=None)

    Base: :class:`Container`
    
    ScrollArea gives a viewing area into another, usually larger area. This allows the user to access more
    widgets than will fit on the display. Scrollbars will be added to the bottom or right edges as needed.

    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
    :param canvas_size: size of the scrollable area (required)
    
    :Attributes:
        - *scrolled_area* -- Use this as the parent for any widgets you wish to place within this container
 
    :Style Attributes:
        - *scrollbar_width* -- width of the scrollbars
        - *slider_line_color* -- color of the line
        - *slider_handle_color* -- color of the handle

.. py:class:: NoteBook(pairs)

    Base: object
    
    A NoteBook allows you to control a set of Panels with a set of ToggleButtons. Set all of the panels to cover the
    same area, and pressing each button will make the associated panel visible, and hide the others. ScrollAreas can
    also be used.
    
    :param pairs: a list of the form [(button1,panel1), (button2,panel2) ...]. panel1,panel2 etc should all occupy the
                  same screen real estate, whereas button1,button2 should be in distinct locations.
                  
    .. code-block:: python
        :caption: Example: create three panels and buttons and use them to create a NoteBook

        but1 = gui.ToggleButton((30,30),(60,60),label="1")
        but2 = gui.ToggleButton((30,100),(60,60),label="2")
        but3 = gui.ToggleButton((30,170),(60,60),label="3")
        panel1 = gui.Panel((0,70),(320,170))
        panel2 = gui.Panel((0,70),(320,170))
        panel3 = gui.Panel((0,70),(320,170))

        nb = NoteBook([(but1,panel1), (but2,panel2), (but3,panel3)])


