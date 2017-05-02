from Tkinter import *
import Tkinter as Tk
from multiprocessing import Process
import tkMessageBox
import threading
import pdb
import FPS as FPS
from collections import Counter
from time import sleep
import xlwt
import xlrd
from xlutils.copy import copy
import RPi.GPIO as GPIO


"""
Fingerprint Class

"""
class FingerPrintScanner():
    """
    FingerPrintScanner Class
    Responsible for scanning fingerprint, reporting scan status to other classes

    Args:
    """

    def __init__(self):
        self._cont = None
        self._idthread = None
        self._enthread = None
        self._status = 0
        self._status_string = None
        self._led_state = [None] * 2
        print('Starting initialization')
        self.fps = FPS.FPS_GT511C3(device_name='/dev/ttyAMA0', baud=9600, timeout=2, is_com=False)
        self.fps.UseSerialDebug = False
        print('Scanner connected')
        self._finger_number = None
        self._finger_scan_number = [None] * 10
        self._collected_scans = None
        self._true_scan_number = None
        self._enroll_check = True
        self._retry_count = 10
        self._ES1 = False
        self._ES1_2 = None
        self._ES2 = False
        self._ES2_2 = None
        self._ES3 = False
        self._ES3_2 = None
        self._idchk = False

    def finger_test(self):
        print('Begin')
        print(self.fps.IsPressFinger())
        sleep(1)
        self.fps.SetLED(True)
        print('Place finger on scanner.')
        while not self.fps.IsPressFinger():
            print('Place finger on scanner.')
            self.fps.delay(1)
            sleep(0.5)
        print('Thank you for touching me.')
        print('Capturing fingerprint.')
        self.fps.CaptureFinger(True)
        self.fps.SetLED(False)

    def custom_print(self, printed_string, state, color):
        if self._status == 0:
            Textbox_update(printed_string)
            lights.led_change(state, color)
            self._status = 1

    def reset_state(self):
        if self._status == 1:
            self._status = 0
    def EStep0(self):
        already_used_check = None
        self.fps.SetLED(True)
        sleep(1)
        self.custom_print('Beginning enrollment process.', 'blink', 'blue')
        self.reset_state()
        self.fps.Open()
        #print("BE enroll count: " + str(self.fps.GetEnrollCount()))
        i = 1
        while i < 200:
            already_used_check = self.fps.CheckEnrolled(i)
            if not already_used_check:
                self._finger_number = i
                i = 200
            else:
                i = i + 1
        #print("Attempting to enroll to ID #: " + str(self._finger_number))
        already_used_check = self.fps.EnrollStart(self._finger_number)
        #print('Already used check: '+str(already_used_check))
        if already_used_check == 0:
            return True
        else:
            return False

    def EStep1(self):
        self._ES1 = False
        self._ES1_2 = False
        while self.fps.IsPressFinger():
            self.custom_print('Remove finger momentarily.', 'blink', 'red')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        while not self.fps.IsPressFinger():
            self.custom_print('Touch the scanner for the first enrollment scan.', 'blink', 'blue')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        self.custom_print('Keep finger on scanner.', 'blink', 'green')
        self.reset_state()
        counter = 0
        while counter <=50 and not self._ES1:
            self._ES1 = self.fps.CaptureFinger(True)
            sleep(0.1)
            counter = counter + 1
        sleep(0.5)
        if self._ES1 == True:
            self._ES1_2 = self.fps.Enroll1()
            #print(str(self._ES1_2))
        if (not self._ES1 or not self._ES1_2 == 0):
            self.custom_print('Enrollment Step 1 failed. Restarting enrollment.', 'blink', 'red')
            self.reset_state()
            return False
        else:
            self.custom_print('Enrollment Step 1 Succeeded', 'steady', 'green')
            self.reset_state()
            return True

    def EStep2(self):
        self._ES2 = False
        self._ES2_2 = False
        while self.fps.IsPressFinger():
            self.custom_print('Remove finger momentarily.', 'blink', 'red')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        while not self.fps.IsPressFinger():
            self.custom_print('Touch the scanner for the second enrollment scan.', 'blink', 'blue')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        self.custom_print('Keep finger on scanner.', 'blink', 'green')
        self.reset_state()
        counter = 0
        while counter <= 50 and not self._ES2:
            self._ES2 = self.fps.CaptureFinger(True)
            sleep(0.1)
            counter = counter + 1
        sleep(0.5)
        if self._ES2 == True:
            self._ES2_2 = self.fps.Enroll2()
            #print(str(self._ES2_2))
        if (not self._ES2 or not self._ES2_2 == 0) and self._retry_count > 0:
            self.custom_print('Enrollment Step 2 failed. Restarting enrollment.', 'blink', 'red')
            self.reset_state()
            return False
        else:
            self.custom_print('Enrollment Step 2 Succeeded', 'steady', 'green')
            self.reset_state()
            return True

    def EStep3(self):
        self._ES3 = False
        self._ES3_2 = False
        while self.fps.IsPressFinger():
            self.custom_print('Remove finger momentarily.', 'blink', 'red')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        while not self.fps.IsPressFinger():
            self.custom_print('Touch the scanner for the third enrollment scan.', 'blink', 'blue')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        self.custom_print('Keep finger on scanner.', 'blink', 'green')
        self.reset_state()
        counter = 0
        while counter <= 50 and not self._ES3:
            self._ES3 = self.fps.CaptureFinger(True)
            sleep(0.1)
            counter = counter + 1
        sleep(0.5)
        if self._ES3 == True:
            # pdb.set_trace()
            # print('Before E3'+str(self.fps._serial.inWaiting()))
            self._ES3_2 = self.fps.Enroll3()
            # print('After E3: '+str(self.fps._serial.inWaiting()))
            #print(str(self._ES3_2))
        if (not self._ES3 or not self._ES3_2 == 0) and self._retry_count > 0:
            self.custom_print('Enrollment Step 3 failed. Restarting enrollment.', 'blink', 'red')
            self.reset_state()
            return False
        else:
            self.custom_print('Enrollment Step 3 Succeeded', 'steady', 'green')
            self.reset_state()
            return True

    def EStep4(self):
        sleep(0.5)
        self.fps.Open()
        AE_enroll_count = self.fps.GetEnrollCount()
        #print("AE enroll count: " + str(AE_enroll_count))
        self.fps.SetLED(False)
        sleep(0.5)

    def enroll_process(self):
        if self.EStep0():
            if self.EStep1():
                if self.EStep2():
                    if self.EStep3():
                        self.EStep4()
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

    def finger_enroll(self):
        self._enroll_check = self.enroll_process()
        while not self._enroll_check and self._retry_count > 0:
            self._retry_count = self._retry_count - 1
            self._enroll_check = self.enroll_process()
        if not self._enroll_check:
            self.custom_print('Enrollmet Failed.', 'steady', 'red')
            self.reset_state()
        else:
            self.custom_print('Enrollment Succeeded', 'steady', 'green')
            self.reset_state()
        newuser_continue()
        return self._enroll_check


    def finger_identify(self):
        self.fps.SetLED(True)
        sleep(1)
        while self.fps.IsPressFinger():
            self.custom_print('Remove finger momentarily.', 'blink', 'red')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        while not self.fps.IsPressFinger():
            self.custom_print('Place finger on scanner for identification.', 'blink', 'blue')
            self.fps.delay(1)
            sleep(0.5)
        self.reset_state()
        self.custom_print('Keep finger placed on scanner.', 'blink', 'green')
        self.reset_state()
        self.fps.Open()
        for i in range(10):
            counter = 0
            while counter <= 50 and not self._idchk:
                self._idchk = self.fps.CaptureFinger(False)
                #print(str(self._idchk)+ ' ' + str(counter))
                sleep(0.1)
                counter = counter + 1
            self._finger_scan_number[i] = self.fps.Identify1_N()
            self._idchk = False
        self.custom_print('Scan captured. You may remove your finger.', 'steady', 'green')
        self.reset_state()
        temp_scans = [None] * 5
        temp_scans[0] = self._finger_scan_number[1]
        j = 1
        for i in range(10):
            if i == 3 or i == 5 or i == 7 or i == 9:
                temp_scans[j] = (self._finger_scan_number[i])
                j += 1
        self._finger_scan_number = temp_scans
        self._collected_scans = Counter(self._finger_scan_number)
        #for j in range(5):
            #print(str(self._finger_scan_number[j]))
        self._true_scan_number = self._collected_scans.most_common(1)
        self.fps.Open()
        self.fps.SetLED(False)
        #print('Identified ID: ' + str(self._true_scan_number))
        if self._true_scan_number == 0:
            self._true_scan_number = 200
        return self._true_scan_number

