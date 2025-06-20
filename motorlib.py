#!/usr/bin/env python3
"""A python 3 library for various
 motors and servos to connect to a raspberry pi"""
# ========================= HEADER ===================================
# title             :rpiMotorlib.py
# description       :A python 3 library for various motors
# and servos to connect to a raspberry pi
# This file is for stepper motor tested on
# 28BYJ-48 unipolar stepper motor with ULN2003  = BYJMotor class
# Bipolar Nema stepper motor with L298N = BYJMotor class.
# Bipolar Nema Stepper motor TB6612FNG = BYJMotor class
# Bipolar Nema Stepper motor A4988  Driver = A4988Nema class
# Bipolar Nema Stepper motor DRV8825 Driver = A4988Nema class
# Bipolar Nema Stepper motor LV8729  Driver = A4988Nema class
# Bipolar Nema Stepper motor A3967 Easy Driver = A3967EasyNema class
# Main author       :Gavin Lyons
# Version           :See changelog at url
# url               :https://github.com/gavinlyonsrepo/RpiMotorLib
# mail              :glyons66@hotmail.com
# python_version    :3.5.3

# ========================== IMPORTS ======================
# Import the system modules needed to run rpiMotorlib.py
import sys
import time
import RPi.GPIO as GPIO

# ==================== CLASS SECTION ===============================





class StopMotorInterrupt(Exception):
    """ Stop the motor """
    pass

