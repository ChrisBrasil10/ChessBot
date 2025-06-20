import os
from pocketsphinx import LiveSpeech, get_model_path

speech = LiveSpeech(
    sampling_rate=16000,  # optional
    hmm=get_model_path('en-us\\en-us'),
    lm=get_model_path('en-us\\3335.lm'),
    dic=get_model_path('en-us\\3335.dic')
)

for phrase in speech:
    print(phrase)
