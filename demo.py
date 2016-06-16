#!/usr/bin/env python
from tingbot import screen, run
from tingbot.graphics import _xy_from_align
import tingbot_gui as gui

action_text = gui.StaticText((0,220),(320,20),align="topleft",
                             style=gui.Style(bg_color=(30,0,0)))

def cb(name,value=None):
    text = name + " actioned: " +str(value)
    action_text.label = text
    print text
    action_text.update() 

panel_layouts = {'xy':(85,0),
                 'size':(235,220),
                 'align':"topleft"}
labels = ('Basics','Slider','Text','Buttons','Dialogs','Dynamic')
notebook_style = gui.get_default_style().copy()
notebook_style.bg_color = (25,25,25)
notebook_args = {'size':(80,28),'align':"topleft",'style':notebook_style}
notebook_buttons = [gui.ToggleButton((0,30*i),label=l,**notebook_args) 
                    for i,l in enumerate(labels)]

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
gui.RadioButton((0,60),(100,25),align="topleft",
                label="Radio 2",  value="R2 value", 
                parent = basic_panel, group = radio_group)
gui.RadioButton((0,90),(100,25),align="topleft",
                label="Radio 3", 
                parent = basic_panel, group = radio_group)

#slider panel
slider_panel = gui.Panel(**panel_layouts)
gui.Slider((0,0),(200,30),align="topleft",
           max_val=100,min_val=40, step=15, 
           parent=slider_panel,
           callback = lambda x: cb("Slider H",x))
gui.Slider((0,40),(30,180),align="topleft",
           parent=slider_panel,
           callback = lambda x: cb("Slider V",x),
           release_callback = lambda x: cb("Slider V Release",x))

#text panel
text_panel = gui.ScrollArea(canvas_size=(500,500),
                            style=gui.Style(bg_color="navy"),
                            **panel_layouts)
positions = ['topleft', 'left', 'bottomleft', 
             'top', 'center', 'bottom', 
             'topright', 'right', 'bottomright']
scrollarea = text_panel.scrolled_area
args = [{'xy':_xy_from_align(x,(500,500)),
         'size':(80,50),
         'align':x,
         'text_align':x,
         'label':x} for x in positions]
texts = [gui.StaticText(parent=scrollarea,**a) for a in args]

#button panel
button_panel = gui.ScrollArea(canvas_size=panel_layouts['size'],**panel_layouts)
button1 = gui.Button((0,0),(100,25),align="topleft",label="Button 1", 
                     parent = button_panel.scrolled_area, 
                     callback = lambda: cb("Button 1"), 
                     long_click_callback = lambda: cb("Button 1(long"))
button2 = gui.Button((0,30),(100,25),align="topleft",label="image:player_play.png", 
                     parent = button_panel.scrolled_area, 
                     callback = lambda: cb("Button 2(image)")) 
button3 = gui.ToggleButton((0,60),(100,25),align="topleft",label="Tog But", 
                            parent = button_panel.scrolled_area, 
                            callback = lambda x: cb("Toggle Button",x))
dropdown1 = gui.DropDown((0,90),(100,25),align="topleft",
                         parent = button_panel.scrolled_area, 
                         values = ("DD one",("two","data for item two")),
                         callback = lambda x,y:cb("DropDown1",(x,y)))
dropdown2 = gui.DropDown((0,120),(100,25),align="topleft", 
                         parent = button_panel.scrolled_area, 
                         values = range(100),
                         callback = lambda x,y:cb("DropDown1",(x,y)))
dropdown3 = gui.DropDown((0,190),(100,25),align="topleft", 
                         parent = button_panel.scrolled_area, 
                         values = ("DD 3","two",3,"ridiculously long text here"),
                         callback = lambda x,y:cb("DropDown3",(x,y)))

#dialog panel
class DialogDemo(gui.Dialog):
    def __init__(self,transition):
        if transition in ('slide_left','slide_right'):
            size = (150,240)
        if transition in ('slide_up','slide_down'):
            size = (320,150)
        super(DialogDemo,self).__init__(size=size,transition=transition)
        button = gui.Button(xy=(75,75), size=(50,50), label="ok", callback=self.close, parent=self.panel)
   
