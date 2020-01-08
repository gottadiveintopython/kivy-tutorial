from pathlib import Path
from kivy.config import Config
Config.set('graphics', 'width', 1280)
Config.set('graphics', 'height', 900)
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty

SRC_DIR = Path(__file__).parents[1] / 'src'


def _modify_sys_path():
    import sys
    sys.path.append(str(SRC_DIR))
_modify_sys_path()


def _register_icon_font():
    from kivy.core.text import LabelBase
    LabelBase.register('Icon', str(SRC_DIR / 'materialdesignicons-webfont.ttf'))
_register_icon_font()


KV_CODE = '''
#:import md_icons kivymd.icon_definitions.md_icons

<Row>:
    Label:
        font_name: 'Icon'
        font_size: 50
        text: md_icons.get(root.icon, '')
        size_hint_x: None
        width: 60
    Label:
        font_size: 30
        text: root.icon

BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        size_hint_y: None
        height: 50
        Label:
            font_name: 'Icon'
            text: md_icons['folder-search']
            color: 0, 0, 0, 1
            font_size: 40
            size_hint_x: None
            width: 50
        TextInput:
            id: ti
            font_size: 30
            multiline: False
            on_text_validate: app.refresh()
    RecycleView:
        id: rv
        viewclass: 'Row'
        RecycleBoxLayout:
            orientation: 'vertical'
            padding: 5
            spacing: 5
            size_hint_y: None
            height: self.minimum_height
            default_size_hint: 1, None
            default_size: 100, 60
'''


class Row(BoxLayout):
    icon = StringProperty()
    text = StringProperty()


class ListingAllIconsApp(App):
    def build(self):
        return Builder.load_string(KV_CODE)
    def on_start(self):
        self.refresh()
    def refresh(self):
        from kivymd.icon_definitions import md_icons
        rv = self.root.ids.rv
        ti = self.root.ids.ti
        if ti.text:
            rv.data = [
                {'icon': key, } for key in md_icons.keys()
                if ti.text in key
            ]
        else:
            rv.data = [
                {'icon': key, } for key in md_icons.keys()
            ]


if __name__ == '__main__':
    ListingAllIconsApp().run()