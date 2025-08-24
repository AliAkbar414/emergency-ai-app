import streamlit as st
import sqlite3
from geopy.distance import geodesic
import openai
import os
import setup_db

# --- Setup OpenAI GPT-5 API Key ---
openai.api_key = "YOUR_API_KEY_HERE"

DB_PATH = "lifeline.db"

# --- Ensure database exists ---
if not os.path.exists(DB_PATH):
    setup_db.setup_database()

st.set_page_config(page_title="Emergency Response App", layout="wide")
st.title("🆘 Emergency Response App")

# --- Helper functions ---
def get_emergency_by_query(query):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT name, steps FROM emergencies WHERE name LIKE ? OR steps LIKE ?",
        (f"%{query}%", f"%{query}%"),
    )
    row = c.fetchone()
    conn.close()
    return {"name": row[0], "steps": row[1]} if row else None

def get_all_emergencies():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name, steps FROM emergencies")
    rows = c.fetchall()
    conn.close()
    return [{"name": r[0], "steps": r[1]} for r in rows]

def get_places_by_city(city):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT city, name, type, address, phone, lat, lon FROM places WHERE city = ?",
        (city,),
    )
    rows = c.fetchall()
    conn.close()
    return [
        {
            "city": r[0],
            "name": r[1],
            "type": r[2],
            "address": r[3],
            "phone": r[4],
            "lat": r[5],
            "lon": r[6],
        }
        for r in rows
    ]

def get_nearest_places(user_lat, user_lon):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT city, name, type, address, phone, lat, lon FROM places")
    rows = c.fetchall()
    conn.close()
    places = []
    for r in rows:
        distance = geodesic((user_lat, user_lon), (r[5], r[6])).km
        places.append(
            {
                "city": r[0],
                "name": r[1],
                "type": r[2],
                "address": r[3],
                "phone": r[4],
                "lat": r[5],
                "lon": r[6],
                "distance": distance,
            }
        )
    places.sort(key=lambda x: x["distance"])
    return places[:10]

def gpt5_guidance(query):
    if not query.strip():
        return "Please provide an emergency scenario."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-5",
            messages=[
                {
                    "role": "system",
                    "content": "You are an emergency medical assistant providing clear, detailed, safe guidance for bystanders.",
                },
                {"role": "user", "content": f"Provide detailed, step-by-step first aid guidance for: {query}"},
            ],
            temperature=0.4,
            max_tokens=500,
        )
        guidance = response["choices"][0]["message"]["content"]
        return guidance.strip()
    except Exception:
        emergency = get_emergency_by_query(query)
        if emergency:
            detailed_steps = f"""
Emergency: {emergency['name']}

Step-by-Step Guidance:
1. {emergency['steps']}
2. Ensure your own safety before helping others.
3. If available, use protective equipment (like gloves).
4. Reassure the person, keep them calm, and monitor their breathing and pulse.
5. Do not leave the person unattended until professional help arrives.
6. If their condition worsens, call emergency services again and update them.
            """
            return detailed_steps.strip()
        return f"Sorry, no guidance found for '{query}'."

# --- Streamlit Interface ---
st.sidebar.header("Search Emergency Guidance")
query = st.sidebar.text_input("Enter emergency scenario:")
city = st.sidebar.text_input("Enter your city (optional):")
user_lat = st.sidebar.number_input("Your Latitude (optional)", value=0.0)
user_lon = st.sidebar.number_input("Your Longitude (optional)", value=0.0)

if st.sidebar.button("Get Guidance"):
    guidance = gpt5_guidance(query)
    st.subheader(f"Guidance for: {query}")
    st.write(guidance)

    # Show nearest places
    if user_lat != 0.0 and user_lon != 0.0:
        nearest = get_nearest_places(user_lat, user_lon)
    elif city:
        nearest = get_places_by_city(city)
    else:
        nearest = []

    if nearest:
        st.subheader("Nearby Emergency Places / Services")
        for place in nearest:
            st.markdown(f"""
**{place['name']}** ({place['type']})  
Address: {place['address']}  
Phone: {place['phone']}  
Distance: {place.get('distance', 'N/A'):.2f} km
""")
