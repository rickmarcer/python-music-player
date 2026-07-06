import pygame
import threading
import time
from structures import Queue, Stack

class PlayerObserver:
    """Interface para observadores do player."""
    def on_song_start(self, song): pass
    def on_song_end(self): pass
    def on_status_change(self, status): pass

class MusicPlayer:
    """Núcleo do player de música usando Pygame e Threads."""
    def __init__(self):
        pygame.mixer.init()
        self.queue = Queue()
        self.history = Stack()
        self.current_song = None
        self.is_paused = False
        self.observers = []
        self.stop_event = threading.Event()
        self._monitor_thread = threading.Thread(target=self._monitor_playback, daemon=True)
        self._monitor_thread.start()

    def add_observer(self, observer):
        self.observers.append(observer)

    def _notify_song_start(self, song):
        for obs in self.observers: obs.on_song_start(song)

    def _notify_song_end(self):
        for obs in self.observers: obs.on_song_end()

    def play_song(self, song):
        self.stop_playback()
        self.current_song = song
        pygame.mixer.music.load(song.file_path)
        pygame.mixer.music.play()
        self.is_paused = False
        self._notify_song_start(song)
        self.history.push(song)

    def pause_resume(self):
        if self.current_song:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
            return True
        return False

    def stop_playback(self):
        pygame.mixer.music.stop()
        self.current_song = None
        self.is_paused = False

    def next_song(self):
        next_s = self.queue.dequeue()
        if next_s:
            self.play_song(next_s)
        else:
            self.stop_playback()
            self._notify_song_end()

    def set_volume(self, volume):
        """Volume de 0.0 a 1.0"""
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))

    def _monitor_playback(self):
        while not self.stop_event.is_set():
            if self.current_song and not pygame.mixer.music.get_busy() and not self.is_paused:
                # Música acabou 
                self.next_song()
            time.sleep(1)
