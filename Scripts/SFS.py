import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


def sfs(df,k):
    features = df.iloc[:, :-1]
    label = df.iloc[:, -1]
    selected = []
    best_accuracy = 0

    for i in range(k):
        best_feature = None
        for feature in features:
            subset = selected + [feature]
            clf = RandomForestClassifier(n_estimators=40)
            clf.fit(df.loc[:, subset], label)
            accuracy = accuracy_score(label, clf.predict(df.loc[:, subset]))
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_feature = feature
        if best_feature is not None:
            selected.append(best_feature)
            print(best_feature)
        else:
            break

    return df.loc[:, selected + [label.name]]

if __name__ == '__main__':
    input_file = '/SQLI/Training/data.csv'
    output_file = '/SQLI/Training/selected_features_SFS.csv'

    df = pd.read_csv(input_file)
    selected_df = sfs(df,40)
    selected_df.to_csv(output_file, index=False)
