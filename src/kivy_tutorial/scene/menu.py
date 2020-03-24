async def main(switcher, nursery, *, parent, drawer, menu, **kwargs):
    import trio
    try:
        def on_go_back(drawer, *args, **kwargs):
            parent_node = menu.current_node.get('@parent', None)
            if parent_node is None:
                return
            menu.switch_page(branch=parent_node)
        drawer.bind(on_go_back=on_go_back)
        parent.add_widget(menu)
        await trio.sleep_forever()
    finally:
        drawer.unbind(on_go_back=on_go_back)
        parent.remove_widget(menu)
