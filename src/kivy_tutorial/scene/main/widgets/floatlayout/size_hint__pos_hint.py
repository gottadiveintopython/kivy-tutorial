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

def add_border(widget):
    from kivy.graphics import Line, Color
    with widget.canvas.after:
        Color([1, 1, 1, 1])
        line = Line(dash_length=4, dash_offset=8)
    def update_inst(w, *args):
        line.rectangle = [*w.pos, *w.size, ]
    widget.bind(pos=update_inst, size=update_inst)
    update_inst(widget)


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
        r'{FloatLayout}は子widgetを好きな所に置けるLayoutだよ。',
        r'これから使い方を見ていくね。',
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
        r'破線で囲まれている部分が{FloatLayout}だよ。',
        r'あくまで見やすくする為に破線を引いたのであって{FloatLayout}に元々はそんな物は無いから注意してね。',
        r'それじゃあここに{Button}を加えてみるよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
            ''')
        magnet = AKMagnet(duration=.4)
        tree.add_widget(magnet)
        tree.do_layout()
        magnet.add_widget(Factory.Button(text='Button'))
    await trio.sleep(.5)
    for line in (
        r'{Button}が{FloatLayout}と同じ大きさなのが見て取れるね。',
        r'これは{Button}の{size_hint}が既定で{code}(1, 1){end}になっているからだよ。',
        r'つまりはこういう事。'
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 1, 1
            ''')
    await trio.sleep(.5)
    await speak(r'試しに{size_hint}を{code}(0.5, 1){end}に変えると')

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 0.5, 1
            ''')
    magnet.size_hint_x = .5
    for line in (
        r'見ての通り{Button}の幅は{FloatLayout}の半分(0.5)になるよ。',
        r'{Button}の高さを{FloatLayout}の半分にしたい時も要領は同じだよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 0.5, 0.5
            ''')
    magnet.size_hint_y = .5
    await trio.sleep(.5)
    for line in (
        r'簡単だね。',
        r'数値は1以上でも構わないよ。',
        r'.',
        r'次は位置の指定を見ていくよ。',
        r"{Button}の左端を{FloatLayout}の左端に揃えたいなら{pos_hint}を{code}{{'x': 0}}{end}に",
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 0.5, 0.5
                    pos_hint: {'x': 0}
            ''')
    magnet.pos_hint = {'x': 0, }
    await trio.sleep(.5)
    await speak(r"{Button}の左端を{FloatLayout}の右端に揃えたいなら{pos_hint}を{code}{{'x': 1}}{end}に")

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 0.5, 0.5
                    pos_hint: {'x': 1}
            ''')
    magnet.pos_hint = {'x': 1, }
    await trio.sleep(.5)
    await speak(r"{Button}の右端を{FloatLayout}の右端に揃えたいなら{pos_hint}を{code}{{'right': 1}}{end}に")

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 0.5, 0.5
                    pos_hint: {'right': 1}
            ''')
    magnet.pos_hint = {'right': 1, }
    await trio.sleep(.5)
    await speak(r"{Button}の上端を{FloatLayout}の上端に揃えたいなら{pos_hint}を{code}{{'top': 1}}{end}に")

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 0.5, 0.5
                    pos_hint: {'right': 1, 'top': 1}
            ''')
    magnet.pos_hint = {'right': 1, 'top': 1, }
    await trio.sleep(.5)
    await speak(
        r"{Button}を{FloatLayout}の中央に置きたいなら{pos_hint}を"
        r"{code}{{'center_x': 0.5, 'center_y': 0.5}}{end}にするんだ。"
    )

    async with fade_transition(code):
        code.text = dedent(r'''
            FloatLayout:
                Button:
                    text: 'Button'
                    size_hint: 0.5, 0.5
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            ''')
    magnet.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
    await trio.sleep(.5)
    for line in (
        r'{size_hint}と比べて複雑だけど要するに',
        r'辞書の鍵として{Button}側の位置を、値として{FloatLayout}側の位置を指定しているよ。',
        "{Button}側のx座標の位置は\n{code}x 左端\ncenter_x 中央\nright 右端{end}\n",
        "{Button}側のy座標の位置は\n{code}y 下端\ncenter_y 中央\ntop 上端{end}\n",
        r"{FloatLayout}側は{code}0{end}が左端/下端、{code}1{end}が右端/上端だね。",
        r"この数値は0以下でも1以上でも構わないよ。",
        r".",
        "これでhintを使ったやり方は終わり。\n次回はhintを使わないやり方を見ていくよ、byebye。",
    ):
        await speak(line)

    switcher.ask_to_switch('menu')


def _finalize_text(text):
    return text.format(**_format_kwargs)


_format_kwargs = {
    'code': '[color=8888FF]',
    'end': '[/color]',
    **{
        key: rf"[color=BBBB00]{key}[/color]"
        for key in (
            'FloatLayout', 'Button', 'size_hint', 'pos_hint',
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
