__all__ = ('AppState', )

from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty


class AppState(EventDispatcher):
    __events__ = ('on_exit', )

    bgm = StringProperty('')
    mute_bgm = BooleanProperty(False)
    hide_slidemenu = BooleanProperty(True)

    def on_exit(self):
        '''利用者がslide menuの'出口'iconを押した時に起きるevent'''
        pass
