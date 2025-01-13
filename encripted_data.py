from data import data_without_duplicates
import json
import sys
import os
original_stdout = sys.stdout
sys.stdout = open(os.devnull, "w")
sys.stdout = original_stdout


data_numerical = data_without_duplicates

encripting_per_header = {}  # pt fiecare coloana -> cuvant: encriptare numerica
# pt fiecare coloana -> valorile care au deja asociate un nr
temp_values_per_header = {}
# pt fiecare coloana -> cate valori non-numerice
non_numeric_count_per_header = {}
distinct_non_numeric_values = []  # nr total de valori non-numerice gasite
# pentru fiecare coloana -> cate valori non-numerice sunt
distinct_non_numeric_count_per_column = {}

for d in data_numerical:
    for cheie, valoare in d.items():
        # Verificăm dacă valoarea este un număr; dacă e șir numeric, o convertim în int
        if isinstance(valoare, str) and valoare.isdigit():
            # Convertim șir numeric la int pentru a evita problemele
            d[cheie] = int(valoare)
        elif not isinstance(valoare, (int, float)):
            # Dacă nu e numeric, criptăm valoarea non-numerică
            if cheie not in temp_values_per_header:
                temp_values_per_header[cheie] = []
                encripting_per_header[cheie] = {}
                non_numeric_count_per_header[cheie] = 0
                distinct_non_numeric_count_per_column[cheie] = set()

            non_numeric_count_per_header[cheie] += 1

            # Adăugăm valoarea la lista de valori distincte
            if valoare not in distinct_non_numeric_values:
                distinct_non_numeric_values.append(valoare)

            distinct_non_numeric_count_per_column[cheie].add(valoare)

            # Criptăm valoarea dacă nu a fost criptată anterior
            if valoare not in temp_values_per_header[cheie]:
                temp_code = len(temp_values_per_header[cheie])
                temp_values_per_header[cheie].append(valoare)
                encripting_per_header[cheie][valoare] = temp_code
                d[cheie] = temp_code
            else:
                d[cheie] = encripting_per_header[cheie][valoare]

print("\n-------------------------------------------------------------------------------------------------------------")
print(f"Non-numeric distinct values count per column (in total {
      len(distinct_non_numeric_values)}):\n")
for cheie, distinct_values in distinct_non_numeric_count_per_column.items():
    print(f"{cheie}: {len(distinct_values)} distinct non-numeric values")

print("\n-------------------------------------------------------------------------------------------------------------")
for cheie in encripting_per_header:

    if cheie!="More":
        print(f"\nThese are the encripted values for {cheie}:")
        for valoare in encripting_per_header[cheie]:
            print(valoare, ":", encripting_per_header[cheie][valoare])

# print("\n-------------------------------------------------------------------------------------------------------------")
# print("Criptarea finală a datelor din 'data_without_duplicates':")
# for record in data_numerical:
#     print(record)

with open("data.json", "w") as file:
    json.dump(data_numerical, file, indent=4)
