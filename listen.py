from sys import byteorder
from array import array
from struct import pack

import pyaudio
import time
import wave

THRESHOLD = 5000 #change?
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
	return max(snd_data) < THRESHOLD

def record():
	p = pyaudio.PyAudio()
	stream_in = p.open(format=FORMAT, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

	num_silent = 0
	snd_started = False

	r = array('h')

	blow_up_time = time.time()+5
	while 1:
		snd_data = array('h', stream_in.read(CHUNK_SIZE))
		if byteorder == 'big':
			snd_data.byteswap()
		r.extend(snd_data)

		silent = is_silent(snd_data)
		if silent:
			if time.time() >= blow_up_time:
				wf = wave.open('C:/users/brand/Downloads/ahem_x.wav', 'rb')
				stream_out = p.open(format = p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(), rate = wf.getframerate(), output = True)
				data = wf.readframes(CHUNK_SIZE)
				while data:
					stream_out.write(data)
					data = wf.readframes(CHUNK_SIZE)
				stream_out.close()
				stream_in = p.open(format=FORMAT, channels=1, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK_SIZE)

				blow_up_time = time.time()+5
			else:
				print(blow_up_time-time.time())
		else:
			blow_up_time = time.time()+5
			print("Talk through your thought process")

if __name__ == '__main__':
	record()