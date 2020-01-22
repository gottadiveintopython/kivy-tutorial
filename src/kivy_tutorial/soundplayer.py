__all__ = ('SoundPlayer', 'global_instance', )


class SoundPlayer:
    def __init__(self, *, file_prefix):
        super().__init__()
        self._sounds = {}
        self._file_prefix = file_prefix

    def play(self, file):
        from kivy.core.audio import SoundLoader
        sounds = self._sounds
        sound = sounds.get(file, None)
        if sound is None:
            sound = SoundLoader.load(f"{self._file_prefix}{file}")
            sounds[file] = sound
        elif sound.state == 'play':
            sound.stop()
        sound.play()


global_instance = SoundPlayer(file_prefix='sound/')
