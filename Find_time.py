import json
import itertools

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
    try:
        with open("plans.json", "r", encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return None
    subjects = []
    for subject, groups in data.items():
        subjects.append(Subject(subject))
        for group_name, week in groups.items():
            for week_number, occurenses in week.items():
                for occurens in occurenses:
                    subjects[-1].add_group(group_name, occurens["day"], occurens["start_time"], occurens["end_time"], week_number)

    return subjects


def check_groups_schedules(groups, lectures):
    used_weeks = set()
    for group in groups:
        used_weeks = used_weeks.union(group.group_occurrences.keys())
    # We pick out each week and cheek if there are any chrashes in any of the weeks. If we detect a chrash we
    # immediately return False
    for week in used_weeks:
        for group in groups:
            for lecture in lectures.values():
                try:
                    for occurence in group.group_occurrences[week]:
                        try:
                            for lecture_occurence in lecture.group_occurrences[week]:
                                if lecture_occurence.day == occurence.day and (lecture_occurence.start_time == occurence.start_time or (lecture_occurence.start_time < occurence.start_time and occurence.start_time < lecture_occurence.end_time) or (occurence.start_time < lecture_occurence.start_time and lecture_occurence.start_time < occurence.end_time)):
                                    return False
                        except KeyError:
                            continue
                except KeyError:
                    continue



    for week in used_weeks:
        list_occurrences=[]
        for group in groups:
            # If any of the groups does not contain the week we are currently testing we catch a keyerror and then
            # continue
            try:
                # We pick out the occurrences in each group and add them to a list and then check the next occurence
                # against alle the others allready in the list until all have been checked or a crash has been detected
                for occurence in group.group_occurrences[week]:
                    if len(list_occurrences) == 0:
                        list_occurrences.append(occurence)
                    else:
                        for ls_occurrence in list_occurrences:
                            if ls_occurrence.day == occurence.day and (ls_occurrence.start_time == occurence.start_time or (ls_occurrence.start_time < occurence.start_time and occurence.start_time < ls_occurrence.end_time) or (occurence.start_time < ls_occurrence.start_time and ls_occurrence.start_time < occurence.end_time)):
                                return False
                        list_occurrences.append(occurence)
            except KeyError:
                continue
    return True


def find_lectures(subjects):
    lectures = {}
    for subject in subjects:
        for group in subject.groups:
            if group.lecture:
                lectures[subject.subject_code] = group
                break

    return lectures


def create_schedules(subjects):
    # all_group_combination_fit holds all the groups that when placed togheter do not overlapp
    all_group_combination_fit = []
    lectures = find_lectures(subjects)
    # Here we remove the lectures from the group list so that we can combine them without the lectures.
    # We also add all weeks with a group to a list
    groups = []
    # The set is being declared here for visibility
    weeks = set()
    for subject in subjects:
        weeks = weeks.union(subject.weeks)
        groups.append(subject.groups)
        for i,group in enumerate(groups[-1]):
            if group.lecture:
                groups[-1].pop(i)

    all_group_combinations = list(itertools.product(*groups))
    print(all_group_combinations)
    for group_combination in all_group_combinations:
        if check_groups_schedules(group_combination, lectures):
            all_group_combination_fit.append(group_combination)

    return all_group_combination_fit

if __name__ == '__main__':
    subjects = get_data()
    #subjects = delete_subject("info132", subjects)
    #subjects = delete_subject("info110", subjects)
    #print(find_lectures(subjects))
    create_schedules(subjects)
