from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty


Builder.load_string(r'''
#:import md_icons kivymd.icon_definitions.md_icons

<KT_Debug_KivymdIconsRow>:
    Label:
        font_name: 'Icon'
        font_size: 50
        text: md_icons.get(root.icon, '')
        size_hint_x: None
        width: 60
    Label:
        font_size: 30
        text: root.icon

<KT_Debug_KivymdIcons>:
    orientation: 'vertical'
    spacing: 10
    padding: 10
    BoxLayout:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size
        spacing: 10
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
            on_text_validate: root.refresh()
    RecycleView:
        id: rv
        viewclass: 'KT_Debug_KivymdIconsRow'
        RecycleBoxLayout:
            orientation: 'vertical'
            padding: 5
            spacing: 5
            size_hint_y: None
            height: self.minimum_height
            default_size_hint: 1, None
            default_size: 100, 60
''')


class KT_Debug_KivymdIconsRow(BoxLayout):
    icon = StringProperty()
    text = StringProperty()


class KT_Debug_KivymdIcons(BoxLayout):
    def refresh(self):
        from kivymd.icon_definitions import md_icons
        rv = self.ids.rv
        ti = self.ids.ti
        if ti.text:
            rv.data = [
                {'icon': key, } for key in md_icons.keys()
                if ti.text in key
            ]
        else:
            rv.data = [
                {'icon': key, } for key in md_icons.keys()
            ]

async def main(
        switcher, nursery, *, parent, appstate,
        task_status, **kwargs):
    import trio

    root = KT_Debug_KivymdIcons()
    root.refresh()
    parent.add_widget(root)
    task_status.started()
    await trio.sleep_forever()
