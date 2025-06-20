import time 
from threading import Timer 

def display(msg):
    print(msg + ' ' + time.strftime('%H:%:M:%S'))

'''
def run_once():
    display('Run once: ')
    t = Timer(5, display,["Timeout:"])
    t.start()
'''

class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
        print('Done')

timer = RepeatTimer(1,display,['Repeating'])
timer.start()

print('threading started')
time.sleep(10)
print('threading finishing')
timer.cancel()

