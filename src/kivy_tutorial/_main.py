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
    from kivy_tutorial.appstate import AppState
    from kivy_tutorial.bgmplayer import BgmPlayer
    from kivy_tutorial import background_animation
    from kivy_tutorial.drawer import KTDrawer

    with activate_nursery(nursery):
        appstate = AppState()
        bgmplayer = BgmPlayer(file_prefix='sound/')
        root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        appstate.bind(
            bgm=partial(_change_bgm, bgmplayer=bgmplayer),
            mute_bgm=partial(_mute_or_unmute_bgm, bgmplayer=bgmplayer),
            hide_drawer=partial(
                _hide_or_unhide_drawer,
                drawer=KTDrawer(appstate=appstate),
                parent=root.ids.top_layer
            ),
        )
        switcher = SceneSwitcher(
            pkgname='kivy_tutorial.scene',
            userdata={
                'parent': root.ids.middle_layer,
                'appstate': appstate,
            },
        )
        nursery.start_soon(partial(
            background_animation.play,
            nursery=nursery,
            parent=root.ids.bottom_layer,
        ))
    # switcher.switch('visual_tests.widgets')
    switcher.switch(os.environ.get('KIVY_TUTORIAL_FIRST_SCENE', 'title'))


def _change_bgm(appstate, file, *, bgmplayer):
    if appstate.mute_bgm:
        bgmplayer.stop()
    else:
        bgmplayer.play(file)


def _mute_or_unmute_bgm(appstate, mute, *, bgmplayer):
    if mute:
        bgmplayer.stop()
    else:
        bgmplayer.play(appstate.bgm)


def _hide_or_unhide_drawer(appstate, hide, *, drawer, parent):
    if hide:
        drawer.detach()
    else:
        drawer.attach(parent)
