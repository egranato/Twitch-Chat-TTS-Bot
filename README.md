# How to use
[Install python](https://www.python.org/downloads/)

Clone this application
`git clone https://github.com/egranato/Twitch-Chat-TTS-Bot.git && cd Twitch-Chat-TTS-Bot`

Create an `.env` file
```
TWITCH_TOKEN=oauth:yourtoken
PREFIX=!
CHANNEL=yourchannel
```
(if you need help with these items look [here](https://pypi.org/project/twitchio/))

[Install pipenv](https://pypi.org/project/pipenv/)

Install required packages
`pipenv install`

Start application
`python main.py`