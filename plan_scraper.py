import json
import time
from sys import platform

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Subject:
    def __init__(self, subject_code):
        self.subject_code = subject_code
        self.weeks = set()
        self.groups = []

    def add_group(self, name, day, start_time, end_time, week_number):
        self.weeks.add(week_number)
        group_exsist = False
        for group in self.groups:
            if group.name == name:
                group.add_group_occurence(day, start_time, end_time, week_number)
                group_exsist = True
                break

        if not group_exsist:
            self.groups.append(Group(name))
            self.groups[-1].add_group_occurence(day, start_time, end_time, week_number)

    def __repr__(self):
        return self.subject_code


class Group:
    def __init__(self, name):
        self.name = name
        self.group_occurrences = {}
        self.lecture = name == "Forelesning"

    def __repr__(self):
        return self.name

    def add_group_occurence(self, day, start_time, end_time, week_number):
        if week_number not in self.group_occurrences:
            self.group_occurrences[week_number] = []
        self.group_occurrences[week_number].append((GroupOccurrence(day, start_time, end_time)))


class GroupOccurrence:
    def __init__(self, day, start_time, end_time):
        self.day = day
        self.start_time = float(start_time)
        self.end_time = float(end_time)

    def __repr__(self):
        return self.day


def extract_data():
    gather = True
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

        content = driver.page_source
        soup = BeautifulSoup(content, "html.parser")
        results = soup.find_all(class_="cal_table")

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
            assert result.contents[0].text.split()[
                       0] == "Calendar", f"Language seems to be wrong expected calendar not \
                       {result.contents[0].text.split()[0]}"
            week_number = result.contents[0].text.split()[2]

            for line in result.contents:
                if any(day in line.text for day in ["mon", "tue", "wed", "thu", "fri"]):
                    subject.add_group(line.contents[2].text, line.contents[0].text.split()[0],
                                      line.contents[1].text.split()[0].replace(":", "."),
                                      line.contents[1].text.split()[2].replace(":", "."), week_number)

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
        for group in subject.groups:
            data[subject.subject_code][group.name] = {}
            for week_number, occurances in group.group_occurrences.items():
                for occurrence in occurances:
                    if week_number in data[subject.subject_code][group.name]:
                        data[subject.subject_code][group.name][week_number].append(
                            {"day": occurrence.day, "start_time": occurrence.start_time,
                             "end_time": occurrence.end_time, "lecture": group.lecture})
                    else:
                        data[subject.subject_code][group.name][week_number] = []
                        data[subject.subject_code][group.name][week_number].append(
                            {"day": occurrence.day, "start_time": occurrence.start_time,
                             "end_time": occurrence.end_time, "lecture": group.lecture})

    with open('plans.json', "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print(data)


if __name__ == '__main__':
    # Test data
    subjects = extract_data()
    write_to_file(subjects)
