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
    from kivyx.uix.magnet import KXMagnet
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
        r'ここでは{Label}を扱う際の肝について話すね。',
        r'それは...',
        r'[color=FF6666]LabelとLabelの持つtextureは分けて考える'
        r'[/color]だよ。',
        r'どういう事なのかこれから具体的に見ていくね。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        preview.clear_widgets()
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
            ''')
        tree = Builder.load_string(dedent('''
            FloatLayout:
                KXMagnet:
                    id: magnet
                    duration: .4
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    Label:
                        id: label
                        text: 'Label'
            '''))
        label = tree.ids.label.__self__
        magnet = tree.ids.magnet.__self__
        preview.add_widget(tree)
    await trio.sleep(.5)
    for line in (
        r'いま左の枠いっぱいに{FloatLayout}が広がっていてその中に{Label}'
        r'が置いてある状態だよ。',
        r'{Label}も{FloatLayout}と同じで境界が見えないwidgetだから'
        r'位置が分かるように境界線を引いてあげるね。',
    ):
        await speak(line)

    async with fade_transition(preview):
        add_border(label)
    await trio.sleep(.5)
    for line in (
        r'{Label}の位置は見てのとおりだね。そして"{Label}の持つtexture"なんだけど',
        r'ここにあるよ。',
    ):
        await speak(line)

    async with fade_transition(preview):
        fill_texture_in_green(label)
    await trio.sleep(.5)
    for line in (
        r'薄く{緑}を塗った部分がそう。',
        r'{texture}が文字列が収まる最小限の大きさになってるのが見てとれるね。',
        r'これが{Label}の特徴の一つなんだ。',
        r'[color=FF6666]{Label}は初期状態だと文字列が入るだけの最小限の'
        r'大きさの{texture}を作ってそこに文字列を描き、その{texture}を自身の中央に表示するんだ。[/color]',
        r'ここで文字列をもっと長くしてみると',
    ):
        await speak(line)

    async with fade_transition(preview, code):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label ' * 100  #
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
            ''')
        label.text = 'Label ' * 100
    await trio.sleep(.5)
    for line in (
        r'こんな風に{Label}自身の領域をはみ出して文字列が表示されるよ。',
        r'[color=FF6666]{Label}は必要であれば自身の大きさを超える大きさの{texture}を作るし、'
        r'{texture}は{Label}の領域をはみ出して表示される[/color]んだ。',
        r'"LabelとLabelの持つtextureは分けて考える"と言った理由はここにあるよ。',
        r'そしてこの特徴は文字列の位置揃えや折り返しをさせたい時に重要になってくるんだ。',
        r"例えば文字列を右に寄せる為に{halign}を{code}'right'{end}にしてみても",
    ):
        await speak(line)

    async with fade_transition(code, preview):
        label.text = 'Label'
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'  #
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    halign: 'right'  #
            ''')
        label.halign = 'right'
    await trio.sleep(.5)
    for line in (
        r'全然右に寄ってないでしょ？',
        r'これは[color=FF6666]{halign}が{texture}の表示位置を決めているわけじゃなく'
        r'{texture}内のどの位置に文字列を描くかを決めているから[/color]なんだ。',
        r'確か{Label}は初期状態だと文字列が入るだけの最小限の大きさの{texture}を作るんだったね。',
        r'これはつまり{texture}には文字列を寄せるだけの余白が無いって事。',
        r'だから結果が何も変わらなかったんだよ。',
        r'ここで必要なのはその余白を作ってあげること。具体的には{text_size}を書き換えてあげるんだ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    halign: 'right'
                    text_size: self.width, None  #
            ''')
        bind_uid_width = label.fbind('width', lambda label, width:
            setattr(label, 'text_size', (width, None)))
        label.text_size = (label.width, None)
    await trio.sleep(.5)
    for line in (
        r'{texture}の幅に余裕ができて文字列が右に寄ってるのが見てとれるね。',
        r'{text_size}は{texture}の大きさを制御する為の物で既定値は{code}None, None{end}だよ。',
        r'その状態だと{texture}は文字列が収まるだけの最小限の大きさになるけど、数値を入れてあげると。'
        r'{texture}は強制的にその大きさで作られるんだ。',
        r'今回の場合は{code}self.width, None{end}だから{texture}の幅は{Label}の幅と同じになって、'
        r'高さは文字列が収まるだけの最小限になっているわけ。',
        r'.',
        r'ところでこの"{text_size}"という名前に違和感を持たなかった？',
        r'たぶん文字の大きさを表すpropertyだと思った人も居ると思うんだ。',
        r'これは海外の人にとっても紛らわしい名前らしくて「名前を{text_bounding_box}'
        r'に変えないか？」といった意見も出てるくらいなんだよ。',
        r'この[u]名前から連想しづらい働きをする点[/u]には注意だね。',
        r'それともう一つ、このように{text_size}の一つ目の要素に数値を入れて{texture}の幅を固定した時の'
        r'特徴として[color=FF6666]文字列がその幅に収まらない時は自動で折り返される[/color]というのがあるよ。',
        r'試しに{Label}に長い文字列を与えてみると',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label ' * 100  #
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    halign: 'right'
                    text_size: self.width, None
            ''')
        label.text = 'Label ' * 100
    await trio.sleep(.5)
    for line in (
        r'ほら折り返されてるでしょ。ついでに中央のbarを動かして{Label}の幅を変えても折り返しが正しく機能'
        r'するのを確かめといてね。',
        r'.',
        r'というわけでこれで文字列の位置揃えや折り返しの方法が分かったね。',
        r'...',
        r'と言いたい所なんだけど一つ注意点があるよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'  #
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    halign: 'right'
                    text_size: self.width, None
            ''')
        label.text = 'Label'
    await trio.sleep(.5)
    for line in (
        r'さっきはこんな風に位置揃えをしてたんだったね。',
        r'ここで「位置揃えしたいが為にわざわざ大きめの{texture}作らないといけないのって非効率じゃない？」'
        r'と思った人は鋭いよ。',
        r'例えばここでさらに文字列を上に寄せると',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    halign: 'right'
                    valign: 'top'  #
                    text_size: self.size  #
            ''')
        label.valign = 'top'
        label.unbind_uid('width', bind_uid_width)
        del bind_uid_width
        bind_uid_size = label.fbind('size', label.setter('text_size'))
        label.text_size = label.size

    await trio.sleep(.5)
    for line in (
        r'こんなにも{texture}を無駄に使う羽目になるからね。',
        r'desktop pcであれば大した問題にはならないかもしれないけど'
        r' mobile端末やRaspberryPiのような非力なdeviceだとこれが致命的みたいなんだ。'
        r'実際teratailにこれが原因と思われる質問が幾つかあったからね。',
        r'だから無駄に大きな{texture}を作らないで位置を寄せる方法を考えないといけないわけ。',
        r'それでどうするかだけど',
        r'とりあえず{text_size}は初期値に戻すね、じゃないと{texture}は最小限の大きさにならないから',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
                    halign: 'right'
                    valign: 'top'
            ''')
        label.unbind_uid('size', bind_uid_size)
        del bind_uid_size
        label.text_size = (None, None)
    await trio.sleep(.5)
    for line in (
        r'すると{halign}と{valign}の意味は無くなるからこれらも消すね。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'center_x': .5, 'center_y': .5, }
                    size_hint: .8, .8
            ''')
        label.halign = label.property('halign').defaultvalue
        label.valign = label.property('valign').defaultvalue
    await trio.sleep(.5)
    for line in (
        r'ここからどうするかだけど',
        r'"Layout基礎編"を視た人は{FloatLayout}でどうやってwidgetを配置するのか知ってるよね？',
        r'そのやり方だとどうなるのか確かめてみるよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'right': 1, 'top': 1, }  #
                    size_hint: .8, .8
            ''')
    magnet.pos_hint = {'right': 1, 'top': 1, }
    await trio.sleep(.5)
    for line in (
        r'望む結果にはならないね。',
        r'{FloatLayout}が見ているのは{Label}であって{Label}の持つ{texture}'
        r'では無いから当然といえば当然なんだけどね。',
        r'ここからどうするか？',
        r'{Label}の大きさを{texture}の大きさに合わせてしまえばいいんだよ。',
    ):
        await speak(line)

    async with fade_transition(code):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'right': .8, 'top': .8, }  #
                    size_hint: None, None  #
                    size: self.texture_size  #
            ''')
    magnet.pos_hint = {'right': .8, 'top': .8, }
    magnet.size_hint = (None, None, )
    magnet.size = label.texture_size
    bind_uid_texture_size = label.fbind('texture_size', magnet.setter('size'))
    await trio.sleep(.5)
    for line in (
        r'はい、これで{texture}を無駄に使わずに済んだね。',
        r'.',
        r'最初からこの方法を教えて欲しかったって？',
        r'う〜ん{halign}と{valign}を使ったやり方も知っておくに越したことはないよ。',
        r'だって君がそれを使わなくても他のlibraryが使ってるからね。例えばKivyMD。',
        r'.',
        r'最後にだけど{padding}も無駄に大きな{texture}を作ることで実現しているからあまり大きな'
        r'値を入れるのは薦めないよ。',
    ):
        await speak(line)

    async with fade_transition(code, preview):
        code.text = dedent('''
            FloatLayout:
                Label:
                    text: 'Label'
                    pos_hint: {'right': .8, 'top': .8, }  #
                    size_hint: None, None  #
                    size: self.texture_size  #
                    padding: 20, 20
            ''')
        label.padding = 20, 20
    await trio.sleep(1)
    for line in (
        r'それじゃあこれで終わるね。今回言った事を抑えておけば{Label}で困る事は少ないはずだよ、byebye。',
    ):
        await speak(line)

    label.unbind_uid('texture_size', bind_uid_texture_size)
    switcher.ask_to_switch('menu')


def _finalize_text(text):
    return text.format(**_format_kwargs)


_format_kwargs = {
    'code': '[color=8888FF]',
    'end': '[/color]',
    **{
        key: rf"[color=BBBB00]{key}[/color]"
        for key in (
            'FloatLayout', 'Button', 'size_hint', 'pos_hint', 'Label',
            'texture', '緑', 'halign', 'text_size', 'text_bounding_box',
            'valign', 'padding',
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
