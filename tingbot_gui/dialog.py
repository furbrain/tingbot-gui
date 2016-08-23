from functools import partial

import tingbot
import pygame
import pdb
import math
from .container import Container, get_root_widget, Panel

from .scrollarea import VirtualPanel
from .statictext import StaticText
from .button import Button


class Dialog(Container,tingbot.input.EventHandler):

    """A Dialog sits on top of the gui and intercepts all events. Useful for alerts, dialog boxes and pop-up menus"""

    def __init__(self, xy=None, size=None, align="center",
                 style=None, cancellable=True, callback=None, transition="popup"):
        """Create a Dialog with size and position specified by xy, size and align
        If cancellable is True, then can be cancelled by clicking outside of the window
        callback will be called with None if cancelled
        if transition is popup, then the window will appear according to xy and size
        if transition if slide_left or slide_right then it will slide in from the specified side;
            height must be the height of the screen
        if transition if slide_up or slide_down then it will slide in from the specified side;
            width must be the width of the screen
        """
        if xy == None:
            xy = (160,120)
        if size == None:
            size = (320,240)
        super(Dialog, self).__init__(
            (160,120), (320,240), "center", parent=None, style=style)
        self.callback = callback
        self.cancellable = cancellable
        self.cancelling = False
        self.blocking = False
        self.return_value = None
        self.transition = transition
        self._run_loop = tingbot.RunLoop(event_handler=self)
        #make copy of screen
        self.screen_copy = tingbot.screen.surface.copy()
        if transition=="popup":
            # grey out whole screen
            tingbot.screen.surface.fill(
                (128, 128, 128), special_flags=pygame.BLEND_RGBA_SUB)
            self.panel = Panel(xy,size,align,self,style)
        else:
            #some kind of animation
            self.panel = VirtualPanel(size,self,style)
            self.bg_pos = [0,0]
            if transition=="slide_down":
                self.panel_pos = [0,-size[1]]
            elif transition=="slide_up":
                self.panel_pos = [0,240]
            elif transition=="slide_right":
                self.panel_pos = [-size[0],0]
            elif transition=="slide_left":
                self.panel_pos = [320,0]
            self.animate_timer = self.create_timer(self.animate,seconds=1/30.0)
              
    def touch_handler(self, event):
        action = None
        if event.type == pygame.MOUSEBUTTONDOWN:
            action = "down"

        elif event.type == pygame.MOUSEMOTION:
            action = "move"

        elif event.type == pygame.MOUSEBUTTONUP:
            action = "up"
        pos = pygame.mouse.get_pos()
        pos = tingbot.graphics._xy_subtract(pos, self.surface.get_abs_offset())
        self.on_touch(pos, action)

    def on_touch(self, pos, action):
        if self.transition=="popup":
            rect = self.panel.rect
        else:
            rect = pygame.Rect(self.panel_pos,self.panel.size)
        within_widget = rect.collidepoint(pos)
        if self.cancellable:
            if action == "down" and not within_widget:
                self.cancelling = True
            if action == "up" and self.cancelling:
                if within_widget:
                    self.cancelling = False
                else:
                    self.close(None)
        if self.transition=="popup":
            super(Dialog, self).on_touch(pos, action)
        else:
            pos = tingbot.graphics._xy_subtract(pos, self.panel_pos)
            self.panel.on_touch(pos,action)                   

    def animation_easing(self, number, towards):
        '''
        Returns the amount to change 'number' for a frame of animation. If animation should
        stop, return 0.
        '''
        change = int(towards - number) * 0.15

        # always round away from zero to prevent the animation getting stuck when fractional
        # changes are calculated
        if change > 0:
            return math.ceil(change)
        else:
            return math.floor(change)

    def animate(self):
        if self.transition=="slide_down":
            change = self.animation_easing(self.panel_pos[1], towards=0)
            self.panel_pos[1] += change
            self.bg_pos[1] += change
        elif self.transition=="slide_up":
            change = self.animation_easing(self.panel_pos[1] + self.panel.size[1], towards=240)
            self.panel_pos[1] += change
            self.bg_pos[1] += change
        elif self.transition=="slide_right":
            change = self.animation_easing(self.panel_pos[0], towards=0)
            self.panel_pos[0] += change
            self.bg_pos[0] += change
        elif self.transition=="slide_left":
            change = self.animation_easing(self.panel_pos[0] + self.panel.size[0], towards=320)
            self.panel_pos[0] += change
            self.bg_pos[0] += change
        if change==0:
            self.animate_timer.stop()

        self.update()

    def deanimate(self):
        if self.transition=="slide_down":
            change = self.animation_easing(self.bg_pos[1], towards=0)
            self.panel_pos[1] += change
            self.bg_pos[1] += change
        elif self.transition=="slide_up":
            change = self.animation_easing(self.bg_pos[1], towards=0)
            self.panel_pos[1] += change
            self.bg_pos[1] += change
        elif self.transition=="slide_right":
            change = self.animation_easing(self.bg_pos[0], towards=0)
            self.panel_pos[0] += change
            self.bg_pos[0] += change
        elif self.transition=="slide_left":
            change = self.animation_easing(self.bg_pos[0], towards=0)
            self.panel_pos[0] += change
            self.bg_pos[0] += change
        self.update()
        if change==0:
            self.deanimate_timer.stop()
            self.close_final()
        
    def draw(self):
        if self.transition=="popup":
            return
        else:
            self.surface.blit(self.panel.surface,self.panel_pos)
            self.surface.blit(self.screen_copy,self.bg_pos)
            
            tingbot.screen.needs_update = True
        
    def run(self):
        self.blocking=True
        self.update(downwards=True)
        self._run_loop.run()
        return self.return_value

    def close(self, ret_value=None):
        """Close this dialog and return ret_value"""
        self.return_value = ret_value
        #restore old appearance of screen
        if self.transition == "popup":
            tingbot.screen.surface.blit(self.screen_copy,(0,0))
            self.close_final()
        else:
            self.animate_timer.stop()
            self.deanimate_timer = self.create_timer(self.deanimate,seconds=0.02)
            
    def close_final(self):
        self.visible = False
        get_root_widget().update(downwards=True)
        if self.callback:
            self.callback(self.return_value)
        if self.blocking:
            self._run_loop.stop()
            
    def run_loop(self):
        return self._run_loop


class MessageBox(Dialog):

    """A simple message box for alerting the user"""

    def __init__(self, xy=None, size=None, align="center", style=None,
                 buttons=None, message="", cancellable=True, callback=None):
        if xy is None:
            xy = (160, 120)
        if size is None:
            size = (280, 200)
        if buttons is None:
            buttons = ['Ok']
        super(MessageBox, self).__init__(
            xy, size, align, style, cancellable, callback)
        (w, h) = size
        text = StaticText(xy=(w / 2, h / 4),
                          size = (w, h / 2),
                          label=message,
                          parent=self.panel)
        but_size = self.style.messagebox_button_size
        button_offset = (w - (len(buttons) - 1) * (but_size[0] + 5)) / 2
        for (i, label) in enumerate(buttons):
            button = Button(
                xy=(button_offset + i * (but_size[0] + 5), h * 3 / 4),
                size=but_size,
                align="center",
                label=label,
                parent=self.panel)

            button.callback = partial(self.close,label)
        
def message_box(xy=None, size=None, align="center", style=None,
                 buttons=None, message="", cancellable=True):
    return MessageBox(xy,size,align,style,buttons,message,cancellable).run()
