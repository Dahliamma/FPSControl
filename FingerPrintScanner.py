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
        self.fps = FPS.FPS_GT511C3(device_name='/dev/ttyUSB0', baud=9600, timeout=2, is_com=False)
        self.fps.UseSerialDebug = True
        print('Scanner connected')
        #self.fps.DeleteAll() #Deleting all enrolled fingerprints for debugging reasons
        self._image = None
        #self.finger_test()
        self._finger_number = None
        self._finger_scan_number = [None] * 5
        self._collected_scans = None
        self._true_scan_number = None
        self._enroll_check = None
        self._retry_count = 10
        self.ES1 = False
        self.ES2 = False
        self.ES3 = False

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
        while not self.fps.IsPressFinger():
            print('Place finger on scanner.')
            self.fps.delay(1)
            sleep(0.5)
        print('Thank you for touching me.')
        print('Beginning enrollment process.')
        self.fps.Open()
        self._finger_number = self.fps.GetEnrollCount()
        print("BE enroll count: " + str(self.fps.GetEnrollCount()))
        print("Attempting to enroll to ID #: " + str(self._finger_number))
        self.fps.EnrollStart(self._finger_number)

    def EStep1(self):
        self.ES1 = self.fps.CaptureFinger(True)
        sleep(0.5)
        self._enroll_check = self.fps.Enroll1()
        print(str(self._enroll_check))
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
            sleep(0.5)
        while not self.fps.IsPressFinger():
            print('Retouch the scanner for the second enrollment scan.')
            self.fps.delay(1)
            sleep(0.5)
        return self.ES1

    def EStep2(self):
        self.ES2 = self.fps.CaptureFinger(True)
        sleep(0.5)
        self._enroll_check = self.fps.Enroll2()
        print(str(self._enroll_check))
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
            sleep(0.5)
        while not self.fps.IsPressFinger():
            print('Retouch the scanner for the third enrollment scan.')
            self.fps.delay(1)
            sleep(0.5)
        return self.ES2

    def EStep3(self):
        self.ES3 = self.fps.CaptureFinger(True)
        sleep(0.5)
        # pdb.set_trace()
        # print('Before E3'+str(self.fps._serial.inWaiting()))
        self._enroll_check = self.fps.Enroll3()
        # print('After E3: '+str(self.fps._serial.inWaiting()))
        print(str(self._enroll_check))
        # self.fps.Open()
        print("AE enroll count: " + str(self.fps.GetEnrollCount()))
        self.fps.SetLED(False)
        return self.ES3

    def finger_enroll(self):
        self.EStep0()
        while not self.EStep1() and self._retry_count > 0:
            print('Retrying ES1')
            self._retry_count = self._retry_count - 1
        if self._ES1 == True:
            self._retry_count = 10
        while not self.EStep2() and self._retry_count > 0:
            print('Retrying ES2')
            self._retry_count = self._retry_count - 1
        if self._ES2 == True:
            self._retry_count = 10
        while not self.EStep3() and self._retry_count > 0:
            print('Retrying ES3')
            self._retry_count = self._retry_count - 1
        if self._ES3 == True:
            self._retry_count = 10

    def finger_identify(self):
        self.fps.SetLED(True)
        sleep(1)
        while not self.fps.IsPressFinger():
            print('Place finger on scanner.')
            self.fps.delay(1)
            sleep(0.5)
        print('Thank you for touching me.')
        print('Beginning identification process.')
        self.fps.Open()
        for i in range(5):
            self.fps.CaptureFinger(False)
            self._finger_scan_number[i] = self.fps.Identify1_N()
        self._collected_scans = Counter(self._finger_scan_number)
        self._true_scan_number = self._collected_scans.most_common(1)
        #self.fps.Open()
        self.fps.SetLED(False)
        print('Identified ID:'+str(self._true_scan_number))
        return self._true_scan_number

if __name__ == "__main__":
    from FingerPrintScanner import FingerPrintScanner
    test = FingerPrintScanner()
    test.finger_identify()