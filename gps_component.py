if option == "🌍 GPS":
    
    if st.button("📍 Get My Location"):

        location = streamlit_js_eval(
            js_expressions="""
            new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        resolve({
                            lat: position.coords.latitude,
                            lon: position.coords.longitude
                        });
                    },
                    (error) => {
                        reject(error);
                    }
                );
            });
            """,
            key="gps"
        )

        if location:
            lat = location["lat"]
            lon = location["lon"]

            st.session_state.lat = lat
            st.session_state.lon = lon

            st.success(f"Location captured ✅\nLat: {lat}, Lon: {lon}")
        else:
            st.error("Location permission denied or not available")