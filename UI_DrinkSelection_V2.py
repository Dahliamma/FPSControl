from Tkinter import *
import Tkinter as Tk
import Tkinter.messagebox as Tk.messagebox
import pdb
#import fingerprintscanner as fingerprintscanner
#import LEDactivate as LED



###
# Initialize the UI Window/Master Object
###
master = Tk.Tk() #Makes the UI window
master.wm_title("UI Drink Selection") #TItle of UI window
master.wm_attributes("-fullscreen", True)
#master.config(background = "#FFFFFF") #Background UI color

###
# UI Function Callbacks
###

#NEW USER PROTOCOL
#unregistered_users = currentuser.find_unregistered()    #Call for unregistered users

###
# DEBUG SHIT TO GET RID OF
unregistered_users = [None]*50
for i in range(50):
    unregistered_users[i] = i
###
xx = BooleanVar()
xx.set(False)
def newuser_protocol():
    Namebox.insert(0,"Select Name...")      #Load first index as "Select Name..."
    for name in unregistered_users:     #Load up Namebox with unregistered users
        Namebox.insert(END,name)
    Namebox.select_set(0)   #Set selected value as top Namebox index: prevents mis-naming
    Tk.messagebox.showinfo("New User","Welcome!\nPlease follow these steps to enroll:\n\n1. Select your name from the list.\n2. Place your finger on the fingerprint scanner and follow the prompts.")
    #LED.Blink(4,5,100,100,100)   #Blink blue LED
    #xx = fingerprintscanner.finger_enroll()    #Call enrollment function
    if xx == True:
        #LED.Solid(2,3,100,100,100)   #Solid green LED for 3 sec
        index = Namebox.curselection()
        if index != 0:
            x = Namebox.get(ACTIVE)
            currentuser.user_register(index)
            Textbox_update("Welcome, "+ x +".\n You can now order your drink.")
    else:
        #LED.Solid(1,3,100,100,100)   #Solid red LED for 3 sec
        Tk.messagebox.showerror("Registration Failed.","An error occurred during enrollment. Please try again.")
    
#SIGN IN USER PROTOCOL 
check = BooleanVar()  #Prototype recognize variable "check"
check.set(False)    #Initialize check to "false", prevents automatic acceptance of user
def signin_protocol():
    Tk.messagebox.showinfo("Sign In","Welcome back.\nPlease use the scanner to sign in.")
    #check = fingerprintscanner.recognize()
    if check == True:
        accept = True
        #Retrieve user name for message prompting
    else:
        accept = False
        Tk.messagebox.showinfo("Access Denied","You don't have permission to use this coffee maker.")

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
    ans = Tk.messagebox.askokcancel("Order Accepted","Thank you for your selection!\nYou ordered " + str(volume_value) + " cups of " + str(y) + " coffee.\nReady to brew?",default="cancel")
    if ans == True:
        if accept == True:
            #bean_count = LoadCell weight protocol
                if bean_count == 0:
                    Tk.messagebox.showerror("Grinder Needs More Beans","There are too few beans to fill your order.\n Please add more before proceeding.")
            #user.strengthpreference = strength_value
            #user.volumepreference = volume_value
        else:
            Tk.messagebox.showerror("User Not Signed In","Looks like you still need to sign in.\nPlease select your user status and scan your finger.")

#UPDATE TEXTBOX METHOD
x = StringVar()
def Textbox_update(x):
    Textbox.insert(0.0,x+"\n\n")

###
# Frame Prototypes for Widget Organization
###
#Left Frame
LFrame = Tk.Frame(master, width=200, height = 800)
LFrame.grid(row=0, column=0, padx=10, pady=2)
#Middle frame
MFrame = Tk.Frame(master,width=200,height=800)
MFrame.grid(row=0,column=1,padx=10,pady=2)
#Right Frame
RFrame = Tk.Frame(master, width=200, height = 800)
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