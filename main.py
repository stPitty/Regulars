import csv
import re
import Regular_Rules as rr


class optimizator():

    def __init__(self, contacts_list):
        self.contacts_list = contacts_list

    def fio_fix(self):
        for empolyee in self.contacts_list:
            fio = (','.join(empolyee[0:3]).strip(','))
            fio_list = re.sub(",", " ", fio).split(' ')
            if len(fio_list) < 3:
                fio_list += ['']
            empolyee[0:3] = fio_list
        return self.contacts_list

    def phone_fix(self, find, rule):
        for employee in self.contacts_list:
            index = 0
            for note in employee:
                employee[index] = re.sub(find, rule, note)
                index += 1

    def unique_fix(self):
        contact_dict = {}
        for employee in self.contacts_list:
            if employee[0] in contact_dict:
                new_employee = employee.copy()
                for note in employee:
                    if note in contact_dict[employee[0]]:
                        new_employee[new_employee.index(note)] = ''
                    elif note not in contact_dict[employee[0]] and note != '':
                        index = new_employee.index(note)
                        contact_dict[employee[0]][index] = new_employee[index]
            else:
                contact_dict[employee[0]] = employee
        self.contacts_list = (list(contact_dict.values()))
        return self.contacts_list


class file_manager():

    def read_file(self, file_url):
        with open(file_url) as f:
            rows = csv.reader(f, delimiter=",")
            contacts = list(rows)
        return contacts

    def write_file(self, file_url, file):
        with open(file_url, "w+", encoding='utf8') as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(file)
        return print("File has been saved")


if __name__ == '__main__':

    secretary = file_manager()
    manager = optimizator(secretary.read_file('data/phonebook_raw.csv'))
    manager.fio_fix()
    manager.phone_fix(rr.find_main, rr.main_rule)
    manager.phone_fix(rr.find_added, rr.added_rule)
    manager.unique_fix()
    secretary.write_file("data/new_phonebook.csv", manager.contacts_list)