class BYJMotor(object):
    """class to control a 28BYJ-48 stepper motor with ULN2003 controller
    by a raspberry pi"""
    def __init__(self, name="BYJMotorX", motor_type="28BYJ"):
        self.name = name
        self.motor_type = motor_type
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.stop_motor = False

    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True

    def motor_run(self, gpiopins, wait=.001, steps=512, ccwise=False,
                  verbose=False, steptype="half", initdelay=.001):
        """motor_run,  moves stepper motor based on 7 inputs
         (1) GPIOPins, type=list of ints 4 long, help="list of
         4 GPIO pins to connect to motor controller
         These are the four GPIO pins we will
         use to drive the stepper motor, in the order
         they are plugged into the controller board. So,
         GPIO 18 is plugged into Pin 1 on the stepper motor.
         (2) wait, type=float, default=0.001, help=Time to wait
         (in seconds) between steps.
         (3) steps, type=int, default=512, help=Number of steps sequence's
         to execute. Default is one revolution , 512 (for a 28BYJ-48)
         (4) counterclockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (5) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (6) steptype, type=string , default=half help= type of drive to
         step motor 3 options full step half step or wave drive
         where full = fullstep , half = half step , wave = wave drive.
         (7) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.
        """
        if steps < 0:
            print("Error BYJMotor 101: Step number must be greater than 0")
            quit()
                
        try:
            self.stop_motor = False
            for pin in gpiopins:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, False)
            time.sleep(initdelay)

            # select step based on user input
            # Each step_sequence is a list containing GPIO pins that should be set to High
            if steptype == "half":  # half stepping.
                step_sequence = list(range(0, 8))
                step_sequence[0] = [gpiopins[0]]
                step_sequence[1] = [gpiopins[0], gpiopins[1]]
                step_sequence[2] = [gpiopins[1]]
                step_sequence[3] = [gpiopins[1], gpiopins[2]]
                step_sequence[4] = [gpiopins[2]]
                step_sequence[5] = [gpiopins[2], gpiopins[3]]
                step_sequence[6] = [gpiopins[3]]
                step_sequence[7] = [gpiopins[3], gpiopins[0]]
            elif steptype == "full":  # full stepping.
                step_sequence = list(range(0, 4))
                step_sequence[0] = [gpiopins[0], gpiopins[1]]
                step_sequence[1] = [gpiopins[1], gpiopins[2]]
                step_sequence[2] = [gpiopins[2], gpiopins[3]]
                step_sequence[3] = [gpiopins[0], gpiopins[3]]
            elif steptype == "wave":  # wave driving
                step_sequence = list(range(0, 4))
                step_sequence[0] = [gpiopins[0]]
                step_sequence[1] = [gpiopins[1]]
                step_sequence[2] = [gpiopins[2]]
                step_sequence[3] = [gpiopins[3]]
            else:
                print("Error: BYJMotor 102 : unknown step type : half, full or wave")
                print(steptype)
                quit()

            #  To run motor in reverse we flip the sequence order.
            if ccwise:
                step_sequence.reverse()

            def display_degree():
                """ display the degree value at end of run if verbose"""
                if self.motor_type == "28BYJ":
                    degree = 1.422222
                    print("Size of turn in degrees = {}".format(round(steps/degree, 2)))
                elif self.motor_type == "Nema":
                    degree = 7.2
                    print("Size of turn in degrees = {}".format(round(steps*degree, 2)))
                else:
                    # Unknown Motor type
                    print("Warning 201 : Unknown Motor Type : {}".format(self.motor_type))
                    print("Size of turn in degrees = N/A")

            def print_status(enabled_pins):
                """   Print status of pins."""
                if verbose:
                    print("Next Step: Step sequence remaining : {} ".format(steps_remaining))
                    for pin_print in gpiopins:
                        if pin_print in enabled_pins:
                            print("GPIO pin on {}".format(pin_print))
                        else:
                            print("GPIO pin off {}".format(pin_print))

            # Iterate through the pins turning them on and off.
            steps_remaining = steps
            while steps_remaining > 0:
                for pin_list in step_sequence:
                    for pin in gpiopins:
                        if self.stop_motor:
                            raise StopMotorInterrupt
                        else:
                            if pin in pin_list:
                                GPIO.output(pin, True)
                            else:
                                GPIO.output(pin, False)
                    print_status(pin_list)
                    time.sleep(wait)
                steps_remaining -= 1

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib: ")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("Error : BYJMotor 103 : RpiMotorLib  : Unexpected error:")
        else:
            # print report status if everything went well
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Motor type = {}".format(self.motor_type))
                print("Initial delay = {}".format(initdelay))
                print("GPIO pins = {}".format(gpiopins))
                print("Wait time = {}".format(wait))
                print("Number of step sequences = {}".format(steps))
                print("Size of step sequence = {}".format(len(step_sequence)))
                print("Number of steps = {}".format(steps*len(step_sequence)))
                display_degree()
                print("Counter clockwise = {}".format(ccwise))
                print("Verbose  = {}".format(verbose))
                print("Steptype = {}".format(steptype))
        finally:
            # switch off pins at end
            for pin in gpiopins:
                GPIO.output(pin, False)



