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
        r'ここでは画面に入り切らない数のwidgetを並べる方法を見ていくよ。',
        r'既に使い方を知っている{BoxLayout}を使うね。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 10
                    padding: 10
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .6, .6
            ''')
        tree = Builder.load_string(dedent('''
            FloatLayout:
                BoxLayout
                    id: boxlayout
                    orientation: 'vertical'
                    spacing: 10
                    padding: 10
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .6, .6
            '''))
        boxlayout = tree.ids.boxlayout.__self__
        add_border(boxlayout)
        preview.add_widget(tree)
    await trio.sleep(.5)
    for line in (
        r'いつもの様に境界線を引いたよ。',
        r'まず何も考えずに子を加えていくとどうなるのか見てみるよ。'
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                BoxLayout:
                    orientation: 'vertical'
                    spacing: 10
                    padding: 10
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .6, .6
                    Button:  #
                        text: 'A'  #
                    Button:  #
                        text: 'B'  #
                    Button:  #
                        text: 'C'  #
            ''')
    for text in 'ABC':
        magnet = AKMagnet(duration=.4)
        magnet.add_widget(Button(text=text))
        boxlayout.add_widget(magnet)
        await trio.sleep(magnet.duration + .2)
    await trio.sleep(.5)
    for line in (
        r'今のところ特に問題は無いね。',
        r'さらに続けると',
    ):
        await speak(line)

    async with fade_transition(code):
        code.lexer_name = 'python'
        code.text = dedent('''
            for text in 'DEFGHIJKLMNOPQ':
                boxlayout.add_widget(Button(text=text))
            ''')
    for text in 'DEFGHIJKLMNOPQ':
        magnet = AKMagnet(duration=.4)
        magnet.add_widget(Button(text=text))
        boxlayout.add_widget(magnet)
        await trio.sleep(magnet.duration)
    await trio.sleep(.5)
    for line in (
        r'無理やり詰め込んだせいか{Button}同士がくっついちゃってるね。',
        r'確か{BoxLayout}の子の{size_hint}が初期値のままだとこんな風に'
        r'{BoxLayout}に収まる様に縮められるんだったね。',
        r'このままだと使いづらいから{Button}の{size_hint_y}と{height}を書き換えて'
        r'常に一定の高さにしてあげるね。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            for child in boxlayout.children:
                child.size_hint_y = None
                child.height = 40
            ''')
        for child in boxlayout.children:
            child.size_hint_y = None
            child.height = 60
    await trio.sleep(.5)
    for line in (
        r'すると当然{Button}が{BoxLayout}に収まらなくなるわけだけど',
        r'こういった時の為のwidgetがあったの覚えてる？',
        r'そう、前回出てきた{ScrollView}だよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.lexer_name = 'kivy'
        code.text = dedent('''
            FloatLayout:
                ScrollView:  #
                    pos_hint: {'center_x': .5, 'center_y': .5, }  #
                    size_hint: .6, .6  #
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: 10
                        padding: 10
                        Button:
                            text: 'A'
                            size_hint_y: None
                            height: 40
                        Button:
                            text: 'B'
                            size_hint_y: None
                            height: 40
                        .
                        .
                        .
            ''')
        preview.clear_widgets()
        tree.remove_widget(boxlayout)
        tree = Builder.load_string(dedent('''
            FloatLayout:
                ScrollView:
                    id: scrollview
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .6, .6
                    canvas.before:
                        Color:
                            rgba: 0, 1, 0, .2
                        Rectangle:
                            pos: self.pos
                            size: self.size
            '''))
        scrollview = tree.ids.scrollview.__self__
        boxlayout.pos_hint = {}
        boxlayout.size_hint = (1, 1, )
        scrollview.add_widget(boxlayout)
        preview.add_widget(tree)
    await trio.sleep(.5)
    for line in (
        r'これで描画範囲を{ScrollView}内に縛ることに成功したね。(緑の領域が{ScrollView})。',
        'これで見えていない{Button}がscrollによって現れれば成功だよ。\n'
        r'実際にscrollできるか確かめてみてね。',
        r'...',
        r'できないでしょ？',
        r'原因は今{BoxLayout}が{ScrollView}にぴったりと収まっているからだよ。',
        r'はみ出てる{Button}があるのに「収まっている」ってどういう事？って思うかもしれないけど'
        r'{Button}は関係無いんだ。',
        r'{ScrollView}がscrollの時に気にするのは自分の直接の子である{BoxLayout}だけだからね。',
        r'その{BoxLayout}がどうなっているかというと破線を見れば分かる通り'
        r'{ScrollView}と同じ大きさでしょ。',
        r'だから{ScrollView}は「scrollしなくても子全体が見えているのだからscrollの必要は無し」'
        r'と判断してしまったんだ。',
        r'ここで問題なのは{Button}がいくら増えても{BoxLayout}の大きさが変わらない事だよ。',
        r'だからそうなるようにしてあげないといけないわけ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.lexer_name = 'kivy'
        code.text = dedent('''
            FloatLayout:
                ScrollView:
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .6, .6
                    BoxLayout:
                        orientation: 'vertical'
                        spacing: 10
                        padding: 10
                        size_hint_y: None  #
                        height: self.minimum_height  #
                        Button:
                            text: 'A'
                            size_hint_y: None
                            height: 40
                        Button:
                            text: 'B'
                            size_hint_y: None
                            height: 40
                        .
                        .
                        .
            ''')
    boxlayout.size_hint_y = None
    boxlayout.bind(minimum_height=boxlayout.setter('height'))
    boxlayout.height = boxlayout.minimum_height
    await trio.sleep(.5)
    for line in (
        r'{minimum_height}がまさにその為にあるようなpropertyで、'
        r'{BoxLayout}が自身の子を全て収めるのに必要な最小限の高さを表しているよ。',
        r'だからそれをそのまま{height}の値として使ってあげれば'
        r'{BoxLayout}の高さは{Button}の数に合わせて自動で伸び縮みしてくれるんだ。',
        r'これでscrollできるようになってるはずだから実際に確かめてみてね。',
        r'まとめると',
        'たくさんのwidgetを並べるには\n'
        '1. 子がむりやり押し縮められないように子の{size_hint}と{size}を弄ってあげる\n'
        '2. 子の数に合わせて親の大きさが変わるように親の{size_hint}と{size}も弄ってあげる\n'
        '3. 親を{ScrollView}の中に入れてあげれば\n'
        r'いいって事。',
        r'それじゃあこれで終わるよ、byebye。',
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
            'FloatLayout', 'Button', 'size_hint', 'BoxLayout', 'ScrollView',
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
