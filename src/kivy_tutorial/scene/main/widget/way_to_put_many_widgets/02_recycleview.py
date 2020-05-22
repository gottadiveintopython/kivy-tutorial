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
    from kivy.uix.button import Button
    from kivy.uix.scrollview import ScrollView
    from kivy.factory import Factory
    from triohelper.triouser import activate_nursery
    from asynckivy.uix.magnet import AKMagnet
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
        r'前回 たくさんのwidgetを並べる方法を話したの覚えてる？',
        r'実はなんだけどあの方法には一つ欠点があるんだ。',
        r'それはwidgetの数があまりにも多いと重くて使い物にならない事だよ。',
        r'例えば一萬個の{Button}を並べてみると',
    ):
        await speak(line)

    async with fade_transition(preview):
        preview.clear_widgets()
        tree = Builder.load_string(dedent('''
            BoxLayout
                orientation: 'vertical'
                padding: 10
                KTLabel:
                    text: 'Button生成中'
                ProgressBar:
                    id: progressbar
                    max: 10000
                    value: 0
            '''))
        progressbar = tree.ids.progressbar.__self__
        preview.add_widget(tree)

    tree = Builder.load_string(dedent('''
        ScrollView:
            BoxLayout
                id: boxlayout
                orientation: 'vertical'
                spacing: 10
                padding: 10
                size_hint_y: None
                height: self.minimum_height
        '''))
    boxlayout = tree.ids.boxlayout.__self__
    boxlayout_add_widget = boxlayout.add_widget

    n_widgets_until_sleep = 500
    for i in range(100):
        boxlayout_add_widget(Button(text=str(i), size_hint_y=None, height='40dp'))
        n_widgets_until_sleep -= 1
        if n_widgets_until_sleep == 0:
            n_widgets_until_sleep = 500
            progressbar.value = i + 1
            await trio.sleep(.1)

    async with fade_transition(preview):
        preview.clear_widgets()
        preview.add_widget(tree)
    del progressbar
    await trio.sleep(.5)
    for line in (
        '生成するのに時間はかかるし生成した後も重いでしょ？\n'
        '(scrollしたり{Button}を押したりして確かめてみてね。)',
    ):
        await speak(line)

    async with fade_transition(preview):
        boxlayout.clear_widgets()
        preview.clear_widgets()
    await trio.sleep(.5)
    for line in (
        r'だからwidgetの数を抑える工夫が要るわけ。',
        r'それが今回扱う{RecycleView}だよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = dedent('''
            RecycleView:
                viewclass: 'Button'
                data: ({'text': str(i), } for i in range(10000))
                RecycleBoxLayout:
                    orientation: 'vertical'
                    spacing: 10
                    padding: 10
                    size_hint_y: None
                    height: self.minimum_height
                    default_size_hint: 1, None
                    default_size: 0, 40
            ''')
        tree = Builder.load_string(dedent('''
            RecycleView:
                viewclass: 'Button'
                data: ({'text': str(i), } for i in range(10000))
                RecycleBoxLayout:
                    orientation: 'vertical'
                    spacing: 10
                    padding: 10
                    size_hint_y: None
                    height: self.minimum_height
                    default_size_hint: 1, None
                    default_size: 0, 40
            '''))
        rv = tree
        preview.add_widget(tree)
    await trio.sleep(.5)
    for line in (
        '画面がほとんどカクついてないでしょ？\n'
        r'(scrollしたり{Button}を押したりして確かめてみて)',
        r'{RecycleView}という名前から察した人も居ると思うけど、このwidgetは'
        r'widgetを使い回す(recycle)事でたくさん作らないようにしているよ。',
        r"例えば仮に今{code}1{end}の{Button}が見えているとして",
        r"その状態でuserが下にscrollした事で{code}1{end}を表示する必要がなくなって代わりに"
        r"{code}12{end}を表示する必要が出てきたとするでしょ。",
        r'すると{RecycleView}は{code}1{end}を表示するのに使っていたwidgetを{code}12{end}'
        r'に使ったりするわけ。',
    ):
        await speak(line)

    rv.scroll_y = 0
    await trio.sleep(.5)
    for line in (
        '画面がほとんどカクついてないでしょ？\n'
        '(scrollしたり{Button}を押したりして確かめてみて)',
        r'{RecycleView}という名前から察した人も居ると思うけど、このwidgetは'
        r'widgetを使い回す(recycle)事でたくさん作らないで済むようにしているよ。',
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
            'ScrollView', 'Button', 'size_hint', 'BoxLayout', 'RecycleView',
            'size', 'minimum_height', 'height', 'size_hint_y',
        )
    }
}


def fill_texture_in_green(label):
    from kivy.graphics import Rectangle, Color
    with label.canvas:
        Color(0, 1, 0, .2)
        rect = Rectangle()
    def update_inst(l, *args):
        rect.size = l.texture_size
        rect.pos = (
            int(l.center_x - l.texture_size[0] / 2.),
            int(l.center_y - l.texture_size[1] / 2.),
        )
    label.bind(center=update_inst, texture_size=update_inst)
    update_inst(label)
