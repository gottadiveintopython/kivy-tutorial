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
    from functools import partial
    from kivy.lang import Builder
    from kivy_tutorial.triouser import activate_nursery
    from kivy_tutorial.sceneswitcher import SceneSwitcher
    from kivy_tutorial.bgmplayer import BgmPlayer
    from kivy_tutorial.soundplayer import SoundPlayer
    from kivy_tutorial import background_animation

    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        switcher = SceneSwitcher(
            pkgname='kivy_tutorial.scene',
            userdata={
                'parent': root.ids.middle_layer,
                'bgmplayer': BgmPlayer(file_prefix='sound/'),
                'soundplayer': SoundPlayer(file_prefix='sound/'),
            },
        )
        nursery.start_soon(partial(
            background_animation.play,
            nursery=nursery,
            parent=root.ids.bottom_layer,
        ))
    # switcher.switch('visual_tests.widgets')
    switcher.switch(os.environ.get('KIVY_TUTORIAL_FIRST_SCENE', 'title'))
