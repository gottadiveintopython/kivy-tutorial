__all__ = ('AppState', )

from kivy.event import EventDispatcher
from kivy.properties import StringProperty, BooleanProperty


class AppState(EventDispatcher):
    bgm = StringProperty('')
    mute_bgm = BooleanProperty(False)
