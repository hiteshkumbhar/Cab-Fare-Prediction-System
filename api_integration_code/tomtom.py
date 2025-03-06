import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import requests

# function to convert the location name into lat, longi  coordinates
def get_coordinates(location):
    geolocator = Nominatim(user_agent="geo_locator")
    location = geolocator.geocode(location)
    if location:
        return location.latitude, location.longitude
    return None

# Function to get the route details from TomTom API
def get_route_tomtom(start_coords, end_coords, departure_time=None):
    api_key = "qru7xtW0tSHNuuPRWAE2"  #chnaged won't work 
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
    if "routes" in response:
        return response["routes"][0]
    return None

# Streamlit app
def main():
    st.title("Enter Pickup and Destination Locations")
    
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
                distance = route["summary"]["lengthInMeters"] / 1000  # for converting  to km
                duration = route["summary"]["travelTimeInSeconds"] / 60  # for converting  to minutes
                
                st.write(f"### Distance: {distance:.2f} km")
                st.write(f"### Estimated Time: {duration:.2f} mins")
                
                # Create map
                m = folium.Map(location=start_coords, zoom_start=10)
                folium.Marker(start_coords, popup="Start", icon=folium.Icon(color="green")).add_to(m)
                folium.Marker(end_coords, popup="Destination", icon=folium.Icon(color="red")).add_to(m)
                
                # route highlight 
                route_coords = route["legs"][0]["points"]
                folium.PolyLine([(point["latitude"], point["longitude"]) for point in route_coords], color="blue", weight=5).add_to(m)
                
                folium_static(m)  # display map in app
            else:
                st.error("Could not find a route. Try another location.")
        else:
            st.error("Invalid locations. Please try again.")

if __name__ == "__main__":
    main()
