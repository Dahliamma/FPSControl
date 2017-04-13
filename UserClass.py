import xlwt
import xlrd
from xlutils.copy import copy


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

    def user_update(self):
        #Not yet implemented
        return

if __name__ == "__main__":
    test_id = int(input('ID to test: '))
    from UserClass import User
    test = User(test_id)
    print('1. Recall User. | 2. Register User.')
    test_choice = int(input('Choice: '))
    if test_choice == 1:
        recall_result = test.user_recall()
        if recall_result == True:
            print('First Name: ' + test._first_name)
            print('Last Name: ' + test._last_name)
            print('Email: ' + test._email)
            print('Status: '+ str(test._status))
            print('Stored Strength: ' + str(test._strength))
            print('Stored Volume: ' + str(test._volume))
        else:
            print('ID not registered')
    elif test_choice == 2:
        test.user_register('mark.spark@ucdenver.edu')