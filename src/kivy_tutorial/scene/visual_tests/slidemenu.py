# export KIVY_TUTORIAL_FIRST_SCENE=visual_tests.slidemenu
from kivy.lang import Builder


KV_CODE = '''
#:import __ kivy_tutorial.widgets

RelativeLayout:
    StackLayout:
        padding: 10
        spacing: 10
        orientation: 'lr-bt'
        KTTightButton:
            text: 'show menu'
            id: show
        KTTightButton:
            text: 'hide menu'
            id: hide
'''


async def main(switcher, nursery, *, appstate, parent, **kwargs):
    import trio
    from kivy_tutorial.triouser import activate_nursery
    try:
        with activate_nursery(nursery):
            root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        root.ids.show.bind(on_release=lambda __: setattr(appstate, 'hide_slidemenu', False))
        root.ids.hide.bind(on_release=lambda __: setattr(appstate, 'hide_slidemenu', True))
        await trio.sleep_forever()
    finally:
        parent.remove_widget(root)
