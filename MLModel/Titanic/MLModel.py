from DataTransformationUtil import DataTransformationUtil
from ZohoAnalytics import ZohoAnalytics
from ModelStorage import ModelStorage
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os


class MLModel:
    dt: DataTransformationUtil = None
    za: ZohoAnalytics = None
    ms: ModelStorage = None

    def __init__(self, za,ms):
        self.za = za
        self.dt = DataTransformationUtil(self.za)
        self.log = self.za.context.log
        self.ms = ms

    def fit(self):
        train_data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame("TrainData", ["PassengerId","Survived","Pclass","Name","Sex","Age","SibSp","Parch","Ticket","Fare","Cabin","Embarked"],"")
        test_data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame("TestData", ["PassengerId","Pclass","Name","Sex","Age","SibSp","Parch","Ticket","Fare","Cabin","Embarked"],"")
        women = train_data.loc[train_data.Sex == 'female']["Survived"]
        rate_women = sum(women)/len(women)
        self.log.INFO("% of women who survive:"+str(rate_women))
        men = train_data.loc[train_data.Sex == 'male']["Survived"]
        rate_men = sum(men)/len(men)
        self.log.INFO("% of men who survived:"+str(rate_men))
        y = train_data["Survived"]
        features = ["Pclass", "Sex", "SibSp", "Parch"]
        X = pd.get_dummies(train_data[features])
        X_test = pd.get_dummies(test_data[features])
        #Train Model
        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
        model.fit(X, y)
        #Test Trained Model
        predictions = model.predict(X_test)
        output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
        self.log.INFO(output)
        #Save Trained Model
        directory = 'models'
        file_path = os.path.join(directory, 'random_forest_model.pkl')
        os.makedirs(directory, exist_ok=True)
        joblib.dump(model, file_path)
        self.ms.store_model('random_forest_model', file_path)
        self.ms.list_models()
        self.log.INFO("Training Completed...Procced to Predict")

    def predict(self):
        # Path to the .pkl file
        pkl_file_path = self.ms.get_model_path('random_forest_model')
        # Load the model from the .pkl file
        model = joblib.load(pkl_file_path)
        features = ["Pclass", "Sex", "SibSp", "Parch"]
        test_data: pd.DataFrame = self.dt.fetch_tabledata_as_DataFrame("TestData", ["PassengerId","Pclass","Name","Sex","Age","SibSp","Parch","Ticket","Fare","Cabin","Embarked"],"")
        X_test = pd.get_dummies(test_data[features])
        # Now, 'model' contains the deserialized machine learning model
        # You can use the loaded model to make predictions or evaluate it
        # Example usage: Making predictions with the loaded model
        # Assuming you have test data in the variable 'X_test'
        predictions = model.predict(X_test)
        output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
        self.dt.upload_tabledata_from_DataFrame("PredictedData", output, {"importType": "truncateadd"})