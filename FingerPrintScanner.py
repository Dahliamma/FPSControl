"""
Fingerprint Class

"""
import FPS as FPS
print('Imported FPS')
from collections import Counter
print('Imported Counter')
from time import sleep
import pdb

class FingerPrintScanner():
    """
    FingerPrintScanner Class
    Responsible for scanning fingerprint, reporting scan status to other classes

    Args:
    """

    def __init__(self):
        self._status = 0
        print('Starting initialization')
        self.fps = FPS.FPS_GT511C3(device_name='/dev/ttyAMA0', baud=9600, timeout=2, is_com=False)
        self.fps.UseSerialDebug = False
        print('Scanner connected')
        #self.fps.DeleteAll() #Deleting all enrolled fingerprints for debugging reasons
        self._image = None
        #self.finger_test()
        self._finger_number = None
        self._finger_scan_number = [None] * 5
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
        self._image = self.fps.GetImage()
        self.fps.SetLED(False)

    def EStep0(self):
        self.fps.SetLED(True)
        sleep(1)
        print('Beginning enrollment process.')
        self.fps.Open()
        self._finger_number = self.fps.GetEnrollCount()
        print("BE enroll count: " + str(self._finger_number))
        print("Attempting to enroll to ID #: " + str(self._finger_number))
        already_used_check = self.fps.EnrollStart(self._finger_number)
        print('Already used check: '+str(already_used_check))
        if already_used_check == 0:
            return True
        else:
            return False

    def EStep1(self):
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
            sleep(0.5)
        while not self.fps.IsPressFinger():
            print('Touch the scanner for the first enrollment scan.')
            self.fps.delay(1)
            sleep(0.5)
        print('Keep finger on scanner.')
        counter = 0
        while counter <=50 and not self._ES1:
            self._ES1 = self.fps.CaptureFinger(True)
            sleep(0.1)
            counter = counter + 1
        sleep(0.5)
        if self._ES1 == True:
            self._ES1_2 = self.fps.Enroll1()
            print(str(self._ES1_2))
        if (not self._ES1 or not self._ES1_2 == 0):
            print('ES1 failed. Restarting enrollment.')
            return False
        else:
            print('ES1 Succeeded')
            return True

    def EStep2(self):
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
            sleep(0.5)
        while not self.fps.IsPressFinger():
            print('Touch the scanner for the second enrollment scan.')
            self.fps.delay(1)
            sleep(0.5)
        print('Keep finger on scanner.')
        counter = 0
        while counter <= 50 and not self._ES2:
            self._ES2 = self.fps.CaptureFinger(True)
            sleep(0.1)
            counter = counter + 1
        sleep(0.5)
        if self._ES2 == True:
            self._ES2_2 = self.fps.Enroll2()
            print(str(self._ES2_2))
        if (not self._ES2 or not self._ES2_2 == 0) and self._retry_count > 0:
            print('ES2 failed. Restarting enrollment.')
            return False
        else:
            print('ES2 Succeeded')
            return True

    def EStep3(self):
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
            sleep(0.5)
        while not self.fps.IsPressFinger():
            print('Touch the scanner for the third enrollment scan.')
            self.fps.delay(1)
            sleep(0.5)
        print('Keep finger on scanner.')
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
            print(str(self._ES3_2))
        if (not self._ES3 or not self._ES3_2 == 0) and self._retry_count > 0:
            print('ES3 failed. Restarting enrollment.')
            return False
        else:
            print('ES3 Succeeded')
            return True

    def EStep4(self):
        sleep(0.5)
        self.fps.Open()
        AE_enroll_count = self.fps.GetEnrollCount()
        print('Enrollment Succeeded')
        print("AE enroll count: " + str(AE_enroll_count))
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
            print('Enrollmet Failed.')

    def finger_identify(self):
        self.fps.SetLED(True)
        sleep(1)
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
            sleep(0.5)
        while not self.fps.IsPressFinger():
            print('Place finger on scanner for identification.')
            self.fps.delay(1)
            sleep(0.5)
        print('Thank you for touching me. Keep it up.')
        print('Beginning identification process.')
        self.fps.Open()
        for i in range(5):
            counter = 0
            while counter <= 50 and not self._idchk:
                self._idchk = self.fps.CaptureFinger(False)
                print(str(self._idchk)+ ' ' + str(counter))
                sleep(0.1)
                counter = counter + 1
            self._finger_scan_number[i] = self.fps.Identify1_N()
            self._idchk = False
        self._collected_scans = Counter(self._finger_scan_number)
        for j in range(5):
            print(str(self._collected_scans[i-1]))
        self._true_scan_number = self._collected_scans.most_common(1)
        #self.fps.Open()
        self.fps.SetLED(False)
        print('Identified ID:'+str(self._true_scan_number))
        return self._true_scan_number

if __name__ == "__main__":
    from FingerPrintScanner import FingerPrintScanner
    test = FingerPrintScanner()
    print('1. Enroll. | 2. Identify. | 3. Enroll and Identify. | 4. DeleteAll.')
    testloop = input('Choice: ')
    sleep(2)
    if testloop == 1 or testloop == 3:
        test.finger_enroll()
    if testloop == 2 or testloop == 3:
        test.finger_identify()
    if testloop == 4:
        print('Are you sure? (Y/N)')
        del_check = raw_input()
        if del_check.lower is 'y':
            del_check_check = False
            while not del_check_check:
                del_check_check = test.fps.DeleteAll()