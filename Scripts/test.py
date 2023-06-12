import joblib
import pandas as pd

# Load train model
path = '/SQLI/Model/'
loadTM = joblib.load(path + 'trainModel')

# Load file test
path = '/SQLI/Test'
loadTest = pd.read_txt