import ctypes
import os
import shutil

from SwSpotify import spotify, SpotifyNotRunning


class Windows:
    def __init__(self):
        self.user_wallpaper_backup_path = None
        self.powershell_path = 'C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe'
        self.get_spotify_window_title_cmd = '(Get-Process | Where-Object {$_.ProcessName -eq "Spotify"} | Select-Object MainWindowTitle).MainWindowTitle'
        self.user32 = ctypes.windll.user32
        self.save_user_wallpaper()

    def save_user_wallpaper(self):
        user_wallpaper_path = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Themes',
                                           'TranscodedWallpaper')
        if os.path.isfile(user_wallpaper_path):
            user_wallpaper_backup_path = os.path.join(os.getcwd(), 'user_wallpaper.jpg')
            shutil.copy2(user_wallpaper_path, user_wallpaper_backup_path)
            self.user_wallpaper_backup_path = user_wallpaper_backup_path

    def set_wallpaper(self, path):
        self.user32.SystemParametersInfoW(20, 0, path, 0)

    def revert_wallpaper(self):
        if self.user_wallpaper_backup_path:
            self.set_wallpaper(self.user_wallpaper_backup_path)

    def get_screen_size(self):
        return {'height': self.user32.GetSystemMetrics(1), 'width': self.user32.GetSystemMetrics(0)}

    def get_current_song(self):
        try:
            title, artist = spotify.current()
            return f"{title} - {artist}"
        except SpotifyNotRunning:
            return None
