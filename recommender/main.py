import pickle
import os
import pandas

with open("./data/War", 'rb') as f:
    print(pickle.load(f).head(10))
