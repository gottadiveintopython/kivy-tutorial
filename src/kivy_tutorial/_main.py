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
    from kivy_tutorial.bgmplayer import BgmPlayer
    from kivy_tutorial import background_animation
    from kivy_tutorial.widgets.drawer import KTDrawer
    from kivy_tutorial.widgets.menu import KTMenu

    with activate_nursery(nursery):
        appstate = _create_appstate()
        drawer = KTDrawer(
            anchor='rm',
            appstate=appstate,
            on_go_back=lambda __: switcher.ask_to_switch('menu'),
        )
        bgmplayer = BgmPlayer(file_prefix='sound/')
        menu = KTMenu(
            source='menu.yaml',
            on_leaf_node=lambda __, scene_name: switcher.ask_to_switch(scene_name),
        )
        root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        root.ids.top_layer.add_widget(drawer)
        update_bgm = partial(_update_bgm, bgmplayer=bgmplayer)
        appstate.bind(bgm=update_bgm, mute_bgm=update_bgm)
        middle_layer = root.ids.middle_layer.__self__
        switcher = SceneSwitcher(
            pkgname='kivy_tutorial.scene',
            userdata={
                'parent': middle_layer,
                'appstate': appstate,
                'drawer': drawer,
                'menu': menu,
            },
        )
        await nursery.start(switcher.attach, middle_layer)
        drawer.bind(on_go_home=lambda __: switcher.ask_to_switch('title'))
        nursery.start_soon(
            run_coro_under_trio,
            background_animation.play(
                widget=root.ids.bottom_layer,
                color='#FFFFFF44',
                max_sprites=200,
            )
        )
    switcher.ask_to_switch(os.environ.get('KIVY_TUTORIAL_FIRST_SCENE', 'title'))


def _update_bgm(appstate, __, *, bgmplayer):
    if appstate.mute_bgm:
        bgmplayer.stop()
    else:
        bgmplayer.play(appstate.bgm)


def _create_appstate():
    from kivy.event import EventDispatcher
    from kivy.properties import StringProperty, BooleanProperty
    class AppState(EventDispatcher):
        bgm = StringProperty()
        mute_bgm = BooleanProperty(False)
    return AppState()
