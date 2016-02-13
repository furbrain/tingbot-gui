Containers
==========

Containers can be used to group widgets together. ScrollAreas can be used to access more widgets than can fit
on the screen otherwise. 

.. py:class:: Container

    Base: :class:`Widget`

    A base class for ScrollAreas and Panels
    
    .. py:method:: add_child(self,widget)
    
        :param Widget widget: The widget to be added to this container
    
        Adds a widget to this container. This should rarely be called as the widget will call this itself 
        on initiation
        
    .. py:method:: remove_child(self,widget)
    
        :param Widget widget: The widget to be added to this container
        
        Remove a widget from this container
        
    .. py:method:: remove_all(self)
    
        Removes all widgets from the container
        
.. py:class:: Panel(xy, size, align="center", parent=None, style=None)

    Base: :class:`Container`

    Panel class, allows you to collect together various widgets and turn on or off as needed

    :param xy: position that the widget will be drawn
    :param size: size of the widget
    :param align: one of topleft, left, bottomleft, top, center, bottom, topright, right, bottomright
    :param Container parent: container for this widget. If None, widget will be placed directly on the main screen
    :param Style style: :ref:`style <Styles>` for this widget. If None, the widget will have the default style
 

.. py:class:: ScrollArea(xy,size,align="center",parent=None,style = None,canvas_size=None)

    Base: :class:`Container`
    
    ScrollArea gives a viewing area into another, usually larger area. This allows the user to access more
    widgets than will fit on the display. Scrollbars will be added to the bottom or right edges as needed.
    The ScrollArea can be moved by dragging within its area. A fast drag will initiate a "flick" where the
    ScrollArea carries on scrolling after the drag finishes. It will gradually slow and stop, unless it runs
    out of room.

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
        - *scrollarea_flick_decay* -- speed that a flick decreases by in pixels per second per second (default 600)
        - *scrollarea_min_flick_speed* -- speed below which a flick stops in pixels per second (default 60)
        - *scrollarea_flick_threshold* -- speed required to generate a flick in pixels per second (default 100)
        - *slider_handle_color* -- color of the handle

    .. py:method:: resize_canvas(self, canvas_size)
    
        :param canvas_size: size of the scrollable area
        
        Resize the scrollable area. Will raise an error if the given size is smaller than required
        to display all the widgets

    :Example:
        .. code-block:: python
            :caption: Create a scrolled area with a size of (500,500)

                scroller = gui.ScrollArea((100,0),(135,220),align="topleft",canvas_size=(500,500))

.. py:class:: RootWidget()

    Base: :class:`Container`
    
    There is only ever one RootWidget and it is generated automatically. All widgets that do not explicitly have
    a parent set are children of this widget.
    
.. py:function:: get_root_widget()

    Returns the RootWidget
    
.. py:function:: show_all()

    Tells the RootWidget to display all it's children. It's generally useful to call this function
    immediately before calling the main run loop - this ensures that all the children you have added are drawn
    on the screen when the program starts.
    
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


