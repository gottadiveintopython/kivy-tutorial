from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior

from kivy_tutorial.triouser import TrioUser
from kivy_tutorial.widgets import KTIcon

KV_CODE = '''
#:import theme kivy_tutorial.theme

<KTDrawerTab>:
    icon: 'menu-left'
    canvas.before:
        Color:
            rgba: theme.drawer_background_color
        Rectangle:
            pos: self.pos
            size: self.size
        PushMatrix:
        Rotate:
            origin: self.center
            angle: self.icon_angle
    canvas.after:
        PopMatrix:
<KTDrawer>:
    size_hint: None, None
    size: self.minimum_size
    FloatLayout:
        size_hint: None, None
        width: tab.width
        height: box.height
        KTDrawerTab:
            id: tab
            size_hint: None, 0.3
            width: self.texture_size[0]
            pos_hint: {'x': 0, 'center_y': .5, }
    BoxLayout:
        id: box
        orientation: 'vertical'
        size_hint: None, None
        size: self.minimum_size
        padding: 10
        spacing: 10
        canvas.before:
            Color:
                rgba: theme.drawer_background_color
            Rectangle:
                pos: self.pos
                size: self.size
        KTIconButton:
            icon: 'home'
            on_release: root.dispatch('on_go_home')
        KTIconButton:
            icon: 'volume-off' if root.appstate.mute_bgm else 'volume-high'
            outline_width: 0 if root.appstate.mute_bgm else theme.button_outline_width
            color: (0, 0, 0, .3, ) if root.appstate.mute_bgm else theme.button_color
            on_release: root.appstate.mute_bgm = not root.appstate.mute_bgm
        KTIconButton:
            icon: 'arrow-left-bold'
            on_release: root.dispatch('on_go_back')
'''
Builder.load_string(KV_CODE)


class KTDrawerTab(ButtonBehavior, KTIcon):
    icon_angle = NumericProperty(0)


class KTDrawer(TrioUser, BoxLayout):
    __events__ = ('on_go_back', 'on_go_home', )
    appstate = ObjectProperty()
    _local_nursery = None

    def attach(self, parent):
        if parent == self.parent:
            return
        self.detach()
        self.nursery.start_soon(self._start_inside_local_nursery, parent)

    async def _start_inside_local_nursery(self, parent):
        import trio
        async with trio.open_nursery() as local_nursery:
            self._local_nursery = local_nursery
            local_nursery.start_soon(self._main, parent)

    async def _main(self, parent):
        from functools import partial
        import trio
        from kivy_tutorial.asynchelper import event, animation
        from kivy_tutorial.soundplayer import global_instance as soundplayer
        await trio.sleep(.1)
        try:
            tab = self.ids.tab
            self.pos_hint = {'center_y': .5, }
            def place_drawer_to_unseen_position(parent, width):
                self.x = parent.width - tab.width
            place_drawer_to_unseen_position(parent, parent.width)
            tab.icon_angle = 0.
            parent.add_widget(self)
            parent.bind(width=place_drawer_to_unseen_position)
            await trio.sleep(.1)
            while True:
                await event(tab, 'on_press')
                soundplayer.play('button.ogg')
                parent.unbind(width=place_drawer_to_unseen_position)
                async with trio.open_nursery() as nursery:
                    nursery.start_soon(partial(
                        animation, self,
                        right=parent.width,
                        d=.3
                    ))
                    nursery.start_soon(partial(
                        animation, tab,
                        icon_angle=180.,
                        d=.3
                    ))
                self.pos_hint['right'] = 1.
                await event(tab, 'on_press')
                soundplayer.play('button.ogg')
                del self.pos_hint['right']
                async with trio.open_nursery() as nursery:
                    nursery.start_soon(partial(
                        animation, self,
                        x=parent.width - tab.width,
                        d=.3
                    ))
                    nursery.start_soon(partial(
                        animation, tab,
                        icon_angle=0.,
                        d=.3
                    ))
                parent.bind(width=place_drawer_to_unseen_position)
        finally:
            parent.remove_widget(self)
            parent.unbind(width=place_drawer_to_unseen_position)

    def detach(self):
        if self._local_nursery is not None:
            self._local_nursery.cancel_scope.cancel()
            self._local_nursery = None

    def on_go_back(self):
        '''利用者が引き出しの'戻る'buttonを押した時に起きるevent'''
        pass

    def on_go_home(self):
        '''利用者が引き出しの'家'buttonを押した時に起きるevent'''
        pass
