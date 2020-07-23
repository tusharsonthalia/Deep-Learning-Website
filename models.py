import random
import numpy as np

def sentiment(text):
    results = ['positive', 'negative']
    res = np.random.choice(results)
    return res

def cnn(image):
    results = ['cat', 'dog']
    res = np.random.choice(results)
    return res
