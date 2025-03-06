# This file contains the code for the "Book a Cab" page of the Streamlit app.

# import streamlit as st
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim
# import requests

# # Function to geocode the location name into coordinates
# def get_coordinates(location):
#     geolocator = Nominatim(user_agent="geo_locator")
#     location = geolocator.geocode(location)
#     if location:
#         return location.latitude, location.longitude
#     return None

# # Function to get the route details from TomTom API
# def get_route_tomtom(start_coords, end_coords, departure_time=None):
#     api_key = "qru7xtW0t1SPzeM5fJDA9SHNuuPRWAE2"  
#     base_url = "https://api.tomtom.com/routing/1/calculateRoute/"
#     coords = f"{start_coords[0]},{start_coords[1]}:{end_coords[0]},{end_coords[1]}"
#     params = {
#         "key": api_key,
#         "traffic": "true",
#         "computeBestOrder": "true",
#         "travelMode": "car",
#         "routeType": "fastest"
#     }
#     if departure_time:
#         params["departAt"] = departure_time
    
#     response = requests.get(base_url + coords + "/json", params=params).json()
#     if "routes" in response:
#         return response["routes"][0]
#     return None

# # Function to handle the "Book a Cab" page
# def book_a_cab_page():
#     st.title("Enter Pickup and Destination Locations")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         start_location = st.text_input("Enter Start Location", "New York, USA")
#     with col2:
#         end_location = st.text_input("Enter Destination Location", "Washington, USA")
    
#     departure_time = st.text_input("Enter Departure Time (YYYY-MM-DDTHH:MM:SS) (Optional)")
    
#     if st.button("Find Route"):
#         start_coords = get_coordinates(start_location)
#         end_coords = get_coordinates(end_location)
        
#         if start_coords and end_coords:
#             route = get_route_tomtom(start_coords, end_coords, departure_time)
            
#             if route:
#                 distance = route["summary"]["lengthInMeters"] / 1000  # for converting  to km
#                 duration = route["summary"]["travelTimeInSeconds"] / 60  # for converting  to minutes
                
#                 st.write(f"### Distance: {distance:.2f} km")
#                 st.write(f"### Estimated Time: {duration:.2f} mins")
                
#                 # Create map
#                 m = folium.Map(location=start_coords, zoom_start=10)
#                 folium.Marker(start_coords, popup="Start", icon=folium.Icon(color="green")).add_to(m)
#                 folium.Marker(end_coords, popup="Destination", icon=folium.Icon(color="red")).add_to(m)
                
#                 # Plot route
#                 route_coords = route["legs"][0]["points"]
#                 folium.PolyLine([(point["latitude"], point["longitude"]) for point in route_coords], color="blue", weight=5).add_to(m)
                
#                 folium_static(m)  # Render the map in the Streamlit app
#             else:
#                 st.error("Could not find a route. Try another location.")
#         else:
#             st.error("Invalid locations. Please try again.")

    



# with moddel pred 





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
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "final_model.pkl")
        if not os.path.exists(model_path):
            st.error("❌ Model file not found. Ensure 'final_model.pkl' is in the correct directory.")
            return None
        with open(model_path, 'rb') as file:
            model = joblib.load(file)
        return model
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        return None

# Function to handle "Book a Cab" page
def book_a_cab_page():
    st.title("🚖 Book a Cab")

    col1, col2 = st.columns(2)
    with col1:
        start_location = st.text_input("Enter Start Location", "New York, USA")
    with col2:
        end_location = st.text_input("Enter Destination Location", "Washington, USA")
    
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
                folium.PolyLine([(point["latitude"], point["longitude"]) for point in route_coords], color="blue", weight=5).add_to(m)
                folium_static(m)
            else:
                st.error("❌ Could not retrieve route details. Try again later.")
        else:
            st.error("❌ Invalid locations. Please try again.")

    if "route_found" in st.session_state and st.session_state.route_found:
        if st.button("Get Fare Estimate"):
            st.session_state.show_fare_inputs = True  # Store flag to show fare inputs

    if st.session_state.get("show_fare_inputs", False):
        st.markdown("## 🚕 Trip Details for Fare Prediction")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.vendor_id = st.selectbox("Cab Provider", options=[1, 2], format_func=lambda x: "OLA" if x == 1 else "UBER")
        with col2:
            st.markdown(f"### 📏 Trip Distance: {st.session_state.distance} km")
        with col3:
            st.session_state.num_passengers = st.number_input("👥 Passengers", min_value=1, max_value=6, value=1)
        
        col4, col5, col6 = st.columns(3)
        with col4:
            st.session_state.payment_method = st.selectbox("💳 Payment Method", options=[1, 2, 3], format_func=lambda x: "Cash" if x == 1 else ("Card" if x == 2 else "Other"))
        with col5:
            st.session_state.extra_charges = random.choice([0, 0.50, 1])
            st.markdown(f"### 💰 Extra Charges: ${st.session_state.extra_charges}")
        with col6:
            st.markdown(f"### ⏳ Trip Duration: {st.session_state.duration} mins")
        
        if st.button("Predict Fare Price"):
            model = load_model()
            if model is None:
                st.warning("⚠️ Fare prediction is unavailable because the model couldn't be loaded.")
                return

            with st.spinner("🧠 Calculating estimated fare..."):
                try:
                    features = {
                        'vendor_id': st.session_state.vendor_id,
                        'mta_tax': 0.5,
                        'distance': st.session_state.distance,
                        'num_passengers': st.session_state.num_passengers,
                        'toll_amount': 0,
                        'payment_method': st.session_state.payment_method,
                        'improvement_charge': st.session_state.extra_charges,
                        'extra_charges': 0.50,
                        'trip_duration': st.session_state.duration,
                        'day_type': 0
                    }
                    input_data = pd.DataFrame([features])
                    st.write("🔍 Model Input Data:", input_data)
                    prediction = model.predict(input_data)
                    st.session_state.fare_prediction = prediction[0]
                except Exception as e:
                    st.error(f"⚠️ Prediction error: {str(e)}")

        if "fare_prediction" in st.session_state:
            st.markdown(f"<h3>💲 Estimated Fare: ${st.session_state.fare_prediction:.2f}</h3>", unsafe_allow_html=True)


# Streamlit main function
def main():
    st.sidebar.title("🚕 Cab Fare Prediction App")
    page = st.sidebar.radio("Go to", ["Book a Cab"])
    if page == "Book a Cab":
        book_a_cab_page()

if __name__ == "__main__":
    main()
