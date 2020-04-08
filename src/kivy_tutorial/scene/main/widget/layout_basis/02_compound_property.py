from contextlib import asynccontextmanager

KV_CODE = r'''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        spacing: dp(10)
        KTCodeLabel:
            id: left_code
            lexer_name: 'kivy'
        Widget:
            size_hint_x: None
            width: 2
            canvas:
                Color:
                    rgba: .4, .4, 1, .5
                Rectangle:
                    pos: self.pos
                    size: self.size
        KTCodeLabel:
            id: right_code
            lexer_name: 'kivy'
    Splitter:
        sizable_from: 'top'
        max_size: self.parent.height
        size_hint_y: None
        height: dp(160)
        KTDialogue:
            id: dialogue
            speaker_image: 'image/serval.png'
            speaker_voice: 'sound/speak.ogg'
            padding: dp(10)
'''


async def main(
        switcher, nursery, *, parent, appstate, drawer, menu,
        task_status, **kwargs):
    from textwrap import dedent
    import trio
    from kivy.lang import Builder
    from kivy.factory import Factory
    from triohelper.triouser import activate_nursery
    from asynckivy.uix.magnet import AKMagnet
    import kivy_tutorial.widgets.basic
    import kivy_tutorial.widgets.codelabel
    import kivy_tutorial.widgets.dialogue

    appstate.bgm = ''

    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
    parent.add_widget(root)
    task_status.started()
    await trio.sleep(1)

    left_code = root.ids.left_code.__self__
    right_code = root.ids.right_code.__self__
    dialogue = root.ids.dialogue.__self__

    async def speak(text):
        return await dialogue.speak(_finalize_text(text), markup=True)

    for line in (
        r'前回「次回はhintを使わないやり方を見ていくよ」って言ってたけど、ちょっと先に別の話をさせてね。',
        r'前回{size_hint}というpropertyを使ったのは覚えているかな？',
    ):
        await speak(line)

    async with fade_transition(left_code):
        left_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: .5, 1
            ''')
    await trio.sleep(.5)
    await speak(
        r'このpropertyは要素二つの{list}なわけなんだけど、'
        r'これへの値の設定の仕方には次のようなやり方もあるんだ。',
    )

    async with fade_transition(right_code):
        right_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint_x: .5
                    size_hint_y: 1
            ''')
    await trio.sleep(.5)
    for line in (
        r'この右側のcodeは左側と完全に等価だよ。',
        r'{size_hint}の二つの要素の内の片方しか書き換えたくない時なんかは右側の方法を使うことになるよ。',
        r'このような関係のpropertyは他にも沢山あってよく使うからここで幾つか覚えてほしいんだ。',
        r'といってもどれも名前から連想しやすい物ばかりだから難しくはないよ。',
        r'まずは{size}',
    ):
        await speak(line)

    async with fade_transition(left_code, right_code):
        left_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    size: 100, 50
            ''')
        right_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: 100
                    height: 50
            ''')
    await trio.sleep(.5)
    for line in (
        r'さっきと同じで右側のcodeは左側と完全に等価だよ。',
        r'ここで示したいのはあくまで{size}の二つの要素を個別に設定するpropertyとして{width}と{height}'
        r'があるって事なので、{size}が何者なのかは気にしないでね',
        r'次は{pos}',
    ):
        await speak(line)

    async with fade_transition(left_code, right_code):
        left_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    pos: 20, 30
            ''')
        right_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    x: 20
                    y: 30
            ''')
    await trio.sleep(.5)
    await speak(r'そして{center}')

    async with fade_transition(left_code, right_code):
        left_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    center: 100, 50
            ''')
        right_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    center_x: 100
                    center_y: 50
            ''')
    await trio.sleep(.5)
    await speak(r'そして{pos_hint}にも同じ事が言えるよ。')

    async with fade_transition(left_code, right_code):
        left_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    pos_hint: {'x': .3, 'y': .6, }
            ''')
        right_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    pos_hint: {'pos': (.3, .6), }
            ''')
    await trio.sleep(.5)
    await speak(r'.')

    async with fade_transition(left_code, right_code):
        left_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    pos_hint: {'center_x': .3, 'center_y': .6, }
            ''')
        right_code.text = dedent('''
            FloatLayout:
                Button:
                    text: 'Button'
                    pos_hint: {'center': (.3, .6), }
            ''')
    await trio.sleep(1)
    for line in (
        r'どう？そんなにややこしくなかったでしょ？',
        r'それじゃあbyebye',
    ):
        await speak(line)

    switcher.ask_to_switch('menu')


def _finalize_text(text):
    return text.format(**_format_kwargs)


_format_kwargs = {
    key: rf"[color=BBBB00]{key}[/color]"
    for key in (
        'size_hint', 'pos_hint', 'list', 'pos',
        'size', 'width', 'height', 'center',
    )
}


@asynccontextmanager
async def fade_transition(*widgets):
    from triohelper.kivy_awaitable import animate
    first_one = widgets[0]
    bind_uids = [
        first_one.fbind('opacity', w.setter('opacity'))
        for w in widgets[1:]
    ]
    try:
        await animate(first_one, opacity=0, d=.4)
        yield
        await animate(first_one, opacity=1, d=.4)
    finally:
        first_one.opacity = 1
        for uid in bind_uids:
            first_one.unbind_uid('opacity', uid)
