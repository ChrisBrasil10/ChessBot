import speech_recognition as sr
from pocketsphinx import LiveSpeech

print("I am listenting")
for phrase in LiveSpeech():
    print(phrase)