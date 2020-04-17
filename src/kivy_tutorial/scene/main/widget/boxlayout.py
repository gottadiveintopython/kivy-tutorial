KV_CODE = r'''
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        id: top_pane
        Splitter:
            sizable_from: 'right'
            max_size: 40000
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
        height: dp(200)
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
    from kivy_tutorial.widgets.basic import KTLabel
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

    async def sleep(duration=.5):
        return await trio.sleep(duration)

    async def speak(text):
        return await dialogue.speak(_finalize_text(text), markup=True)

    await speak(r'{BoxLayout}は子widgetを縦一列または横一列に並べるwidgetだよ。')

    async with fade_transition(code):
        preview.clear_widgets()
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
            ''')
        tree = Builder.load_string(dedent('''
            FloatLayout:
                BoxLayout:
                    id: layout
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
            '''))
        layout = tree.ids.layout.__self__
        preview.add_widget(tree)
    await sleep()
    await speak('これもまた境界が見えないwidgetの一つだから位置が分かるように境界線を引いてあげるね。')

    async with fade_transition(preview):
        add_border(layout)
    await sleep()
    await speak(r'そしてここに子widgetを幾つか加えてみるよ。')

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:  #
                        text: 'A'  #
            ''')
    magnet_a = AKMagnet(duration=.4)
    button_a = Factory.Button(text='A')
    magnet_a.add_widget(button_a)
    layout.add_widget(magnet_a)
    await trio.sleep(.2)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:  #
                        text: 'A'  #
                    Button:  #
                        text: 'B'  #
            ''')
    magnet_b = AKMagnet(duration=.4)
    button_b = Factory.Button(text='B')
    magnet_b.add_widget(button_b)
    layout.add_widget(magnet_b)
    await trio.sleep(.2)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:  #
                        text: 'A'  #
                    Button:  #
                        text: 'B'  #
                    Button:  #
                        text: 'C'  #
            ''')
    magnet_c = AKMagnet(duration=.4)
    button_c = Factory.Button(text='C')
    magnet_c.add_widget(button_c)
    layout.add_widget(magnet_c)
    await sleep()
    for line in (
        r'子widgetが横に並んでいるね。',
        r"{BoxLayout}には{orientation}というpropertyがあってこの値が{code}'horizontal'{end}(初期値)"
        r"だとこうなるんだ。",
        r"試しにこれを{code}'vertical'{end}にすると",
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    orientation: 'vertical'  #
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:
                        text: 'A'
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
            ''')
    layout.orientation = 'vertical'
    await sleep()
    for line in (
        r'という風に縦に並ぶよ',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:
                        text: 'A'
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
            ''')
    layout.orientation = 'horizontal'
    await sleep()
    for line in (
        r'この{BoxLayout}なんだけど',
        r'一つ不自由な点があるから先に触れておくね。',
        r'それは{red}子widgetを右から左、下から上には並べられない事{end}だよ。',
        r'横に並べる場合は必ず左から右だし、縦に並べる場合は必ず上から下なわけ。',
        r'だからもしそのような事がしたいのならpython側で子widgetの順番を裏返さない'
        r'といけないんだ、例えばこんな風にね。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.lexer_name = 'text'
        code.text = dedent('''
            def reverse_children(widget):
                children = widget.children[:]
                widget.clear_widgets()
                for child in children:
                    widget.add_widget(child)

            reverse_children(some_boxlayout)
            ''')
    reverse_children(layout)
    await sleep()
    for line in (
        r'この点さえ除けばかなり使いやすいwidgetにはなってるよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.lexer_name = 'kivy'
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:
                        text: 'A'
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
            ''')
    reverse_children(layout)
    await sleep()
    for line in (
        r'それじゃあこれから細かい配置のやり方を見ていくよ。',
        r'現在三つの{Button}が全く同じ幅になってるよね。',
        r'これはこれらの{Button}の{size_hint_x}が同じ値(初期値の{code}1{end})'
        r'だからなんだ。',
        r'試しにどれか一つに異なる値を入れてみると',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:
                        text: 'A'
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
                        size_hint_x: 2  #
            ''')
    magnet_c.size_hint_x = 2
    await sleep()
    for line in (
        r'幅が均等ではなくなるよ。',
        r'{red}{BoxLayout}が子を横に並べる時、{size_hint_x}が{code}None{end}ではない'
        r'子widget達の幅は{size_hint_x}の比になるんだ。{end}',
        'このcodeだと\n'
        'Aの{size_hint_x}が{code}1{end}\n'
        'Bの{size_hint_x}が{code}1{end}\n'
        'Cの{size_hint_x}が{code}2{end}\n'
        r'だから幅の比が{code}1:1:2{end}になったわけ。',
        r'もし{size_hint_x}が{code}None{end}の子widgetがあった場合は'
        r'その子の幅を差し引いた残りを{code}None{end}ではない子達が分け合う事になるよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    Button:
                        text: 'A'
                        size_hint_x: None  #
                        width: 100  #
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
                        size_hint_x: 2
            ''')
    magnet_a.size_hint_x = None
    magnet_a.width = 100
    await sleep()
    for line in (
        '中央のbarを動かして\n'
        '1. Aの幅が{code}100{end}pixelで固定されている事\n'
        '2. 残りの領域をBとCが{code}1:2{end}の比で分け合ってる事\n'
        r'を確かめてね。',
        r'.',
        r'それじゃあ次は{spacing}について見ていくよ。',
        r'これは子widget同士の隙間を定める物だよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10  #
                    Button:
                        text: 'A'
                        size_hint_x: None
                        width: 100
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
                        size_hint_x: 2
            ''')
    layout.spacing = 10
    await sleep()
    for line in (
        r'これでAとBの間、BとCの間にそれぞれ{code}10{end}pixelの隙間ができたよ。',
        r'このpropertyに関しては特に難しいところは無いね。次は{padding}。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10
                    padding: 20  #
                    Button:
                        text: 'A'
                        size_hint_x: None
                        width: 100
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
                        size_hint_x: 2
            ''')
    layout.padding = 20
    await sleep()
    for line in (
        r'{padding}は{BoxLayout}の端の余白を定める物なんだ。',
        r'上下左右に{code}20{end}pixelの余白ができてるのが分かるね。',
        r'これに関しては{spacing}とは違って幾つかの指定方法があるから触れておくね。',
        r'左右と上下を分けて指定したいならこう',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10
                    padding: 20, 0  # left-right, top-bottom
                    Button:
                        text: 'A'
                        size_hint_x: None
                        width: 100
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
                        size_hint_x: 2
            ''')
    layout.padding = (20, 0, )
    await sleep()
    for line in (
        r'上下左右を全て個別に指定したいならこう',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10
                    padding: 0, 10, 20, 40  # left, top, right, bottom
                    Button:
                        text: 'A'
                        size_hint_x: None
                        width: 100
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
                        size_hint_x: 2
            ''')
    layout.padding = (0, 10, 20, 40)
    await sleep()
    for line in (
        r'CSSの{padding}みたいなもんだと思うよ、多分。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10
                    padding: 10  #
                    Button:
                        text: 'A'
                        size_hint_x: None
                        width: 100
                    Button:
                        text: 'B'
                    Button:
                        text: 'C'
                        size_hint_x: 2
            ''')
    layout.padding = 10
    await sleep()
    for line in (
        r'次は子widgetの縦の長さをいじってみるね。',
        'Aの{size_hint_y}を{code}.5{end}、\n'
        'Bの{size_hint_y}を{code}1.2{end}\n'
        r'にすると',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10
                    padding: 10
                    Button:
                        text: 'A'
                        size_hint: None, .5  #
                        width: 100
                    Button:
                        text: 'B'
                        size_hint_y: 1.2  #
                    Button:
                        text: 'C'
                        size_hint_x: 2
            ''')
    magnet_a.size_hint_y = .5
    magnet_b.size_hint_y = 1.2
    await sleep()
    for line in (
        r'となるよ。',
        r'{FloatLayout}の時とは違って余白を差し引いた値が割合の基準になってるから気を付けてね。具体的には',
        r'{red}{BoxLayout}が子を横に並べる時、{size_hint_y}が{code}None{end}ではない子の縦の長さは'
        '\n\n({BoxLayout}の縦の長さ - 上下の余白) × 子の{size_hint_y}\n\n'
        r'で決まるよ。{end}',
        r'そして子の{size_hint_y}が{code}None{end}の場合は{FloatLayout}の時と同じで{height}の値がそのまま使われるよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10
                    padding: 10
                    Button:
                        text: 'A'
                        size_hint: None, .5
                        width: 100
                    Button:
                        text: 'B'
                        size_hint_y: 1.2
                    Button:
                        text: 'C'
                        size_hint: 2, None  #
                        height: 50  #
            ''')
    magnet_c.size_hint_y = None
    magnet_c.height = 50
    await sleep()
    for line in (
        r'これも特に難しいところは無いね。次は子の縦の位置の指定方法を見ていくよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .9, .5
                    spacing: 10
                    padding: 10
                    Button:
                        text: 'A'
                        size_hint: None, .5
                        width: 100
                        pos_hint: {'y': 1, }  #
                    Button:
                        text: 'B'
                        size_hint_y: 1.2
                        pos_hint: {'top': 1, }  #
                    Button:
                        text: 'C'
                        size_hint: 2, None
                        height: 50
                        pos_hint: {'center_y': .5, }  #
            ''')
    magnet_a.pos_hint = {'y': 1, }
    magnet_b.pos_hint = {'top': 1, }
    magnet_c.pos_hint = {'center_y': .5, }
    await sleep()
    for line in (
        r'これも余白を考慮する点を除けば{FloatLayout}の時と同じだね。',
        r'それじゃあこれで{BoxLayout}の解説は終わるね。',
        r'.',
        r'えっ？子を縦に並べる場合の解説がまだだって？',
        r'その場合も要領は全く同じだよ。これまでの解説に出てきた縦に関する言葉と横に関する言葉を反転させればいいだけだから。',
        r'例えばさっき出てきたこの文章',
    ):
        await speak(line)

    top_pane = root.ids.top_pane.__self__
    async with fade_transition(top_pane):
        top_pane.clear_widgets()
        top_pane.orientation = 'vertical'
        left_label = KTLabel(markup=True, valign='center')
        left_label.bind(size=left_label.setter('text_size'))
        right_label = KTLabel(markup=True, valign='center')
        right_label.bind(size=right_label.setter('text_size'))
        top_pane.add_widget(left_label)
        top_pane.add_widget(right_label)
        left_label.text = _finalize_text(dedent('''
            {red}{BoxLayout}が子を横に並べる時、{size_hint_y}が{code}None{end}ではない子の縦の長さは
            
            ({BoxLayout}の縦の長さ - 上下の余白) × 子の{size_hint_y}

            で決まるよ。{end}'''))
    await sleep()
    for line in (
        r'これはこうするだけ。',
    ):
        await speak(line)

    async with fade_transition(right_label):
        right_label.text = _finalize_text(dedent('''
            {red}{BoxLayout}が子を縦に並べる時、{size_hint_x}が{code}None{end}ではない子の横の長さは
            
            ({BoxLayout}の横の長さ - 左右の余白) × 子の{size_hint_x}

            で決まるよ。{end}'''))
    await sleep()
    for line in (
        r'ね、そのまんま入れ替わっただけでしょ？',
        r'それじゃあこれで本当に終わるよ、bye。',
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
            'FloatLayout', 'Button', 'size_hint_x', 'pos_hint', 'BoxLayout',
            'padding', 'orientation', 'spacing', 'size_hint_y', 'height',
        )
    }
}


def reverse_children(widget):
    children = widget.children[:]
    widget.clear_widgets()
    for child in children:
        widget.add_widget(child)
