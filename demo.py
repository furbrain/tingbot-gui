#!/usr/bin/env python
from tingbot import screen, run
from tingbot.graphics import _xy_from_align
import tingbot_gui as gui

print """
Usage instructions for testing:
Click everything!
Remember to test long clicks for buttons, and also moving mouse off button before completing click
Cancel alerts by clicking outside them. Also "cancel the cancel by moving mouse back into alert before releasing
"""
action_text = gui.StaticText((0,220),(320,20),align="topleft",style=gui.Style(bg_color=(30,0,0)))

def cb(name,value=None):
    text = name + " actioned: " +str(value)
    action_text.label = text
    print text
    action_text.update() 

panel_layouts = {'xy':(85,0),
                 'size':(320-85,220),
                 'align':"topleft"}
labels = ('Basics','Slider','Text','Buttons','Dialogs')
notebook_buttons = [gui.ToggleButton((0,30*i),(80,28),align="topleft",label=l) for i,l in enumerate(labels)]

#basic control panel
basic_panel = gui.Panel(**panel_layouts)
gui.CheckBox((0,0),(100,25), align="topleft",
             label="Checkbox",
             parent = basic_panel, 
             callback=lambda x:cb("Checkbox",x))
radio_group = gui.RadioGroup(callback=cb)
gui.RadioButton((0,30),(100,25),align="topleft",
                label="Radio 1", 
                parent = basic_panel, 
                group = radio_group, 
                callback=lambda :cb("Radio Button 1"))
gui.RadioButton((0,60),(100,25),align="topleft",label="Radio 2", parent = basic_panel, group = radio_group)
gui.RadioButton((0,90),(100,25),align="topleft",label="Radio 3", parent = basic_panel, group = radio_group)

#slider panel
slider_panel = gui.Panel(**panel_layouts)
gui.Slider((0,0),(200,30),align="topleft",max_val=100,min_val=40,parent=slider_panel,change_callback = lambda x: cb("Slider H",x))
gui.Slider((0,40),(30,180),align="topleft",parent=slider_panel,change_callback = lambda x: cb("Slider V",x))

#text panel
text_panel = gui.ScrollArea(canvas_size=(300,300),style=gui.Style(bg_color="navy"),**panel_layouts)
positions = ['topleft', 'left', 'bottomleft', 'top', 'center', 'bottom', 'topright', 'right', 'bottomright']
scrollarea = text_panel.scrolled_area
args = [{'xy':_xy_from_align(x,(300,300)),
         'size':(100,50),
         'align':x,
         'text_align':x,
         'label':x} for x in positions]
texts = [gui.StaticText(parent=scrollarea,**a) for a in args]

#button panel
button_panel = gui.Panel(**panel_layouts)
button1 = gui.Button((0,0),(100,25),align="topleft",label="Button 1", 
                     parent = button_panel, callback = lambda: cb("Button 1"), long_click_callback = lambda: cb("Button 1(long"))
button2 = gui.ToggleButton((0,30),(100,25),align="topleft",label="Tog But", 
                            parent = button_panel, callback = lambda x: cb("Toggle Button",x))
dropdown1 = gui.DropDown((0,60),(100,25),align="topleft",
                         parent = button_panel, values = ("DD one",("two","data for item two")),
                         callback = lambda x:cb("DropDown1",x))
dropdown2 = gui.DropDown((0,90),(100,25),align="topleft", 
                         parent = button_panel, values =("DD 2","two","3","4","5","6","7","8","9"),
                         callback = lambda x:cb("DropDown1",x))
dropdown3 = gui.DropDown((0,190),(100,25),align="topleft", 
                         parent = button_panel, values = ("DD 3","two","three","ridiculously long text here"),
                         callback = lambda x:cb("DropDown3",x))

#dialog panel
dialog_panel = gui.Panel(**panel_layouts)

def alert():
    gui.MessageBox(message="Alert triggered",callback = lambda x:cb("Alert dialog",x))
    
def question():
    gui.MessageBox(message="Do you like cheese?",buttons=["Yes","No","Maybe"],callback = lambda x:cb("Question dialog",x))

def popup():
    gui.PopupMenu(xy=(160,120), menu_items = [("File",lambda: cb("File (Popup)")),("Save",lambda: cb("Save (Popup)"))])
    
gui.Button((0,0),(80,25),align="topleft",parent = dialog_panel, label="Alert",callback=alert)
gui.Button((0,30),(80,25),align="topleft",parent = dialog_panel, label="Question",callback=question)
gui.Button((0,60),(80,25),align="topleft",parent = dialog_panel, label="Popup",callback=popup)

notebook_panels = [basic_panel,slider_panel,text_panel,button_panel,dialog_panel]
nb = gui.NoteBook(zip(notebook_buttons,notebook_panels))
gui.get_root_widget().fill('black')
gui.get_root_widget().update(downwards=True)
def loop():
    pass

run(loop)
