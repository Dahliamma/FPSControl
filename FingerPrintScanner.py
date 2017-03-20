"""
Fingerprint Class
"""
import FPS as FPS
print('Imported FPS')
import time as time
print('Imported time')

class FingerPrintScanner():
    """
    FingerPrintScanner Class
    Responsible for scanning fingerprint, reporting scan status to other classes

    Args:
    """

    def __init__(self):
        self._status = 0;
        print('Starting initialization')
        self.initialize()

    def initialize(self):
        print('Begin')
        fps = FPS.FPS_GT511C3(device_name='/dev/ttyAMA0', baud=9600, timeout=2, is_com=False)
        print('Scanner connected')
        counter = 1
        while counter<5:
            fps.SetLED(True)
            time.sleep(0.5)
            print ('On')
            fps.SetLED(False)
            time.sleep(0.5)
            print ('Off')
            counter = counter+1

if __name__ == "__main__":
    test_fps = FingerPrintScanner()