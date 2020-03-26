async def main(
        switcher, nursery, *, parent, appstate, drawer, menu,
        task_status, **kwargs):
    import trio
    from functools import partial
    from kivy.factory import Factory
    from triohelper import or_
    from triohelper.kivy_awaitable import animate, event
    from kivy_tutorial.widgets.basic import KTTightLabel, KTTightButton

    try:
        appstate.bgm = 'n75.ogg'
        menu.reset()

        # ignore 'on_go_back' and 'on_go_home' during the scene
        avoid_event = lambda *args, **kwargs: True
        drawer.bind(on_go_back=avoid_event, on_go_home=avoid_event)

        task_status.started()

        async def _show_title_label():
            title_label = KTTightLabel(
                text='Kivyへのいざない',
                opacity=0,
                font_size='70sp',
                pos_hint={'center_x': .5, },
            )
            parent.add_widget(title_label)
            await trio.sleep(0.1)
            title_label.y = parent.height
            await or_(
                animate(
                    title_label,
                    d=3,
                    opacity=1,
                    center_y=parent.height * 0.6,
                    force_final_value=True,
                ),
                event(parent, 'on_touch_down'),
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
            parent.add_widget(start_button)
            await trio.sleep(0.01)
            await or_(
                animate(
                    start_button,
                    d=3,
                    opacity=1,
                    force_final_value=True,
                ),
                event(parent, 'on_touch_down'),
            )
        await _show_start_button()

        await event(start_button, 'on_release_anim')
        switcher.ask_to_switch('menu')
    finally:
        drawer.unbind(on_go_back=avoid_event, on_go_home=avoid_event)
