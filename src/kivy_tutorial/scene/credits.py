KV_CODE = r'''
#:import webbrowser webbrowser
#:import theme kivy_tutorial.theme

BoxLayout:
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
    BoxLayout:
        Widget:
        KTTightLabel:
            text: 'Font ...'
        KTLabelButton:
            text: 'Asterism'
            on_release: webbrowser.open(r'https://www.asterism-m.com/')
        Widget:
    AnchorLayout:
        KTTightButton:
            text: '戻る'
            on_release_anim: root.switch_scene('menu')
'''
async def main(
        switcher, nursery, *, parent, appstate,
        task_status, **kwargs):
    import trio
    from kivy.lang import Builder
    from triohelper.triouser import activate_nursery

    appstate.bgm = 'n75.ogg'
    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
    root.switch_scene = lambda name: switcher.ask_to_switch(name)
    parent.add_widget(root)
    task_status.started()
    await trio.sleep_forever()
