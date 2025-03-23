import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import requests
import joblib
import os
import pandas as pd
import random
import math
import base64


# Function to encode the image
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


# Function to set the background image
def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
    }
    .reportview-container {
        background: rgba(0,0,0,0);
    }
    .main {
        background-color: rgba(255,255,255,0.8);
        padding: 2rem;
        border-radius: 10px;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


# Add a title to the page
st.title("🚖 Cab Fare Prediction")

# Set the background image
set_background('online-cab-services-image.jpg')

# Set page config
# st.set_page_config(page_title="Cab Fare Prediction", layout="wide")

# Function to get coordinates from location name
def get_coordinates(location):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(location)
    return (location.latitude, location.longitude) if location else None


# Function to get route from TomTom API
def get_route_tomtom(start_coords, end_coords, departure_time=None):
    api_key = "qru7xtW0t1SPzeM5fJDA9SHNuuPRWAE2"
    base_url = "https://api.tomtom.com/routing/1/calculateRoute/"
    coords = f"{start_coords[0]},{start_coords[1]}:{end_coords[0]},{end_coords[1]}"
    params = {
        "key": api_key,
        "traffic": "true",
        "computeBestOrder": "true",
        "travelMode": "car",
        "routeType": "fastest"
    }
    if departure_time:
        params["departAt"] = departure_time

    response = requests.get(base_url + coords + "/json", params=params).json()
    return response.get("routes", [None])[0]


# Function to load trained model
def load_model():
    try:
        model_path = r"saved_models/model.pkl"
        if not os.path.exists(model_path):
            st.error("❌ Model file not found. Ensure 'model.pkl' is in the correct directory.")
            return None
        with open(model_path, 'rb') as file:
            model = joblib.load(file)
        return model
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        return None


# Main content
start_location = st.text_input("Enter Start Location", "Thane")
end_location = st.text_input("Enter Destination Location", "Kharghar Railway Station")
departure_time = st.text_input("Enter Departure Time (YYYY-MM-DDTHH:MM:SS) (Optional)")

if st.button("Find Route"):
    start_coords = get_coordinates(start_location)
    end_coords = get_coordinates(end_location)

    if start_coords and end_coords:
        route = get_route_tomtom(start_coords, end_coords, departure_time)
        if route:
            distance = math.floor(route["summary"]["lengthInMeters"] / 1000)
            duration = math.floor(route["summary"]["travelTimeInSeconds"] / 60)

            st.session_state.route_found = True
            st.session_state.distance = distance
            st.session_state.duration = duration

            st.write(f"### Distance: {distance} km")
            st.write(f"### Estimated Time: {duration} mins")

            m = folium.Map(location=start_coords, zoom_start=10)
            folium.Marker(start_coords, popup="Start", icon=folium.Icon(color="green")).add_to(m)
            folium.Marker(end_coords, popup="Destination", icon=folium.Icon(color="red")).add_to(m)
            route_coords = route["legs"][0]["points"]
            folium.PolyLine([(point["latitude"], point["longitude"]) for point in route_coords], color="blue",
                            weight=5).add_to(m)
            folium_static(m)
        else:
            st.error("❌ Could not retrieve route details. Try again later.")
    else:
        st.error("❌ Invalid locations. Please try again.")

if "route_found" in st.session_state and st.session_state.route_found:
    st.markdown("## 🚕 Trip Details for Fare Prediction")

    col1, col2, col3 = st.columns(3)
    with col1:
        vendor_id = st.selectbox("Cab Provider", options=[1, 2], format_func=lambda x: "OLA" if x == 1 else "UBER")
    with col2:
        st.markdown(f"### 📏 Trip Distance: {st.session_state.distance} km")
    with col3:
        num_passengers = st.number_input("👥 Passengers", min_value=1, max_value=6, value=1)

    col4, col5, col6 = st.columns(3)
    with col4:
        payment_method = st.selectbox("💳 Payment Method", options=[1, 2, 3],
                                      format_func=lambda x: "Cash" if x == 1 else ("Card" if x == 2 else "Other"))
    with col5:
        extra_charges = random.choice([0, 0.50, 1])
        st.markdown(f"### 💰 Extra Charges: ${extra_charges}")
    with col6:
        st.markdown(f"### ⏳ Trip Duration: {st.session_state.duration} mins")

    if st.button("Predict Fare Price"):
        model = load_model()
        if model is None:
            st.warning("⚠️ Fare prediction is unavailable because the model couldn't be loaded.")
        else:
            with st.spinner("🧠 Calculating estimated fare..."):
                try:
                    features = {
                        'vendor_id': vendor_id,
                        'mta_tax': 0.5,
                        'distance': st.session_state.distance,
                        'num_passengers': num_passengers,
                        'toll_amount': 0,
                        'payment_method': payment_method,
                        'improvement_charge': extra_charges,
                        'extra_charges': 0.50,
                        'trip_duration': st.session_state.duration,
                        'day_type': 0
                    }
                    input_data = pd.DataFrame([features])
                    st.write("🔍 Model Input Data:")
                    st.dataframe(input_data, hide_index=True)
                    prediction = model.predict(input_data)
                    st.markdown(f"<h3>💲 Estimated Fare: ${prediction[0]:.2f}</h3>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"⚠️ Prediction error: {str(e)}")
