from contextlib import asynccontextmanager

KV_CODE = r'''
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
    import kivy_tutorial.widgets.dialogue

    appstate.bgm = ''

    with activate_nursery(nursery):
        root = Builder.load_string(KV_CODE)
    parent.add_widget(root)
    task_status.started()
    await trio.sleep(1)

    dialogue = root

    async def speak(text):
        return await dialogue.speak(_finalize_text(text), markup=True)

    for line in (
        r'大家好、Layout基礎編担当のservalだよ。',
        r'ここではLayoutの中で最も仕組みが単純な{FloatLayout}を使ってLayoutの基礎を学んでいくよ。',
        r'Kivyを始めたばかりの時につまづきやすい点ばかりなので絶対に跳ばさないでね。',
    ):
        await speak(line)


    switcher.ask_to_switch('menu')


def _finalize_text(text):
    return text.format(**_format_kwargs)


_format_kwargs = {
    key: rf"[color=BBBB00]{key}[/color]"
    for key in (
        'FloatLayout',
    )
}
