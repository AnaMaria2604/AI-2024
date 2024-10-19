from data import data_without_duplicates
import random


def encoding():
    '''Aici vom face ca un fel de parola unica de 12 caractere de la 0 la 9 '''
    ch = []
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    for i in range(1, 13):
        number = random.choice(numbers)
        ch.append(number)

    password = ""
    random.shuffle(ch)
    for i in ch:
        password += i

    return password


data_numerical = data_without_duplicates

encripting_per_header = {}  # pt fiecare coloana-> cuvant: encriptare numerica
temp_values_per_header = {}  # pt fiecare coloana-> valorile care au deja asociate un nr
unique_numbers_per_header = {}  # pt fiecare coloana-> numerele asociate variabilelor din temp_values_per_header
non_numeric_count_per_header = {}  # pt fiecare coloana-> cate valori non-numerice
distinct_non_numeric_values = []  # nr total de valori non-numerice gasite
distinct_non_numeric_count_per_column = {}  # pentru fiecare coloana-> cate valori non-numerice sunt

for d in data_numerical:
    for cheie, valoare in d.items():
        if not isinstance(valoare, (int, float)) and not valoare.isdigit():

            if cheie not in temp_values_per_header:
                temp_values_per_header[cheie] = []
                unique_numbers_per_header[cheie] = []
                encripting_per_header[cheie] = {}
                non_numeric_count_per_header[cheie] = 0
                distinct_non_numeric_count_per_column[cheie] = set()

            non_numeric_count_per_header[cheie] += 1
            if valoare not in distinct_non_numeric_values:
                distinct_non_numeric_values.append(valoare)
            distinct_non_numeric_count_per_column[cheie].add(valoare)

            if valoare not in temp_values_per_header[cheie]:
                temp = encoding()

                while temp in unique_numbers_per_header[cheie]:
                    temp = encoding()

                unique_numbers_per_header[cheie].append(temp)

                temp_values_per_header[cheie].append(valoare)
                encripting_per_header[cheie][valoare] = temp
                d[cheie] = temp
            else:
                d[cheie] = encripting_per_header[cheie][valoare]

# print(data_numerical)

print("\n-------------------------------------------------------------------------------------------------------------")
print(f"Non-numeric distinct values count per column(in total {len(distinct_non_numeric_values)}):")
for cheie, distinct_values in distinct_non_numeric_count_per_column.items():
    print(f"{cheie}: {len(distinct_values)} distinct non-numeric values")

print("\n-------------------------------------------------------------------------------------------------------------")
for cheie in encripting_per_header:
    print(f"\nThese are the encripted values for {cheie}:")
    for valoare in encripting_per_header[cheie]:
        print(valoare, ":", encripting_per_header[cheie][valoare])

# print("\n-------------------------------------------------------------------------------------------------------------")
# print(f"Total distinct non-numeric values: {len(distinct_non_numeric_values)}")
# print("Distinct non-numeric values found:")
# print(distinct_non_numeric_values)