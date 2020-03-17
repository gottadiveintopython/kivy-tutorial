KV_CODE = r'''
#:import webbrowser webbrowser
#:import theme kivy_tutorial.theme

BoxLayout:
    opacity: 0
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    KTLabel:
        text: '使用素材'
        font_size: theme.label_font_size * 2
    KTLabel:
        text: '(site名をclickするとweb browserが開きます)'
        font_size: theme.label_font_size * .7
        size_hint_y: None
        height: self.texture_size[1]
    BoxLayout:
        Widget:
        KTTightLabel:
            text: 'BGM ...'
        KTLabelButton:
            markup: True
            text: 'H/MIX GALLERY'
            on_release: webbrowser.open(r'http://www.hmix.net/')
        Widget:
    BoxLayout:
        Widget:
        KTTightLabel:
            text: '効果音 ...'
        KTLabelButton:
            text: 'Pocket Sound'
            on_release: webbrowser.open(r'https://pocket-se.info/')
        Widget:
    BoxLayout:
        Widget:
        KTTightLabel:
            text: '画像 ...'
        KTLabelButton:
            text: 'いらすとや'
            on_release: webbrowser.open(r'https://www.irasutoya.com/')
        Widget:
    Widget:
    AnchorLayout:
        KTTightButton:
            text: '戻る'
            on_release: root.switch_scene('menu')
'''


async def main(switcher, nursery, *, parent, appstate, drawer, **kwargs):
    import trio
    from kivy.lang import Builder
    from triohelper.triouser import activate_nursery
    from triohelper.kivy_awaitable import animation

    try:
        nursery.start_soon(_handle_on_go_back, switcher, drawer)
        appstate.bgm = 'n75.ogg'
        appstate.hide_drawer = False
        with activate_nursery(nursery):
            root = Builder.load_string(KV_CODE)
        root.switch_scene = lambda name: switcher.switch(name)
        parent.add_widget(root)
        await animation(root, opacity=1, d=.5)
        await trio.sleep_forever()
    finally:
        with trio.move_on_after(1) as cleanup_scope:
            cleanup_scope.shield = True
            await animation(root, opacity=0, d=.5)
            parent.remove_widget(root)


async def _handle_on_go_back(switcher, drawer):
    from triohelper.kivy_awaitable import event
    await event(drawer, 'on_go_back')
    switcher.switch('menu')
