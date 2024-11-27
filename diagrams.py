import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# setari ca sa nu mai apara print-ruile de la fisierele din care import date
import sys, os
original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w') # mute print

#from data import data_without_duplicates
data_without_duplicates = pd.read_json("balanced_data.json")

sys.stdout = original_stdout # unmute print

def generate_histograms(df):
    # parcurgem toate coloanele din DataFrame
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            # date numerice
            plt.figure(figsize=(9, 7))
            df[column].value_counts().plot(kind='bar', edgecolor='black')
            plt.title(f'Histogram for {column}')
            plt.xlabel(column)
            plt.xticks(rotation=45, fontsize=10)  # setam rotirea labelurilor pe x
            plt.ylabel('Frequency')
            plt.show()
        else:
            # date non-numerice
            plt.figure(figsize=(9, 7))
            df[column].value_counts().plot(kind='bar', edgecolor='black')
            plt.title(f'Histogram for {column}')
            plt.xlabel(column)
            plt.xticks(rotation=45, fontsize=10)  # setam rotirea labelurilor pe x
            plt.ylabel('Frequency')
            plt.show()

def generate_boxplots(df):
    # parcurgem toate coloanele din DataFrame
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            # date numerice
            plt.figure(figsize=(9, 7))  # setem dimensiunea graficului
            plt.title(f'Boxplot for {column}', fontsize=16, pad=20)  # setam titlul
            sns.boxplot(df[column]) # generam box
            plt.xlabel(column, fontsize=14, labelpad=15)  # setam label pe x
            plt.xticks(rotation=45, fontsize=10)  # setam rotirea labelurilor pe x
            plt.yticks(fontsize=10) # setam dimensiunea labelurilor pe y
            plt.tight_layout() # ajustam dimensiunea graficului
            plt.show()
        else:
            # cautam cate o variabila numerica pentru a crea boxplot in functie de o variabila non-numerica 
            # (facem toate combinatiile posibile)
            numeric_columns = df.select_dtypes(include=['number']).columns
            for num_col in numeric_columns:
                plt.figure(figsize=(9, 7))
                sns.boxplot(x=df[column], y=df[num_col])
                plt.title(f'Boxplot for {num_col} by {column}', fontsize=16, pad=20)
                plt.xlabel(column, fontsize=14, labelpad=15)  # setam label pe x
                plt.ylabel(num_col, fontsize=14, labelpad=15)  # setam label pe y
                plt.xticks(rotation=45, fontsize=10)  # rotim labelurile categorice
                plt.yticks(fontsize=10)  # setam dimensiunea labelurilor pe y
                plt.tight_layout()  # ajustam dimensiunea graficului
                plt.show()

df = pd.DataFrame(data_without_duplicates)

#generate_boxplots(df)
generate_histograms(df)