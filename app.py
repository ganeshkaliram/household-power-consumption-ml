import streamlit as st

st.set_page_config(page_title="Household Energy Predictor", layout="centered")

import joblib
import numpy as np
import pandas as pd

st.title("🏠 Classroom Power Consumption Prediction (ML)")
st.write("Predict household electricity usage based on appliances and days.")

# Load model
model = joblib.load("model/energy_model.pkl")

st.sidebar.header("Enter Household Details")

days = st.sidebar.number_input("Number of days", 1, 31, 30)
lights = st.sidebar.number_input("Number of lights", 0, 20, 5)
fans = st.sidebar.number_input("Number of fans", 0, 10, 3)
other_appliances = st.sidebar.number_input("Other appliances", 0, 15, 2)

cost_per_kwh = 6  # INR

if st.button("🔮 Predict Energy Consumption"):
    # Base prediction from ML
    base_daily = model.predict(np.array([[0]]))[0]

    # Appliance adjustment
    appliance_factor = (
        lights * 0.05 +
        fans * 0.08 +
        other_appliances * 0.4
    )

    daily_energy = base_daily + appliance_factor
    total_energy = daily_energy * days
    estimated_cost = total_energy * cost_per_kwh

    # Projections
    monthly_energy = daily_energy * 30
    yearly_energy = daily_energy * 365

    monthly_cost = monthly_energy * cost_per_kwh
    yearly_cost = yearly_energy * cost_per_kwh

    # CO2
    co2_per_kwh = 0.82
    co2_emission = total_energy * co2_per_kwh

    # ================= RESULTS =================

    st.subheader("📊 Prediction Results")
    st.success(f"🔋 Total Energy: {total_energy:.2f} kWh")
    st.success(f"💰 Total Cost: ₹{estimated_cost:.2f}")

    st.subheader("📅 Projections")
    st.info(f"📆 Monthly Energy: {monthly_energy:.2f} kWh")
    st.info(f"📆 Monthly Cost: ₹{monthly_cost:.2f}")

    st.info(f"🗓️ Yearly Energy: {yearly_energy:.2f} kWh")
    st.info(f"🗓️ Yearly Cost: ₹{yearly_cost:.2f}")

    st.subheader("🌱 Environmental Impact")
    st.warning(f"Estimated CO₂ Emissions: {co2_emission:.2f} kg")

    # ================= CHART =================

    chart_data = pd.DataFrame({
        "Type": ["Daily", "Monthly", "Yearly"],
        "Energy (kWh)": [daily_energy, monthly_energy, yearly_energy]
    })

    st.subheader("📊 Energy Consumption Chart")
    st.bar_chart(chart_data.set_index("Type"))

    # ================= DOWNLOAD REPORT =================

    report_text = f"""
Household Energy Report

Days: {days}
Lights: {lights}
Fans: {fans}
Other Appliances: {other_appliances}

Daily Energy: {daily_energy:.2f} kWh
Total Energy: {total_energy:.2f} kWh
Total Cost: ₹{estimated_cost:.2f}

Monthly Cost: ₹{monthly_cost:.2f}
Yearly Cost: ₹{yearly_cost:.2f}

CO2 Emission: {co2_emission:.2f} kg
"""

    st.download_button(
        label="⬇️ Download Energy Report",
        data=report_text,
        file_name="energy_report.txt",
        mime="text/plain"
    )

else:
    st.info("⬅️ Enter values and click Predict to see advanced results.")

