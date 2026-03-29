import requests

# ---------------- CITY → LAT/LON ----------------
def get_lat_lon_from_city(city):
    try:
        url = f"https://nominatim.openstreetmap.org/search?city={city}&format=json"
        response = requests.get(url, headers={"User-Agent": "mediflow-app"})
        data = response.json()

        if len(data) == 0:
            return None

        lat = float(data[0]["lat"])
        lon = float(data[0]["lon"])

        return lat, lon

    except:
        return None


# ---------------- NEARBY HOSPITALS ----------------
def get_nearby_hospitals(lat, lon):
    try:
        overpass_url = "http://overpass-api.de/api/interpreter"

        query = f"""
        [out:json];
        (
          node["amenity"="hospital"](around:3000,{lat},{lon});
          way["amenity"="hospital"](around:3000,{lat},{lon});
          relation["amenity"="hospital"](around:3000,{lat},{lon});
        );
        out center;
        """

        response = requests.post(overpass_url, data=query)
        data = response.json()

        hospitals = []

        for el in data["elements"]:

            name = el.get("tags", {}).get("name", "Unknown Hospital")

            # get lat/lon safely
            if "lat" in el:
                h_lat = el["lat"]
                h_lon = el["lon"]
            else:
                h_lat = el["center"]["lat"]
                h_lon = el["center"]["lon"]

            hospitals.append({
                "hospital": name,
                "lat": h_lat,
                "lon": h_lon,
                "specialty": "general",   # default
                "doctors": [{"name": "General Doctor"}]
            })

        return hospitals

    except:
        return []