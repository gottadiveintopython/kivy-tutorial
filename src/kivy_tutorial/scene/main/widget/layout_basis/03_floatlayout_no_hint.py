from contextlib import asynccontextmanager

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

    code = root.ids.code.__self__
    dialogue = root.ids.dialogue.__self__
    preview = root.ids.preview.__self__

    async def speak(text):
        return await dialogue.speak(_finalize_text(text), markup=True)

    for line in (
        r'今回はhint系propertyを使わない配置のやり方を見ていくよ。',
        r'なんで二種類のやり方があるのか？どう違うのか？など色々気になる点はあると思うけど、'
        r'それは僕には難しいから...{なまず先生}にでも解説を頼んでみるね。',
        r'とりあえず今は[color=FF6666]hintが使える場面ではできる限りhintを使う'
        r'[/color]とだけ覚えといて。',
        r'それじゃあ本題に入るよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = 'FloatLayout:'
        tree = Builder.load_string(dedent('''
            FloatLayout:
                size_hint: .8, .8
                pos_hint: {'center_x': .5, 'center_y': .5, }
                canvas.after:
                    Color:
                        rgb: 1, 1, 1
                    Line:
                        dash_length: 4
                        dash_offset: 8
                        rectangle: [*self.pos, *self.size, ]
            '''))
        preview.add_widget(tree)
    for line in (
        r'前々回に使った境界線付きの{FloatLayout}だよ。',
        r'その時はここで{size_hint}を使って大きさを指定していたんだったね。',
        r'今回はそれに代えて{size}を使うよ。',
        r'{size_hint}が割合による指定だったのに対し{size}ではpixel数を指定するよ。',
        r'それじゃあとりあえず幅が200pixelで高さが100pixelの{Button}を作ってみるね。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size: 200, 100
            ''')
        magnet = AKMagnet(duration=.4)
        tree.add_widget(magnet)
        tree.do_layout()
        magnet.add_widget(Factory.Button(text='Button'))
    await trio.sleep(.5)
    for line in (
        r'あれっ？{Button}の大きさが{code}200x100{end}にはとても見えないね。というか{FloatLayout}と同じだね。',
        r'実はこれは{FloatLayout}において最初につまづきやすい点の一つで',
        r'{size_hint}が有効になっている間は{size}による位置の指定ができないんだ。(厳密には少し違う)',
        r'確か{size_hint}の既定値は{code}1, 1{end}なんだったね。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size: 200, 100
                    size_hint: 1, 1
            ''')
    await trio.sleep(.5)
    for line in (
        r'これが{size}を指定したのにも関わらず{FloatLayout}と同じ大きさになってしまった原因なんだ。',
        r'じゃあどうすればいいのか？',
        r'{size_hint}を無効にすればいいんだよ。',
        r'具体的には{size_hint}に数値の代わりに{None}を入れてあげるんだ。'
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size: 200, 100
                    size_hint: None, 1
            ''')
    magnet.size_hint_x = None
    magnet.width = 200
    await trio.sleep(.5)
    for line in (
        r'{Button}の幅が{code}200{end}pixelになったね。',
        r'続いて{size_hint}の二つ目の数値も{None}にするよ。'
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size: 200, 100
                    size_hint: None, None
            ''')
    magnet.size_hint_y = None
    magnet.height = 100
    await trio.sleep(.5)
    for line in (
        r'というわけで以上のようにすれば割合ではない大きさの指定ができるのでした。',
        r'次は{size}を使いながらも割合で指定する方法を見ていくよ。',
        r'親と同じ大きさにしたいならこう',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size: self.parent.size
                    size_hint: None, None
            ''')
    magnet.size_hint = (1, 1)
    await trio.sleep(.5)
    await speak(r'幅を親の半分に、高さを親の四半分にしたいならこうだよ。')

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: self.parent.width / 2
                    height: self.parent.height / 4
                    size_hint: None, None
            ''')
    magnet.size_hint = (.5, .25)
    await trio.sleep(.5)
    for line in (
        r'次はhintを使わない位置指定のやり方を見ていくよ。',
        r'これは単に{pos}にpixel数を入れてあげるだけ。',
        r'試しに{pos}を{code}20, 0{end}とすると',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: self.parent.width / 2
                    height: self.parent.height / 4
                    size_hint: None, None
                    pos: 20, 0
            ''')
    magnet.pos = (20, 0)
    await trio.sleep(.5)
    await speak(r'{pos}を{code}20, 50{end}にすると')

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: self.parent.width / 2
                    height: self.parent.height / 4
                    size_hint: None, None
                    pos: 20, 50
            ''')
    magnet.pos = (20, 50)
    await trio.sleep(.5)
    for line in (
        r'となるよ。',
        r'実はなんだけど{FloatLayout}でこのようなやり方で位置を指定することは基本無いよ。',
        r'理由は座標の原点がどこにあるのかが分からないから。',
        r'今回は左の枠の左下が原点になってるけどこのアプリの作り方次第では'
        r'Windowの左下を原点にだってできるからね。',
        r'というわけでそんな信頼できない方法ではなくちゃんと{FloatLayout}からの'
        r'相対位置で指定する方法を紹介するね。',
        r'{Button}の左下を{FloatLayout}の左下に揃えたいならこう',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: self.parent.width / 2
                    height: self.parent.height / 4
                    size_hint: None, None
                    pos: self.parent.pos
            ''')
    magnet.pos_hint = {'pos': (0, 0, ), }
    await trio.sleep(.5)
    await speak(r'{Button}を中央揃えしたいならこう')

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: self.parent.width / 2
                    height: self.parent.height / 4
                    size_hint: None, None
                    center: self.parent.center
            ''')
    magnet.pos_hint = {'center': (.5, .5, ), }
    await trio.sleep(.5)
    await speak(r'{Button}の右上を{FloatLayout}の右上に揃えたいならこうだよ。')

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: self.parent.width / 2
                    height: self.parent.height / 4
                    size_hint: None, None
                    right: self.parent.right
                    top: self.parent.top
            ''')
    magnet.pos_hint = {'right': 1, 'top': 1, }
    await trio.sleep(.5)
    for line in (
        r'もちろん{pos_hint}の時と同じで{Button}は{FloatLayout}をはみ出しても構わないよ。',
        r'そしてこれもやはり{pos_hint}が設定されている場合はそっちが重んじられるから注意してね。',
        r"例えば{pos_hint}が{code}{{'x': 0, }}{end}だと",
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    width: self.parent.width / 2
                    height: self.parent.height / 4
                    size_hint: None, None
                    right: self.parent.right
                    top: self.parent.top
                    pos_hint: {'x': 0, }
            ''')
    magnet.pos_hint = {'x': 0, 'top': 1, }
    await trio.sleep(.5)
    for line in (
        r'という風に左寄せになってしまうよ。',
        r'それと[color=FF6666]hint系propertyはあくまで非hint系propertyを算出するためにある'
        r'[/color]っていうのも大事な点だよ。',
        r'例えば{size_hint}を使えばそれを基に算出された値が{size}に書き込まれて'
        r'それがwidgetの大きさになるし、使わなければ君が{size}に書き込んだ値が'
        r'そのままwidgetの大きさになる。',
        r'だから[color=FF6666]hintを使おうが使わまいがwidgetの現在の大きさや位置が'
        r'知りたければ常に{size}や{pos}が使える[/color]って事なんだ。',
        r'ただ一点だけ[color=FF6666]配置の計算がいつ行われるか[/color]には'
        r'気をつけないといけないけど、今言った事が事実なことに変わりはないよ。',
        r'.',
        r'それじゃあこれで終わるね、byebye'
    ):
        await speak(line)

    switcher.ask_to_switch('menu')


def _finalize_text(text):
    return text.format(**_format_kwargs)


_format_kwargs = {
    'code': '[color=8888FF]',
    'end': '[/color]',
    'None': '[color=8888FF]None[/color]',
    **{
        key: rf"[color=BBBB00]{key}[/color]"
        for key in (
            'FloatLayout', 'Button', 'size_hint', 'pos_hint', 'size', 'pos',
            'なまず先生',
        )
    }
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
