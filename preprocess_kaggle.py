import pandas as pd

df = pd.read_csv(
    "data/household_power_consumption.csv",
    sep=';',
    low_memory=False
)

df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"], errors="coerce")

df["Global_active_power"] = pd.to_numeric(df["Global_active_power"], errors="coerce")

df = df.dropna()

# Convert to daily energy (kWh approx)
df["date"] = df["DateTime"].dt.date

daily_energy = df.groupby("date")["Global_active_power"].mean().reset_index()
daily_energy.columns = ["date", "avg_power_kw"]

daily_energy["daily_energy_kwh"] = daily_energy["avg_power_kw"] * 24

daily_energy.to_csv("data/daily_energy.csv", index=False)

print("Daily energy file created: data/daily_energy.csv")
