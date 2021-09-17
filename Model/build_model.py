from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

from Data.data import df, df2, df3, df4

from pathlib import Path
import pandas as pd


def build_model(dataframe_list):
    combined_dfs = pd.concat(dataframe_list, join='inner')
    ml_dfs = pd.get_dummies(combined_dfs, columns=['Started', 'Home/Away'], prefix='', prefix_sep='')
    ml_dfs.dropna(inplace=True)

    y = ml_dfs['Draftkings Fantasy Points Scored'].values
    X = ml_dfs.drop(columns=['Draftkings Fantasy Points Scored', 'Opponent', 'Draftkings Position', 'Pos', 'Draftkings Salary', 'Age']).values

    scaler = StandardScaler().fit(X)
    X = scaler.transform(X)

    number_input_features = 24

    nn = Sequential()
    # Hidden layer
    nn.add(Dense(units=50, input_dim=number_input_features, activation="relu"))
    nn.add(Dense(units=100, activation="relu"))
    nn.add(Dense(units=200, activation="tanh"))
    nn.add(Dense(units=100, activation="relu"))
    nn.add(Dense(units=50, activation="relu"))

    # Output layer
    nn.add(Dense(units=1, activation="linear"))

    # Compile the model
    nn.compile(loss="mean_squared_error", optimizer="adam", metrics=["mse"])

    # Train the model
    nn.fit(X, y, validation_split=0.3, epochs=10)

    # Save model as JSON
    nn_json = nn.to_json()

    model_file_path = Path("Model/model.json")
    with open(model_file_path, "w") as json_file:
        json_file.write(nn_json)

    # Save weights
    weights_file_path = "Model/model.h5"
    nn.save_weights(weights_file_path)


dataframes = [df, df2, df3, df4]
build_model(dataframes)