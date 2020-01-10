from textwrap import dedent
from pathlib import Path
import trio
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.app import App

SRC_DIR = Path(__file__).parent


def _add_resource_search_path():
    from kivy.resources import resource_add_path
    resource_add_path(str(SRC_DIR / 'assets'))
_add_resource_search_path()


def _set_default_font_to_japanese():
    LabelBase.register('yomogi', 'font/yomogifont.otf')
    Builder.load_string(dedent('''
    <Label,TextInput>:
        font_name: 'yomogi'
    <Popup>:
        title_font: 'yomogi'
    '''))
_set_default_font_to_japanese()


def _set_default_font_size():
    Builder.load_string(dedent('''
    <Label,TextInput>:
        font_size: max(sp(15), 30)
    <Popup>:
        title_size: max(sp(15), 30)
    '''))
_set_default_font_size()


def _register_icon_font():
    LabelBase.register('Icon', 'font/materialdesignicons-webfont.ttf')
_register_icon_font()


class TutorialApp(App):
    nursery = None

    def build(self):
        from kivy_tutorial import KTMain
        return KTMain()

    def on_start(self):
        self.nursery.start_soon(self.root.start)

    async def root_task(self):
        async with trio.open_nursery() as nursery:
            self.nursery = nursery

            async def event_loop():
                await self.async_run(async_lib='trio')
                nursery.cancel_scope.cancel()

            nursery.start_soon(event_loop)


if __name__ == "__main__":
    trio.run(TutorialApp().root_task)
