import sys,os
original_stdout=sys.stdout
sys.stdout=open(os.devnull,"w")
from data import data_without_duplicates
sys.stdout=original_stdout


data_numerical = data_without_duplicates

encripting_per_header = {}  # pt fiecare coloana -> cuvant: encriptare numerica
temp_values_per_header = {}  # pt fiecare coloana -> valorile care au deja asociate un nr
non_numeric_count_per_header = {}  # pt fiecare coloana -> cate valori non-numerice
distinct_non_numeric_values = []  # nr total de valori non-numerice gasite
distinct_non_numeric_count_per_column = {}  # pentru fiecare coloana -> cate valori non-numerice sunt

for d in data_numerical:
    for cheie, valoare in d.items():
        if not isinstance(valoare, (int, float)) and not valoare.isdigit():

            if cheie not in temp_values_per_header:
                temp_values_per_header[cheie] = []  
                encripting_per_header[cheie] = {}  
                non_numeric_count_per_header[cheie] = 0  
                distinct_non_numeric_count_per_column[cheie] = set()  

            non_numeric_count_per_header[cheie] += 1

            if valoare not in distinct_non_numeric_values:
                distinct_non_numeric_values.append(valoare)
            
            distinct_non_numeric_count_per_column[cheie].add(valoare)

            if valoare not in temp_values_per_header[cheie]:
                temp_code = len(temp_values_per_header[cheie])
                temp_values_per_header[cheie].append(valoare)
                encripting_per_header[cheie][valoare] = temp_code
                d[cheie] = temp_code  
            else:
                d[cheie] = encripting_per_header[cheie][valoare]  

print("\n-------------------------------------------------------------------------------------------------------------")
print(f"Non-numeric distinct values count per column (in total {len(distinct_non_numeric_values)}):\n")
for cheie, distinct_values in distinct_non_numeric_count_per_column.items():
    print(f"{cheie}: {len(distinct_values)} distinct non-numeric values")

print("\n-------------------------------------------------------------------------------------------------------------")
for cheie in encripting_per_header:
    print(f"\nThese are the encripted values for {cheie}:")
    for valoare in encripting_per_header[cheie]:
        print(valoare, ":", encripting_per_header[cheie][valoare])

# print("\n-------------------------------------------------------------------------------------------------------------")
# print("Criptarea finală a datelor din 'data_without_duplicates':")
# for record in data_numerical:
#     print(record)
