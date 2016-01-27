#!/usr/bin/env python
import tingbot_gui as gui

def test_exception(exception,code):
    try:
        code()
    except exception:
        pass
    else: #pragma: no cover - should not reach here
        raise Exception("Should have raised " + repr(exception))

def test_bad_radiobutton():
    #must provide a RadioGroup
    gui.RadioButton((0,0),(100,30),align="topleft",label="bad_boy")

def test_bad_scrollarea():
    #must provide a canvas_size
    gui.ScrollArea((0,0),(100,30),align="topleft")
    
def test_bad_style():
    #can only use known attributes
    style = gui.Style(bad_attribute=12,align="topleft")
    

def run_tests():
    widget = gui.Widget((0,0),(100,30),align="topleft")
    scroller = gui.ScrollArea((100,100),(100,100),align="topleft",canvas_size=(80,30))
    button = gui.Button((0,0),(80,30),align="topleft",parent = scroller.scrolled_area,label="Ok")
    
    test_exception(ValueError,test_bad_radiobutton)
    test_exception(ValueError,test_bad_scrollarea)
    test_exception(TypeError,test_bad_style)
    test_exception(NotImplementedError,widget.draw)
    test_exception(ValueError,lambda: scroller.resize_canvas((80,29)))
    test_exception(ValueError,lambda: scroller.resize_canvas((79,30)))
    
if __name__=="__main__":
    run_tests()