class User():
    """
    User class, responsible for storing and recalling user information.
    """
    def __init__(self):
        self._first_name = None
        self._last_name = None
        self._email = None
        self._status = None
        self._strength = None
        self._volume = None
        self._working_row = None
        self._ID = None
        self._rb = xlrd.open_workbook('UserData.xls')
        self._r_sheet = self._rb.sheet_by_index(0)
        self._wb = copy(self._rb)
        self._w_sheet = self._wb.get_sheet(0)
        self._unregistered_users = [None]
        self._unregistered_rows = [None]
        self.find_unregistered()

    def user_recall(self, FPSID):
        self._ID = FPSID
        recall_check = False
        print(str(self._r_sheet.nrows))
        counter = 1
        while counter < self._r_sheet.nrows:
            print('Value: ' + str(self._r_sheet.cell(counter, 6).value))
            print('Type: ' + str(self._r_sheet.cell_type(counter, 6)))
            if int(self._r_sheet.cell_type(counter, 6)) == 2 and int(self._r_sheet.cell(counter, 6).value) == self._ID:
                self._working_row = counter
                print('Working Row: ' + str(self._working_row))
                self._first_name = str(self._r_sheet.cell(counter, 0).value)
                self._last_name = str(self._r_sheet.cell(counter, 1).value)
                self._email = str(self._r_sheet.cell(counter, 2).value)
                self._status = int(self._r_sheet.cell(counter, 5).value)
                if int(self._r_sheet.cell_type(counter, 3)) == 2:
                    self._strength = int(self._r_sheet.cell(counter, 3).value)
                else:
                    self._strength = None
                if int(self._r_sheet.cell_type(counter, 4)) == 2:
                    self._volume = int(self._r_sheet.cell(counter, 4).value)
                else:
                    self._volume = None
                counter = self._r_sheet.nrows
                recall_check = True
            else:
                counter += 1
        return recall_check

    def user_register(self, unregistered_number, FPSID):
        register_check = False
        self._ID = FPSID
        self._working_row = self._unregistered_rows[unregistered_number-1]
        self._w_sheet.write(self._working_row, 6, self._ID)
        self._w_sheet.write(self._working_row, 5, 0)
        self.user_recall(self._ID)
        self._wb.save('UserData.xls')
        return register_check

    def database_update(self):
        #Not yet implemented
        return

    def find_unregistered(self):
        j = 0
        for i in range(self._r_sheet.nrows):
            if self._r_sheet.cell_type(i, 6) == 0:
                if j == 0:
                    self._unregistered_users[j] = str(self._r_sheet.cell(i, 0).value) + ' ' + str(self._r_sheet.cell(i, 1).value)
                    self._unregistered_rows[j] = i
                    j += 1
                else:
                    self._unregistered_users.append(str(self._r_sheet.cell(i, 0).value) + ' ' + str(self._r_sheet.cell(i, 1).value))
                    self._unregistered_rows.append(i)
                    j += 1
        return self._unregistered_users

    def user_update(self, offense, new_strength, new_volume):
        change_check = [False] * 3
        new_vals = [None] * 3
        if offense:
            self._status += 1
            new_vals[2] = self._status
            change_check[2] = True
        if not new_strength == self._strength:
            self._strength = new_strength
            new_vals[0] = self._strength
            change_check[0] = True
        if not new_volume == self._volume:
            self._volume = new_volume
            new_vals[1] = self._volume
            change_check[1] = True
        for i in range(3):
            if change_check[i] and not new_vals[i] is None:
                self._w_sheet.write(self._working_row, i+3, new_vals[i])
        self._wb.save('UserData.xls')

