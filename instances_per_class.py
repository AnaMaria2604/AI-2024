# setari ca sa nu mai apara print-ruile de la fisierele din care import date
import sys, os
original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w') # mute print

from data import data_without_duplicates

sys.stdout = original_stdout # unmute print

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
print(f"Numarul total de clase este: {len(class_counts)}")