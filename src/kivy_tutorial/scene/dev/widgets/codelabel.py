async def main(switcher, nursery, *, parent, task_status, **kwargs):
    import trio
    from pathlib import Path
    from kivy.uix.scrollview import ScrollView
    from kivy_tutorial.widgets.codelabel import KTCodeLabel
    from kivy_tutorial.widgets.basic import KV_CODE

    sv = ScrollView(
        pos_hint={'center_x': .5, 'center_y': .5, },
        size_hint=(.95, .9, ),
    )
    label = KTCodeLabel(
        text=KV_CODE,
        lexer_name='kivy',
        size_hint_y=None,
    )
    label.bind(minimum_height=label.setter('height'))
    sv.add_widget(label)
    parent.add_widget(sv)
    task_status.started()
    await trio.sleep_forever()
