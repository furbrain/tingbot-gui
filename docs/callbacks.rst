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
                        max_val = 200,change_callback = slider_callback)
    
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
                      change_callback = lambda x: slider_callback(x,"1"))
    sld2 = gui.Slider((120,150),(230,20),max_val=200,
                      change_callback = lambda x: slider_callback(x,"2"))
    sld3 = gui.Slider((120,190),(230,20),max_val=200,
                      change_callback = lambda x: slider_callback(x,"3"))

For more information about ``lambda`` the `Mouse vs Python blog <http://www.blog.pythonlibrary.org/2010/07/19/the-python-lambda/>`_ is a good summary of the subject.

Full example
------------

Here is a fully worked example with a Button, a ToggleButton, and a ScrollArea containing a slider, 
two checkboxes and three radio buttons

.. code-block:: python    
    :caption: Example: Full worked example
    
    from tingbot import screen,run
    import tingbot_gui as gui

        
    def loop():
        pass    
           
    def print_text(text):       
        screen.rectangle((160,230),(320,20),'black')
        screen.text(text,(160,230),font_size=16)
           
    def slider_cb(value):
        print_text("Slider value: %d" % int(value))

    def value_callback(name,value):
        print_text(name + " value: " + str(value))

    def pressed(name=""):
        print_text("%s pressed" % name)
        

    style = gui.get_default_style()
    style.slider_handle_color="aqua"
    screen.fill(color="black")

    but1 = gui.Button((50,30),(90,50),label="Button",callback=lambda: pressed("Button"))
    but1.update()
    but2 = gui.ToggleButton((150,30),(90,50),label="Toggle",
                            callback = lambda x: value_callback("Toggle Button",x))
    but2.update()

    panel = gui.ScrollArea((0,60),(320,160),align="topleft",canvas_size=(640,240))

    slider = gui.Slider((0,0),(200,20),align="topleft",
                        min_val=100,
                        max_val=200,
                        change_callback=slider_cb,parent=panel.scrolled_area)

    chk1 = gui.CheckBox((0,30),(200,20),align="topleft",
                        parent=panel.scrolled_area, 
                        label="Checkbox 1", 
                        callback = lambda x: value_callback("Checkbox 1",x))
    chk2 = gui.CheckBox((0,60),(200,20),align="topleft",
                        parent=panel.scrolled_area, 
                        label="Checkbox 2", 
                        callback = lambda x: value_callback("Checkbox 2",x))

    group = gui.RadioGroup(callback=value_callback)
    radio1 = gui.RadioButton((0,90),(200,20),align="topleft",
                             parent=panel.scrolled_area,
                             label="Radiobutton 1",
                             value=1,
                             group=group)
    radio2 = gui.RadioButton((0,120),(200,20),align="topleft",
                             parent=panel.scrolled_area,
                             label="Radiobutton 2",
                             value=2,
                             group=group)
    radio3 = gui.RadioButton((0,150),(200,20),align="topleft",
                             parent=panel.scrolled_area,
                             label="Radiobutton 3",
                             value=3,
                             group=group)
                             
    panel.update(downwards=True)
    run(loop)    

