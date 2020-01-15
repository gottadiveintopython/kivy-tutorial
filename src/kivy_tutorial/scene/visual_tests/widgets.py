# export KIVY_TUTORIAL_FIRST_SCENE=visual_tests.widgets

KV_CODE = '''
BoxLayout:
    orientation: 'vertical'
    spacing: 10
    padding: 10
    Label:
        text: 'widgetの見た目のtest'
        size_hint_y: None
        height: self.texture_size[1]
    BoxLayout:
        spacing: 10
        KTIconButton:
            icon: 'arrow-right'
        KTIconButton:
            icon: 'twitter'
        KTTightLabel:
            text: 'KTTightLabel'
        KTIconButton:
            icon: 'twitch'
        KTIconButton:
            icon: 'blender-software'
    BoxLayout:
        spacing: 10
        KTIcon:
            icon: 'menu'
        KTIcon:
            icon: 'menu-open'
        KTIcon:
            icon: 'folder-clock'
        KTIcon:
            icon: 'menu-right'
    KTButton:
        text: "Beautiful is better than ugly."
    KTButton:
        text: "Explicit is better than implicit."
    KTButton:
        text: "Simple is better than complex."
    KTButton:
        text: "Complex is better than complicated."
    KTButton:
        text: "Flat is better than nested."
'''


async def main(switcher, nursery, *, parent, **kwargs):
    import trio
    from kivy.lang import Builder
    import kivy_tutorial.widgets
    from kivy_tutorial.triouser import activate_nursery
    try:
        with activate_nursery(nursery):
            root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        await trio.sleep_forever()
    finally:
        parent.remove_widget(root)
