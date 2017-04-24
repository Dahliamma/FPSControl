"""
Fingerprint Class

"""
import FPS as FPS
print('Imported FPS')
from collections import Counter
print('Imported Counter')
from time import sleep
import xlwt
import xlrd
from xlutils.copy import copy
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

    def EStep0(self):
        already_used_check = None
        self.fps.SetLED(True)
        sleep(1)
        print('Beginning enrollment process.')
        self.fps.Open()
        print("BE enroll count: " + str(self.fps.GetEnrollCount()))
        i = 1
        while i < 200:
            already_used_check = self.fps.CheckEnrolled(i)
            if not already_used_check:
                self._finger_number = i
                i = 200
            else:
                i = i + 1
        print("Attempting to enroll to ID #: " + str(self._finger_number))
        already_used_check = self.fps.EnrollStart(self._finger_number)
        print('Already used check: '+str(already_used_check))
        if already_used_check == 0:
            return True
        else:
            return False

    def EStep1(self):
        self._ES1 = False
        self._ES1_2 = False
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
        self._ES2 = False
        self._ES2_2 = False
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
        self._ES3 = False
        self._ES3_2 = False
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
        for i in range(10):
            counter = 0
            while counter <= 50 and not self._idchk:
                self._idchk = self.fps.CaptureFinger(False)
                print(str(self._idchk)+ ' ' + str(counter))
                sleep(0.1)
                counter = counter + 1
            self._finger_scan_number[i] = self.fps.Identify1_N()
            self._idchk = False
        temp_scans = [None] * 5
        temp_scans[0] = self._finger_scan_number[1]
        j = 1
        for i in range(10):
            if i == 3 or i == 5 or i == 7 or i == 9:
                temp_scans[j] = (self._finger_scan_number[i])
                j += 1
        self._finger_scan_number = temp_scans
        self._collected_scans = Counter(self._finger_scan_number)
        for j in range(5):
            print(str(self._finger_scan_number[j]))
        self._true_scan_number = self._collected_scans.most_common(1)
        self.fps.Open()
        self.fps.SetLED(False)
        print('Identified ID: ' + str(self._true_scan_number))
        if self._true_scan_number == 0:
            self._true_scan_number = 200
        return self._true_scan_number

class User():
    """
    User class, responsible for storing and recalling user information.
    """
    def __init__(self, FPSID):
        self._first_name = None
        self._last_name = None
        self._email = None
        self._status = None
        self._strength = None
        self._volume = None
        self._working_row = None
        self._ID = FPSID
        self._rb = xlrd.open_workbook('UserData.xls')
        self._r_sheet = self._rb.sheet_by_index(0)
        self._wb = copy(self._rb)
        self._w_sheet = self._wb.get_sheet(0)

    def user_recall(self):
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

    def user_register(self, email):
        register_check = False
        print(email)
        exist_check = self.user_recall()
        if not exist_check:
            counter = 1
            while counter < self._r_sheet.nrows:
                print(str(self._r_sheet.cell(counter, 2).value).lower())
                print(email.lower())
                print(str(self._r_sheet.cell(counter, 2).value).lower() == email.lower())
                if str(self._r_sheet.cell(counter, 2).value).lower() == email.lower():
                    self._w_sheet.write(counter, 6, self._ID)
                    self._w_sheet.write(counter, 5, 0)
                    self._working_row = counter
                    print('Writing data in row: ' + str(self._working_row))
                    counter = self._r_sheet.nrows
                    register_check = True
                else:
                    counter += 1
        else:
            print('Supplied ID already registered to: ' + self._first_name + ' ' + self._last_name)

        self._wb.save('UserData.xls')
        return register_check

    def database_update(self):
        #Not yet implemented
        return

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
        if not new_strength == self._volume:
            self._volume = new_volume
            new_vals[1] = self._volume
            change_check[1] = True
        for i in range(3):
            if change_check[i] and not new_vals[i] is None:
                self._w_sheet.write(self._working_row, i+3, new_vals[i])
        self._wb.save('UserData.xls')

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