import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from encripted_data import data_numerical

# Assuming data_numerical is already a Pandas DataFrame
data_numerical = pd.DataFrame(data_numerical)

# Function to create histograms with one plot per page and added space
def plot_distributions(df):
    # Histograms for numerical variables
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    for col in numeric_cols:
        plt.figure(figsize=(8, 6))  # Set size for each plot
        sns.histplot(df[col], bins=30, kde=True)  # Histogram + Kernel Density Estimation
        plt.title(f'Histogram for {col}', fontsize=16, pad=20)  # Space between title and chart
        plt.xlabel(col, fontsize=14, labelpad=15)  # Space between label and x-axis
        plt.ylabel('Frequency', fontsize=14)
        plt.xticks(rotation=45, fontsize=10)  # Rotate x-axis labels
        plt.yticks(fontsize=10)

        plt.tight_layout()
        plt.show()

# Call the function to generate one plot per page
plot_distributions(data_numerical)
