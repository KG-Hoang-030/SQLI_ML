import joblib
import featureExtraction
from tkinter import *
import tkinter as tk 

# Load train model
path = '/SQLI/Model/'
loadTM = joblib.load(path + 'trainModel')

# tkinter GUI
root = Tk()

root.title()

canvas = Canvas(root, width= 600, height=200)
canvas.pack()

# Query
label = Label(root, text='Query: ', font=1)
canvas.create_window(70, 50, window=label)

entry = Entry(root,width=40,font=1)
canvas.create_window(330, 50, window=entry)

def testQuery():
    global query
    query = str(entry.get())

    if loadTM.predict([featureExtraction.featureExtr(query)]) == 0:
        Pred_Result = ('Query vừa nhập là: Lành tính')
        label_Prediction = Label(root, text=Pred_Result,fg='green', font=1)
    else:
        Pred_Result = ('Query vừa nhập là: Độc hại')
        label_Prediction = Label(root, text=Pred_Result,fg='red', font=1)


    canvas.create_window(300, 160, window=label_Prediction)

button = Button (root, text='      Phát hiện      ',command=testQuery, bg='cyan', fg='black',font=1)
canvas.create_window(300, 110, window=button)

root.mainloop()