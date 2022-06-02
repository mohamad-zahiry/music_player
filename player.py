import vlc


class Player:
    def __init__(self):
        self.player = vlc.MediaPlayer()

    def __getattribute__(self, name: str):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return self.player.__getattribute__(name)

    def set_audio(self, path):
        media = vlc.Media(path)
        self.player.set_media(media)

    def set_equalizer(self, n: int):
        p_equalizer = vlc.AudioEqualizer()
        p_equalizer.set_preamp(n)
        self.player.set_equalizer(p_equalizer)

    def get_position_percent(self):
        if self.player.is_playing():
            return round(self.player.get_position() * 100)
        return 0
