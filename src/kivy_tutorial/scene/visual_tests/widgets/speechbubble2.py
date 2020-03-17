# export KIVY_TUTORIAL_FIRST_SCENE=visual_tests.speechbubble2

KV_CODE = '''
RelativeLayout:
    Image:
        id: antelope
        source: "image/sable_antelope.png"
        size_hint: None, None
        size: self.texture_size
'''


async def main(switcher, nursery, *, parent, **kwargs):
    import trio
    from kivy.lang import Builder
    import kivy_tutorial.widgets.basic
    from triohelper.triouser import activate_nursery
    try:
        with activate_nursery(nursery):
            root = Builder.load_string(KV_CODE)
            parent.add_widget(root)
            antelope = root.ids.antelope
            def on_touch_down(w, t):
                if w.collide_point(*t.opos):
                    nursery.start_soon(speak, root, t.opos, )
            antelope.bind(on_touch_down=on_touch_down)
        await trio.sleep_forever()
    finally:
        parent.remove_widget(root)


async def speak(parent, speaker_pos):
    import trio
    from triohelper.kivy_awaitable import animation
    from kivy_tutorial.widgets.speechbubble import KTSpeechBubble
    from kivy_tutorial.widgets.basic import KTLabel
    bubble = KTSpeechBubble(
        pos=speaker_pos,
        size=(0, 0, ),
        size_hint=(None, None),
        speaker_pos=speaker_pos,
    )
    parent.add_widget(bubble)
    await animation(
        bubble, size=(200, 100),
        center=(speaker_pos[0] + 200, speaker_pos[1]),
        d=.2,
    )
    label = KTLabel(text="Hello", color=(0, 0, 0, 1))
    bubble.add_widget(label)
    await trio.sleep(1)
    parent.remove_widget(bubble)
