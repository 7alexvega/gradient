import requests
import spotipy

from config import config


class Spotify:
    def __init__(self):
        self.oath = spotipy.SpotifyOAuth(
            client_id=config['spotify']['client_id'],
            client_secret=config['spotify']['client_secret'],
            redirect_uri=config['spotify']['redirect_uri'],
            scope='user-read-currently-playing')
        self.spotify = spotipy.Spotify(auth=self.oath.get_access_token()['access_token'],
                                       auth_manager=spotipy.SpotifyOAuth())

    def get_album_art_image(self, album_art_url):
        return requests.get(album_art_url).content

    def get_current_album_art_url(self):
        if self.oath.is_token_expired(self.oath.get_cached_token()):
            self.refresh_token()

        track = self.spotify.current_user_playing_track()
        image_url = track['item']['album']['images'][0]['url']

        return image_url

    def refresh_token(self):
        refresh_token = self.oath.get_cached_token()['refresh_token']
        new_token = self.oath.refresh_access_token(refresh_token)
        self.spotify = spotipy.Spotify(auth=new_token['access_token'], auth_manager=spotipy.SpotifyOAuth())
