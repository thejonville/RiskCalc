import streamlit as st
import math

st.title("Futures Contracts Position Sizer")

# Updated tick values
tick_values = {
    "GC": 100,    # Gold Futures: $100/tick
    "MGC": 10,    # Micro Gold: $10/tick
    "NQ": 20,     # Nasdaq E-mini: $20/tick
    "MNQ": 2      # Nasdaq Micro: $2/tick
}

st.write("Enter your desired risk and stop size (in ticks):")

risk_amount = st.number_input("Dollar risk per trade", min_value=0.0, value=200.0)
stop_ticks = st.number_input("Stop size (in ticks)", min_value=1, value=8)

st.header("Recommended Contracts and Dollar Risk")

def calc_contracts(risk, stop, tick_value):
    contracts = risk / (stop * tick_value)
    return max(0, math.floor(contracts))

data = {"Market": [], "Contracts": [], "Actual Dollar Risk": []}
for market, tick_value in tick_values.items():
    contracts = calc_contracts(risk_amount, stop_ticks, tick_value)
    actual_risk = contracts * stop_ticks * tick_value
    data["Market"].append(market)
    data["Contracts"].append(contracts)
    data["Actual Dollar Risk"].append(f"${actual_risk:,.2f}")

st.table(data)

if all(c == 0 for c in data["Contracts"]):
    st.warning("Your risk amount is too small for any contract with the chosen stop size.")
