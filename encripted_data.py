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

encripting = {} #aici stocam toate variabilele schimbate si cu ce sunt ele schimate
temp_values = [] #aici stocam toate valorile pe care le schimbam
unique_numbers=[] # aici stocam toate valorile unice cu care schimbam valorile din timp_values
data_numerical=data_without_duplicates

for dictionar in data_numerical:
    for cheie, valoare in dictionar.items():
        if not isinstance(valoare, (int, float)) and not valoare.isdigit(): #vedem daca nu e int sau float sau daca nu e string ce poate fi int
            if valoare not in temp_values: #daca nu am schimbat deja anterior variabila
                temp = encoding()
                while temp in unique_numbers: #generam numere pana cand gasim unul care nu a mai fost folosit
                    temp = encoding()
                unique_numbers.append(temp)

                temp_values.append(valoare)
                encripting[valoare] = temp
                dictionar[cheie] = temp #inlocuim valoarea
            else:
                dictionar[cheie] = encripting[valoare] #inlocuim valoarea cu cea deja generata in alti pasi

print(data_numerical)

print("These are the encripted values:")
for cheie in encripting:
    print(cheie, ":", encripting[cheie])
