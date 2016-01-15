import tingbot
import pygame
from .container import Container

class ModalWindow(Container):
    """A ModalWindow sits on top of the gui and intercepts all events. Useful for alerts, dialog boxes and pop-up menus"""
    def __init__(self,xy,size,align="center",style=None,cancellable=True,callback=None):
        """Create a Modal window with size and position specified by xy, size and align
        If cancellable is True, then can be cancelled by clicking outside of the window
        callback will be called with None if cancelled
        """
        super(ModalWindow,self).__init__(xy,size,align,parent=None,style=style)
        self.callback = callback
        self.cancellable = cancellable
        self.cancelling=False
        tingbot.input.set_modal_handler(self.event_handler)
        ###FIXME###
        #set root widget to invisible
        #grey out whole screen
        tingbot.screen.surface.fill((128,128,128),special_flags=pygame.BLEND_RGBA_SUB)
      
    def event_handler(self,event):
        action=None
        if event.type == pygame.MOUSEBUTTONDOWN:
            action="down"

        elif event.type == pygame.MOUSEMOTION:
            action="move"

        elif event.type == pygame.MOUSEBUTTONUP:
            action="up"
        pos = pygame.mouse.get_pos()
        pos = tingbot.graphics._xy_subtract(pos,self.surface.get_abs_offset())
        self.on_touch(pos,action)
        
    def on_touch(self,pos,action):
        within_widget = pygame.Rect((0,0),self.size).collidepoint(pos)
        if self.cancellable:
            if action=="down" and not within_widget:
                self.cancelling = True
            if action=="up" and self.cancelling:
                if within_widget:
                    self.cancelling=False
                else:
                    self.close()
        super(ModalWindow,self).on_touch(pos,action)
        
    def draw(self):
        pass
        
    def close(self,ret_value=None):
        """Close this modal window and return ret_value"""
        tingbot.input.unset_modal_handler()
        self.visible = False
        tingbot.screen.surface.fill((128,128,128),special_flags=pygame.BLEND_RGBA_ADD)
        if self.callback:
            self.callback(ret_value)
        
