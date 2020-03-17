async def main(switcher, nursery, *, parent, appstate, drawer, **kwargs):
    import trio
    from triohelper.kivy_awaitable import animate
    from kivy_tutorial.widgets.basic import KTMenu

    try:
        nursery.start_soon(_handle_on_go_back, switcher, drawer)
        appstate.bgm = 'n75.ogg'
        appstate.hide_drawer = False
        root = KTMenu(nursery=nursery, opacity=0)
        root.update(
            switcher=switcher,
            data=[
                ('自己紹介', 'aboutme', ),
                ('本編', 'menu.contents', ),
                ('使用素材', 'credits', ),
                ('戻る', 'title', ),
            ]
        )
        parent.add_widget(root)
        await animate(root, opacity=1, d=.5)
        await trio.sleep_forever()
    finally:
        with trio.move_on_after(1) as cleanup_scope:
            cleanup_scope.shield = True
            await animate(root, opacity=0, d=.5)
            parent.remove_widget(root)


async def _handle_on_go_back(switcher, drawer):
    from triohelper.kivy_awaitable import event
    await event(drawer, 'on_go_back')
    switcher.switch('title')
