PREVIOUS_SCENE = 'menu'

async def main(switcher, nursery, *, parent, appstate, drawer, **kwargs):
    import trio
    from kivy_tutorial.asynchelper import animation
    from kivy_tutorial.widgets import KTMenu

    try:
        nursery.start_soon(_handle_on_go_back, switcher, drawer)
        appstate.bgm = 'n75.ogg'
        appstate.hide_drawer = False
        root = KTMenu(nursery=nursery, opacity=0)
        root.update(
            switcher=switcher,
            data=[
                ('layout編', 'menu.contents.layout', ),
                ('戻る', PREVIOUS_SCENE, ),
            ]
        )
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
    switcher.switch(PREVIOUS_SCENE)
