__all__ = ('BgmPlayer', )

from kivy.core.audio import SoundLoader
from kivyx.core.audio import Bgm


class BgmPlayer:

    def __init__(self, *, file_prefix):
        self._file_prefix = file_prefix
        self._bgms = {}
        self._current_bgm = None
        self._current_filename = None

    def _get_bgm(self, filename):
        bgms = self._bgms
        if filename not in bgms:
            bgms[filename] = Bgm(
                SoundLoader.load(f"{self._file_prefix}{filename}"),
                fade_in_duration=2.,
                fade_out_duration=1.,
                # max_volume=.5,
                )
        return bgms[filename]

    def stop(self):
        if self._current_bgm is not None:
            self._current_bgm.stop()

    def play(self, filename:str):
        cur_bgm = self._current_bgm
        cur_filename = self._current_filename
        if cur_filename == filename:
            cur_bgm.play()
            return
        if cur_bgm is not None:
            cur_bgm.stop()
        self._current_bgm = bgm = self._get_bgm(filename)
        self._current_filename = filename
        bgm.play()
