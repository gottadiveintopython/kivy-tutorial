from kivy.lang import Builder
Builder.load_string(r'''
<KT_Dev_SpeechBubble@KTSpeechBubble>
    background_color: 1, 1, 1, .3
    size_hint: .5, .5
    pos_hint: {'center': (.5, .5), }
''')

KV_CODE = '''
GridLayout:
    cols: 3
    spacing: 20
    padding: 20
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.x
            speaker_y: self.parent.top
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.center_x
            speaker_y: self.parent.top
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.right
            speaker_y: self.parent.top
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.x
            speaker_y: self.parent.center_y
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.center_x
            speaker_y: self.parent.center_y
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.right
            speaker_y: self.parent.center_y
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.x
            speaker_y: self.parent.y
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.center_x
            speaker_y: self.parent.y
    FloatLayout:
        KT_Dev_SpeechBubble:
            speaker_x: self.parent.right
            speaker_y: self.parent.y
'''


async def main(switcher, nursery, *, parent, task_status, **kwargs):
    import trio
    from kivy.lang import Builder
    import kivy_tutorial.widgets.speechbubble
    from triohelper.triouser import activate_nursery

    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
    parent.add_widget(root)
    task_status.started()
    await trio.sleep_forever()
