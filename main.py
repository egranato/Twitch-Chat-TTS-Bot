#!/usr/bin/env python3
import os
import re
import random
import uuid
import atexit
from twitchio.ext import commands
from gtts import gTTS
from playsound import playsound
from better_profanity import profanity
from decouple import config

# destination for tts audio files
output_folder = '.\\output'

# profanity filtering set up
custom_bad_words = []
filter_words = [
    'puppies',
    'rainbows',
    'birdies',
]
profanity.load_censor_words(custom_bad_words)

# tts process
def play_message(message):
    # generate unique identifier
    id = uuid.uuid4().hex
    file_name = output_folder + '\\' + id + '.mp3'

    # create tts file
    tts = gTTS(message)
    tts.save(file_name)

    # play tts file
    playsound(file_name)

    # delete tts file
    if os.path.exists(file_name):
        os.remove(file_name)

# twitch listener
class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        # prefix can be a callable, which returns a list of strings or a string...
        # initial_channels can also be a callable which returns a list of strings...
        super().__init__(token=config('TWITCH_TOKEN'), prefix=config('PREFIX'), initial_channels=[config('CHANNEL')])

    async def event_ready(self):
        # Notify us when everything is ready!
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        print(message.author.display_name + ": " + message.content)
        message_content = message.content

        if (profanity.contains_profanity(message_content)):
            clean_text = profanity.censor(message_content)
            replaced_text = re.sub(r"([*])\1{1,}", random.choice(filter_words), clean_text)
            play_message(replaced_text)
        else:
            play_message(message_content)

def exit_handler():
    # clean up tts files that get missed
    audio_files = os.listdir(output_folder)
    for file in audio_files:
        os.remove(output_folder + '\\' + file)

# register clean up function to run when app is killed
atexit.register(exit_handler)
# run twitch listener
bot = Bot()
bot.run()