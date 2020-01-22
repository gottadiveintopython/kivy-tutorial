__all__ = ('KTIcon', 'KTButton', 'KTIconButton', 'KTTightLabel', 'KTTightButton', )

from kivy.properties import StringProperty, ColorProperty, NumericProperty
from kivy.lang import Builder
from kivy.factory import Factory

import trio

from kivy_tutorial.triouser import TrioUser
from kivy_tutorial.soundplayer import global_instance as soundplayer


KV_CODE = '''
#:import md_icons kivymd.icon_definitions.md_icons

<KTTightLabel@Label>:
    size_hint: None, None
    width: self.texture_size[0] + dp(10)
    height: self.texture_size[1] + dp(10)

<KTIcon>:
    font_name: 'Icon'
    text: md_icons.get(self.icon, '')

<KTButton>:
    outline_width: 2
    outline_color: 1, 1, 1, 1
    color: 0, 0, 0, 1
    font_size: max(sp(15), 30)
    canvas.before:
        PushMatrix:
        Scale:
            origin: self.center
            x: self._scaling
            y: self._scaling
        Color:
            rgba: self._border_color
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.background_color
        Rectangle:
            pos: self.x + dp(4), self.y + dp(4)
            size: self.width - dp(8), self.height - dp(8)
        PopMatrix:

<KTTightButton@KTButton>:
    size_hint: None, None
    width: self.texture_size[0] + dp(10)
    height: self.texture_size[1] + dp(10)

<KTIconButton>:
    font_name: 'Icon'
    text: md_icons.get(self.icon, '')
    font_size: max(sp(20), 40)
    size_hint: None, None
    width: max(sp(30), 60)
    height: max(sp(30), 60)
    canvas.before:
        Clear:
        PushMatrix:
        Scale:
            origin: self.center
            x: self._scaling
            y: self._scaling
        Color:
            rgba: self._border_color
        Ellipse:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.background_color
        Ellipse:
            pos: self.x + dp(4), self.y + dp(4)
            size: self.width - dp(8), self.height - dp(8)
        PopMatrix:
'''
Builder.load_string(KV_CODE)


class KTIcon(Factory.Label):
    icon = StringProperty()


class KTButton(TrioUser, Factory.Label):
    __events__ = ('on_press', 'on_release', )
    border_color = ColorProperty('#444444')
    border_color2 = ColorProperty('#AAAAAA')
    background_color = ColorProperty('#999933')
    sound = StringProperty('button.ogg')
    _border_color = ColorProperty(border_color.defaultvalue)
    _scaling = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.nursery.start_soon(self._trio_main)

    def on_press(self):
        if self.sound:
            soundplayer.play(self.sound)

    def on_release(self):
        pass

    async def _trio_main(self):
        import trio
        import asynckivy
        try:
            coro = self._asynckivy_main()
            asynckivy.start(coro)
            await trio.sleep_forever()
        finally:
            coro.close()

    async def _asynckivy_main(self):
        import asynckivy
        from asynckivy import animation, or_, event
        
        coro_blink = None
        current_touch = None
        try:
            while True:
                __, current_touch = await event(
                    self, 'on_touch_down',
                    filter=lambda w, t: w.collide_point(*t.opos) and not t.is_mouse_scrolling,
                    return_value=True,
                )
                self.dispatch('on_press')
                current_touch.grab(self)
                coro_blink = self._blink()
                asynckivy.start(coro_blink)
                await event(self, 'on_touch_up',
                    filter=lambda w, t: t is current_touch and t.grab_current is w,
                    return_value=True,
                )
                coro_blink.close()
                current_touch.ungrab(self)
                if self.collide_point(*current_touch.pos):
                    self.dispatch('on_release')
                    await animation(self, _scaling=.8, d=.05)
                    await animation(self, _scaling=1, d=.05)
        finally:
            if coro_blink is not None:
                coro_blink.close()
            if current_touch is not None:
                current_touch.ungrab(self)


    async def _blink(self):
        from asynckivy import sleep
        try:
            while True:
                await sleep(.1)
                self._border_color = self.border_color2
                await sleep(.1)
                self._border_color = self.border_color
        finally:
            self._border_color = self.border_color


class KTIconButton(KTButton):
    icon = StringProperty()


KTTightLabel = Factory.KTTightLabel
KTTightButton = Factory.KTTightButton
