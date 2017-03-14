"""
Fingerprint Class
"""
import FPS as FPS
from time import *
class FingerPrintScanner():
    """
    FingerPrintScanner Class
    Responsible for scanning fingerprint, reporting scan status to other classes

    Args:
    """

    def __init__(self):
        self._status = 0;
        self.initialize

    def initialize(self):
        fps = FPS.FPS_GT511C3(device_name='/dev/ttyAMA0', baud=9600, timeout=2, is_com=False)
        counter = 1
        while counter<5:
            fps.SetLED(True)
            time.sleep(2)
            fps.SetLED(False)
            time.sleep(2)
            counter = counter+1