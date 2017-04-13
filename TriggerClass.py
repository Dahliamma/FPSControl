from FingerPrintScanner import *
from UserClass import *


class Trigger():
    def __init__(self):
        self._brew_strength = None
        self._brew_volume = None
        self._user_print_obj = FingerPrintScanner()
        self._user_info_obj = None

    def take_inputs(self):
        self._user_print_obj.finger_identify()
        self._user_info_obj = User(self._user_print_obj._true_scan_number)
        recall_check = self._user_info_obj.user_recall()
        if recall_check:
            if type(self._user_info_obj._strength) == int and type(self._user_info_obj._volume) == int:
                print('Stored strength: ' + str(self._user_info_obj._strength))
                print('Stored volume: ' + str(self._user_info_obj._volume) + 'Oz.')
                print('Use stored preferences? (1=Yes | 2=No)')
                use_preference = input('Choice: ')