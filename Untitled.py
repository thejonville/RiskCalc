import streamlit as st
import math

st.title("Futures Contracts Position Sizer")

# Updated tick values
tick_values = {
    "GC": 100,      # Gold Futures: $100/tick
    "MGC": 10,      # Micro Gold: $10/tick
    "NQ": 20,       # Nasdaq E-mini: $20/tick
    "MNQ": 2,       # Nasdaq Micro: $2/tick
    "BTCUSD": 1,    # Bitcoin spot: $1/pip per lot
    "ETHUSD": 1     # Ethereum spot: $1/pip per lot
}

st.write("Enter your desired risk and stop size (in ticks):")

risk_amount = st.number_input("Dollar risk per trade", min_value=0.0, value=200.0)
stop_ticks = st.number_input("Stop size (in ticks)", min_value=0.1, value=8.0, step=0.1)

st.header("Recommended Contracts and Dollar Risk")

def calc_contracts(risk, stop, tick_value):
    contracts = risk / (stop * tick_value)
    return max(0, math.floor(contracts))

data = {"Market": [], "Contracts/Lots": [], "Actual Dollar Risk": []}

for market, tick_value in tick_values.items():
    contracts = calc_contracts(risk_amount, stop_ticks, tick_value)
    actual_risk = contracts * stop_ticks * tick_value
    data["Market"].append(market)
    # Show as "lots" for crypto, "contracts" for others
    if market in ["BTCUSD", "ETHUSD"]:
        data["Contracts/Lots"].append(f"{contracts} lots")
    else:
        data["Contracts/Lots"].append(contracts)
    data["Actual Dollar Risk"].append(f"${actual_risk:,.2f}")

st.table(data)

if all(c == 0 for c in [int(str(c).split()[0]) if isinstance(c, str) else c for c in data["Contracts/Lots"]]):
    st.warning("Your risk amount is too small for any contract with the chosen stop size.")
