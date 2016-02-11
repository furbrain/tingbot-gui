.. tingbot documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Tingbot GUI's documentation!
=======================================

Contents:

.. toctree::
   :maxdepth: 2

   widgets
   containers
   dialogs
   style
   callbacks
   example
   
   
Graphical user interface
========================

This module provides a graphical user interface for the `tingbot <http://tingbot.com>`_.
It allows you to include some of the commoner elements (also known as widgets) of your phone or computer 
interface within your application, rather than having to develop them from scratch.

Getting Started
===============
Let's build a simple application to get started - a colour [#]_ picker. Any colour can be described with three
numbers - red, green and blue [#]_ , so we're going to have three sliders, and a button to display the chosen colour. 


Setup
-----

So first of all lets import all the relevant libraries

.. code-block:: python    

   from tingbot import screen, run
   import tingbot_gui as gui
   
   #all the rest of the code goes here
   
   def loop():
       pass
   
   screen.fill("black")
   gui.get_root_widget().update(downwards=True)    
   run(loop)

This imports the ``tingbot_gui`` library and renames it ``gui`` to simplify the typing. We create an (empty) run loop,
and set the whole system going. The second to last line ensures that all of the widgets added
All the rest of the code below should be inserted just below the line that states
``#all the rest of the code goes here``

Add some sliders
----------------

Lets add some sliders to allow the user to select the individual colour elements. We'll put these on the
right hand side of the screen

.. code-block:: python

   red = gui.Slider((190,20),(25,150),align="top",max_val=255)
   green = gui.Slider((240,20),(25,150),align="top",max_val=255)
   blue = gui.Slider((290,20),(25,150),align="top",max_val=255)
   
This adds three sliders, one for each colour. We set their position with first pair of numbers, and the size within
the second pair. The ``align="top`` means that the red slider is positioned with the middle of its top border
at (180,20).

Add a button
------------

Now we need to make something happen. Let's add a button, and also create a callback to display the chosen
color when it is pressed

.. code-block:: python

   def display():
       color = (int(red.value),int(green.value),int(blue.value))
       screen.rectangle((20,20),(100,100),color,align="topleft")
       
   button = gui.Button((240,200),(80,30),align="top",label="Display",callback=display)  

This creates a function ``display`` which creates a color with values determined by the value of each of the sliders.
We use ``int`` to ensure that the values are integers. ``screen.rectangle`` draws the selected colour on the screen.
The last line creates a button labelled "Display", and tells it to call the ``display`` function when it is 
pressed. Note that there is no pair of brackets in the reference to ``display``. This means that the *function itself*
is passed to the Button. If we put ``callback=display()`` then the result of the function would be passed (which would be None).
At this point you will be able to get your colour picker up and running, but it's not very pretty...

Add some labels
---------------

It's not obvious which slider is red, green or blue, so lets add some labels next

.. code-block:: python

    gui.StaticText((190,0),(50,20),align="top",label="Red")
    gui.StaticText((240,0),(50,20),align="top",label="Green")
    gui.StaticText((290,0),(50,20),align="top",label="Blue")

Again we have used the "top" alignment - this allows us to make sure that all the labels
are correctly centered. StaticText will automatically centre its label unless you tell it
otherwise. Note that we have not assigned these labels to variables. Because we are not
going to do anything more with these labels, we can just declare them.

Add some clever labels with lambda
----------------------------------

Lets finally add some numbers to each slider to reflect it's current value.

.. code-block:: python

   red_label = gui.StaticText((190,180),(50,20),label="0")
   green_label = gui.StaticText((240,180),(50,20),label="0")
   blue_label = gui.StaticText((290,180),(50,20),label="0")

   def update_label(label,value):
       label.label = str(int(value))
       
   red.change_callback = lambda x: update_label(red_label,x)    
   green.change_callback = lambda x: update_label(green_label,x)    
   blue.change_callback = lambda x: update_label(blue_label,x)    
   
First of all we create some more labels - ``red_label, ``green_label`` and ``blue_label``, and
we next take a function ``update_label`` that takes a label and a value and sets that label
to display that value as an integer.

Finally we use a special keyword ``lambda``. This creates a temporary function, as if we had written

.. code-block:: python

   def temp_func(x):
       return update_label(red_label,x)
       
See the section on :ref:`Callbacks` for more on how to use callbacks and lambda.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. rubric:: Footnotes

.. [#] I'm English, so I use the english spelling of *colour*. However, historically the majority of software was
       written in the USA, so in software, the standard is to spell it *color*.
.. [#] Actually there are several ways of specifying a colour, many of which are better than simple red
       green and blue. However, red green and blue is simplest, so we'll stick with that for this example.
       See the Wikipedia entry on `color spaces <http://en.wikipedia.org/wiki/Color_space>`_ for more detail
       than you can possibly want.
