__all__ = ('main', )


KV_CODE = '''
RelativeLayout:
    FloatLayout
        id: bottom_layer
    FloatLayout
        id: middle_layer
    FloatLayout
        id: top_layer
'''


async def main(*, nursery, parent):
    import os
    from kivy.lang import Builder
    from kivy_tutorial.triouser import activate_nursery
    from kivy_tutorial.sceneswitcher import SceneSwitcher
    from kivy_tutorial.bgmplayer import BgmPlayer

    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        switcher = SceneSwitcher(
            pkgname='kivy_tutorial.scene',
            userdata={
                'parent': root.ids.middle_layer,
                'bgmplayer': BgmPlayer(),
            },
        )
    # switcher.switch('visual_tests.widgets')
    switcher.switch(os.environ.get('KIVY_TUTORIAL_FIRST_SCENE', 'title'))
