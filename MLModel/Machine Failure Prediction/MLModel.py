from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import lightgbm as lgb
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import StackingClassifier
import time


class MLModel:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None
    ms: ModelStorage = None

    def __init__(self, za, ms):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log
        self.ms = ms

    def fit(self):
        table_name = "Machine Failure Prediction Train"
        column_names = ['UDI', 'Product ID', 'Type', 'Air temperature [K]',
                                                                   'Process temperature [K]',
                                                                   'Rotational speed [rpm]', 'Torque [Nm]',
                                                                   'Tool wear [min]', 'Target',
                                                                   'Failure Type']
        data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)

        data = data.drop('Product ID', axis=1)

        # data.groupby(['Target','Failure Type']).count().drop(['Process temperature [K]',
        #                                                     'Rotational speed [rpm]',
        #                                                     'Torque [Nm]',
        #                                                     'Tool wear [min]',
        #                                                     'Air temperature [K]'],axis=1).rename(columns = {'Type':'count'})

        # data['Type'].value_counts()

        Type = ['L', 'M', 'H']

        # Label Encoding Type column
        data['Type'] = data['Type'].apply(lambda x: Type.index(x))

        # data['Target'].value_counts()

        data = data.rename(columns={'Air temperature [K]': 'airtemp', 'Process temperature [K]': 'processtemp',
                                    'Rotational speed [rpm]': 'rpm', 'Torque [Nm]': 'torque',
                                    'Tool wear [min]': 'toolwear'})

        X_train, X_test, y_train, y_test = train_test_split(data.drop(['Failure Type', 'Target'], axis=1),
                                                            data['Target'], test_size=0.3, random_state=4)

        id = pd.Series(X_test['UDI'], name='UDI').astype(int)
        X_test.drop('UDI', axis=1, inplace=True)
        X_train.drop('UDI', axis=1, inplace=True)

        classifier = []
        imported_as = []

        # LGBM
        lgbm = lgb.LGBMClassifier()
        classifier.append('LightGBM')
        imported_as.append('lgbm')

        # MultiLayerPerceptron
        mlp = MLPClassifier()
        classifier.append('Multi Layer Perceptron')
        imported_as.append('mlp')

        # Bagging
        bc = BaggingClassifier()
        classifier.append('Bagging')
        imported_as.append('bc')

        # GBC
        gbc = GradientBoostingClassifier()
        classifier.append('Gradient Boosting')
        imported_as.append('gbc')

        # ADA
        ada = AdaBoostClassifier()
        classifier.append('Ada Boost')
        imported_as.append('ada')

        # XGB
        xgb = XGBClassifier()
        classifier.append('XG Boost')
        imported_as.append('xgb')

        # Logistic Regression
        lr = LogisticRegression()
        classifier.append('Logistic Regression')
        imported_as.append('lr')

        # RFC
        rfc = RandomForestClassifier()
        classifier.append('Random Forest')
        imported_as.append('rfc')

        # KNN
        knn = KNeighborsClassifier(n_neighbors=1)
        classifier.append('k Nearest Neighbours')
        imported_as.append('knn')

        # SVM
        svc = SVC()
        classifier.append('Support Vector Machine')
        imported_as.append('svc')

        # Grid
        param_grid = {'C': [0.1, 1, 10, 100, 1000, 2000], 'gamma': [1, 0.1, 0.01, 0.001, 0.0001], 'kernel': ['rbf']}
        grid = GridSearchCV(SVC(), param_grid, refit=True, verbose=3)
        classifier.append('SVM tuning grid')
        imported_as.append('grid')

        # Stacking
        estimators = [('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
                      ('svr', SVC(random_state=42))]
        stc = StackingClassifier(estimators=estimators, final_estimator=LogisticRegression())
        classifier.append('Stacked (RFR & SVM)')
        imported_as.append('stc')

        classifiers = pd.DataFrame({'Classifier': classifier, 'Imported as': imported_as})
        print('All Models Imported\nModels stored in dataframe called classifiers')

        class Modelling:
            def __init__(self, X_train, Y_train, X_test, Y_test, models):
                self.X_train = X_train
                self.X_test = X_test
                self.Y_train = Y_train
                self.Y_test = Y_test
                self.models = models

            def fit(self):
                model_acc = []
                model_time = []
                for i in self.models:
                    start = time.time()
                    if i == 'knn':
                        accuracy = []
                        for j in range(1, 200):
                            kn = KNeighborsClassifier(n_neighbors=j)
                            kn.fit(self.X_train, self.Y_train)
                            predK = kn.predict(self.X_test)
                            accuracy.append([accuracy_score(self.Y_test, predK), j])
                        temp = accuracy[0]
                        for m in accuracy:
                            if temp[0] < m[0]:
                                temp = m
                        i = KNeighborsClassifier(n_neighbors=temp[1])
                    if i == 'grid':
                        i.fit(self.X_train, self.y_train)
                        i = i.best_estimator_
                        i.fit(self.X_train, self.y_train)
                        model_acc.append(accuracy_score(self.Y_test, i.predict(self.X_test)))
                    i.fit(self.X_train, self.Y_train)
                    model_acc.append(accuracy_score(self.Y_test, i.predict(self.X_test)))
                    stop = time.time()
                    model_time.append((stop - start))
                    print(i, 'has been fit')
                self.models_output = pd.DataFrame(
                    {'Models': self.models, 'Accuracy': model_acc, 'Runtime (s)': model_time})

            def results(self):
                models = self.models_output
                models = models.sort_values(by=['Accuracy', 'Runtime (s)'], ascending=[False, True]).reset_index().drop(
                    'index', axis=1)
                self.best = models['Models'][0]
                models['Models'] = models['Models'].astype(str).str.split("(", n=2, expand=True)[0]
                models['Accuracy'] = models['Accuracy'].round(5) * 100
                self.models_output_cleaned = models
                return (models)

            def best_model(self, type):
                if type == 'model':
                    return (self.best)
                elif type == 'name':
                    return (self.models_output_cleaned['Models'][0])

            def best_model_accuracy(self):
                return (self.models_output_cleaned['Accuracy'][0])

            def best_model_runtime(self):
                return (round(self.models_output_cleaned['Runtime (s)'][0], 3))

            def best_model_predict(self, X_test):
                return (self.best.predict(X_test))

            def best_model_clmatrix(self):
                return (classification_report(self.Y_test, self.best.predict(self.X_test)))

        models_to_test = [bc, gbc, ada, rfc, mlp, lr, knn, stc, lgbm, xgb]

        classification = Modelling(X_train, y_train, X_test, y_test, models_to_test)
        classification.fit()

        self.log.INFO(classification.results())

        self.log.INFO(classification.best_model('model'))
        model = classification.best_model('model')

        preds = classification.best_model_predict(X_test)

        self.log.INFO(classification.best_model_clmatrix())

        y_test.reset_index(drop=True, inplace=True)
        id.reset_index(drop=True, inplace=True)
        output = pd.DataFrame({'Actual': y_test, 'Predicted': preds})

        output = pd.concat([id, output], axis=1)
        self.log.INFO(output)
        # Save Trained Model
        directory = 'models'
        file_path = os.path.join(directory, 'MachineFailurePred.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(model, file_path)
        self.ms.store_model('MachineFailurePred', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):
        table_name = "Machine Failure Prediction Validation"
        column_names = ['UDI', 'Product ID', 'Type', 'Air temperature [K]',
                                                                   'Process temperature [K]',
                                                                   'Rotational speed [rpm]', 'Torque [Nm]',
                                                                   'Tool wear [min]', 'Target',
                                                                   'Failure Type']
        final_table_name = "Predicted Machine Failure Data"
        import_type = "truncateadd"
        # Path to the .pkl file
        pkl_file_path = self.ms.get_model_path('MachineFailurePred')
        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)
        data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame(table_name, column_names)


        data = data.drop('Product ID', axis=1)

        # data.groupby(['Target','Failure Type']).count().drop(['Process temperature [K]',
        #                                                     'Rotational speed [rpm]',
        #                                                     'Torque [Nm]',
        #                                                     'Tool wear [min]',
        #                                                     'Air temperature [K]'],axis=1).rename(columns = {'Type':'count'})

        # data['Type'].value_counts()

        Type = ['L', 'M', 'H']

        # Label Encoding Type column
        data['Type'] = data['Type'].apply(lambda x: Type.index(x))

        # data['Target'].value_counts()

        data = data.rename(columns={'Air temperature [K]': 'airtemp', 'Process temperature [K]': 'processtemp',
                                    'Rotational speed [rpm]': 'rpm', 'Torque [Nm]': 'torque',
                                    'Tool wear [min]': 'toolwear'})

        X = data.drop(['Target', 'Failure Type'], axis=1)
        y = data['Target']

        id = pd.Series(X['UDI'], name='UDI').astype(int)
        X.drop('UDI', axis=1, inplace=True)

        preds = model.predict(X)

        self.log.INFO(accuracy_score(y, preds))
        self.log.INFO(classification_report(y, preds))

        y.reset_index(drop=True, inplace=True)
        id.reset_index(drop=True, inplace=True)
        output = pd.DataFrame({'Actual': y, 'Predicted': preds})

        output = pd.concat([id, output], axis=1)
        self.log.INFO(output)

        self.dt.upload_tabledata_from_DataFrame(final_table_name, output, {"importType": import_type})