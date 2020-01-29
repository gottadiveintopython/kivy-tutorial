# export KIVY_TUTORIAL_FIRST_SCENE=visual_tests.menu

from kivy.factory import Factory


async def main(switcher, nursery, *, appstate, parent, **kwargs):
    from kivy.factory import Factory as F
    import trio
    from kivy_tutorial.widgets import KTMenu
    from kivy_tutorial.triouser import activate_nursery
    try:
        with activate_nursery(nursery):
            root = F.BoxLayout()
            menu1 = KTMenu()
            menu1.update(
                switcher=switcher,
                data=[
                    ('項目が沢山ある場合', 'visual_tests.menu')
                    for __ in range(20)
                ]
            )
            menu2 = KTMenu()
            menu2.update(
                switcher=switcher,
                data=[
                    ('項目が少ない場合', 'visual_tests.menu')
                    for __ in range(3)
                ]
            )
        root.add_widget(menu1)
        root.add_widget(menu2)
        parent.add_widget(root)
        await trio.sleep_forever()
    finally:
        parent.remove_widget(root)
