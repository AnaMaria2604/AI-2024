# setari ca sa nu mai apara print-ruile de la fisierele din care import date
import numpy as np
import pandas as pd
from encripted_data import data_numerical as data
import sys
import os
original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')  # mute print


sys.stdout.reconfigure(encoding='utf-8')


sys.stdout = original_stdout  # unmute print

# convertim lista de dictionare in DataFrame (structutra similara cu un tabel)
df = pd.DataFrame(data)

# calculam matricea de corelatie
correlation_matrix = df.corr()

# optional: setari pentru a vedea in intregime matricea in terminal (altfel se vedeau doar primele si ultimele coloane si "...")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print(correlation_matrix)

##############################################


def distribution_and_extremes(correlation_matrix):
    # convert DataFrame la matrice clasica (array numpy)
    matrix_values = correlation_matrix.values

    # valori extreme
    max_value = np.max(correlation_matrix)
    min_value = np.min(correlation_matrix)

    print(f"Max value: {max_value}")
    print(f"Min value: {min_value}")

    # distributie per interval
    # [-1, -0.9], [-0.9, -0.8], ..., [0.9, 1.0]
    intervals = np.arange(-1, 1.1, 0.1)

    # initializam dictionar cu cheile (intervalele) si 0-uri
    count_per_interval = {}
    for i in range(len(intervals) - 1):
        # cheile dictionarului sunt sub forma [start, end)
        key = f"[{round(intervals[i], 1)}, {round(intervals[i+1], 1)})"
        count_per_interval[key] = 0

   # calculam numarul de valori din fiecare interval
    for i in range(len(intervals) - 1):
        start_interval = intervals[i]
        end_interval = intervals[i + 1]
        key = f"[{round(start_interval, 1)}, {round(end_interval, 1)})"
        count_per_interval[key] = np.sum(
            (matrix_values >= start_interval) & (matrix_values < end_interval))

    # print
    for interval, count in count_per_interval.items():
        print(f"{interval}: {count} valori")

    # sunt 27 valori, avem 27 de coloane -> avem 1 doar pe diagonala principala
    print(np.sum(matrix_values == 1.0), "valori sunt egale cu 1")


distribution_and_extremes(correlation_matrix)
