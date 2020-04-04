__all__ = ('KTDialogue', )

from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder
from kivy.factory import Factory as F
from triohelper.triouser import TrioUser
from triohelper import new_nursery
import kivy_tutorial.widgets.basic

Builder.load_string(r'''
<KTDialogue>:
    spacing: dp(30)
    FloatLayout:
        id: where_speech_bubble_goes
        KTIcon:
            id: indicator
            opacity: 0
            color: 1, 1, 1, 1
            size_hint: None, None
            size: self.texture_size
            pos_hint: {'right': .998, 'y': .005, }
    Image:
        id: speaker
        source: root.speaker_image
        size_hint: None, None
        height: min(root.height, self.texture_size[1])
        width:
            (
            self.height * (self.texture_size[0] / self.texture_size[1])
            if self.texture_size[1] else 1  # 零除算を防いでいる
            )
        canvas.before:
            PushMatrix:
            Rotate:
                origin: self.center
                angle: root._speaker_angle
        canvas.after:
            PopMatrix:
<KTDialogueLabel@KTLabel>:
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1]
''')


class KTDialogue(TrioUser, F.BoxLayout):
    speaker_image = StringProperty()
    speaker_voice = StringProperty()
    _speaker_angle = NumericProperty()
    _sound = None
    _bubble = None
    _child_nursery = None

    def on_speaker_voice(self, __, filename):
        from kivy.core.audio import SoundLoader
        sound = SoundLoader.load(filename)
        sound.volume = .5
        self._sound = sound

    def shutup(self):
        if self._child_nursery is not None:
            self._child_nursery.cancel_scope.cancel()
            self._child_nursery = None
        bubble, self._bubble = self._bubble, None
        if bubble and bubble.parent:
            bubble.parent.remove_widget(bubble)

    @new_nursery
    async def speak(self, text, *, markup=False, new_nursery):
        import trio
        from kivy_tutorial.widgets.speechbubble2 import KTSpeechBubble2
        from triohelper.kivy_awaitable import animate, event
        from triohelper import or_
        from triohelper import new_cancel_scope
        from asynckivy.uix.magnet import AKMagnet

        self.shutup()
        self._child_nursery = new_nursery

        # 吹き出しが現れるanimationを開始
        speaker = self.ids.speaker
        where_speech_bubble_goes = self.ids.where_speech_bubble_goes
        magnet = AKMagnet(
            size=(0, 0), x=speaker.x, y=speaker.center_y, duration=.3)
        bubble = KTSpeechBubble2(border_color="#777777")
        self._bubble = bubble
        magnet.add_widget(bubble)
        magnet.pos_hint = {'center_x': .5, 'center_y': .5, }
        self.ids.where_speech_bubble_goes.add_widget(magnet, index=1)

        # 話し手を揺らすanimationを開始
        new_nursery.start_soon(self._wave_speaker)

        # 吹き出しが現れるanimationの完了を待つ
        await trio.sleep(magnet.duration + .1)
        magnet.disappear()
        del magnet

        if self._sound is not None:
            self._sound.play()

        # 吹き出しの中に文字列が現れるanimation
        label = F.KTDialogueLabel(
            text=text, markup=markup, opacity=0)
        sview = F.ScrollView(
            do_scroll_x=False,
            bar_width='10dp',
            scroll_type=['bars', 'content'],
        )
        sview.add_widget(label)
        bubble.add_widget(sview)
        await animate(label, opacity=1, d=.1)

        # 指示iconが点滅するanimationを開始
        new_nursery.start_soon(self._blink_indicator)

        # scrollが要る場合は一番下までscrollされるまで 'pan-vertical'-icon
        indicator = self.ids.indicator
        if sview.height < label.height:
            indicator.icon = 'pan-vertical'
            await event(
                sview, 'scroll_y',
                filter=lambda sview, scroll_y: scroll_y <= 0
            )

        #
        indicator.icon = 'gesture-tap'
        await or_(
            event(label, 'on_touch_down', return_value=True),
            event(
                bubble, 'on_touch_down',
                return_value=True,
                filter=lambda w, t: \
                    (not t.is_mouse_scrolling) and \
                    w.collide_point(*t.opos) and \
                    not sview.collide_point(*bubble.to_local(*t.opos)),
            ),
        )
        new_nursery.cancel_scope.cancel()

    async def _blink_indicator(self):
        from triohelper.kivy_awaitable import animate
        indicator = self.ids.indicator
        try:
            while True:
                await animate(indicator, opacity=1, d=.6)
                await animate(indicator, opacity=0, d=.6)
        finally:
            indicator.opacity = 0

    async def _wave_speaker(self):
        from triohelper.kivy_awaitable import animate
        try:
            await animate(self, _speaker_angle=10, t='out_quad')
            while True:
                await animate(self, _speaker_angle=-10, t='in_out_quad', d=2)
                await animate(self, _speaker_angle=10, t='in_out_quad', d=2)
        finally:
            self._speaker_angle = 0