class LEDactivate():
    def __init__(self,state,color):
        self.Pin_OUT1 = 27  # Red
        self.Pin_OUT2 = 26  # Blue
        self.Pin_OUT3 = 25  # Green
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

    def led_work(self):
        while True: #Infinite loop
            while self.state == 0: #Blinking
                if self.color == 1: #RED
                    self.BLUE.ChangeDutyCycle(0)
                    self.GREEN.ChangeDutyCycle(0)
                    for i in range (100): #Ramping up intensity to 100
                        self.RED.ChangeDutyCycle(i)
                        sleep(0.005)
                    for i in range(100): #Ramping down intensity to 0
                        self.RED.ChangeDutyCycle(100 - i)
                        sleep(0.005)
                elif self.color == 2: #GREEN
                    self.RED.ChangeDutyCycle(0)
                    self.BLUE.ChangeDutyCycle(0)
                    for i in range(100): #Ramping up intensity to 100
                        self.GREEN.ChangeDutyCycle(i)
                        sleep(0.005)
                    for i in range(100): #Ramping down intensity to 0
                        self.GREEN.ChangeDutyCycle(100 - i)
                        sleep(0.005)
                elif self.color == 3: #BLUE
                    self.RED.ChangeDutyCycle(0)
                    self.GREEN.ChangeDutyCycle(0)
                    for i in range(100): #Ramping up intensity to 100
                        self.BLUE.ChangeDutyCycle(i)
                        sleep(0.005)
                    for i in range(100): #Ramping down intensity to 0
                        self.BLUE.ChangeDutyCycle(100 - i)
                        sleep(0.005)
            while self.state == 1: #Steady on
                if self.color == 1:
                    self.GREEN.ChangeDutyCycle(0)
                    self.BLUE.ChangeDutyCycle(0)
                    self.RED.ChangeDutyCycle(100) #Setting red to 100
                    sleep(1)
                elif self.color == 2:
                    self.RED.ChangeDutyCycle(0)
                    self.BLUE.ChangeDutyCycle(0)
                    self.GREEN.ChangeDutyCycle(100) #Setting green to 100
                    sleep(1)
                elif self.color == 3:
                    self.RED.ChangeDutyCycle(0)
                    self.GREEN.ChangeDutyCycle(0)
                    self.BLUE.ChangeDutyCycle(100) #Setting blue to 100
                    sleep(1)
            while self.state == 2: #Steady off
                self.RED.ChangeDutyCycle(0)
                self.BLUE.ChangeDutyCycle(0)
                self.GREEN.ChangeDutyCycle(0)
                sleep(1) #Sleeping in off state

    def led_change(self, new_status, new_color):
        #Resetting everything to be off before changing state/color
        self.state = 2
        #Setting new color and state values
        if new_color == 'red':
            self.color = 1
        elif new_color == 'green':
            self.color = 2
        elif new_color == 'blue':
            self.color = 3
        if new_status == 'blink':
            self.state = 0
        elif new_status == 'steady':
            self.state = 1
        elif new_status == 'off':
            self.state = 2

