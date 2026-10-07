import streamlit as st

from logic import ZONES, TIME_BLOCKS, COSTS, best_promise_time

st.title("Rosa's Pizza: Best Delivery Promise")
st.write("Choose a zone and time block, and find the promised delivery time that earns the most profit.")

# 1. Zone and time block dropdowns
zone = st.selectbox("Zone", ZONES)
time_block = st.selectbox("Time block", TIME_BLOCKS)

# 2. Range of promised times to try
min_promise, max_promise = st.slider(
    "Range of promised times to try (minutes)", 3, 90, (3, 63)
)
step = st.number_input("Step (minutes)", min_value=1, max_value=30, value=3)

# 3. Cost inputs (defaults come from COSTS in the notebook)
margin = st.number_input("Profit margin per order ($)", min_value=0.0, value=float(COSTS["margin"]))
churn = st.number_input("Estimated churn per late order (lost future orders)", min_value=0.0, value=float(COSTS["churn_orders"]))
refund = st.number_input("Refund cost per late order ($)", min_value=0.0, value=float(COSTS["refund"]))

# 4. Button to calculate
if st.button("Find best promise"):
    if min_promise >= max_promise:
        st.error("The minimum promise must be smaller than the maximum.")
    else:
        promise_B = list(range(min_promise, max_promise + 1, int(step)))
        costs = {"refund": refund, "churn_orders": churn, "margin": margin}

        best_promise, best_profit = best_promise_time(zone, time_block, promise_B, costs)

        st.success(f"Recommended promise for {zone}, {time_block}: **{best_promise} minutes**")
        st.write(f"Expected profit: ${best_profit:,.2f}")
        st.caption("Delivery times are simulated, so results may vary slightly between runs.")
