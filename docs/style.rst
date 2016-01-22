.. _Styles:

Styles
======


The appearance of many of the gui components (also known as widgets) are highly configurable.
There are two ways to alter the style of the interface

1. Use the default style. This will affect every single widget, even ones that have already
   been created.
    
   .. code-block:: python    
        :caption: Example: alter the background color to blue for every widget
        
        style = gui.get_default_style()
        style.bg_color = "blue"

2. Use a custom style. This allows you to customize individual widgets or groups of widgets

   .. code-block:: python
        :caption: Example: create two buttons with a smaller font size 
        
        custom_style = gui.Style(button_text_font_size = 12)
        button1 = gui.Button((50,50),(80,80),label="Small text",style=custom_style)
        button2 = gui.Button((150,50),(80,80),label="Small again",style=custom_style)
        button3 = gui.Button((250,50),(80,80),label="OK")
        
   Custom made styles will all inherit the default settings, so you only need to specify
   those items that need to be altered
    
Styles can be updated dynamically, even after the widget has been created

.. py:class:: Style(**kwargs)

    :param \*\*kwargs: specify style attributes as required 
    :returns: A new Style with attributes set as per kwargs, all others are as per default settings

.. py:function:: get_default_style()

    :returns: The default style.