class A4988Nema(object):
    """ Class to control a Nema bi-polar stepper motor with a A4988 also tested with DRV8825"""
    def __init__(self, direction_pin, step_pin, mode_pins, motor_type="A4988"):
        """ class init method 3 inputs
        (1) direction type=int , help=GPIO pin connected to DIR pin of IC
        (2) step_pin type=int , help=GPIO pin connected to STEP of IC
        (3) mode_pins type=tuple of 3 ints, help=GPIO pins connected to
        Microstep Resolution pins MS1-MS3 of IC, can be set to (-1,-1,-1) to turn off
        GPIO resolution.
        (4) motor_type type=string, help=Type of motor two options: A4988 or DRV8825
        """
        self.motor_type = motor_type
        self.direction_pin = direction_pin
        self.step_pin = step_pin
        
        self.dir_pinALT = 0
        self.step_pinALT = 0

        if mode_pins[0] != -1:
            self.mode_pins = mode_pins
        else:
            self.mode_pins = False

        self.stop_motor = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True
    
    def setALTPins(self, dir_pin, step_pin):
        self.dir_pinALT = dir_pin
        self.step_pinALT = step_pin

    def resolution_set(self, steptype):
        """ method to calculate step resolution
        based on motor type and steptype"""
        if self.motor_type == "A4988":
            resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (1, 1, 1)}
        elif self.motor_type == "DRV8825":
            resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (0, 0, 1),
                          '1/32': (1, 0, 1)}
        elif self.motor_type == "LV8729":
            resolution = {'Full': (0, 0, 0),
                          'Half': (1, 0, 0),
                          '1/4': (0, 1, 0),
                          '1/8': (1, 1, 0),
                          '1/16': (0, 0, 1),
                          '1/32': (1, 0, 1),
                          '1/64': (0, 1, 1),
                          '1/128': (1, 1, 1)}
        else:
            print("Error invalid motor_type: {}".format(self.motor_type))
            quit()

        # error check stepmode
        if steptype in resolution:
            pass
        else:
            print("Error invalid steptype: {}".format(steptype))
            quit()

        if self.mode_pins != False:
            GPIO.output(self.mode_pins, resolution[steptype])

    def motor_go(self, clockwise=False, steptype="Full",
                 steps=200, stepdelay=.005, verbose=False, initdelay=.05):
        """ motor_go,  moves stepper motor based on 6 inputs
         (1) clockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (2) steptype, type=string , default=Full help= type of drive to
         step motor 5 options
            (Full, Half, 1/4, 1/8, 1/16) 1/32 for DRV8825 only 1/64 1/128 for LV8729 only
         (3) steps, type=int, default=200, help=Number of steps sequence's
         to execute. Default is one revolution , 200 in Full mode.
         (4) stepdelay, type=float, default=0.05, help=Time to wait
         (in seconds) between steps.
         (5) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (6) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.
        """
        self.stop_motor = False
        # setup GPIO
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.output(self.direction_pin, clockwise)
        if self.mode_pins != False:
            GPIO.setup(self.mode_pins, GPIO.OUT)

        try:
            # dict resolution
            self.resolution_set(steptype)
            time.sleep(initdelay)

            for i in range(steps):
                if self.stop_motor:
                    raise StopMotorInterrupt
                else:
                    GPIO.output(self.step_pin, True)
                    time.sleep(stepdelay)
                    GPIO.output(self.step_pin, False)
                    time.sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i+1), end="\r", flush=True)

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib:")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("RpiMotorLib  : Unexpected error:")
        else:
            # print report status
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Motor type = {}".format(self.motor_type))
                print("Clockwise = {}".format(clockwise))
                print("Step Type = {}".format(steptype))
                print("Number of steps = {}".format(steps))
                print("Step Delay = {}".format(stepdelay))
                print("Intial delay = {}".format(initdelay))
                print("Size of turn in degrees = {}"
                      .format(degree_calc(steps, steptype)))
        finally:
            # cleanup
            GPIO.output(self.step_pin, False)
            GPIO.output(self.direction_pin, False)
            if self.mode_pins != False:
                for pin in self.mode_pins:
                    GPIO.output(pin, False)
                    
                    
    def motor_go_sync(self, clockwiseA=False, clockwiseB=False, steptype="Full",
             steps=200, stepdelay=.005, verbose=False, initdelay=.05):
        
        """ motor_go,  moves stepper motor based on 6 inputs
         (1) clockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (2) steptype, type=string , default=Full help= type of drive to
         step motor 5 options
            (Full, Half, 1/4, 1/8, 1/16) 1/32 for DRV8825 only 1/64 1/128 for LV8729 only
         (3) steps, type=int, default=200, help=Number of steps sequence's
         to execute. Default is one revolution , 200 in Full mode.
         (4) stepdelay, type=float, default=0.05, help=Time to wait
         (in seconds) between steps.
         (5) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (6) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.
        """
        self.stop_motor = False
        # setup GPIO
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        
        GPIO.setup(self.dir_pinALT, GPIO.OUT)
        GPIO.setup(self.step_pinALT, GPIO.OUT)
        
        GPIO.output(self.direction_pin, clockwiseA)
        GPIO.output(self.dir_pinALT, clockwiseB)
        if self.mode_pins != False:
            GPIO.setup(self.mode_pins, GPIO.OUT)

        try:
            # dict resolution
            self.resolution_set(steptype)
            time.sleep(initdelay)

            for i in range(steps):
                if self.stop_motor:
                    raise StopMotorInterrupt
                else:
                    GPIO.output(self.step_pin, True)
                    GPIO.output(self.step_pinALT, True)
                    time.sleep(stepdelay)
                    GPIO.output(self.step_pin, False)
                    GPIO.output(self.step_pinALT, False)
                    time.sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i+1), end="\r", flush=True)

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib:")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("RpiMotorLib  : Unexpected error:")
        else:
            # print report status
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Motor type = {}".format(self.motor_type))
                print("Clockwise = {}".format(clockwiseA))
                print("Step Type = {}".format(steptype))
                print("Number of steps = {}".format(steps))
                print("Step Delay = {}".format(stepdelay))
                print("Intial delay = {}".format(initdelay))
                print("Size of turn in degrees = {}"
                      .format(degree_calc(steps, steptype)))
        finally:
            # cleanup
            GPIO.output(self.step_pin, False)
            GPIO.output(self.direction_pin, False)
            GPIO.output(self.step_pinALT, False)
            GPIO.output(self.dir_pinALT, False)
            if self.mode_pins != False:
                for pin in self.mode_pins:
                    GPIO.output(pin, False)


