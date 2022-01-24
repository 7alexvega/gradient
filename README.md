# Gradient

Gradient is a Python program designed to create a reactive and ambient music listening experience.


## About
Gradient works by locally observing which songs are playing on Spotify. Once it detects a song change, it reaches out to the Spotify API to retrieve the corresponding album art image and creates a wallpaper from it. Furthermore, it calculates the dominant colors present in the album art and uses the Phillips Hue API to match the lights to the dominant colors.

## Prerequisites 
  - [Create a Spotify developer account and application](https://developer.spotify.com/documentation/web-api/quick-start/), obtaining the following: `client_id`, `client_secret` and `redirect_url`
  - [Create a Hue developer user](https://developers.meethue.com/develop/get-started-2/), obtaining an authorized user api key

## Installation

Clone the repository and install requirements via pip
```bash
pip install -r requirements.txt
```
Fill in relevant fields in the `config.yml` file. All fields are required. Example below:
```bash
spotify:
  client_id: xxxxxxxxxxxxxxx
  client_secret: xxxxxxxxxxxxxxx
  redirect_uri: http://localhost:8888/callback

hue:
  bridge:
    host: 192.168.1.88
    scheme: http
    api_key: xxxxxxxxxxxxxxx
  lights:
    - 3
    - 4

image:
  extension: jpg
  background_blur_amount: 20
  wallpaper_dir: wallpapers

gradient:
  refresh_delay_s: 1
```

## Usage

```bash
python gradient.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
