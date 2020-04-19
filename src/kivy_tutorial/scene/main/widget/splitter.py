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
    # from asynckivy.uix.magnet import AKMagnet
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
        r'{Splitter}ちょっと面白いwidgetだよ。',
        r'だってsplitが"割る"や"裂く"のような意味なのにその意味に沿った働きをしていないからね。',
        r'それじゃあ一体何をするwidgetなのか、これから見ていくよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = dedent('''
            FloatLayout:
                Splitter:
                    pos_hint: {'x': .1, 'y': .1, }
                    size_hint: None, None
                    sizable_from: 'right'
                    Button:
                        text: 'Button'
            ''')
        tree = Builder.load_string(dedent('''
            FloatLayout:
                Splitter:
                    id: splitter
                    pos_hint: {'x': .1, 'y': .1, }
                    size_hint: None, None
                    sizable_from: 'right'
                    Button:
                        text: 'Button'
            '''))
        splitter = tree.ids.splitter.__self__
        preview.add_widget(tree)
    await trio.sleep(.5)
    for line in (
        r'{Splitter}に{Button}を加えたところだよ。',
        r'いつものように{Splitter}自身の領域が見て分かるように境界線を引いてあげるね。'
    ):
        await speak(line)

    async with fade_transition(preview):
        add_border(splitter)
    await trio.sleep(.5)
    for line in (
        r'子である{Button}ととなりに並んでいる{棒}を合わせた物が{Splitter}自身の領域になっているのが分かるね。',
        r'ちょっとこの{棒}をdragしてみてくれる？',
        r'{Button}の幅を伸縮できるでしょ？',
        r'{red}{Splitter}は子に{棒}を取り付けてその{棒}を動かす事で子を伸縮できるようにするんだ。{end}',
        r'{棒}の位置は上下左右のいずれかを選べて、例えば上に取り付けると',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Splitter:
                    pos_hint: {'x': .1, 'y': .1, }
                    size_hint: None, None
                    sizable_from: 'top'  #
                    Button:
                        text: 'Button'
            ''')
        splitter.sizable_from = 'top'
    await trio.sleep(.5)
    for line in (
        r'{Button}を縦に伸縮できるようになるよ。{棒}を動かして確かめてみてね。',
        r'実はこれが{Splitter}の機能の全てなんだ。',
        r'ね？何も裂いてないでしょ？',
        'じゃあ何で"{Splitter}"っていう名前が付いてるかというと\nとあるwidget'
        'と組み合わせて使うことで\n裂いているように見せかけられるからだよ、多分。'
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Splitter:
                        sizable_from: 'right'
                        min_size: self.parent.width * .2
                        max_size: self.parent.width * .8
                        Button:
                            text: 'A'
                    Button:
                        text: 'B'
            ''')
        tree = Builder.load_string(dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Splitter:
                        id: splitter
                        sizable_from: 'right'
                        min_size: self.parent.width * .2
                        max_size: self.parent.width * .8
                        Button:
                            text: 'A'
                    Button:
                        text: 'B'
            '''))
        add_border(tree.ids.splitter)
        preview.add_widget(tree)
    await trio.sleep(.5)
    for line in (
        r'それが{BoxLayout}。',
        r'まあ"裂く"というよりは"drag可能な境界を作る"と言ったほうが正しいと思うけどね。',
        r'ともかくたったこれだけのcodeでdrag可能な境界を作れるのは便利だね。',
        r'ここで「{Splitter}とBの{size_hint_x}が共に{code}1{end}のはずなのに'
        r'{Splitter}とBの幅の比が{code}1:1{end}に固定されていないのはおかしい」'
        r'と思った人は鋭いよ。',
        r"実は{Splitter}は{sizable_from}が{code}'right'{end}または{code}'left'{end}"
        r"のとき自身の{size_hint_x}を自動で{code}None{end}にするし、"
        r"{sizable_from}が{code}'top'{end}または{code}'bottom'{end}"
        r"のとき自身の{size_hint_y}を自動で{code}None{end}にするんだ。",
        r'つまり何も書かなくても今{size_hint_x}はこうなってるって事。'
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Splitter:
                        sizable_from: 'right'
                        min_size: self.parent.width * .2
                        max_size: self.parent.width * .8
                        # size_hint_x: None
                        Button:
                            text: 'A'
                    Button:
                        text: 'B'
            ''')
    await trio.sleep(.5)
    for line in (
        r'基本{Splitter}を{BoxLayout}の中に入れて使う時は{Splitter}の{size_hint}'
        r'を触る必要は無いって覚えておけば大丈夫だよ。',
        r'そして{min_size}と{max_size}だけど、これらは{Splitter}の大きさの最小と最大を定めているよ。',
        r'細かく言うと'
        r"{sizable_from}が{code}'right'{end}または{code}'left'{end}"
        r"の場合は{Splitter}の{red}幅{end}の最大と最小を定めるし、",
        r"{sizable_from}が{code}'top'{end}または{code}'bottom'{end}"
        r"の場合は{Splitter}の{red}高さ{end}の最大と最小を定めるよ。",
        r"{Splitter}の大きさの最小と最大を定める事で結果として{棒}の可動域を定める事になるから、"
        r"むしろその為にあると言った方が良いね。",
        r'.',
        r'最後にまとめると',
        '1. {Splitter}自体は何も裂かない。\n'
        '2. ただ子を伸縮可能にしているだけ。\n'
        '3. でも{BoxLayout}と組み合わせることで裂いているかの様に見せかけられる。',
        r'って事。',
        r'それじゃあこれで終わるね。',
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
            'FloatLayout', 'Button', 'size_hint_x', 'size_hint_y', 'Splitter',
            'BoxLayout', '棒', 'sizable_from', 'size_hint', 'min_size', 'max_size',
        )
    }
}
