import pandas as pd
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from tensorflow.keras.models import model_from_json


def load_model(test_df):
    # load json and create model
    model_file_path = Path("Model/model.json")
    with open(model_file_path, "r") as json_file:
        model_json = json_file.read()
    loaded_model = model_from_json(model_json)

    # load weights into new model
    weights_file_path = "Model/model.h5"
    loaded_model.load_weights(weights_file_path)

    test_ml_dfs = pd.get_dummies(test_df, columns=['Started', 'Home/Away'], prefix='', prefix_sep='')
    test_ml_dfs.dropna(inplace=True)

    test_X = test_ml_dfs.drop(columns=['Draftkings Fantasy Points Scored', 'Opponent',
                                       'Draftkings Position', 'Pos', 'Draftkings Salary', 'Age']).values

    scaler = StandardScaler().fit(test_X)
    test_X = scaler.transform(test_X)

    test_ml_dfs["predicted"] = loaded_model.predict(test_X)

    return test_ml_dfs
