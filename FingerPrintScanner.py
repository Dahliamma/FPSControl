"""
Fingerprint Class
"""
import FPS as FPS
print('Imported FPS')
#import time as time
#print('Imported time')

class FingerPrintScanner():
    """
    FingerPrintScanner Class
    Responsible for scanning fingerprint, reporting scan status to other classes

    Args:
    """

    def __init__(self):
        self._status = 0
        print('Starting initialization')
        self.initialize()

    def initialize(self):
        print('Begin')
        fps = FPS.FPS_GT511C3(device_name='/dev/ttyAMA0', baud=9600, timeout=2, is_com=False)
        fps.UseSerialDebug = False
        print('Scanner connected')
        print(fps.IsPressFinger())
        FPS.delay(1)
        fps.SetLED(True)
        print('Place finger on scanner.')
        while not fps.IsPressFinger():
            print('Place finger on scanner.')
            FPS.delay(1)
        print('Thank you for touching me.')
        print('Capturing fingerprint.')
        fps.CaptureFinger(True)
        self.image = fps.GetImage()
        fps.SetLED(False)

if __name__ == "__main__":
    test_fps = FingerPrintScanner()