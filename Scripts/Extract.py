import featureExtraction
import pandas as pd


queryAttack = []
label1 = 1
with open('/SQLI/Dataset/queryAttack.txt', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        queryAttack.append((featureExtraction.featureExtr2(line,label1)))


feature_names = ['Length', 'Keywords', 'KeywordsFreq', 'InSpcChars', 'InComment', 'InWildcards', 'InEscape', 
                 'SpcCharsFreq', 'unionStr', 'errorBaseStr', 'boolStr', 'timeBaseStr', 'InParam', 'InEncoding', 
                 'errorMess', 'storedProc', 'unusualChars', 'hasSubquery', 'hasMulquery', 'conditionStm', 'hasUnusualContent', 
                 'binaryDataFeature', 'dbSpecific', 'httpHeader', 'Cookies', 'httpRequest', 'webRelated', 'Label']
attack = pd.DataFrame(queryAttack, columns=feature_names)
# print(attack)
attack.to_csv(r'/SQLI/Training/trainingQueryAttack.csv', index=False)


queryLegit = []
label0 = 0
with open('/SQLI/Dataset/queryLegit.txt', encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        queryLegit.append((featureExtraction.featureExtr2(line,label0)))

feature_names = ['Length', 'Keywords', 'KeywordsFreq', 'InSpcChars', 'InComment', 'InWildcards', 'InEscape', 
                 'SpcCharsFreq', 'unionStr', 'errorBaseStr', 'boolStr', 'timeBaseStr', 'InParam', 'InEncoding', 
                 'errorMess', 'storedProc', 'unusualChars', 'hasSubquery', 'hasMulquery', 'conditionStm', 'hasUnusualContent', 
                 'binaryDataFeature', 'dbSpecific', 'httpHeader', 'Cookies', 'httpRequest', 'webRelated', 'Label']
legit = pd.DataFrame(queryLegit, columns=feature_names)
legit.to_csv(r'/SQLI/Training/trainingQueryLegit.csv', index=False)

