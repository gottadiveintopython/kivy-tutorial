async def main(switcher, nursery, *, parent, appstate, **kwargs):
    import trio
    from functools import partial
    from kivy.factory import Factory
    from kivy_tutorial.asynchelper import or_, animation, event
    from kivy_tutorial.widgets import KTTightLabel, KTTightButton

    try:
        appstate.bgm = 'n75.ogg'
        # appstate.hide_drawer = True
        root = Factory.RelativeLayout()
        parent.add_widget(root)

        async def _show_title_label():
            title_label = KTTightLabel(
                text='Kivyへのいざない',
                opacity=0,
                font_size='70sp',
                pos_hint={'center_x': .5, },
            )
            root.add_widget(title_label)
            await trio.sleep(0.1)
            title_label.y = root.height
            await or_(
                animation(
                    title_label,
                    d=3,
                    opacity=1,
                    center_y=root.height * 0.6,
                    force_final_value=True,
                ),
                event(root, 'on_touch_down'),
            )
            title_label.pos_hint['center_y'] = 0.6
            title_label.property('pos_hint').dispatch(title_label)
        await _show_title_label()

        start_button = None
        async def _show_start_button():
            nonlocal start_button
            start_button = KTTightButton(
                nursery=nursery,
                text='開始',
                opacity=0,
                font_size='70sp',
                pos_hint={'center_x': .5, 'center_y': .25, },
            )
            root.add_widget(start_button)
            await trio.sleep(0.01)
            await or_(
                animation(
                    start_button,
                    d=3,
                    opacity=1,
                    force_final_value=True,
                ),
                event(root, 'on_touch_down'),
            )
        await _show_start_button()

        await event(start_button, 'on_release')
        await animation(root, opacity=0)
        switcher.switch('menu')
    finally:
        parent.remove_widget(root)
