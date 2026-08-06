import speech_recognition as sr
from mutagen.mp3 import MP3
from pathlib import Path
from pydub import AudioSegment

p = Path("testdata/audio/my-real-voice1.mp3")
audio_info = MP3(p)
duration = audio_info.info.length
print(f"Duration of my-real-voice1.mp3: {duration:.2f} seconds")

sound = AudioSegment.from_mp3(p)
wav_path = Path("testdata/audio/my-real-voice1.wav")
sound.export(wav_path, format="wav")

r = sr.Recognizer()
with sr.AudioFile(str(wav_path)) as source:
    audio_data = r.record(source)

print("--- Attempting Speech Recognition ---")
try:
    text_bn = r.recognize_google(audio_data, language="bn-BD")
    print(f"Recognized Bengali Speech: '{text_bn}'")
except Exception as e:
    print("Bengali Recognition Error:", e)

try:
    text_en = r.recognize_google(audio_data, language="en-US")
    print(f"Recognized English Speech: '{text_en}'")
except Exception as e:
    print("English Recognition Error:", e)
