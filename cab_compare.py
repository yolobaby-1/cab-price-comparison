import streamlit as st
import random
import urllib.parse

# Cab providers
CAB_PROVIDERS = ["Uber", "Ola", "Rapido", "Indrive"]
RIDE_TYPES = ["Sedan", "Hatchback", "Bike"]

def generate_estimate():
    return random.randint(250, 400)

def generate_eta():
    return random.randint(2, 10)

def apply_surge(price):
    """Random surge: +0% to +50%"""
    surge_multiplier = random.uniform(1.0, 1.5)
    return int(price * surge_multiplier), surge_multiplier

def generate_deep_link(provider, pickup, drop, ride_type):
    pickup_encoded = urllib.parse.quote(pickup)
    drop_encoded = urllib.parse.quote(drop)
    
    if provider.lower() == "uber":
        return f"https://m.uber.com/ul/?action=setPickup&pickup={pickup_encoded}&dropoff={drop_encoded}&ride_type={ride_type}"
    elif provider.lower() == "ola":
        return f"https://book.olacabs.com/?pickup={pickup_encoded}&drop={drop_encoded}&ride_type={ride_type}"
    elif provider.lower() == "rapido":
        return f"https://rapido.bike/book?pickup={pickup_encoded}&drop={drop_encoded}&ride_type={ride_type}"
    elif provider.lower() == "indrive":
        return f"https://indriver.com/app?pickup={pickup_encoded}&drop={drop_encoded}&ride_type={ride_type}"
    else:
        return "#"

st.title("🚕 Cab Price Comparison - Interactive MVP")

pickup = st.text_input("Enter Pickup Location", "Andheri, Mumbai")
drop = st.text_input("Enter Drop Location", "BKC, Mumbai")

# Select one or multiple ride types
selected_rides = st.multiselect("Select Ride Type(s)", RIDE_TYPES, default=RIDE_TYPES)

if st.button("Compare Prices"):
    st.write(f"Showing results from **{pickup}** to **{drop}** for selected ride types: {', '.join(selected_rides)}")

    results = []
    for provider in CAB_PROVIDERS:
        for ride in RIDE_TYPES:
            if ride not in selected_rides:
                continue
            price = generate_estimate()
            surge_price, surge_multiplier = apply_surge(price)
            eta = generate_eta()
            results.append({
                "Cab App": provider,
                "Ride Type": ride,
                "Base Fare": price,
                "Fare": surge_price,
                "ETA": eta,
                "Surge Multiplier": surge_multiplier,
                "Value": surge_price + eta*10  # simple value metric
            })

    if not results:
        st.warning("No ride types selected!")
    else:
        # Highlight best option by Value
        best_option = min(results, key=lambda x: x["Value"])

        # Sort by fare
        results = sorted(results, key=lambda x: x["Fare"])

        # Display table with Book Now buttons
        for r in results:
            fare_str = f"₹{r['Fare']}"
            eta_str = f"{r['ETA']} mins"
            link = generate_deep_link(r["Cab App"], pickup, drop, r["Ride Type"])

            # Highlight surge fares in red
            if r["Surge Multiplier"] > 1.1:
                fare_display = f"<span style='color:red'>{fare_str} (Surge x{r['Surge Multiplier']:.2f})</span>"
            else:
                fare_display = fare_str

            if r == best_option:
                st.markdown(f"✅ **{r['Cab App']} | {r['Ride Type']} | {fare_display} | {eta_str}**", unsafe_allow_html=True)
                st.markdown(f"[**Book Now**]({link})", unsafe_allow_html=True)
            else:
                st.markdown(f"{r['Cab App']} | {r['Ride Type']} | {fare_display} | {eta_str}", unsafe_allow_html=True)
                st.markdown(f"[Book Now]({link})", unsafe_allow_html=True)
