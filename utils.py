import requests

# ---------------- IP-BASED LOCATION ----------------
def get_user_location():
    """
    Gets approximate location using IP address.
    """
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5)
        data = res.json()

        city = data.get("city", "Unknown")
        return city

    except:
        return "Unknown"


def get_lat_lon():
    """
    Returns approximate latitude and longitude using IP.
    """
    try:
        res = requests.get("https://ipapi.co/json/", timeout=5)
        data = res.json()

        lat = data.get("latitude")
        lon = data.get("longitude")

        return lat, lon

    except:
        return None, None


# ---------------- CITY → LAT/LON ----------------
def get_lat_lon_from_city(city):
    """
    Converts city name into coordinates using OpenStreetMap Nominatim API.
    """
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            "q": city,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "MediFlowAI/1.0"
        }

        res = requests.get(url, params=params, headers=headers, timeout=5)
        data = res.json()

        if len(data) > 0:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon

        return None, None

    except:
        return None, None


# ---------------- NEARBY HOSPITALS ----------------
def get_nearby_hospitals(lat, lon):
    """
    Fetch hospitals near a location using OpenStreetMap Overpass API.
    Falls back to mock data if API fails.
    """

    try:
        overpass_url = "https://overpass-api.de/api/interpreter"

        query = f"""
        [out:json];
        (
          node["amenity"="hospital"](around:5000,{lat},{lon});
          way["amenity"="hospital"](around:5000,{lat},{lon});
          relation["amenity"="hospital"](around:5000,{lat},{lon});
        );
        out center;
        """

        res = requests.post(overpass_url, data=query, timeout=10)
        data = res.json()

        hospitals = []

        for element in data.get("elements", []):

            tags = element.get("tags", {})

            name = tags.get("name", "Unknown Hospital")

            # fallback coordinates
            el_lat = element.get("lat") or element.get("center", {}).get("lat")
            el_lon = element.get("lon") or element.get("center", {}).get("lon")

            if el_lat and el_lon:
                hospitals.append({
                    "hospital": name,
                    "lat": el_lat,
                    "lon": el_lon,
                    "specialty": tags.get("healthcare", "general")
                })

        # If API returns empty → fallback mock
        if not hospitals:
            return mock_hospitals(lat, lon)

        return hospitals

    except:
        return mock_hospitals(lat, lon)


# ---------------- MOCK DATA (FALLBACK) ----------------
def mock_hospitals(lat, lon):
    """
    Fallback hospitals if API fails.
    """

    return [
        {
            "hospital": "City General Hospital",
            "lat": lat + 0.01,
            "lon": lon + 0.01,
            "specialty": "general"
        },
        {
            "hospital": "Heart Care Center",
            "lat": lat + 0.02,
            "lon": lon - 0.01,
            "specialty": "cardiology"
        },
        {
            "hospital": "Ortho Clinic",
            "lat": lat - 0.01,
            "lon": lon + 0.02,
            "specialty": "orthopedic"
        },
        {
            "hospital": "Eye Vision Hospital",
            "lat": lat - 0.02,
            "lon": lon - 0.02,
            "specialty": "ophthalmology"
        }
    ]