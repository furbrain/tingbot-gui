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

