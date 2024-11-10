import csv
import random

def load_groups(filename):
    groups = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            groups[row['group_name']] = [int(row['group_size']), ['п/г1','п/г2']]
    return groups

def load_subjects(filename):
    subjects = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            group = row['group_name']
            subject = row['subject_name']
            hours = int(row['hours'])
            subject_type = row['subject_type']
            is_divided = row['is_divided'].lower() == 'true'
            if group not in subjects:
                subjects[group] = []
            subjects[group].append((subject, hours, subject_type, is_divided))
    return subjects

def load_teachers(filename):
    teachers = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            teacher = row['teacher_name']
            subject = row['subject_name']
            lesson_type = row['lesson_type']
            if teacher not in teachers:
                teachers[teacher] = []
            teachers[teacher].append((subject, lesson_type))
    return teachers

def load_auditoriums(filename):
    auditoriums = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            auditoriums[row['room_name']] = int(row['room_capacity'])
    return auditoriums

def save_schedule_to_file(schedule, filename='result.txt'):
    sorted_schedule = sorted(schedule, key=lambda x: (x[0], x[2][0], x[2][1]))
    with open(filename, mode='w') as file:
        for entry in sorted_schedule:
            group, subject, slot, teacher, room, subject_type, _ = entry
            day, hour = slot
            file.write(f"Group: {'-'.join(group)}, Day {day}, Pair {hour}: Subject {subject}, Teacher {teacher}, Room {room}, Type: {subject_type}\n")
    print(f"Schedule is saved in the file '{filename}'.")

def save_schedule_to_csv_file(schedule, filename='result.csv'):
    sorted_schedule = [['-'.join(group), subject, slot[0], slot[1], teacher, room, subject_type] for group, subject, slot, teacher, room, subject_type, _ in sorted(schedule, key=lambda x: (x[0], x[2][0], x[2][1]))]
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(sorted_schedule)

suffix = '_rand'
groups = load_groups(f'groups{suffix}.csv')
subjects = load_subjects(f'subjects{suffix}.csv')
teachers = load_teachers(f'teachers{suffix}.csv')
auditoriums = load_auditoriums(f'rooms{suffix}.csv')
slots = [(day, hour) for day in range(1, 5) for hour in range(1, 4)]

