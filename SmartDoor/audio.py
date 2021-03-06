from audioapi import *
import io
from pydub import AudioSegment
from pydub.playback import play

def playsound(input_str, voice):
    print(f'*playsound: {input_str}')

    ret, data = tts(input_str, voice)
    if ret:
        sound = io.BytesIO(data)
        song = AudioSegment.from_mp3(sound)
        play(song)
    else:
        print(data)
