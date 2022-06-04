import os


class PlayList:
    def __init__(self) -> None:
        self.songs = []
        self.songs_paths = []
        self.cur_song = 0

    def add_music(self, path):
        base_name = os.path.basename(path)
        self.songs.append(base_name)
        self.songs_paths.append(path)

    def next(self):
        if self.cur_song >= len(self.songs) - 1:
            self.cur_song = 0
        else:
            self.cur_song += 1

        return (self.songs[self.cur_song], self.songs_paths[self.cur_song])

    def previous(self):
        if self.cur_song <= 0:
            self.cur_song = len(self.songs) - 1
        else:
            self.cur_song -= 1

        return (self.songs[self.cur_song], self.songs_paths[self.cur_song])

    def get_song(self, no):
        self.cur_song = no
        return (self.songs[self.cur_song], self.songs_paths[self.cur_song])

    def get_all_songs(self):
        return list(zip(self.songs, self.songs_paths))
