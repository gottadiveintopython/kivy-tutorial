# export KIVY_TUTORIAL_FIRST_SCENE=visual_tests.speechbubble

KV_CODE = '''
<KTSpeechBubble2@KTSpeechBubble>
    background_color: 1, 1, 1, .3
    size_hint: .5, .5
    pos_hint: {'center': (.5, .5), }
GridLayout:
    cols: 3
    spacing: 20
    padding: 20
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.x
            speaker_y: self.parent.top
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.center_x
            speaker_y: self.parent.top
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.right
            speaker_y: self.parent.top
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.x
            speaker_y: self.parent.center_y
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.center_x
            speaker_y: self.parent.center_y
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.right
            speaker_y: self.parent.center_y
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.x
            speaker_y: self.parent.y
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.center_x
            speaker_y: self.parent.y
    FloatLayout:
        KTSpeechBubble2:
            speaker_x: self.parent.right
            speaker_y: self.parent.y
'''


async def main(switcher, nursery, *, parent, **kwargs):
    import trio
    from kivy.lang import Builder
    import kivy_tutorial.speechbubble
    from kivy_tutorial.triouser import activate_nursery
    try:
        with activate_nursery(nursery):
            root = Builder.load_string(KV_CODE)
        parent.add_widget(root)
        await trio.sleep_forever()
    finally:
        parent.remove_widget(root)
