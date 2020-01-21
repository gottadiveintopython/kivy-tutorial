__all__ = ('BgmPlayer', )

import trio
from kivy_tutorial.asynchelper import animation
from kivy_tutorial.triouser import TrioUser


class Bgm:
    '''kivy.core.audio.Soundを
    
    - 再生する時は音量を徐々に上げ
    - 停止する時は音量を徐々に下げ
    - 再生の際は前回停止した位置から始める
    '''
    def __init__(self, sound):
        self.sound = sound
        self._pos = 0
        sound.loop = True

    @property
    def pos(self):
        sound = self.sound
        return self._pos if sound.state == 'stop' else sound.get_pos()

    async def stop(self):
        sound = self.sound
        if sound.state == 'stop':
            return
        await animation(sound, volume=0)
        self._pos = sound.get_pos()
        sound.stop()
        await trio.sleep(.1)

    async def play(self):
        sound = self.sound
        if sound.state == 'play':
            return
        sound.volume = 0
        sound.play()
        await trio.sleep(.1)  # play()のあと直ちにseek()はできないのでsleep()を挟む
        sound.seek(self._pos)
        await animation(sound, volume=.5)


class BgmPlayer(TrioUser):

    def __init__(self, *, file_prefix, polling_interval=2, **kwargs):
        super().__init__(**kwargs)
        self._next_file = None
        self._bgms = {}
        self._current_bgm = None
        self.nursery.start_soon(self._keep_polling, polling_interval, file_prefix)

    def stop(self):
        self._next_file = ''

    def play(self, next_file):
        self._next_file = next_file

    async def _keep_polling(self, polling_interval, file_prefix):
        from kivy.core.audio import SoundLoader
        bgms = self._bgms
        while True:
            next_file = self._next_file
            current_bgm = self._current_bgm
            await trio.sleep(polling_interval)
            if next_file is None:
                continue
            elif not next_file:
                self._next_file = None
                if current_bgm is not None:
                    await current_bgm.stop()
                    self._current_bgm = None
            else:
                self._next_file = None
                next_bgm = bgms.get(next_file, None)
                if next_bgm is None:
                    next_bgm = Bgm(SoundLoader.load(f"{file_prefix}{next_file}"))
                    bgms[next_file] = next_bgm
                if current_bgm is not None and next_bgm is not current_bgm:
                    await current_bgm.stop()
                self._current_bgm = next_bgm
                await next_bgm.play()
