async def main(
        switcher, nursery, *, parent, drawer, menu, appstate,
        task_status, **kwargs):
    import trio
    from kivy.uix.screenmanager import SlideTransition

    appstate.bgm = 'n75.ogg'
    try:
        def on_go_back(drawer, *args, **kwargs):
            parent_node = menu.current_node.get('@parent', None)
            if parent_node is None:
                switcher.ask_to_switch('title')
            else:
                menu.switch_page(
                    branch=parent_node,
                    transition=SlideTransition(direction='right', duration=.5),
                )
            return True
        drawer.bind(on_go_back=on_go_back)
        parent.add_widget(menu)
        task_status.started()
        await trio.sleep_forever()
    finally:
        drawer.unbind(on_go_back=on_go_back)
