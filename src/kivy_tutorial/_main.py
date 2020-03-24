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
    from asynckivy.compatibility.trio import run_coro_under_trio
    from triohelper.triouser import activate_nursery
    from kivy_tutorial.sceneswitcher import SceneSwitcher
    from kivy_tutorial.appstate import AppState
    from kivy_tutorial.bgmplayer import BgmPlayer
    from kivy_tutorial import background_animation
    from kivy_tutorial.widgets.drawer import KTDrawer
    from kivy_tutorial.widgets.menu import KTMenu

    with activate_nursery(nursery):
        appstate = AppState()
        drawer = KTDrawer(
            appstate=appstate,
            on_go_back=lambda __: switcher.switch('menu'),
        )
        bgmplayer = BgmPlayer(file_prefix='sound/')
        menu = KTMenu(
            source='menu.yaml',
            on_leaf_node=lambda __, scene_name: switcher.switch(scene_name),
        )
        root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        drawer.attach(root.ids.top_layer)
        update_bgm = partial(_update_bgm, bgmplayer=bgmplayer)
        appstate.bind(bgm=update_bgm, mute_bgm=update_bgm)
        switcher = SceneSwitcher(
            pkgname='kivy_tutorial.scene',
            userdata={
                'parent': root.ids.middle_layer,
                'appstate': appstate,
                'drawer': drawer,
                'menu': menu,
            },
        )
        drawer.bind(on_go_home=lambda __: switcher.switch('title'))
        nursery.start_soon(
            run_coro_under_trio,
            background_animation.play(
                widget=root.ids.bottom_layer,
                color='#FFFFFF44',
                max_sprites=200,
            )
        )
    switcher.switch(os.environ.get('KIVY_TUTORIAL_FIRST_SCENE', 'title'))


def _update_bgm(appstate, __, *, bgmplayer):
    if appstate.mute_bgm:
        bgmplayer.stop()
    else:
        bgmplayer.play(appstate.bgm)
