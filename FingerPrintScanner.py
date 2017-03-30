"""
Fingerprint Class

"""
import FPS as FPS
print('Imported FPS')
from collections import Counter
print('Imported Counter')
import LegacyEnroll
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
        self._enroll_check = None

    def finger_test(self):
        print('Begin')
        print(self.fps.IsPressFinger())
        self.fps.delay(1)
        self.fps.SetLED(True)
        print('Place finger on scanner.')
        while not self.fps.IsPressFinger():
            print('Place finger on scanner.')
            self.fps.delay(1)
        print('Thank you for touching me.')
        print('Capturing fingerprint.')
        self.fps.CaptureFinger(True)
        self._image = self.fps.GetImage()
        self.fps.SetLED(False)

    def finger_enroll(self):
        self.fps.SetLED(True)
        self.fps.delay(1)
        while not self.fps.IsPressFinger():
            print('Place finger on scanner.')
            self.fps.delay(1)
        print('Thank you for touching me.')
        print('Beginning enrollment process.')
        self.fps.Open()
        self._finger_number = self.fps.GetEnrollCount()
        print("BE enroll count: " + str(self.fps.GetEnrollCount()))
        print("Attempting to enroll to ID #: "+str(self._finger_number))
        self.fps.EnrollStart(-1)
        #Enroll1
        self.fps.CaptureFinger(True)
        self._enroll_check = self.fps.Enroll1()
        print(str(self._enroll_check))
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
        while not self.fps.IsPressFinger():
            print('Retouch the scanner for the second enrollment scan.')
            self.fps.delay(1)
        #Enroll2
        self.fps.CaptureFinger(True)
        self._enroll_check = self.fps.Enroll2()
        print(str(self._enroll_check))
        while self.fps.IsPressFinger():
            print('Remove finger momentarily.')
            self.fps.delay(1)
        while not self.fps.IsPressFinger():
            print('Retouch the scanner for the third enrollment scan.')
            self.fps.delay(1)
        #Enroll3
        self.fps.CaptureFinger(True)
        pdb.set_trace()
        self._enroll_check = self.fps.Enroll3()
        print(str(self._enroll_check))
        #self.fps.Open()
        print("AE enroll count: " + str(self.fps.GetEnrollCount()))
        self.fps.SetLED(False)

    def finger_identify(self):
        self.fps.SetLED(True)
        self.fps.delay(1)
        while not self.fps.IsPressFinger():
            print('Place finger on scanner.')
            self.fps.delay(1)
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