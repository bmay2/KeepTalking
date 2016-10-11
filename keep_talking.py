from array import array
import argparse
import pyaudio
import sys
import time
import wave

def listen(session_length, max_silence, audio):
    p = pyaudio.PyAudio()

    CHUNK_SIZE = 1024
    FORMAT = pyaudio.paInt16
    RATE = 44100
    stream_in = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        output=True,
        frames_per_buffer=CHUNK_SIZE
    )

    alert_count = 0
    r = array('h')
    alert_time = time.time()+max_silence
    session_end_time = time.time()+session_length
    while time.time() < session_end_time:
        snd_data = array('h', stream_in.read(CHUNK_SIZE))
        if sys.byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        threshold = 5000
        is_silent = max(snd_data) < threshold
        if is_silent:
            should_alert = time.time() >= alert_time
            if should_alert:
                alert(p, audio, CHUNK_SIZE)
                alert_count += 1

                stream_in = p.open(
                    format=FORMAT,
                    channels=1,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK_SIZE
                )

                alert_time = time.time()+max_silence
            #else: print(alert_time-time.time())
        else:
            alert_time = time.time()+max_silence
            #print("Keep talking through your thought process!")
    return alert_count

def alert(p, audio, CHUNK_SIZE):
    wf = wave.open(audio, 'rb')
    stream_out = p.open(
        format = p.get_format_from_width(wf.getsampwidth()),
        channels = wf.getnchannels(),
        rate = wf.getframerate(),
        output = True
    )

    data = wf.readframes(CHUNK_SIZE)
    while data:
        stream_out.write(data)
        data = wf.readframes(CHUNK_SIZE)
    stream_out.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--session_length", type=int, default=1800)
    parser.add_argument("-s", "--max_silence", type=int, default=5)
    parser.add_argument("-a", "--audio", default='audio_files/ahem_x.wav')
    args = parser.parse_args()
    alert_count = listen(args.session_length, args.max_silence, args.audio)
    print("You were too silent {0} time(s) during your {1} second session."
        .format(alert_count, args.session_length))