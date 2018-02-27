FPWORDS = list()
FNWORDS = list()
import numpy as np
def cross_validation(X, y):
    #import random
    #combined = list(zip(X, y))
    #random.shuffle(combined)
    #X[:], y[:] = zip(*combined)

    avg_precision = 0
    avg_recall = 0
    n_fold = 8
    n_data = len(y)
    n_test = int(n_data/n_fold)
    for i in range(n_fold):
        # generate test_X, test_y, train_X, train_y
        test_start = n_test*i
        test_end = n_test*(i+1) if i < n_fold-1 else n_data+1
        test_X = X[test_start:test_end]
        test_y = y[test_start:test_end]
        train_X = X[:test_start]
        train_X.extend(X[test_end:])
        train_y = y[:test_start]
        train_y.extend(y[test_end:])

        train_X = np.matrix(train_X)
        train_y = np.matrix(train_y).T
        # predict y from test_X
        predict_y = get_predict(train_X, train_y, test_X, "forest")

        # calculate precision and recall
        precision, recall = cal_precision_recall(predict_y, test_y, test_X, test_start)

        avg_precision += precision
        avg_recall += recall

    avg_precision /= n_fold
    avg_recall /= n_fold
    print("precision: {}, recall:{}".format(avg_precision, avg_recall))


def get_predict(train_X, train_y, test_X, model):
    if model == "svm":
        from sklearn import svm
        clf = svm.SVC(gamma=0.125, C=0.5, kernel='poly', tol=1e-4)
    elif model == "logistic":
        from sklearn import linear_model
        clf = linear_model.LogisticRegression(penalty='l2', C=4, intercept_scaling=10, solver='newton-cg')
    elif model == "linear":
        from sklearn import linear_model
        clf = linear_model.LinearRegression()
    elif model == "forest":
        from sklearn.ensemble import RandomForestClassifier
        clf = RandomForestClassifier(n_estimators=30, criterion="entropy", max_features=None, min_samples_split=18)
    elif model == "tree":
        from sklearn import tree
        clf = tree.DecisionTreeClassifier(criterion="entropy", max_depth=8, min_samples_leaf=3, min_impurity_split=0.5)
    elif model == "adaboost":
        from sklearn.ensemble import AdaBoostClassifier
        clf = AdaBoostClassifier(algorithm='SAMME')
    elif model == "gaussian":
        from sklearn.gaussian_process import GaussianProcessClassifier
        clf = GaussianProcessClassifier()
    elif model == "nb":
        from sklearn.naive_bayes import GaussianNB
        clf = GaussianNB()
    elif model == "neighbor":
        from sklearn.neighbors import KNeighborsClassifier
        clf = KNeighborsClassifier(n_neighbors=15, algorithm='auto', p=1, metric="russellrao")
    elif model == "mlp":
        from sklearn.neural_network import MLPClassifier
        clf = MLPClassifier(solver='adam', alpha=0.5)
    elif model == "quadratic":
        from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
        clf = QuadraticDiscriminantAnalysis()
    clf.fit(train_X, train_y)
    return clf.predict(test_X)


def cal_precision_recall(predict_y, test_y, test_X, start_idx):
    true_negative = 0
    true_positive = 0
    false_negative = 0
    false_positive = 0
    idx = 0
    for py, ty in zip(predict_y, test_y):
        if py == 0:
            if ty == 0:
                true_negative += 1
            else:
                false_negative += 1
                #FNWORDS.add(word0_map[test_X[idx][0]])
                FNWORDS.append(start_idx+idx)
        else:
            if ty == 1:
                true_positive += 1
            else:
                false_positive += 1
                #FPWORDS.add(word0_map[test_X[idx][0]])
                FPWORDS.append(start_idx+idx)
        idx += 1

    precision = true_positive/(true_positive+false_positive)
    recall = true_positive/(true_positive+false_negative)

    return precision, recall


if __name__ == '__main__':
    mode = "cv" # cv, IJ
    from sklearn import preprocessing
    from sklearn.preprocessing import LabelEncoder
    lb = LabelEncoder()
    import csv

    all_X = list()
    all_y = list()
    word_0 = list()
    with open('processed_I.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(spamreader)[3:]
        for row in spamreader:
            all_X.append([float(e) for e in row[4:]])
            word_0.append(row[3])
            all_y.append(int(row[2]))

    JX = list()
    Jy = list()

    if mode == "IJ":
        with open('processed_J.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            next(reader)
            for row in reader:
                JX.append([float(e) for e in row[4:]])
                word_0.append(row[3])
                Jy.append(int(row[2]))
    
    word0_map = dict()
    word_0_label = preprocessing.scale(lb.fit_transform(word_0))
    for w0, w0l in zip(word_0, word_0_label):
        word0_map[w0l] = w0
    for w0l, X in zip(word_0_label, all_X + JX):
        X.insert(0, w0l)

    # feature selection - Tree Based
    import numpy as np
    from sklearn.ensemble import ExtraTreesClassifier
    from sklearn.feature_selection import SelectFromModel
    X = np.matrix(all_X)
    y = np.matrix(all_y).T
    print(X.shape)
    clf = ExtraTreesClassifier()
    clf = clf.fit(X, y)
    model = SelectFromModel(clf, prefit=True)
    X_new = model.transform(X)
    print(X_new.shape)

    # print selected features
    #selected_features = [h for i, h in enumerate(header) if i in clf.feature_importances_.argsort()[-X_new.shape[1]:][::-1]]
    #print(sorted(clf.feature_importances_.argsort()[-X_new.shape[1]:][::-1]))
    selected_features = list()
    for idx in clf.feature_importances_.argsort()[-X_new.shape[1]:][::-1]:
        selected_features.append(header[idx])
    #print(selected_features)
    all_X = X_new.tolist()
     
    if mode == "cv":
        cross_validation(all_X, all_y)
    elif mode == "IJ":
        JX_new = model.transform(JX)
        predict_y = get_predict(all_X, all_y, JX_new, "forest")
        precision, recall = cal_precision_recall(predict_y, Jy, JX_new)
        print("precision: {}, recall:{}".format(precision, recall))


    # generate false positive and false negative data csv
    if mode == "cv":
        fp_csv = 'I_false_positive.csv'
        fn_csv = 'I_false_negative.csv'
    elif mode == "IJ":
        fp_csv = 'J_false_positive.csv'
        fn_csv = 'J_false_negative.csv'

    orig_data = list()
    with open('set_I_examples.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        next(reader)
        for row in reader:
            orig_data.append(row)

    with open(fp_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for i in FPWORDS:
            writer.writerow(orig_data[i])
    with open(fn_csiv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for i in FNWORDS:
            writer.writerow(orig_data[i])
    #print(FPWORDS)
    #print(FNWORDS)
