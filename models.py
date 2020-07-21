import random
import numpy as np

def sentiment(text):
    results = ['positive', 'negative']
    res = np.random.choice(results)
    return res
