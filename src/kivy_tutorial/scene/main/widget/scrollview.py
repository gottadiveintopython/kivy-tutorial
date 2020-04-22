KV_CODE = r'''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        Splitter:
            sizable_from: 'right'
            max_size: self.parent.width
            RelativeLayout:
                id: preview
                canvas.before:
                    StencilPush:
                    Rectangle:
                        pos: 0, 0
                        size: self.size
                    StencilUse:
                canvas.after:
                    StencilUnUse:
                    Rectangle:
                        pos: self.pos
                        size: self.size
                    StencilPop:
        BoxLayout:
            padding: dp(10)
            ScrollView:
                KTCodeLabel:
                    id: code
                    size_hint: None, None
                    size: self.minimum_size
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
    import kivy_tutorial.widgets.basic
    import kivy_tutorial.widgets.codelabel
    import kivy_tutorial.widgets.dialogue
    from kivy_tutorial.utils import fade_transition, add_border

    appstate.bgm = ''

    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
    parent.add_widget(root)
    task_status.started()
    await trio.sleep(1)

    code = root.ids.code.__self__
    dialogue = root.ids.dialogue.__self__
    preview = root.ids.preview.__self__

    async def speak(text):
        return await dialogue.speak(_finalize_text(text), markup=True)

    for line in (
        r'{ScrollView}はwidgetが大きすぎて収まらない時にscroll操作で'
        r'隅々まで見られるようにしたいなって時に使えるwidgetだよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = dedent('''
            FloatLayout:
                ScrollView:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
            ''')
        tree = Builder.load_string(dedent('''
            FloatLayout:
                ScrollView:
                    id: scrollview
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
            '''))
        scrollview = tree.ids.scrollview.__self__
        preview.add_widget(tree)
    await trio.sleep(.5)
    for line in (
        r'これも境界の見えないwidgetの一つだからそれが分かるように線を引いてあげるね。',
    ):
        await speak(line)

    async with fade_transition(preview):
        add_border(scrollview)
    await trio.sleep(.5)
    for line in (
        r'ここに{Button}を加えてみるよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                ScrollView:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    Button:  #
                        text: 'Button'  #
                        font_size: '80sp'  #
            ''')
        button = Factory.Button(text='Button', font_size='80sp')
        scrollview.add_widget(button)
    await trio.sleep(.5)
    for line in (
        r'{Button}が{ScrollView}にぴったりと収まっているのが見てとれるね。',
        r'ちょっとこの状態で{Button}をscrollしようとしてみてくれる？',
        r'できないでしょ？',
        r'ここで{Button}の{size_hint_x}を{code}2{end}にしてみると',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                ScrollView:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    Button:
                        text: 'Button'
                        font_size: '80sp'
                        size_hint_x: 2  #
            ''')
        scrollview.remove_widget(button)
        button.size_hint_x = 2
        scrollview.add_widget(button)
    await trio.sleep(.5)
    for line in (
        r'横にscrollできるようになってるでしょ？ちょっと試してみて。',
        r'さらに{size_hint_y}も{code}2{end}にしてあげると',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                ScrollView:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    Button:
                        text: 'Button'
                        font_size: '80sp'
                        size_hint: 2, 2  #
            ''')
        scrollview.remove_widget(button)
        button.size_hint_y = 2
        scrollview.add_widget(button)
    await trio.sleep(.5)
    for line in (
        r'縦と横どちらにでもscrollできるようになってるでしょ？これも確かめておいてね。',
        '{ScrollView}は子が自身の領域に収まらない時、\n'
        '1. はみ出ている部分を描画させず\n'
        '2. scrollによって見られるように\n'
        r'してくれるんだ。',
        r'それからちょっとここで{Button}を長く押してみてくれない？。',
        r'{Button}の色が変わるまでに時間がかかるでしょ？',
        r'実は{ScrollView}を使うと普通のtouchとscrollを区別するために次のような事が起こるんだ。',
        r'{red}利用者が画面に指を触れてから{scroll_timeout}ミリ秒以内に{scroll_distance}pixel以上'
        r'動いた時にはscrollとして判断し、そうじゃなければ通常のtouchとみなす。{end}',
        r'これが{Button}の反応が遅れてしまった原因なんだ。試しに{scroll_timeout}を小さくしてみると',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                ScrollView:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    scroll_timeout: 100 #
                    Button:
                        text: 'Button'
                        font_size: '80sp'
                        size_hint: 2, 2
            ''')
        scrollview.scroll_timeout = 100
    await trio.sleep(.5)
    for line in (
        r'{Button}の反応は良くなった反面scrollしづらいでしょ？実際に確かめてね。',
        r'このpropertyは特に理由が無い限り初期値のままが良いと思うよ。',
        r'あと今回は{ScrollView}の子として大きな{Button}を使ったわけだけど、実際の開発では'
        r'{BoxLayout}や{GridLayout}を使う事が多いよ。',
        r'そうする事で画面に収まりきらない数のwidgetをscroll操作によって見られるようにするわけ。',
        r'そこで次回からはそんな感じのより実用的な使い方を見ていくね、byebye',
    ):
        await speak(line)

    switcher.ask_to_switch('menu')


def _finalize_text(text):
    return text.format(**_format_kwargs)


_format_kwargs = {
    'code': '[color=8888FF]',
    'red': '[color=FF6666]',
    'end': '[/color]',
    **{
        key: rf"[color=BBBB00]{key}[/color]"
        for key in (
            'FloatLayout', 'Button', 'size_hint_x', 'size_hint_y',
            'BoxLayout', 'ScrollView', 'scroll_distance', 'scroll_timeout', 'GridLayout',
        )
    }
}
