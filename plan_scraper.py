from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
import json
from sys import platform



class Subject:
    def __init__(self, subject_code):
        self.subject_code = subject_code
        self.weeks = {}

    def add_group(self, name, day, start_time, end_time, week_number):
        try:
            self.weeks[int(week_number)].append(Group(name, day, start_time, end_time))
        except KeyError:
            self.weeks[int(week_number)] = []
            self.weeks[int(week_number)].append(Group(name, day, start_time, end_time))

    def __repr__(self):
        return self.subject_code


class Group:
    def __init__(self, name, day, start_time, end_time):
        self.name = name
        self.day = day
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.lecture = name == "Forelesning"

    def __repr__(self):
        return self.name


def extract_data():
    gather =  True
    subjects = []
    options = Options()
    options.add_argument("-headless")
    print("Starting up the Geckodriver. This might take a minute.")
    if platform == "win32":
        driver = webdriver.Firefox(executable_path="dep/geckodriver.exe", options=options)
    elif platform == "linux" or platform == "linux2":
        driver = webdriver.Firefox(executable_path="dep/geckodriver", options=options)
    else:
        assert False, f"Expected platform win32, linux or linux2 not {platform}"
    while gather:
        subject_code = input("What subject would you like to fetch: ").upper()
        url = f"https://tp.uio.no/uib/timeplan/timeplan.php?id={subject_code}&type=course&sem=20v&lang=en"
        driver.get(url)
        time.sleep(2)
        results = driver.find_elements_by_class_name("cal_table")
        if len(results) == 0:
            print(f"Found no tables. maybe the subject code is wrong. Subject code given {subject_code}")
            again = input("Do you want to try again [y/n]: ")
            if again != "y":
                if len(subjects) >= 1:
                    break
                else:
                    exit()
            else:
                continue
        subject = Subject(subject_code)
        for result in results:
            text = result.text.split('\n')
            assert text[0].split()[0] == "Calendar", f"Language seems to be wrong expected calendar not {text[0].split()[0]}"
            for string in text:
                if any(day in string for day in ["mon", "tue", "wed", "thu", "fri"]):
                    string = string.split()
                    if string[-1] == "Forelesning":
                        subject.add_group(string[-1], string[0], string[2].replace(":", "."), string[4].replace(":", "."),text[0].split()[2])
                    else:
                        subject.add_group(string[-2] + " " + string[-1], string[0], string[2].replace(":", "."), string[4].replace(":", "."),text[0].split()[2])
        subjects.append(subject)
        another = input("Do you want to fetch another subject [y/n]: ")
        if another.lower() != "y":
            gather = False
    driver.quit()
    print("All done gathering data")
    return subjects


def write_to_file(subjects=None, delete=False):
    data = {}
    if not delete:
        try:
            with open('plans.json', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            pass
            # we have already made the data dict which we will now use.
            # This is just here to catch these specific errors so the program doesn't stop.

    for subject in subjects:
        data[subject.subject_code] = {}
        for week_number, subjects in subject.weeks.items():
            data[subject.subject_code][week_number] = {}
            for group in subjects:
                data[subject.subject_code][week_number][group.name] = {"day": group.day, "start_time": group.start_time, "end_time": group.end_time, "lecture": group.lecture}

    with open('plans.json', "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4)

    print(data)



if __name__ == '__main__':
    # Test data
    subjects = extract_data()
    write_to_file(subjects)

