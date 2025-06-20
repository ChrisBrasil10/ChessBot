import speech_recognition as sr
import threading
from chessClock import ChessClock


r = sr.Recognizer()
clock = ChessClock()
listening = True

countdown_thread = threading.Thread(target = clock.tick)
countdown_thread.start()

while listening:
    with sr.Microphone(sample_rate = 16000) as source:
        print('Speak Anything:')
        audio = None
        TIME_LIMIT = 5
        try:
            r.energy_threshold = 300
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, TIME_LIMIT, phrase_time_limit= TIME_LIMIT)
            try:
                print("recognizing......")
                data = r.recognize_google(audio) #convert audio to text
                print('I Heard: {}'.format(data))
            except:
                data = None
                print("no recognition")
        except:
            print("none here")

    print("DATA is this rn: ", data)

    if data == "terminate":
        print("terminated ")
        clock.end()
        listening = False

    if data == "pause":
        print("paused")
        clock.pause()
        
    if data == "resume":
        clock.resume()

    if data == "capture":
        clock.pressClock()


