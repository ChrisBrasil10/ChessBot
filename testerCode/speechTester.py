 #pip3 install SpeechRecognition
#speech_recognition has dependency on pyaudio! + pyaudio has dependency on portaudio
# thus:  brew install portaudio -> pip install pyaudio

#from pocketsphinx import LiveSpeech 
'''
for phrase in LiveSpeech():
    print(phrase)
'''

import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print('Speak Anything:')
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)#convert audio to text
        print('You said: {}'.format(text))

    except:
        print('Sorry could not recognize your voice')
        


'''
import os
from pocketsphinx import LiveSpeech

speech = LiveSpeech()

for phrase in speech:
    print(phrase)

'''

'''
speech = LiveSpeech(
    sampling_rate=16000,  # optional
    lm=get_model_path('en-us.lm.bin'), #what is this thing again? what does lm stand for again?
    dic=get_model_path('cmudict-en-us.dict')
)
'''

