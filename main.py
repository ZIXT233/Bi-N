import sys
import wave
import numpy
import struct
import pyaudio
import threading
import subprocess

def mp3_to_wav(mp3_file):
    mpg123_command = 'mpg123 -w "%s" -r 10000 -m "%s"'
    out_file_name = mp3_file[:-4]+'.wav'
    cmd = mpg123_command % (out_file_name, mp3_file)
    temp = subprocess.call(cmd, shell=True)
    return out_file_name

def play(file):
    CHUNK = 1024
    file.rewind()
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(file.getsampwidth()),
        channels=file.getnchannels(),
            rate=file.getframerate(),
            output=True)

    data = file.readframes(CHUNK)
    while data != '':
        stream.write(data)
        data = file.readframes(CHUNK)

    stream.stop_stream()
    stream.close()
    p.terminate()
    file.rewind()


try:
    mp3_file = sys.argv[1]
except IndexError:
    print("Usage: %s filename.mp3" % sys.argv[0])
    sys.exit(-1)

file_name = mp3_to_wav(mp3_file)
file = wave.open(file_name, 'rb')
play(file)

