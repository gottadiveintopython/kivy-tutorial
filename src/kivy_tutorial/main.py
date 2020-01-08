__all__ = ('KTMain', )

from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

from .lazy_screen_manager import KTLazyScreenManager



Builder.load_string(f'''
<KTMain>:
    KTLazyScreenManager:
        id: scrmgr
        pkg_name: '{__name__}.scene'
        Screen:
            name: 'blank'
''')


class KTMain(FloatLayout):
    nursery = ObjectProperty()
    async def start(self):
        pass