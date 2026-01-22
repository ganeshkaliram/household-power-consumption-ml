import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("data/daily_energy.csv")

# Simple time features
df["day_index"] = range(len(df))

X = df[["day_index"]]
y = df["daily_energy_kwh"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "model/energy_model.pkl")
print("Model trained and saved.")
