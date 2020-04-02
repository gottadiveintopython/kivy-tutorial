async def main(switcher, nursery, *, parent, task_status, **kwargs):
    import trio
    from kivy_tutorial.widgets.dialogue import KTDialogue

    dialogue = KTDialogue(
        nursery=nursery,
        speaker_image=r'image/catfish.png',
        speaker_voice=r'sound/speak.ogg',
        padding='20dp',
    )
    parent.add_widget(dialogue)
    task_status.started()
    await trio.sleep(.1)
    await dialogue.speak(
        text='[color=4444FF]なまず[/color]好き？',
        markup=True,
    )
    await dialogue.speak(text='そうなんだ、具体的にどこが好き？')
    await dialogue.speak(
        text='[color=FF4400]なまず[/color]好き？' * 200,
        markup=True,
    )
    switcher.ask_to_switch('menu')
