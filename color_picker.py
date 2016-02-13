from tingbot import screen, run
import tingbot_gui as gui

#all the rest of the code goes here
red = gui.Slider((190,20),(25,150),align="top",max_val=255)
green = gui.Slider((240,20),(25,150),align="top",max_val=255)
blue = gui.Slider((290,20),(25,150),align="top",max_val=255)
 
def display():
   color = (int(red.value),int(green.value),int(blue.value))
   screen.rectangle((20,20),(120,150),color,align="topleft")
   gui.MessageBox(message="HTML code is #%02X%02X%02X" % color)
   
button = gui.Button((240,200),(80,30),align="top",label="Display",callback=display)  

gui.StaticText((190,0),(50,20),align="top",label="Red")
gui.StaticText((240,0),(50,20),align="top",label="Green")
gui.StaticText((290,0),(50,20),align="top",label="Blue")

red_label = gui.StaticText((190,180),(50,20),label="0")
green_label = gui.StaticText((240,180),(50,20),label="0")
blue_label = gui.StaticText((290,180),(50,20),label="0")

def update_label(label,value):
    label.label = str(int(value))
    label.update()
   
red.callback = lambda x: update_label(red_label,x)    
green.callback = lambda x: update_label(green_label,x)    
blue.callback = lambda x: update_label(blue_label,x)    


def loop():
   pass
   
screen.fill("black")
gui.get_root_widget().update(downwards=True)    
run(loop)

