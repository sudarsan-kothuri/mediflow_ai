import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import streamlit_js_eval
import math
import streamlit.components.v1 as components
import uuid

from utils import (
    get_lat_lon_from_city,
    get_nearby_hospitals
)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="MediFlow AI+", layout="wide")

# ---------------- STYLE ----------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; }
div[data-testid="stSidebar"] { background-color: #f5f7fa; }
</style>
""", unsafe_allow_html=True)

# ---------------- AUTO REFRESH ----------------
components.html("""
<script>
setTimeout(function(){
    window.location.reload();
}, 10000);
</script>
""", height=0)

# ---------------- SESSION STATE ----------------
if "lat" not in st.session_state:
    st.session_state.lat = None

if "lon" not in st.session_state:
    st.session_state.lon = None

if "hospitals" not in st.session_state:
    st.session_state.hospitals = []

if "bookings" not in st.session_state:
    st.session_state.bookings = []

if "patient" not in st.session_state:
    st.session_state.patient = {}

if "disease" not in st.session_state:
    st.session_state.disease = "Fever"

# ---------------- DISTANCE ----------------
def distance_km(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2

    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# ---------------- COST ----------------
def get_op_cost(specialty):
    cost_map = {
        "general": 300,
        "cardiology": 800,
        "orthopedic": 600,
        "ophthalmology": 500,
        "dentistry": 400,
        "pediatrics": 350
    }
    return cost_map.get(specialty.lower(), 300)

# ---------------- TIME SLOTS ----------------
def get_time_slots():
    return ["09:00 AM","10:00 AM","11:00 AM","02:00 PM","03:00 PM","04:00 PM"]

# ---------------- DISEASE FILTER ----------------
def filter_hospitals_by_disease(hospitals, disease):

    disease_map = {
        "Fever": ["general", "internal"],
        "Heart": ["cardiology"],
        "Bone": ["orthopedic"],
        "Eye": ["ophthalmology"],
        "Dental": ["dentistry"],
        "Child": ["pediatrics"]
    }

    keywords = disease_map.get(disease, [])

    filtered = []
    for h in hospitals:
        specialty = h.get("specialty", "").lower()
        if any(k in specialty for k in keywords):
            filtered.append(h)

    return filtered if filtered else hospitals

# ---------------- LOAD HOSPITALS ----------------
def load_hospitals():

    if st.session_state.lat and st.session_state.lon:

        if st.session_state.hospitals:
            return

        hospitals = get_nearby_hospitals(
            st.session_state.lat,
            st.session_state.lon
        )

        if not hospitals:
            hospitals = [
                {
                    "hospital": "City General Hospital",
                    "lat": st.session_state.lat + 0.01,
                    "lon": st.session_state.lon + 0.01,
                    "specialty": "general",
                    "doctors": [{"name": "Dr. Rao"}, {"name": "Dr. Mehta"}]
                },
                {
                    "hospital": "Heart Care Center",
                    "lat": st.session_state.lat + 0.02,
                    "lon": st.session_state.lon - 0.01,
                    "specialty": "cardiology",
                    "doctors": [{"name": "Dr. Sharma"}, {"name": "Dr. Iyer"}]
                }
            ]

        st.session_state.hospitals = hospitals

# ---------------- FIXED GPS LOCATION ----------------
def detect_location():

    location = streamlit_js_eval(
        js_expressions="""
        new Promise((resolve) => {

            if (!navigator.geolocation) {
                resolve(null);
                return;
            }

            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    resolve({
                        lat: pos.coords.latitude,
                        lon: pos.coords.longitude,
                        accuracy: pos.coords.accuracy
                    });
                },
                () => resolve(null),
                {
                    enableHighAccuracy: true,
                    timeout: 15000,
                    maximumAge: 0
                }
            );

        });
        """,
        key="gps"
    )

    if location and location["lat"] and location["lon"]:

        lat = float(location["lat"])
        lon = float(location["lon"])
        accuracy = float(location.get("accuracy", 9999))

        # ✅ STRICT VALIDATION
        if accuracy > 1000:
            st.warning("⚠️ Low accuracy GPS detected. Enable high accuracy or move outdoors.")
            return

        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            st.error("Invalid coordinates received")
            return

        st.session_state.lat = lat
        st.session_state.lon = lon
        st.session_state.accuracy = accuracy

        # ✅ FORCE hospital reload
        st.session_state.hospitals = []
        load_hospitals()

        st.rerun()

    else:
        st.error("❌ Location access denied or unavailable")

# ---------------- UI ----------------
st.title("🏥 MediFlow AI+ Smart Healthcare")

col1, col2 = st.columns([1, 2])

# ---------------- LEFT PANEL ----------------
with col1:

    st.header("📍 Controls")

    if st.button("Detect Location"):
        detect_location()

    city = st.text_input("Enter City")

    if st.button("Set City"):
        lat, lon = get_lat_lon_from_city(city)
        st.session_state.lat = lat
        st.session_state.lon = lon
        load_hospitals()
        st.rerun()

    if st.session_state.lat and st.session_state.lon:
        st.success("📍 Location Detected")
        st.write(f"Lat: {st.session_state.lat}")
        st.write(f"Lon: {st.session_state.lon}")

        if "accuracy" in st.session_state:
            st.write(f"Accuracy: {st.session_state.accuracy} meters")

    st.subheader("🩺 Disease")

    disease = st.selectbox(
        "Select condition",
        ["Fever", "Heart", "Bone", "Eye", "Dental", "Child"]
    )

    st.session_state.disease = disease

    st.subheader("👤 Patient Details")

    name = st.text_input("Name")
    age = st.number_input("Age", 1, 120)
    phone = st.text_input("Phone")

    if st.button("Save Patient"):
        st.session_state.patient = {
            "name": name,
            "age": age,
            "phone": phone
        }
        st.success("Saved")

    st.subheader("📋 Bookings")

    for b in st.session_state.bookings:
        st.write(f"""
        🆔 {b['booking_id']}  
        🏥 {b['hospital']}  
        👨‍⚕️ {b['doctor']}  
        ⏰ {b['time']}  
        💰 ₹{b['cost']}  
        👤 {b['patient'].get('name','')}
        """)
        st.markdown("---")

# ---------------- RIGHT PANEL ----------------
with col2:

    st.header("🗺️ Map")

    if st.session_state.lat and st.session_state.lon:

        m = folium.Map(
            location=[st.session_state.lat, st.session_state.lon],
            zoom_start=16
        )

        folium.Marker(
            [st.session_state.lat, st.session_state.lon],
            tooltip="You are here",
            icon=folium.Icon(color="blue")
        ).add_to(m)

        hospitals = st.session_state.hospitals
        hospitals = filter_hospitals_by_disease(hospitals, st.session_state.disease)

        for h in hospitals:
            folium.Marker(
                [h["lat"], h["lon"]],
                tooltip=h["hospital"],
                icon=folium.Icon(color="red")
            ).add_to(m)

        st_folium(m, width=900, height=550)

        st.subheader("🏥 Hospitals")

        for h in hospitals:

            cost = get_op_cost(h.get("specialty","general"))

            dist = distance_km(
                st.session_state.lat,
                st.session_state.lon,
                h["lat"],
                h["lon"]
            )

            st.markdown(f"""
            ### 🏥 {h['hospital']}
            📍 Distance: {round(dist,2)} km  
            💰 Cost: ₹{cost}
            """)

            doctors = h.get("doctors", [{"name":"General Doctor"}])
            doctor_names = [d["name"] for d in doctors]

            doctor = st.selectbox(
                "Doctor",
                doctor_names,
                key=f"doc_{h['hospital']}"
            )

            slot = st.selectbox(
                "Time",
                get_time_slots(),
                key=f"time_{h['hospital']}"
            )

            url = f"https://www.google.com/maps/dir/?api=1&destination={h['lat']},{h['lon']}"
            st.markdown(f"[🧭 Navigate]({url})")

            def is_slot_taken(doctor, slot):
                for b in st.session_state.bookings:
                    if b["doctor"] == doctor and b["time"] == slot:
                        return True
                return False

            if st.button(f"Book {h['hospital']}", key=f"book_{h['hospital']}"):

                if is_slot_taken(doctor, slot):
                    st.error("❌ Slot already booked")
                else:
                    booking_id = "OP-" + str(uuid.uuid4())[:8]

                    booking = {
                        "booking_id": booking_id,
                        "hospital": h["hospital"],
                        "doctor": doctor,
                        "time": slot,
                        "cost": cost,
                        "patient": st.session_state.patient
                    }

                    st.session_state.bookings.append(booking)

                    st.success(f"✅ Booking Confirmed: {booking_id}")

            st.markdown("---")

    else:
        st.info("Detect location to continue")