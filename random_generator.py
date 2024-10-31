import random
import csv

NUM_GROUPS = 4
NUM_SUBJECTS = 6
NUM_TEACHERS = 6
NUM_ROOMS = 6
GROUP_NAMES = [f"Group{i + 1}" for i in range(NUM_GROUPS)]
SUBJECT_NAMES = [f"Subject{i + 1}" for i in range(NUM_SUBJECTS)]
TEACHER_NAMES = [f"T{i + 1}" for i in range(NUM_TEACHERS)]
ROOM_CAPACITY = [20, 30, 40]

def generate_groups():
    groups = []
    for group_name in GROUP_NAMES:
        group_size = random.randint(20, 40)
        groups.append({"group_name": group_name, "group_size": group_size})
    return groups

def generate_subjects():
    subjects = []
    for group in GROUP_NAMES:
        num_subjects = random.randint(1, NUM_SUBJECTS)
        for _ in range(num_subjects):
            subject = random.choice(SUBJECT_NAMES)
            hours = random.randint(1, 2) * 1.5 * 20
            subject_type = random.choice(["Lecture", "Practice"])
            is_divided = random.choice([True, False])
            subjects.append({"group_name": group, "subject_name": subject, "hours": int(hours), "subject_type": subject_type, "is_divided": is_divided})
    return subjects

def generate_teachers():
    teachers = []
    for teacher in TEACHER_NAMES:
        num_subjects = random.randint(1, NUM_SUBJECTS)
        subjects = random.sample(SUBJECT_NAMES, num_subjects)
        for subject in subjects:
            lesson_type = random.choice(["Lecture", "Practice"])
            teachers.append({"teacher_name": teacher, "subject_name": subject, "lesson_type": lesson_type})
    return teachers

def generate_rooms():
    rooms = []
    for i in range(NUM_ROOMS):
        room_name = f"Room{i + 1}"
        room_capacity = random.choice(ROOM_CAPACITY)
        rooms.append({"room_name": room_name, "room_capacity": room_capacity})
    return rooms

def save_to_csv(filename, data, headers):
    with open(filename, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

def generate_files():
    groups = generate_groups()
    subjects = generate_subjects()
    teachers = generate_teachers()
    rooms = generate_rooms()

    save_to_csv("groups_rand.csv", groups, ["group_name", "group_size"])
    save_to_csv("subjects_rand.csv", subjects, ["group_name", "subject_name", "hours", "subject_type", "is_divided"])
    save_to_csv("teachers_rand.csv", teachers, ["teacher_name", "subject_name", "lesson_type"])
    save_to_csv("rooms_rand.csv", rooms, ["room_name", "room_capacity"])

    print("Files are generated")


generate_files()
