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
        r'最後にhint系propertyの多分最も重要な点について話して終わりにするね。',
        r'これまでの知識で{size_hint}や{pos_hint}を使えば割合による指定ができる'
        r'って事は分かってるよね？',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = dedent('''
            FloatLayout:
                Button:
                    size_hint: .5, .5
                    text: 'Button'
            ''')
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
        preview.do_layout()
        magnet = AKMagnet(size_hint=(.5, .5, ), duration=.4)
        tree.add_widget(magnet)
        tree.do_layout()
        magnet.add_widget(Factory.Button(text='Button'))
    for line in (
        r'ここで{FloatLayout}を{BoxLayout}に置き換えてみると',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            BoxLayout:
                Button:
                    size_hint: .5, .5
                    text: 'Button'
            ''')
    preview.clear_widgets()
    tree.clear_widgets()
    tree = Builder.load_string(dedent('''
        BoxLayout:
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
    preview.do_layout()
    tree.add_widget(magnet)
    for line in (
        r'こうなるんだ。',
        r'{Button}の幅がどう見ても親の半分({code}.5{end})ではないよね。',
        r'実は[color=FF6666]hint系propertyがどのような作用をするかは直接の親がなんであるか'
        r'によって変わるんだ[/color]。',
        r'だから各widgetごとに子のhint系propertyをどのように扱うのかを知る必要があるって事。',
        r'僕の知る限りは名前に"Layout"と付かないwidgetは一切自分の子のhintには興味を持たない'
        r'から、基本"Layout"の付くwidgetだけを調べとけば大丈夫なはずだよ。',
        r'.',
        r'それじゃあこれでLayout基礎編は終わるね。',
        r'後は自分の使いたいwidgetをその都度調べていくだけ。bye',
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
            'FloatLayout', 'BoxLayout', 'Button', 'size_hint', 'pos_hint',
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
