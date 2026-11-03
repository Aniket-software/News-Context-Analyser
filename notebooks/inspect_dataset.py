import pandas as pd
import os

data_path = "data/raw"

files = ["train.tsv", "validation.tsv", "test.tsv"]

for file in files:
    path = os.path.join(data_path, file)

    df = pd.read_csv(path, sep="\t")

    print("\n-----------------------------")
    print("File:", file)
    print("Dataset shape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nMissing values:")
    print(df.isnull().sum())