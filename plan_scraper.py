from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
import json
from sys import platform


class Subject:
    def __init__(self, subject_code):
        self.subject_code = subject_code
        self.groups = []

    def add_group(self, name, day, start_time, end_time, week_number):
        self.groups.append(Group(name, day, start_time, end_time, week_number))

    def __repr__(self):
        return self.subject_code


class Group:
    def __init__(self, name, day, start_time, end_time, week_number):
        self.name = name
        self.day = day
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.lecture = name == "Forelesning"
        self.week_number = week_number

    def __repr__(self):
        return self.name


def extract_data():
    subject_code = input("What subject would you like to fetch: ").upper()
    url = f"https://tp.uio.no/uib/timeplan/timeplan.php?id={subject_code}&type=course&sem=20v&lang=en"
    options = Options()
    options.add_argument("-headless")
    if platform == "win32":
        driver = webdriver.Firefox(executable_path="dep/geckodriver.exe", options=options)
    elif platform == "linux" or platform == "linux2":
        driver = webdriver.Firefox(executable_path="dep/geckodriver", options=options)
    else:
        assert False, f"Expected platform win32, linux or linux2 not {platform}"
    driver.get(url)
    time.sleep(2)
    results = driver.find_elements_by_class_name("cal_table")
    assert len(results) > 0, f"Found no tables. maybe the subject code is wrong. Subject code given {subject_code}"
    subject = Subject(subject_code)
    for result in results:
        text = result.text.split('\n')
        assert text[0].split()[0] == "Calendar", f"Language seems to be wrong expected calendar not {text[0].split()[0]}"
        for string in text:
            if any(day in string for day in ["mon", "tue", "wed", "thu", "fri"]):
                string = string.split()
                if string[-1] == "Forelesning":
                    subject.add_group(string[-1], string[0], string[2].replace(":", "."),string[4].replace(":", "."), text[0].split()[2])
                else:
                    subject.add_group(string[-2] + " " + string[-1], string[0], string[2].replace(":", "."), string[4].replace(":", "."), text[0].split()[2])
    driver.quit()
    return subject


def write_to_file():
    pass
    # TODO write data to file


def clean_data(subject):
    week_plan = {}
    for group in subject.groups:
        if group.week_number in week_plan:
            week_plan[group.week_number].append(group)
        else:
            week_plan[group.week_number] = []
            week_plan[group.week_number].append(group)
    print(week_plan)
    number_of_groups = set()
    for lis in week_plan.values():
        number_of_groups.add(len(lis))
    print(number_of_groups)
    if len(number_of_groups) <3 and min(number_of_groups) <= 2:
        pass
        # TODO How are we going to create the standard week.
    elif len(number_of_groups) >=3:
        # There are to many weeks who are different and all weeks will be retained and tested later
        return subject

    # TODO check if there how many different weeks there are.


if __name__ == '__main__':
    # Test data
    data = extract_data()
    clean_data(data)
    print("hello")
