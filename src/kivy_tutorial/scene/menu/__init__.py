KV_CODE = r'''
BoxLayout:
    opacity: 0
    orientation: 'vertical'
    AnchorLayout:
        halign: 'center'
        valign: 'center'
        KTTightButton:
            text: '自己紹介'
    AnchorLayout:
        halign: 'center'
        valign: 'center'
        KTTightButton:
            text: '本編'
    AnchorLayout:
        halign: 'center'
        valign: 'center'
        KTTightButton:
            text: '使用素材'
            on_release: root.switch_scene('credits')
    AnchorLayout:
        halign: 'center'
        valign: 'center'
        KTTightButton:
            text: '戻る'
            on_release: root.switch_scene('title')
'''


async def main(switcher, nursery, *, parent, appstate, drawer, **kwargs):
    import trio
    from kivy.lang import Builder
    from kivy_tutorial.triouser import activate_nursery
    from kivy_tutorial.asynchelper import animation

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
    from kivy_tutorial.asynchelper import event
    await event(drawer, 'on_go_back')
    switcher.switch('title')
