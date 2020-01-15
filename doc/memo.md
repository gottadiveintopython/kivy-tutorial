# asynchelper.eventはon_touch_xxx系のevent処理に使えない

以下のようなcodeにおいて

```python3
async def main(some_widget):
    from kivy_tutorial.asynchelper import event
    await event(some_widget, 'on_touch_down')
    print('押されました')  # A
    await event(some_widget, 'on_touch_up')
    print('離されました')
```

userが素早くclickした場合、A行が実行される時点で既に`on_touch_up`が発生済みになる事があるので`asynchelper.event`は使い物にならない。ただ代わりに`asynckivy`を使うことで解決できる。
