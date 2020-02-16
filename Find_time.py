import json
from plan_scraper import Subject, Group


def delete_subject(subject_code):
    pass

def get_data():
    with open("plans.json", "r", encoding='utf-8') as file:
        data = json.load(file)
    subjects = []
    for subject, weeks in data.items():
        subjects.append(Subject(subject))
        for week, groups in weeks.items():
            for group_name, group_info in groups.items():
                subjects[-1].add_group(group_name, group_info["day"],group_info["start_time"],group_info["end_time"], week)

    print(data)







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
    get_data()
