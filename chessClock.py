import time 
import ChessTimer
import lcd_main as lcd
from multiprocessing import shared_memory


class ChessClock:
    def __init__(self, timecontrol='10|5'): #(30, 5)  
        slash = timecontrol.index('|')
        self.universalTime = int(timecontrol[:slash])
        self.inc = int(timecontrol[slash + 1:])
        self.timer = ChessTimer.ChessTimer()

        self.whiteTime = self.universalTime * 60 - self.inc      #to convert the seconds to minutes 
        self.blackTime = self.universalTime * 60 - self.inc
        
        #give white and black initializations 
        self.side = True #True means white is moving right now and clock is ticking rn  
        self.printing = True

        self.pressClock()
        self.pressClock()
        
        self.shm_b = shared_memory.SharedMemory(name='i_hate_this', create=False, size=10)
        print("I just ran shm b")
        print(self.shm_b.buf[0])
        #self.shm_b.buff[0]
        
    def pressClock(self): #press clock changes the sides each time 
        # the start call press clock to start as white
        print("I have pressed clock---------------------------------------------------------")
        if self.side:
            self.increment(True)
            self.timer.switch_to("Black") #after white press clock it is blacks turn to move 
        else:
            self.increment(False)
            self.timer.switch_to("White")
        self.switch_turn()

    def switch_turn(self):
        self.side = not self.side
        
    def pause(self):
        self.timer.switch_to("Pause")
        #print("swtich t o pause clapsaodijfskdfj;alsdkfj;slakdjf;alskdjf;slakjf")
        #self.switch_turn() #switch the turn to self again
        self.shm_b.buf[0] = False
        #self.working = False

    def resume(self):
        if self.side:
            self.timer.switch_to("White")
        else:
            self.timer.switch_to("Black")
        self.shm_b.buff[0] = True

    def increment(self, side):
        if side:
            self.blackTime += self.inc
        else:
            self.whiteTime += self.inc

    def convert(self, seconds): #source: https://www.geeksforgeeks.org/python-program-to-convert-seconds-into-hours-minutes-and-seconds/
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        if sec <= 0 and min <= 0 and hour <= 0:
            return 'Out of Time'
        elif min == 0:
            return seconds
        elif min < 30:
            return '%02d:%02d' % (min, sec)
        else:
            return '%d:%02d:%02d' % (hour, min, sec)

    def restart(self):
        self.timer.all_elapsed_time(reset=True)
        self.whiteTime = self.universalTime * 60
        self.blackTime = self.universalTime * 60
        self.side = True
        self.working = True

    def __repr__(self):
        timedict = self.timer.all_elapsed_time()
        wtime = round(self.whiteTime - timedict["White"], 2)
        btime = round(self.blackTime - timedict["Black"], 2)
        message = ['W:' + str(self.convert(wtime)),'B:' + str(self.convert(btime))]
        #print("W:" + str(self.convert(wtime)) + "\n" + "B:" + str(self.convert(btime)))
        return message

    def tick(self):
        while self.printing:
            print("buf is: ", self.shm_b.buf[0])

            if self.shm_b.buf[0]:
                print(self.__repr__())
                lcd.printMessage(self.__repr__())
                time.sleep(1)

    def end(self):
        self.printing = False


'''
x = ChessClock('10|3')
x.tick()

x.pressClock()
time.sleep(1)
x.end()
x.pressClock()
time.sleep(2)
x.pause_time()
time.sleep(3)
x.resume_time()
time.sleep(4)
print(x)
'''
