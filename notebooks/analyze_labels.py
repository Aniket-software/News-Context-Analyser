import pandas as pd

train = pd.read_csv("data/raw/train.tsv", sep="\t")

print("Label Distribution:")
print(train["label"].value_counts())

print("\nLabel Percentages:")
print(train["label"].value_counts(normalize=True) * 100)

print("\nSample Fake News:")
print(train[train["label"] == 0]["title"].head(3))

print("\nSample Real News:")
print(train[train["label"] == 1]["title"].head(3))