"""
if __name__ == "__main__":
    from FingerPrintScanner import FingerPrintScanner
    test = FingerPrintScanner()
    print('1. Enroll. | 2. Identify. | 3. Enroll and Identify. | 4. DeleteAll.')
    testloop = input('Choice: ')
    if testloop == 4:
        print('Are you sure? (0=N | 1=Y)')
        del_check = input()
        if del_check == 1:
            del_check_check = False
            test.fps.Open()
            while not del_check_check:
                print('Deleteing...')
                del_check_check = test.fps.DeleteAll()
    sleep(0.5)
    if testloop == 1 or testloop == 3:
        test.finger_enroll()
    if testloop == 2 or testloop == 3:
        test.finger_identify()
"""

###
# Initialize the UI Window/Master Object
###
master = Tk.Tk() #Makes the UI window
master.wm_title("UI Drink Selection") #TItle of UI window
master.wm_attributes("-fullscreen", True)
lights = LEDactivate(0, 3) #Creating the LED object as blue, blinking initially
led_thread = threading.Thread(name='LED_Control', target=lights.led_work) #Starting led_work in the background
led_thread.start()
scanner = FingerPrintScanner()
cur_user = User()

#master.config(background = "#FFFFFF") #Background UI color

###
# UI Function Callbacks
###

#NEW USER PROTOCOL
#unregistered_users = currentuser.find_unregistered()    #Call for unregistered users

###
# DEBUG SHIT TO GET RID OF
"""
unregistered_users = [None]*50
for i in range(50):
    unregistered_users[i] = i
###
"""

xx = BooleanVar()
xx.set(False)