def generate_schedule():
    schedule = []
    used_slots_gen = {} 
    for group, subject_list in subjects.items():
        for subject, hours, subject_type, is_divided in subject_list:
            t = hours / 1.5 / 14
            d = t - (hours / 1.5 // 14)
            if d > 0.5:
                t = t + 1
            else:
                t = hours / 1.5 // 14
            if subject_type == "Lecture":
                for _ in range(int(t)):
                    slot = random.choice([s for s in slots if not(s in used_slots_gen and ((group in [g[0] for g in used_slots_gen[s][0]]) or (group in [g[0] for g in [gin[0] for gin in used_slots_gen[s][0]] if g])))])
                    if slot not in used_slots_gen:
                        used_slots_gen[slot] = ([], [], [])   
                    _, teachers_in_slot, rooms_in_slot = used_slots_gen[slot]
                    rand_teacher = random.choice([teacher for teacher, _ in teachers.items() if not(teacher in [t for t, _, _ in teachers_in_slot] and (subject_type != 'Lecture' or ([teacher, subject, "Lecture"] not in teachers_in_slot)))])
                    rand_room = random.choice([room for room, _ in auditoriums.items() if not(room in [r for r, _, _, _ in rooms_in_slot] and (subject_type != 'Lecture' or (subject not in [s for _, s, _, _ in rooms_in_slot]) or (rand_teacher not in [t for _, _, t, _ in rooms_in_slot]) or ([room, "Practice"] in [[r[0], r[3]] for r in rooms_in_slot])  or ([room, subject, rand_teacher, "Lecture"] not in teachers_in_slot) ))])
                    schedule.append(([group], subject, slot, rand_teacher, rand_room, subject_type, is_divided))
                    used_slots_gen[slot][0].append([[group], rand_room])
                    used_slots_gen[slot][1].append([rand_teacher, subject, subject_type])
                    used_slots_gen[slot][2].append([rand_room, subject, rand_teacher, subject_type])  

            if subject_type == "Practice":
                for _ in range(int(t)):
                    if is_divided:
                        for subgroup in groups[group][1]:
                            slot = random.choice([s for s in slots if not(s in used_slots_gen and ((group in [g[0] for g in used_slots_gen[s][0]]) or (not(is_divided) and (group in [g[0] for g in [gin[0] for gin in used_slots_gen[s][0]] if g])) or (is_divided and (group in [g[0] for g in [gin[0] for gin in used_slots_gen[s][0]] if len(g) == 1]) or ([group, subgroup] in [[g[0], g[1]] for g in [gin[0] for gin in used_slots_gen[s][0]] if len(g) == 2]))))])
                            if slot not in used_slots_gen:
                                used_slots_gen[slot] = ([], [], []) 
                            _, teachers_in_slot, rooms_in_slot = used_slots_gen[slot]
                            rand_teacher = random.choice([teacher for teacher, _ in teachers.items() if not(teacher in [t for t, _, _ in teachers_in_slot])])
                            rand_room = random.choice([room for room, _ in auditoriums.items() if not(room in [r for r, _, _, _ in rooms_in_slot])])
                            schedule.append(([group, subgroup], subject, slot, rand_teacher, rand_room, subject_type, is_divided))
                            used_slots_gen[slot][0].append([[group, subgroup], rand_room])
                            used_slots_gen[slot][1].append([rand_teacher, subject, subject_type])
                            used_slots_gen[slot][2].append([rand_room, subject, rand_teacher, subject_type])
                    if not is_divided:
                        slot = random.choice([s for s in slots if not(s in used_slots_gen and ((group in [g[0] for g in used_slots_gen[s][0]]) or (not(is_divided) and (group in [g[0] for g in [gin[0] for gin in used_slots_gen[s][0]] if g])) or (is_divided and (group in [g[0] for g in [gin[0] for gin in used_slots_gen[s][0]] if len(g) == 1]))))])
                        if slot not in used_slots_gen:
                            used_slots_gen[slot] = ([], [], []) 
                        _, teachers_in_slot, rooms_in_slot = used_slots_gen[slot]
                        rand_teacher = random.choice([teacher for teacher, _ in teachers.items() if not(teacher in [t for t, _ , _ in teachers_in_slot])])
                        rand_room = random.choice([room for room, _ in auditoriums.items() if not(room in [r for r, _, _, _ in rooms_in_slot])])
                        schedule.append(([group], subject, slot, rand_teacher, rand_room, subject_type, is_divided))
                        used_slots_gen[slot][0].append([[group], rand_room])
                        used_slots_gen[slot][1].append([rand_teacher, subject, subject_type])
                        used_slots_gen[slot][2].append([rand_room, subject, rand_teacher, subject_type])

    return schedule

def fitness(schedule):
    result = 100
    used_slots = {} 

    for (group, subject, slot, teacher, room, subject_type, is_divided) in schedule:
        if slot in used_slots:
            groups_in_slot, teachers_in_slot, rooms_in_slot = used_slots[slot]

            if teacher in [t for t, _, _ in teachers_in_slot] and (subject_type != 'Lecture' or ([teacher, subject, room, "Lecture"] not in teachers_in_slot)):
                return 0
            if (group in [g[0] for g in groups_in_slot]) or (len(group) == 1 and group[0] in [g[0] for g in [gin[0] for gin in groups_in_slot] if g]) or (len(group) == 2 and group[0] in [g[0] for g in [gin[0] for gin in groups_in_slot] if len(g) == 1]):
                return 0
            if room in [r for r, _, _, _ in rooms_in_slot] and (subject_type != 'Lecture' or (subject not in [s for _, s, _, _ in rooms_in_slot]) or (teacher not in [t for _, _, t, _ in rooms_in_slot]) or ([room, "Practice"] in [[r[0], r[3]] for r in rooms_in_slot])):
                return 0
        else:
            used_slots[slot] = ([], [], [])

        used_slots[slot][0].append([group, room])
        used_slots[slot][1].append([teacher, subject, room])
        used_slots[slot][2].append([room, subject, teacher, subject_type])

        if not(subject_type == 'Practice' and is_divided and group[0] in groups and groups[group[0]][0] / 2 > auditoriums[room]):
            result += 1
        if not(subject_type == 'Practice' and not is_divided and group[0] in groups and groups[group[0]][0] > auditoriums[room]):
            result += 1
        if not(subject_type == 'Lecture' and group[0] in groups and sum([groups[g[0][0]][0] for g in used_slots[slot][0] if g[1] == room]) > auditoriums[room]):
                result += 1
        if not(teacher not in [t for t, subs in teachers.items() if (subject, subject_type) in subs]):
            result += 1

    for _, slots_in_use in group_slots(schedule).items():
        slots_in_use = sorted(slots_in_use)
        for i in range(1, len(slots_in_use)):
            if slots_in_use[i][0] == slots_in_use[i - 1][0]:
                gap = slots_in_use[i][1] - slots_in_use[i - 1][1]
                if gap > 1:
                    result -= (gap - 1)

    for _, subject_list in subjects.items():
        for _, hours, _, _ in subject_list:
            t = hours / 1.5 / 14
            d = t - (hours / 1.5 // 14)
            if d > 0.5:
                t = t + 1
            else:
                t = hours / 1.5 // 14
            t = t * 1.5 * 14
            result -= 0.5 * abs(hours - t)

    return result

def group_slots(schedule):
    slots_by_entity = {}
    for (group, _, slot, teacher, _, subject_type, _) in schedule:
        if subject_type == 'Lecture':
            if group[0] not in slots_by_entity:
                slots_by_entity[group[0]] = []
            if teacher not in slots_by_entity:
                slots_by_entity[teacher] = []
            slots_by_entity[group[0]].append(slot)
            slots_by_entity[teacher].append(slot)
    return slots_by_entity

def selection(population, fitness_values):
    total_fitness = sum(fitness_values)
    probabilities = [(f / total_fitness) for f in fitness_values]
    total_probabilities = sum(probabilities)
    probabilities = [p / total_probabilities for p in probabilities]
    return random.choices(population, probabilities, k=2)

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child = parent1[:point] + parent2[point:]
    return child

def mutate(individual, mutation_rate=0.2):
    if random.random() < mutation_rate:
        old_fitness = fitness(individual)
        index = random.randint(0, len(individual) - 1)
        group, subject, slot, teacher, room, subject_type, is_divided = individual[index]
        new_slot = random.choice(slots)
        new_teacher = random.choice([t for t, subs in teachers.items() if (subject, subject_type) in subs])
        new_room = random.choice([r for r, _ in auditoriums.items()])
        individual[index] = (group, subject, new_slot, new_teacher, new_room, subject_type, is_divided)
        count = 0
        while(fitness(individual) <= old_fitness and count < 10):
            new_slot = random.choice(slots)
            new_teacher = random.choice([t for t, subs in teachers.items() if (subject, subject_type) in subs])
            new_room = random.choice([r for r, _ in auditoriums.items()])
            individual[index] = (group, subject, new_slot, new_teacher, new_room, subject_type, is_divided)
            count = count + 1
        if(fitness(individual) <= old_fitness):
            individual[index] = (group, subject, slot, teacher, room, subject_type, is_divided)
    return individual

def genetic_algorithm(pop_size, generations):
    population = [generate_schedule() for _ in range(pop_size)]

    for generation in range(generations):
        fitness_values = [fitness(ind) for ind in population]
        print(f"Generation {generation + 1}: Total fitness: {sum(fitness_values)}")
        new_population = []
        for _ in range(pop_size):
            parent1, parent2 = selection(population, fitness_values)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population

        best_individual = max(population, key=fitness)
        print(f"Generation {generation + 1}: The best fitness = {fitness(best_individual)}")
    return max(population, key=fitness)

best_schedule = genetic_algorithm(pop_size=10, generations=1000)
print(f"The best schedule: {best_schedule}")
save_schedule_to_file(best_schedule)
save_schedule_to_csv_file(best_schedule)