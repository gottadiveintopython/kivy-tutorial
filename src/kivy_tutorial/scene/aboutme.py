# export KIVY_TUTORIAL_FIRST_SCENE=aboutme

KV_CODE = r'''
RelativeLayout:
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
    from functools import partial
    from pathlib import Path
    import trio
    from kivy.lang import Builder
    from kivy.factory import Factory as F
    from kivy.resources import resource_find
    from triohelper.triouser import activate_nursery
    from triohelper.kivy_awaitable import animate

    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        antelope = F.Image(
            source='image/sable_antelope.png',
            allow_stretch=True,
        )
        root.add_widget(antelope)
    task_status.started()
    await trio.sleep(.5)

    async with trio.open_nursery() as sub_nursery:
        where_antelope_goes = root.ids.where_antelope_goes
        antelope.size_hint = (None, None, )
        sub_nursery.start_soon(partial(
            animate, antelope, d=1,
            pos=where_antelope_goes.pos,
            size=where_antelope_goes.size,
        ))

        desc = root.ids.desc
        desc.text = Path(resource_find(r'text/aboutme.txt')).read_text(encoding='utf-8')
        sub_nursery.start_soon(partial(animate, desc, d=2, opacity=1))

        where_menu_goes = root.ids.where_menu_goes
        with activate_nursery(nursery):
            menu = _create_menu()
        menu.size = where_menu_goes.size
        menu.size_hint = (None, None, )
        menu.x = where_menu_goes.x
        menu.top = where_menu_goes.y
        root.add_widget(menu)
        await animate(menu, y=where_menu_goes.y, d=1)

    root.remove_widget(antelope)
    antelope.size_hint = (1, 1, )
    antelope.pos_hint = {'x': 0, 'y': 0, }
    where_antelope_goes.add_widget(antelope)

    root.remove_widget(menu)
    menu.size_hint = (1, 1, )
    antelope.pos_hint = {'x': 0, 'y': 0, }
    where_menu_goes.add_widget(menu)

    await trio.sleep_forever()


def _create_menu():
    from kivy.factory import Factory as F
    root = F.BoxLayout()
    def on_release(button):
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
        button = F.KTIconButton(icon=icon, on_release=on_release)
        button.url = url
        case.add_widget(button)
        root.add_widget(case)
    return root