"""def newuser_update():
    print('Entered newuser_update')
    while scanner._enthread.is_alive():
        if scanner._status == 1:
            Textbox_update(scanner._status_string)
            lights.led_change(scanner._led_state[0], scanner._led_state[1])
            scanner._status = 2
    if scanner._enroll_check == True:
        # LED.Solid(2,3,100,100,100)   #Solid green LED for 3 sec
        index = 0
        while index == 0:
            index = Namebox.curselection()
        if index != 0:
            x = Namebox.get(ACTIVE)
            cur_user.user_register(index, scanner._finger_number)
            Textbox_update("Welcome, " + x + ".\n You can now order your drink.")
    else:
        # LED.Solid(1,3,100,100,100)   #Solid red LED for 3 sec
        tkMessageBox.showerror("Registration Failed.", "An error occurred during enrollment. Please try again.")
"""
def newuser_protocol():
    Namebox.insert(0,"Select Name...")      #Load first index as "Select Name..."
    unregistered_users = cur_user._unregistered_users
    for name in unregistered_users:     #Load up Namebox with unregistered users
        Namebox.insert(END,name)
    Namebox.select_set(0)   #Set selected value as top Namebox index: prevents mis-naming
    ans = tkMessageBox.showinfo("New User","Welcome!\nPlease follow these steps to enroll:\n\n1. Select your name from the list.\n2. Place your finger on the fingerprint scanner and follow the prompts.")
    sleep(1)
    #lights.led_change('blink', 'blue')
    scanner._enthread = threading.Thread(name='enroll', target=scanner.finger_enroll)
    scanner._enthread.start()
def newuser_continue():
    if scanner._enroll_check == True:
        # LED.Solid(2,3,100,100,100)   #Solid green LED for 3 sec
        index = 0
        Textbox_update('Please choose your name from the list to the right.')
        while index == 0:
            tuple = Namebox.curselection()
            index = tuple[0]
        if not index == 0:
            pdb.set_trace()
            cur_user.user_register(index, scanner._finger_number)
            pdb.set_trace()
            x = cur_user._first_name + ' ' + cur_user._last_name
            Textbox_update("Welcome, " + x + ".\n You can now order your drink.")
    else:
        # LED.Solid(1,3,100,100,100)   #Solid red LED for 3 sec
        tkMessageBox.showerror("Registration Failed.", "An error occurred during enrollment. Please try again.")

#SIGN IN USER PROTOCOL
"""
def signin_update():
    print('Entered signin_update')
    check = BooleanVar()  # Prototype recognize variable "check"
    check.set(False)
    print(idthreadstatus)
    while idthreadstatus:
        if scanner._status == 1:
            Textbox_update(str(scanner._status_string))
            lights.led_change(str(scanner._led_state[0]), str(scanner._led_state[1]))
            scanner._status = 2
    identified_finger = scanner._true_scan_number
    if not identified_finger == 200:
        check = True
    else:
        check = False
    if check == True:
        accept = True
        cur_user.user_recall(identified_finger)
    else:
        accept = False
        tkMessageBox.showinfo("Access Denied", "You don't have permission to use this coffee maker.")
"""
def signin_protocol():
    tkMessageBox.showinfo("Sign In","Welcome back.\nPlease use the scanner to sign in.")
    sleep(1)
    #scanner.finger_identify()
    scanner._idthread = threading.Thread(name='identify', target=scanner.finger_identify)
    scanner._idthread.start()
    """
    u = Process(name='updater', target=signin_update)
    pdb.set_trace()
    u.start()
    """

#TRIGGER BREWING PROTOCOL
accept = BooleanVar()   #prototype acceptance variable
accept.set(False)       #Initialize accept to "false", prevents automatic access to 
def brew_trigger(volume_value,strength_value):
    # vol is an object of type IntVar
    # stren is an object of type IntVar
    volume_value = volume_value.get()
    strength_value = strength_value.get()
    if strength_value == 1:
        y = "weak"
    elif strength_value == 2:
        y = "medium"
    else:
        y = "strong"
    ans = tkMessageBox.askokcancel("Order Accepted","Thank you for your selection!\nYou ordered " + str(volume_value) + " cups of " + str(y) + " coffee.\nReady to brew?",default="cancel")
    pdb.set_trace()
    if not cur_user._ID == None:
        accept.set(True)
    if ans == True:
        if accept == True:
            #bean_count = LoadCell weight protocol
            if bean_count == 0:
                tkMessageBox.showerror("Grinder Needs More Beans","There are too few beans to fill your order.\n Please add more before proceeding.")
            sleep(5)
            ans = tkMessageBox.askokcancel("Filter Cleaning", "Did you clean the filter?\nPress OK if you have, Cancel if you haven't", default="cancel")
            if ans == False:
                offense = True
            else:
                offense = False
            cur_user.user_update(offense, strength_value, volume_value)
        else:
            tkMessageBox.showerror("User Not Signed In","Looks like you still need to sign in.\nPlease select your user status and scan your finger.")

