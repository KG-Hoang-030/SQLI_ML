import numpy as np
import pandas as pd
import seaborn as sn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn import metrics
import matplotlib.pyplot as plt
import pickle as cPickle
import featureExtraction


# Take feature vector
path = '/SQLI/Training/'
ds = pd.read_csv(path + "data.csv", encoding='utf-8')

# Present data as dataFrame
df = pd.DataFrame(ds,columns=['Length', 'Keywords', 'KeywordsFreq', 'InSpcChars', 'InComment', 'InWildcards', 'InEscape', 
                              'SpcCharsFreq', 'unionStr', 'errorBaseStr', 'boolStr', 'timeBaseStr', 'InParam', 'InEncoding', 'errorMess', 
                              'storedProc', 'unusualChars', 'hasSubquery', 'hasMulquery', 'conditionStm', 'hasUnusualContent', 'binaryDataFeature', 
                              'dbSpecific', 'httpHeader', 'Cookies', 'httpRequest', 'webRelated', 'Label'])

X = df[['Length', 'Keywords', 'KeywordsFreq', 'InSpcChars', 'InComment', 'InWildcards', 'InEscape', 'SpcCharsFreq', 'unionStr', 
        'errorBaseStr', 'boolStr', 'timeBaseStr', 'InParam', 'InEncoding', 'errorMess', 'storedProc', 'unusualChars', 'hasSubquery', 
        'hasMulquery', 'conditionStm', 'hasUnusualContent', 'binaryDataFeature', 'dbSpecific', 'httpHeader', 'Cookies', 'httpRequest', 'webRelated']]
X.fillna(0, inplace=True)
y = df['Label']

# Preprocessing 
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.20)

rf = RandomForestClassifier(n_estimators =40) # 40 trees

'''
print(X_train.isnull().sum())
X.fillna(0, inplace=True)
print(X_train.isnull().sum())
'''

rf.fit (X_train,y_train)
y_pred = rf.predict(X_test)

# Cross validation(10 folds)
print(np.mean(cross_val_score(rf, X_train, y_train, cv=10)))

# Confusion Matrix
confusion_matrix = pd.crosstab(y_test,y_pred,rownames=['Actual'],colnames=['Predicted'])
sn.heatmap(confusion_matrix,annot=True)
print(confusion_matrix)



print('Accuracy: ',metrics.accuracy_score(y_test,y_pred))
print('F1 Score: ',metrics.f1_score(y_pred, y_test))
print('Precision Score: ', metrics.precision_score(y_pred, y_test))
print('Recall Score: ', metrics.recall_score(y_pred, y_test))

plt.show()

# Save Model
with open('/SQLI/Model/trainModel', 'wb') as f:
    cPickle.dump(rf, f)