class A3967EasyNema(object):
    """ Class to control a Nema bi-polar stepper motor with A3967 Easy driver
    motor controller """

    def __init__(self, direction_pin, step_pin, mode_pins):
        """ class init method 3 inputs
        (1) direction type=int , help=GPIO pin connected to DIR pin of IC
        (2) step_pin type=int , help=GPIO pin connected to STEP of IC
        (3) mode_pins type=tuple of 2 ints, help=GPIO pins connected to
        Microstep Resolution pins MS1-MS2 of IC, can be set to (-1,-1) to turn off
        GPIO resolution.
        """

        self.direction_pin = direction_pin
        self.step_pin = step_pin

        if mode_pins[0] != -1:
            self.mode_pins = mode_pins
        else:
            self.mode_pins = False

        self.stop_motor = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    def motor_stop(self):
        """ Stop the motor """
        self.stop_motor = True

    def motor_move(self, stepdelay=.05, steps=200, clockwise=False,
                   verbose=False, steptype="Full", initdelay=.1):
        """ motor_move,  moves stepper motor based on 6 inputs
         (1) stepdelay type=float, default=0.05, help=Time to wait
         (in seconds) between steps.
         (2) steps, type=int, default=200, help=Number of steps sequence's
         to execute. Default is 200 ,
         (3) clockwise, type=bool default=False
         help="Turn stepper counterclockwise"
         (4) verbose, type=bool  type=bool default=False
         help="Write pin actions",
         (5) steptype, type=string , default=Full help= type of drive to
         step motor 4 options
            (Full, Half, 1/4, 1/8)
         (6) initdelay, type=float, default=1mS, help= Intial delay after
         GPIO pins initialized but before motor is moved.
        """

        def ms_steps_pins():
            """ Method to handle MS pins setup """
            # dict resolution
            resolution = {'Full': (0, 0),
                          'Half': (1, 0),
                          '1/4': (0, 1),
                          '1/8': (1, 1)}
            # error check stepmode input
            if steptype in resolution:
                pass
            else:
                print("Error invalid steptype: {}".format(steptype))
                quit()

            if self.mode_pins != False:
                GPIO.output(self.mode_pins, resolution[steptype])

        # setup GPIO
        self.stop_motor = False
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.output(self.direction_pin, clockwise)

        if self.mode_pins != False:
            GPIO.setup(self.mode_pins, GPIO.OUT)

        ms_steps_pins()
        time.sleep(initdelay)

        try:
            for i in range(steps):
                if self.stop_motor:
                    raise StopMotorInterrupt
                else:
                    GPIO.output(self.step_pin, False)
                    time.sleep(stepdelay)
                    GPIO.output(self.step_pin, True)
                    time.sleep(stepdelay)
                    if verbose:
                        print("Steps count {}".format(i+1), end="\r", flush=True)

        except KeyboardInterrupt:
            print("User Keyboard Interrupt : RpiMotorLib:")
        except StopMotorInterrupt:
            print("Stop Motor Interrupt : RpiMotorLib: ")
        except Exception as motor_error:
            print(sys.exc_info()[0])
            print(motor_error)
            print("RpiMotorLib  : Unexpected error:")
        else:
            # print report status
            if verbose:
                print("\nRpiMotorLib, Motor Run finished, Details:.\n")
                print("Clockwise = {}".format(clockwise))
                print("Step Type = {}".format(steptype))
                print("Number of steps = {}".format(steps))
                print("Step Delay = {}".format(stepdelay))
                print("Intial delay = {}".format(initdelay))
                print("Size of turn in degrees = {}"
                      .format(degree_calc(steps, steptype)))
        finally:
            # cleanup
            GPIO.output(self.step_pin, False)
            GPIO.output(self.direction_pin, False)
            if self.mode_pins != False:
                for pin in self.mode_pins:
                    GPIO.output(pin, False)


