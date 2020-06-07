__all__ = (
    'KTLabel', 'KTTightLabel', 'KTButton', 'KTTightButton', 'KTLabelButton',
    'KTIcon', 'KTIconButton',
)
import typing

from kivy.properties import StringProperty, ColorProperty, NumericProperty
from kivy.lang import Builder
from kivy.factory import Factory as F
import trio
from asynckivy.compatibility.trio import run_coro_under_trio

from triohelper.triouser import TrioUser
from kivy_tutorial import theme


KV_CODE = '''
#:import md_icons kivymd.icon_definitions.md_icons
#:import theme kivy_tutorial.theme

<KTLabel@Label>:
    font_size: theme.label_font_size
    font_name: theme.font_name

<KTTightLabel@KTLabel>:
    size_hint: None, None
    width: self.texture_size[0] + dp(10)
    height: self.texture_size[1] + dp(10)

<KTLabelButton@ButtonBehavior+KTTightLabel>:
    outline_width: theme.button_outline_width
    outline_color: theme.button_background_color
    color: theme.button_color

<KTIcon>:
    font_size: theme.label_font_size
    font_name: 'Icons'
    size: theme.icon_size
    text: md_icons.get(self.icon, '')

<KTButton>:
    outline_width: theme.button_outline_width
    outline_color: theme.button_outline_color
    color: theme.button_color
    font_size: theme.button_font_size
    font_name: theme.font_name
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
    font_name: 'Icons'
    text: md_icons.get(self.icon, '')
    font_size: theme.icon_font_size
    size_hint: None, None
    size: theme.icon_size
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


class KTIcon(F.Label):
    icon = StringProperty()


class KTButton(TrioUser, F.Label):
    __events__ = ('on_press', 'on_release', 'on_release_anim', )
    border_color = ColorProperty(theme.button_border_color)
    border_color2 = ColorProperty(theme.button_border_color2)
    background_color = ColorProperty(theme.button_background_color)
    soundfile = StringProperty('sound/button.ogg')
    _border_color = ColorProperty(border_color.defaultvalue)
    _scaling = NumericProperty(1)

    def on_kv_post(self, *args):
        self.nursery.start_soon(run_coro_under_trio, self._ak_main())

    def on_press(self):
        from kivy.core.audio import SoundLoader
        SoundLoader.load(self.soundfile).play()

    def on_release(self):
        pass

    def on_release_anim(self):
        pass

    async def _ak_main(self):
        import asynckivy
        from asynckivy import animate, or_, event
        
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
                coro_blink = self._ak_blink()
                asynckivy.start(coro_blink)
                await event(self, 'on_touch_up',
                    filter=lambda w, t: t is current_touch and t.grab_current is w,
                    return_value=True,
                )
                coro_blink.close()
                current_touch.ungrab(self)
                if self.collide_point(*current_touch.pos):
                    self.dispatch('on_release')
                    await animate(self, _scaling=.8, d=.05)
                    await animate(self, _scaling=1, d=.05)
                    self.dispatch('on_release_anim')
        finally:
            if coro_blink is not None:
                coro_blink.close()
            if current_touch is not None:
                current_touch.ungrab(self)

    async def _ak_blink(self):
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


KTLabel = F.KTLabel
KTTightLabel = F.KTTightLabel
KTLabelButton = F.KTLabelButton
KTTightButton = F.KTTightButton
