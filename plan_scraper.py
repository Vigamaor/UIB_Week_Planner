import json
import time

import icalendar
import requests
import datetime



# TODO These classes can probably be reworked down two classes removing the subject class and just using a dict.
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
            self.groups.append(Group(name, self.subject_code))
            self.groups[-1].add_group_occurence(day, start_time, end_time, week_number)

    def __repr__(self):
        return self.subject_code


class Group:
    def __init__(self, name, subject_code):
        self.name = name

        self.group_occurrences = {}
        self.lecture = name == "Forelesning"
        self.subject_code = subject_code

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


    while gather:
        subject_code = input("What subject would you like to fetch: ").upper()
        semester = "20h"  # TODO must be fixed to work with multiple semesters.
        url = f"https://tp.uio.no/uib/timeplan/ical.php?sem={semester}&id%5B0%5D={subject_code}&type=course"
        try:
            cal = icalendar.Calendar.from_ical(requests.get(url).text)
        except ValueError:
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
        for result in cal.subcomponents:
            name = result.get("SUMMARY").replace(subject_code, "").strip("\n").strip(".").strip()
            day = f"{result.get('dtstart').dt.strftime('%A')}"
            start_time = float(f"{result.get('dtstart').dt.hour}.{result.get('dtstart').dt.minute}")
            end_time = float(f"{result.get('dtend').dt.hour}.{result.get('dtend').dt.minute}")
            week_number = result.get('dtstart').dt.isocalendar()[1]

            subject.add_group(name, day, start_time, end_time, week_number)

        subjects.append(subject)
        another = input("Do you want to fetch another subject [y/n]: ")
        if another.lower() != "y":
            gather = False

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
