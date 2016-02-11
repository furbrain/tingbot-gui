.. _Callbacks: 
        
Callbacks
=========

Basic usage
+++++++++++

Several classes use callbacks to respond to user events. The simplest of these take no arguments

.. code-block:: python    
    :caption: Example: respond to a button press
    
    def button_callback():
        screen.text("Button pressed")

    but = gui.Button((40,40),(80,80),label="Button",callback = button_callback)
        
Notice that ``button_callback`` has no brackets when passed to the Button. Other callbacks will take a value dependent on the state of the widget.
For example, the callback for a slider will pass it's current value as a float

.. code-block:: python    
    :caption: Example: display the value of a slider
    
    def slider_callback(value):
        screen.rectangle((0,0),(320,200),"black","topleft")
        screen.text("%d" % int(value))

    slider = gui.Slider((0,200),(320,20),align="topleft",
                        max_val = 200, callback = slider_callback)
    
Passing extra arguments to callbacks
++++++++++++++++++++++++++++++++++++

Sometimes it is useful to pass an extra value to the callback, if you have several widgets, where you want to use
the same callback. This can be done using ``lambda``.

.. code-block:: python    
    :caption: Example: display which button was pressed

    def button_callback(name):
        screen.rectangle((0,80),(320,240),"black","topleft")
        screen.text("Button %s pressed" % name)

    but1 = gui.Button((40,40),(80,80),label="1",callback = lambda : button_callback("1"))
    but2 = gui.Button((130,40),(80,80),label="2",callback = lambda : button_callback("2"))
    but3 = gui.Button((220,40),(80,80),label="3",callback = lambda : button_callback("3"))

If the callback should be passed a value from the widget, then you need to use the form ``lambda x:`` as below.

.. code-block:: python    
    :caption: Example: display which slider has changed

    def slider_callback(value,name):
        screen.rectangle((0,0),(320,100),"black","topleft")
        screen.text("Slider %s: %d" % (name,int(value)),(160,50))

    sld1 = gui.Slider((120,110),(230,20),max_val=200,
                      callback = lambda x: slider_callback(x,"1"))
    sld2 = gui.Slider((120,150),(230,20),max_val=200,
                      callback = lambda x: slider_callback(x,"2"))
    sld3 = gui.Slider((120,190),(230,20),max_val=200,
                      callback = lambda x: slider_callback(x,"3"))

For more information about ``lambda`` the `Mouse vs Python blog <http://www.blog.pythonlibrary.org/2010/07/19/the-python-lambda/>`_ is a good summary of the subject.


