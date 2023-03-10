import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load our dataset into a Pandas Dataframe for advanced manipulations.
df = pd.read_csv(r"data_streaming_project/datasets/Orientation.csv")
# Convert our first column which is in UNIX EPOCH time to DMY....a format that Apache Superset will pick easily.
df['time'] = pd.to_datetime(df['time'], unit='ms').dt.strftime('%d-%m-%Y %H:%M:%S')
print(df.head(5))