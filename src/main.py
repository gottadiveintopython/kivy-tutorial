from textwrap import dedent
from pathlib import Path
import trio
from kivy.config import Config
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 720)
Config.set('graphics', 'maxfps', 60)
import kivy
kivy.require("2.0.0")
from kivy.lang import Builder
from kivy.app import App

SRC_DIR = Path(__file__).parent


def _add_resource_search_path():
    from kivy.resources import resource_add_path
    resource_add_path(str(SRC_DIR / 'assets'))
_add_resource_search_path()


def _register_fonts():
    from kivy.core.text import LabelBase
    LabelBase.register('Icon', 'font/materialdesignicons-webfont.ttf')
    LabelBase.register('yomogi', 'font/yomogifont.otf')
_register_fonts()


class TutorialApp(App):
    def build(self):
        from kivy.uix.floatlayout import FloatLayout
        return FloatLayout()

    def on_start(self):
        from functools import partial
        import kivy_tutorial
        self.nursery.start_soon(partial(
            kivy_tutorial.main,
            nursery=self.nursery,
            parent=self.root,
        ))

    async def root_task(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def event_loop():
                await self.async_run(async_lib='trio')
                nursery.cancel_scope.cancel()

            nursery.start_soon(event_loop)


if __name__ == "__main__":
    trio.run(TutorialApp().root_task)
