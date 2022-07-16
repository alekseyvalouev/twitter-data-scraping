import pandas as pd

df = pd.read_csv("temp_save.csv")

print(df["id"].notnull().sum())