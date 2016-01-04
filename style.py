defaults = {
    'bg_color':"black"
}

class Style(object):
    def __init__(self,**kwargs):
        self.__dict__.update(defaults)
        #update based on kwargs, check for invalid args also and throw error
        for arg,value in kwargs.items():
            if arg in defaults:
                self.__dict__[arg] = value
            else:
                raise TypeError("__init__() got an unexpected keyword argument '%s'" % arg)
   
default_style = Style()

def get_default_style():
    return default_style
