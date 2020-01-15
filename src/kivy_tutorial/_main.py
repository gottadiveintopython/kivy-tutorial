__all__ = ('main', )


KV_CODE = '''
FloatLayout:
    FloatLayout
        id: bottom_layer
        pos_hint: {'x': 0, 'y': 0, }
    FloatLayout
        id: middle_layer
        pos_hint: {'x': 0, 'y': 0, }
    FloatLayout
        id: top_layer
        pos_hint: {'x': 0, 'y': 0, }
'''


async def main(*, nursery, parent):
    import os
    from kivy.lang import Builder
    from kivy_tutorial.sceneswitcher import SceneSwitcher

    root = Builder.load_string(KV_CODE)
    parent.add_widget(root)
    switcher = SceneSwitcher(
        nursery=nursery,
        pkgname='kivy_tutorial.scene',
        userdata={
            'parent': root.ids.middle_layer,
        },
    )
    switcher.switch(os.environ.get('KIVY_TUTORIAL_FIRST_SCENE', 'title'))