def degree_calc(steps, steptype):
    """ calculate and returns size of turn in degree
    , passed number of steps and steptype"""
    degree_value = {'Full': 1.8,
                    'Half': 0.9,
                    '1/4': .45,
                    '1/8': .225,
                    '1/16': 0.1125,
                    '1/32': 0.05625,
                    '1/64': 0.028125,
                    '1/128': 0.0140625}
    degree_value = (steps*degree_value[steptype])
    return degree_value


def importtest(text):
    """ testing import """
    # print(text)
    text = " "
    
    
        
class motorSys():
    
    def __init__(self):
        
        self.motorX = A4988Nema(13, 19, (5, 5, 5), "DRV8825")
        self.motorY = A4988Nema(22, 23, (25, 25, 25), "DRV8825")
        self.motorX.setALTPins(22, 23)
        
        self.xEnablePin = 26 #Enable pin for force stopping flow of power to the x stepper motor
        self.yEnablePin = 24 # Enable pin for force stopping flow of power to the y stepper motor
        
        self.xOffset = 0
        self.yOffset = 0
        
        self.position = [0, 0]
        self.position_coord = ["h", "1"]
        
        self.EMPin = 21
        
        self.column_to_step_dict = {
            "h": 0,
            "g": 280,
            "f": 560,
            "e": 840,
            "d": 1120,
            "c": 1400,
            "b": 1680,
            "a": 1960,
            "x": 1960,
            "y": 1960
        }
        
        self.row_to_step_dict = {
            "1": 150,
            "2": 480,
            "3": 760,
            "4": 1040,
            "5": 1320,
            "6": 1600,
            "7": 1880,
            "8": 2160
        }
        
        self.column_to_spot = {
            "x": 1,
            "y": 1,
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8
        }
        
        self.spot_to_column = {
            1: "x",
            1: "y",
            1: "a",
            2: "b",
            3: "c",
            4: "d",
            5: "e",
            6: "f",
            7: "g",
            8: "h"
        }
        
        GPIO.setup(self.xEnablePin, GPIO.OUT)
        GPIO.setup(self.yEnablePin, GPIO.OUT)
        
        GPIO.setup(self.EMPin, GPIO.OUT)
        
        GPIO.output(self.xEnablePin, GPIO.HIGH)
        GPIO.output(self.yEnablePin, GPIO.HIGH)
        
        print("MotorLib Initialized!")
        
        
    def push_move(self, origin, destination, abnormal_move):
        
        if abnormal_move:
            self.abnormalMove(origin, destination)
        else:
            self.normalMove(origin, destination)
    
        
        
    def normalMove(self, origin, destination):
        
        self.move_to_square(origin)
        
        move = self.delta_coordinate(origin, destination)
        
        self.EMSet(True)
        
        time.sleep(0.5)
        
        if self.move_is_diagonal(origin, destination):
            self.just_move_diag(-move[0], -move[1])
            self.move_to_square(destination)
        else:
            self.move_to_square(destination)
            
        self.EMSet(False)
        
        
    def abnormalMove(self, origin, destination):
        
        self.move_to_square(origin)
        
        self.EMSet(True)
        
        isCapture = False
        
        self.select_best_origin_node(origin, destination)
    
        self.select_best_destination_node(origin, destination)
        
        if destination[0] == "x" or destination[0] == "y":
            if destination[0] == "x":
                self.just_move(285, 0)
            else:
                self.just_move(570, 0)
            
            if self.position[1] < self.row_to_step_dict[destination[1]]:
                self.just_move_diag(142, 142)
            else:
                self.just_move_diag(142, -142)
                
        else:
            self.move_to_square_diag(destination)
            
        self.EMSet(False)
        
            
    def move_to_square(self, destination):
        
        move = self.delta_go_to(destination)
        
        print(move)
        
        self.just_move(-move[0], -move[1])
        
    def move_to_square_diag(self, destination):
        
        move = self.delta_go_to(destination)
        
        self.just_move_diag(-move[0], -move[1])
    
    
    def move_to_steps(self, destination):
        
        move = self.delta_steps(destination)
        
        self.just_move(-move[0], -move[1])
        
        
    def select_best_origin_node(self, origin, destination):
        
        if origin[0] == "a":
            if origin[1] == "1":
                self.move_coord_to_node("a1", "b2")
            elif origin[1] == "8":
                self.move_coord_to_node("b7", "a8")
        elif origin[0] == "h":
            if origin[1] == "1":
                self.move_coord_to_node("h1", "g2")
            elif origin[1] == "8":
                self.move_coord_to_node("g7", "h8")
        else:
            o = self.coord_to_steps(origin)
            d = self.coord_to_steps(destination)
            
            if origin[1] == "1":
                
                if d[0] > o[0]:
                    self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] - 1  ], str( (int(origin[1]) + 1) ) ] )
                else:
                    self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] + 1  ], str((int(origin[1]) + 1)) ] )
            elif origin[1] == "8":
                if d[0] > o[0]:
                    self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] - 1  ], str((int(origin[1]) - 1)) ] )
                else:
                    self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] + 1 ], str((int(origin[1]) - 1)) ] )
            else:
                if d[0] >= o[0]:
                    if d[1] >= o[1]:
                        self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] - 1 ], str((int(origin[1]) + 1)) ] )
                    else:
                        self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] - 1 ], str((int(origin[1]) - 1)) ] )
                else:
                    if d[1] >= o[1]:
                        self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] + 1 ], str((int(origin[1]) + 1)) ] )
                    else:
                        self.move_coord_to_node(origin, [ self.spot_to_column[ self.column_to_spot[ origin[0] ] + 1 ], str((int(origin[1]) - 1)) ] )
                        
    def select_best_destination_node(self, origin, destination):
    
        o = self.coord_to_steps(origin)
        d = self.coord_to_steps(destination)
        
        if destination[0] == "a":
            if d[1] > o[1]:
                self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] + 1  ], str( (int(destination[1]) - 1) ) ]  )
            else:
                self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] + 1  ], str( (int(destination[1]) + 1) ) ]  )
        elif destination[0] == "h":
            if d[1] > o[1]:
                self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] - 1  ], str( (int(destination[1]) - 1) ) ]  )
            else:
                self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] - 1  ], str( (int(destination[1]) + 1) ) ]  )
        else:
            if d[0] >= o[0]:
                if d[1] >= o[1]:
                    self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] + 1  ], str( (int(destination[1]) - 1) ) ]  )
                else:
                    self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] + 1  ], str( (int(destination[1]) + 1) ) ]  )
            else:
                if d[1] >= o[1]:
                    self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] - 1  ], str( (int(destination[1]) - 1) ) ]  )           
                else:
                    self.move_to_node( destination, [ self.spot_to_column[ self.column_to_spot[ destination[0] ] - 1  ], str( (int(destination[1]) + 1) ) ]  )

            
                
    def move_to_node(self, coordA, coordB):
        
        cordA = self.coord_to_steps(coordA)
        cordB = self.coord_to_steps(coordB)
        
        #self.move_to_square(coordA)
        
        self.move_to_steps( [ round((cordA[0] + cordB[0]) / 2) , round((cordA[1] + cordB[1]) / 2) ] )
    
    def move_coord_to_node(self, coordA, coordB):
        
        cordA = self.coord_to_steps(coordA)
        cordB = self.coord_to_steps(coordB)
        
        if cordA[0] > cordB[0]:
            self.just_move_diag( round((cordA[0] - cordB[0]) / 2) , round((cordA[1] - cordB[1]) / 2) )
        else:
            self.just_move_diag( round((cordB[0] - cordA[0]) / 2) , round((cordB[1] - cordA[1]) / 2) )
        
    def just_move(self, stepX, stepY):
        
        self.enable()
    
        self.motorX.motor_go(stepX < 0, "Half", abs(stepX), 0.0009, False, 0.05)
        self.motorY.motor_go(stepY < 0, "Half", abs(stepY), 0.0009, False, 0.05)
        
        self.position = [ self.position[0] + stepX, self.position[1] + stepY ]
        
        self.disable()
        
    def just_move_diag(self, stepX, stepY):
        
        self.enable()
    
        self.motorX.motor_go_sync(stepX < 0, stepY < 0, "Half", abs(stepX), 0.0009, False, 0.05)
        
        self.position = [ self.position[0] + stepX, self.position[1] + stepY ]
        
        self.disable()
    
    
    #Coordinate input is a string (i.e. "a8")
    #Return tuple ordered (X, Y) of chess coordinate converted into motor coordinates
    def coord_to_steps(self, coordinate):
        return ( int( self.column_to_step_dict[coordinate[0]] ), int( self.row_to_step_dict[coordinate[1]] ))
    
    def getNode(self, coord):
        return ( spot_to_column[ column_to_spot[coord[0]] - 1 ], "" + ( int(coord[0]) + 1 ) )
    
    def move_is_diagonal(self, origin, destination):
        o = ( self.column_to_spot[origin[0]], int(origin[1]) )
        d = ( self.column_to_spot[destination[0]], int(destination[1]) )
        
        return abs(o[0] - d[0]) == abs(o[1] - d[1])
    
    
    def delta_coordinate(self, origin, destination):
        o = self.coord_to_steps(origin)
        d = self.coord_to_steps(destination)
        return ( o[0] - d[0], o[1] - d[1] )
    
    
    def delta_go_to(self, destination):
        d = self.coord_to_steps(destination)
        print("position:")
        print(d)
        return ( self.position[0] - d[0], self.position[1] - d[1] )
    
    
    def delta_steps(self, destination):
        return (self.position[0] - destination[0], self.position[1] - destination[1])
    
    
    def disable(self):
        GPIO.output(self.xEnablePin, GPIO.HIGH)
        GPIO.output(self.yEnablePin, GPIO.HIGH)
    
    def enable(self):
        GPIO.output(self.xEnablePin, GPIO.LOW)
        GPIO.output(self.yEnablePin, GPIO.LOW)
        
    def EMSet(self, enabled):
        GPIO.output(self.EMPin, enabled)
        
    def positionset(self, pos):
        self.position = pos
    
    def getPosition(self):
        return self.position
    
    

# ===================== MAIN ===============================


MotorSys = motorSys()
MotorSys.positionset([0, 0])
MotorSys.EMSet(False)
#MotorSys.push_move("a2", "a4", False)


#print(test.delta_coordinate("a8", "b7"))





