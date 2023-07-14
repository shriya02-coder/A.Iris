import streamlit as st
import requests       
def search_op(location, radius=10):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1"
    response = requests.get(url)
    result = response.json()
    if not result:
        return []
    name = ""
    place = result[0]
    latitude, longitude = float(place["lat"]), float(place["lon"])

    url = f"https://nominatim.openstreetmap.org/search?q=opthalmologist&format=json&limit=10&viewbox={longitude - radius},{latitude - radius},{longitude + radius},{latitude + radius}"
    response = requests.get(url)
    result = response.json()
    if not result:
        return []
    
    op = []
    for place in result:
        if location.lower() in place["display_name"].lower():
            op.append({
                "name": place["display_name"],
                "latitude": float(place["lat"]),
                "longitude": float(place["lon"]),
                "address": place.get("address", {}).get("road", ""),
            })
    return op

def main():
    
    st.write("------------------------------------------")
    st.title("Find Ophthalmologist Near You")

    location = st.text_input("Enter a location:")
    # radius = st.slider("Radius (km):", 0, 50, 10)

    if location:
        op = search_op(location)
        if op:
            st.write("Opthalmologists in your area:")
            for op in op:
                st.write("-", op["name"])
        else:
            st.write("No ophthalmologist found in your area.")

if __name__ == '__main__':
    main()
