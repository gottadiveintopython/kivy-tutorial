# triohelper.kivy_awaitable.eventはon_touch_xxx系のevent処理に使えない

以下のようなcodeにおいて

```python
async def main(some_widget):
    from triohelper.kivy_awaitable import event
    await event(some_widget, 'on_touch_down')
    print('押されました')  # A
    await event(some_widget, 'on_touch_up')
    print('離されました')
```

userが素早くclickした場合、A行が実行される時点で既に`on_touch_up`が発生済みになる事があるので`triohelper.kivy_awaitable.event`は使い物にならない。ただ代わりに`asynckivy`を使うことで解決できる。

# kivy.core.audio.Soundはplay()の直後にseek()できない?

使うaudio provider次第かもしれないが`play()`の直後に`seek()`しても指定した位置からは再生できない。

```python
from kivy.core.audio import SoundLoader
sound = SoundLoader.load(...)
sound.play()
sound.seek(3)  # <- 失敗する
```

ただ少し時間を置くとうまくいく

```python
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
sound = SoundLoader.load(...)
sound.play()
Clock.schedule_once(lambda __: sound.seek(3), 0.1)
```

# ShaderTransitionの不都合

ShaderTransitionによる切り替え中は後ろにあるwidgetが表示されない。

# Kivyに依存していない状態のSceneSwitcher

- b8147356f6cdbc1be0027b5441c4f3774879646f
