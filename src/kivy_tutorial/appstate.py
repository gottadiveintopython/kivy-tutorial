__all__ = ('AppState', )

from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty


class AppState(EventDispatcher):
    __events__ = ('on_exit', )

    bgm = StringProperty('')
    mute_bgm = BooleanProperty(False)
    hide_drawer = BooleanProperty(True)

    def on_exit(self):
        '''利用者が引き出しの'出口'buttonを押した時に起きるevent'''
        pass
