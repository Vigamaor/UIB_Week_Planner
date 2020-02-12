import json


class Group:
    def __init__(self, name, day, start_time, end_time, subject):
        self.name = name
        self.day = day
        self.start_time = float(start_time)
        self.end_time = float(end_time)
        self.lecture = name == "Forelesning"
        self.subject = subject

    def __repr__(self):
        return self.name


def get_data():
    with open("tider.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    global info104
    global info110
    global info135
    global lectures

    for gruppe_data in data["INFO104"].items():
        objekt = Group(gruppe_data[0], gruppe_data[1]["day"], gruppe_data[1]["Starttid"], gruppe_data[1]["endtid"],
                       "info104")
        if objekt.lecture:
            lectures.append(objekt)
        else:
            info104.append(objekt)
    for gruppe_data in data["INFO110"].items():
        objekt = Group(gruppe_data[0], gruppe_data[1]["day"], gruppe_data[1]["Starttid"], gruppe_data[1]["endtid"],
                       "info110")
        if objekt.lecture:
            lectures.append(objekt)
        else:
            info110.append(objekt)
    for gruppe_data in data["INFO135"].items():
        objekt = Group(gruppe_data[0], gruppe_data[1]["day"], gruppe_data[1]["Starttid"], gruppe_data[1]["endtid"],
                       "info135")
        if objekt.lecture:
            lectures.append(objekt)
        else:
            info135.append(objekt)


def sort():
    list_of_subjects = []
    for subject in info104:
        for subject2 in info110:
            for subject3 in info135:
                if not (
                        subject.day == "thu" or subject2.day == "thu" or subject3.day == "thu" or subject.day == "fri" or subject2.day == "fri" or subject3.day == "fri" or subject.day == "mon" or subject2.day == "mon" or subject3.day == "mon"):
                    if subject.day == "wed" or subject2.day == "wed" or subject3.day == "wed":
                        for lecture in lectures:
                            if subject.day == lecture.day or subject2.day == lecture.day or subject3.day == lecture.day:
                                if (subject.start_time == lecture.start_time or (
                                        lecture.start_time < subject.end_time and lecture.end_time > subject.start_time)) or (
                                        lecture.start_time == subject2.start_time or (
                                        subject2.start_time < lecture.end_time and subject2.end_time > lecture.start_time)) or (
                                        lecture.start_time == subject3.start_time or (
                                        subject3.start_time < lecture.end_time and subject3.end_time > lecture.start_time)):
                                    # TODO her skjærer det seg
                                    continue
                        if subject.day == subject2.day:
                            if subject.start_time == subject2.start_time or (
                                    subject2.start_time < subject.end_time and subject2.end_time > subject.start_time):
                                # TODO her skjærer det seg
                                continue
                        if subject.day == subject3.day:
                            if subject.start_time == subject3.start_time or (
                                    subject3.start_time < subject.end_time and subject3.end_time > subject.start_time):
                                # TODO her skjærer det seg
                                continue
                        if subject2.day == subject3.day:
                            if subject2.start_time == subject3.start_time or (
                                    subject3.start_time < subject2.end_time and subject3.end_time > subject2.start_time):
                                # TODO her skjærer det seg
                                continue
                        list_of_subjects.append([subject, subject2, subject3])

    return list_of_subjects


info104 = []
info110 = []
info135 = []
lectures = []

get_data()
list_of_subjects = sort()
print("hei")
