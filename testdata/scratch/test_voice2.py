from pathlib import Path
import miniaudio
import wave
import speech_recognition as sr

mp3_path = Path("testdata/audio/my-real-voice1.mp3")
wav_path = Path("testdata/audio/my-real-voice1.wav")

print(f"Decoding {mp3_path}...")
decoded = miniaudio.decode_file(str(mp3_path))
print(f"Sample Rate: {decoded.sample_rate}, Channels: {decoded.nchannels}, Format: {decoded.sample_format}")

# Save to WAV format
with wave.open(str(wav_path), "wb") as wf:
    wf.setnchannels(decoded.nchannels)
    wf.setsampwidth(decoded.sample_width)
    wf.setframerate(decoded.sample_rate)
    wf.writeframes(decoded.samples)

print(f"Exported WAV to {wav_path}")

r = sr.Recognizer()
with sr.AudioFile(str(wav_path)) as source:
    audio_data = r.record(source)

print("\n================ SPEECH RECOGNITION RESULTS ================")

# Try English Recognition
try:
    text_en = r.recognize_google(audio_data, language="en-US")
    print(f"[ENGLISH RECOGNITION]: '{text_en}'")
except Exception as e:
    print("[ENGLISH ERROR]:", e)

# Try Bengali Recognition
try:
    text_bn = r.recognize_google(audio_data, language="bn-BD")
    print(f"[BENGALI RECOGNITION]: '{text_bn}'")
except Exception as e:
    print("[BENGALI ERROR]:", e)

print("============================================================\n")
