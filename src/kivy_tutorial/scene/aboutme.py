# export KIVY_TUTORIAL_FIRST_SCENE=aboutme

KV_CODE = r'''
BoxLayout:
    padding: dp(10)
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: 5
        FloatLayout:
            size_hint_x: .6
            id: where_antelope_goes
        KTLabel:
            id: desc
            opacity: 0
            text_size: self.width, None
        Widget:
            size_hint_x: None
            width: dp(30)
    FloatLayout:
        size_hint_y: 1
        id: where_menu_goes
'''


async def main(
        switcher, nursery, *, parent, appstate,
        task_status, **kwargs):
    from pathlib import Path
    import trio
    from kivy.lang import Builder
    from kivy.factory import Factory as F
    from kivy.resources import resource_find
    import asynckivy as ak
    from kivyx.uix.magnet import KXMagnet
    from triohelper.triouser import activate_nursery

    appstate.bgm = 'n74.ogg'
    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        await trio.sleep(.1)
        antelope = KXMagnet(
            size=parent.size,
            pos=parent.pos,
            pos_hint={'x': 0, 'y': 0, },
            duration=.5,
        )
        antelope.add_widget(F.Image(
            source='image/sable_antelope.png',
            allow_stretch=True,
        ))
        parent.add_widget(antelope)
    task_status.started()
    await trio.sleep(.5)

    parent.remove_widget(antelope)
    root.ids.where_antelope_goes.add_widget(antelope)

    desc = root.ids.desc
    desc.text = Path(resource_find(r'text/aboutme.txt')).read_text(encoding='utf-8')
    ak.start(ak.animate(desc, d=2, opacity=1))

    where_menu_goes = root.ids.where_menu_goes
    menu = KXMagnet(
        x=where_menu_goes.x,
        top=where_menu_goes.y,
        size=where_menu_goes.size,
        pos_hint={'x': 0, 'y': 0, },
    )
    with activate_nursery(nursery):
        menu.add_widget(_create_menu())
    where_menu_goes.add_widget(menu)

    await trio.sleep_forever()


def _create_menu():
    from kivy.factory import Factory as F
    root = F.BoxLayout()
    def on_release_anim(button):
        import webbrowser
        webbrowser.open(button.url)
    for icon, url in (
        ('github-circle', 'https://github.com/gottadiveintopython'),
        ('quicktime', 'https://qiita.com/gotta_dive_into_python'),
        ('twitter', 'https://twitter.com/dive_into_py'),
        ('discord', 'https://discord.gg/UCQwfrb'),
        ('youtube', 'https://www.youtube.com/channel/UCcu_WzusAoPX2cyi8K2N-0g'),
        ('email', 'mailto:flow4re2c@gmail.com'),
    ):
        case = F.AnchorLayout()
        button = F.KTIconButton(icon=icon, on_release_anim=on_release_anim)
        button.url = url
        case.add_widget(button)
        root.add_widget(case)
    return root