#UPDATE TEXTBOX METHOD
def Textbox_update(x):
    Textbox.insert(0.0,x+"\n\n")


###
# Frame Prototypes for Widget Organization
###
#Left Frame
LFrame = Tk.Frame(master, width=240, height = 800)
LFrame.grid(row=0, column=0, padx=10, pady=2)
#Middle frame
MFrame = Tk.Frame(master,width=240,height=800)
MFrame.grid(row=0,column=1,padx=10,pady=2)
#Right Frame
RFrame = Tk.Frame(master, width=240, height = 800)
RFrame.grid(row=0, column=2, padx=10, pady=2)
#Subframe for Account Buttons
Accounts_btnFrame = Tk.Frame(LFrame, width=200, height = 200)
Accounts_btnFrame.grid(row=1, column=0, padx=10, pady=2)
#Subframe for Selection Buttons
Selection_btnFrame = Tk.Frame(MFrame,width=200,height=200)
Selection_btnFrame.grid(row=0,column=0,columnspan=2,ipadx=2)

#Look for Coffee Cup image and load into label
try:
    img = PhotoImage(file="cupsmall.png")
    Imgspace = Tk.Label(LFrame,image=img)
    Imgspace.grid(row=0, column=0, padx=10, pady=2)
except:
    print("Image not found")

###
# Textbox for User Interface/Messaging in Left Frame
###
string_test = StringVar()
string_test = "Welcome to the Dept. of BIOE  Rube Goldberg Coffee Maker.\nPlease register or sign in.\n"
Textbox = Tk.Text(LFrame, width = 30, height = 10, takefocus=0)
Textbox.grid(row=2, column=0, padx=10, pady=2)
Textbox.insert(0.0,string_test)

###
# Registration Button in Left Frame
###
NewUser_button = Tk.Button(Accounts_btnFrame,text="  New User  ",command=lambda: newuser_protocol())
NewUser_button.grid(row=0, column=0, padx=10, pady=2)

###
# Sign In Button in Left Frame
###
SignIn_button = Tk.Button(Accounts_btnFrame,text="    Sign In    ",command=lambda: signin_protocol())
SignIn_button.grid(row=0, column=1, padx=10, pady=2)

###
# Strength Selection Radio Button Widgets in MFrame
###
strength_value = IntVar()
strength_value.set(2)
Label1 = Tk.Label(Selection_btnFrame, text="Strength").grid(row=0,column=0)
str_button1 = Tk.Radiobutton(Selection_btnFrame,text="   Weak   ",value=1,variable=strength_value,indicatoron=0).grid(row=1,column=0)
str_button2 = Tk.Radiobutton(Selection_btnFrame,text=" Medium ",value=2,variable=strength_value,indicatoron=0).grid(row=2,column=0)
str_button3 = Tk.Radiobutton(Selection_btnFrame,text="  Strong  ",value=3,variable=strength_value,indicatoron=0).grid(row=3,column=0)

###
# Volume Selection Radio Button Widgets in MFrame
###
volume_value = IntVar()
volume_value.set(8)
label2 = Tk.Label(Selection_btnFrame, text="Volume").grid(row=0,column=1)
vol_button1 = Tk.Radiobutton(Selection_btnFrame,text="   4 cups   ",value=4,variable=volume_value,indicatoron=0).grid(row=1,column=1)
vol_button2 = Tk.Radiobutton(Selection_btnFrame,text="   8 cups   ",value=8,variable=volume_value,indicatoron=0).grid(row=2,column=1)
vol_button3 = Tk.Radiobutton(Selection_btnFrame,text="   12 cups  ",value=12,variable=volume_value,indicatoron=0).grid(row=3,column=1)

###
# Brew Button Widget in MFrame
###
Confirm_button = Tk.Button(Selection_btnFrame,text="      Brew      ",command=lambda:brew_trigger(volume_value,strength_value))
Confirm_button.grid(row=4,column=0,columnspan=2,pady=25)

###
# Listbox Widget with scrollbar function in RFrame
###
Scrollbar = Tk.Scrollbar(RFrame,orient=VERTICAL)
Namebox = Tk.Listbox(RFrame,height=25,width=25,yscrollcommand=Scrollbar.set)
Namebox.grid(row=0,column=0)
Scrollbar.grid(row=0,column=1,sticky=N+S)
Scrollbar.config(command=Namebox.yview)

master.mainloop() #start monitoring and updating the GUI