dialog_panel = gui.Panel(**panel_layouts)

def alert():
    cb("Alert dialog",gui.message_box(message="Alert triggered"))
    
def question():
    gui.MessageBox(message="Do you like cheese?",
                   buttons=["Yes","No","Maybe"],
                   cancellable=False,
                   callback = lambda x:cb("Question dialog",x))

def popup(xy = (160,120)):
    gui.PopupMenu(xy, menu_items = [("File",lambda: cb("File (Popup)")),
                                    ("Save",lambda: cb("Save (Popup)"))])
                                    
def slide_in():
    for x in ['slide_up','slide_left','slide_down','slide_right']:
        cb("Dialog slide",x)
        DialogDemo(x).run()
    
gui.Button((0,0),(80,25),align="topleft",parent = dialog_panel, 
           label="Alert",callback=alert)
gui.Button((0,30),(80,25),align="topleft",parent = dialog_panel, 
           label="Question",callback=question)
gui.Button((0,60),(80,25),align="topleft",parent = dialog_panel, 
           label="Popup",callback=popup)
gui.Button((0,90),(80,25),align="topleft",parent = dialog_panel, 
           label="Popup2",callback=lambda: popup((310,230)))
gui.Button((0,120),(80,25),align="topleft",parent = dialog_panel, 
           label="Slide-ins",callback=slide_in)
gui.TextEntry((0,150),(160,25),align="topleft",parent = dialog_panel,
           label="Text",callback=lambda x: cb("TextEntry",x))
gui.PasswordEntry((0,180),(160,25),align="topleft",parent = dialog_panel,
           label="Text",callback=lambda x: cb("PasswordEntry",x))

#dynamic list panel
dynamic_panel = gui.Panel(**panel_layouts)
scroller = gui.ScrollArea((100,0),(135,220),align="topleft",
                          parent=dynamic_panel,canvas_size=(135,75))

def make_button(index,pos,text="Dynamic"):
    label = text + ' ' + str(index)
    button = gui.PopupButton((0,pos*25),(135,25),align="topleft",
                             parent = scroller.scrolled_area,
                             label = label,
                             callback = lambda: cb(label))
    return button                         

button_list = [make_button(i,i,"Original") for i in range(3)]
count = 3

def add_item():
    global count
    cb("Add dynamic item",count)
    scroller.resize_canvas((135,(len(button_list)+1)*25))
    button_list.append(make_button(count,len(button_list)))
    count += 1
    scroller.update(downwards=True)

def remove_last_item():
    cb("Remove dynamic item",'last')
    if button_list:
        scroller.scrolled_area.remove_child(button_list.pop())
        scroller.resize_canvas((135,max(len(button_list)*25,10)))
        scroller.update(downwards=True)
    
def remove_all():
    cb("Remove dynamic items",'all')
    scroller.scrolled_area.remove_all()
    scroller.resize_canvas((135,10))
    button_list[:] = []
    scroller.update(downwards=True)

gui.Button((0,0),(90,25),align="topleft",parent=dynamic_panel,
           label="Add item",callback=add_item)
gui.Button((0,30),(90,25),align="topleft",parent=dynamic_panel,
           label="Del last",callback=remove_last_item)
gui.Button((0,60),(90,25),align="topleft",parent=dynamic_panel,
           label="Del all",callback=remove_all)


def nb_cb(button,panel):
    print "Notebook panel changed: " +button.label

notebook_panels = [basic_panel,slider_panel,text_panel,
                   button_panel,dialog_panel,dynamic_panel]
nb = gui.NoteBook(zip(notebook_buttons,notebook_panels),callback = nb_cb)
print "Current notebook tab: " + nb.selected.label

gui.get_root_widget().fill(notebook_style.bg_color)
gui.show_all()
def loop():
    pass

run(loop)
