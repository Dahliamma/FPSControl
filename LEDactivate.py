import RPi.GPIO as GPIO
from time import sleep
class LEDactivate():
    def __init__(self,state,color):
        self.Pin_OUT1 = 27  # Red
        self.Pin_OUT2 = 26  # Blue
        self.Pin_OUT3 = 25  # Green
        self.DurOn = 5
        self.DurrOff = 3
        self.Freq = 100
        GPIO.setmode(GPIO.BCM)  # set pin mode to broadcom
        GPIO.setup(self.Pin_OUT1, GPIO.OUT)  # gpio pin 17 (physical pin 11) set to output
        GPIO.setup(self.Pin_OUT2, GPIO.OUT)  # gpio pin 17 (physical pin 11) set to output
        GPIO.setup(self.Pin_OUT3, GPIO.OUT)  # gpio pin 17 (physical pin 11) set to output
        GPIO.output(self.Pin_OUT1, False)  # LED off
        GPIO.output(self.Pin_OUT2, False)  # LED off
        GPIO.output(self.Pin_OUT3, False)  # LED off
        self.RED = GPIO.PWM(self.Pin_OUT1, self.Freq)
        self.RED.start(0)
        self.GREEN = GPIO.PWM(self.Pin_OUT2, self.Freq)
        self.GREEN.start(0)
        self.BLUE = GPIO.PWM(self.Pin_OUT3, self.Freq)
        self.BLUE.start(0)
        self.state = state
        self.color = color
        if self.state == 0:
            self.DurOn = 5
            self.DurOff = 10
            self.intensityR = 100
            self.intensityG = 100
            self.intensityB = 100
            if self.state == 0:
                    if self.color == 1:
                        while True:
                            self.RED.ChangeDutyCycle(self.intensityR)  # LED on
                            sleep(self.DurOn)
                            self.RED.ChangeDutyCycle(0)  # LED off
                            sleep(self.DurOff)

                    if self.color == 2:
                        while True:
                            self.GREEN.ChangeDutyCycle(self.intensityG)  # LED on
                            sleep(self.DurOn)  # wait 1 second
                            self.GREEN.ChangeDutyCycle(0)  # LED off
                            sleep(self.DurOff)  # wait 1 second

                    if self.color == 3:
                        while True:
                            self.RED.ChangeDutyCycle(self.intensityB)  # LED on
                            sleep(self.DurOn)  # wait 1 second
                            self.BLUE.ChangeDutyCycle(0)  # LED off
                            sleep(self.DurOff)  # wait 1 second

            self.RED.ChangeDutyCycle(0)  # LED off
            self.GREEN.ChangeDutyCycle(0)  # LED off
            self.BLUE.ChangeDutyCycle(0)  # LED off

        if self.state == 1:
                self.intensityR = 100
                self.intensityG = 100
                self.intensityB = 100
                if self.color == 1:
                    while True:
                        self.RED.ChangeDutyCycle(self.intensityR)  # LED on

                if self.color == 2:
                    while True:
                        self.GREEN.ChangeDutyCycle(self.intensityG)  # LED on

                if self.color == 3:
                    while True:
                        self.BLUE.ChangeDutyCycle(self.intensityB)  # LED on

                self.RED.ChangeDutyCycle(0)  # LED off
                self.GREEN.ChangeDutyCycle(0)  # LED off
                self.BLUE.ChangeDutyCycle(0)  # LED off

LEDtest1 = LEDactivate(0, 1)

