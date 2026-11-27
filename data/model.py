import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer


def train_model():

    df = pd.read_csv("data/Food_Delivery_Times.csv")

    df.columns = df.columns.str.strip().str.replace(" ","_").str.replace("(","").str.replace(")", "").str.replace("-","_")
    print(df.columns.tolist())

    X = df.drop(columns=["Delivery_Time_min", "Order_ID"], errors="ignore")
    y = df["Delivery_Time_min"]

    numeric_features = X.select_dtypes(include=["number"]).columns
    categorical_features = X.select_dtypes(include=["object"]).columns

    numeric_transformer = SimpleImputer(strategy="median")

    categorical_transformer = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ])

    model = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X, y)

    return model


def predict_delivery(model, distance, weather, traffic, time_of_day,
                     vehicle_type, preparation, experience):

    data = pd.DataFrame([{
        "Distance_km": distance,
        "Weather": weather,
        "Traffic_Level": traffic,
        "Time_of_Day": time_of_day,
        "Vehicle_Type": vehicle_type,
        "Preparation_Time_min": preparation,
        "Courier_Experience_yrs": experience
    }])
    return model.predict(data)[0]
