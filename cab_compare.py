import streamlit as st
import random

# Cab apps and ride types
CAB_PROVIDERS = ["Uber", "Ola", "Rapido", "Bounce"]
RIDE_TYPES = ["Sedan", "Hatchback", "Bike"]

def generate_estimate():
    """Random fare estimate between 250 and 400 INR"""
    return random.randint(250, 400)

def generate_eta():
    """Random ETA between 2 and 10 minutes"""
    return random.randint(2, 10)

st.title("🚕 Cab Price Comparison Prototype - All Ride Types")

# User inputs
pickup = st.text_input("Enter Pickup Location", "Andheri, Mumbai")
drop = st.text_input("Enter Drop Location", "BKC, Mumbai")

# Compare button
if st.button("Compare Prices"):
    st.write(f"Comparing cab prices from **{pickup}** to **{drop}** for all ride types:")

    results = []
    for provider in CAB_PROVIDERS:
        for ride in RIDE_TYPES:
            price = generate_estimate()
            eta = generate_eta()
            results.append({
                "Cab App": provider,
                "Ride Type": ride,
                "Estimated Fare": price,  # keep as number for sorting
                "ETA": f"{eta} mins"
            })

    # Sort results by cheapest fare
    results = sorted(results, key=lambda x: x["Estimated Fare"])

    # Convert fare back to string with currency for display
    for r in results:
        r["Estimated Fare"] = f"₹{r['Estimated Fare']}"

    # Display results
    st.table(results)
