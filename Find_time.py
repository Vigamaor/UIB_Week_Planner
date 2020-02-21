import json

from plan_scraper import Subject, write_to_file


def delete_subject(subject_code, subjects):
    found = False
    for idx, item in enumerate(subjects):
        if item.subject_code == subject_code.upper():
            subjects.pop(idx)
            found = True
    write_to_file(subjects=subjects, delete=True)

    if not found:
        print(f"We could not find the subject {subject_code} in you list of subjects.")

    return subjects


def get_data():
    with open("plans.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    subjects = []
    for subject, groups in data.items():
        subjects.append(Subject(subject))
        for group_name, week in groups.items():
            for week_number, occurenses in week.items():
                for occurens in occurenses:
                    subjects[-1].add_group(group_name, occurens["day"], occurens["start_time"], occurens["end_time"], week_number)

    print(data)
    return subjects


def check_groups_schedules(groups):
    pass


def create_schedules():
    pass


'''LEGACY def sort():
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
'''


if __name__ == '__main__':
    subjects = get_data()
    subjects = delete_subject("info132", subjects)
