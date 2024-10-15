from data import data_without_duplicates

def count_instances_per_class(data):
    counter = {}

    for entry in data:
        race = entry.get('Race', '-')
        if race in counter:
            counter[race] += 1
        else:
            counter[race] = 1

    return counter


# Utilizare:
class_counts = count_instances_per_class(data_without_duplicates)
for race, count in class_counts.items():
    print(f"Clasa: {race} -> Numar de instanțe: {count}")
