from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivyx.uix.drawer import KXDrawer

KV_CODE = '''
#:import SoundLoader kivy.core.audio.SoundLoader
#:set sound SoundLoader.load('sound/button.ogg')
#:import theme kivy_tutorial.theme

<KTDrawer>:
    size_hint: None, None
    size: box.size
    background_color: theme.drawer_background_color
    on_pre_open: sound.play()
    on_pre_close: sound.play()
    BoxLayout:
        id: box
        orientation: 'vertical'
        size_hint: None, None
        size: self.minimum_size
        padding: 10
        spacing: 10
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


class KTDrawer(KXDrawer):
    __events__ = ('on_go_back', 'on_go_home', )
    appstate = ObjectProperty()

    def on_go_back(self):
        '''利用者が引き出しの'戻る'buttonを押した時に起きるevent'''
        pass

    def on_go_home(self):
        '''利用者が引き出しの'家'buttonを押した時に起きるevent'''
        pass
