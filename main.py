import streamlit as st
import sqlite3
import openai
import os
import setup_db

# --- Setup OpenAI GPT-5 API Key ---
openai.api_key = "YOUR_API_KEY_HERE"

DB_PATH = "lifeline.db"

# --- Ensure database exists ---
if not os.path.exists(DB_PATH):
    setup_db.setup_database()

# --- Page Config ---
st.set_page_config(page_title="🆘 Emergency Response App", layout="wide")

# --- Custom CSS for Styling ---
st.markdown(
    """
    <style>
        /* Emergency Call Buttons */
        .emergency-btn {
            display: block;
            width: 100%;
            padding: 18px;
            font-size: 20px;
            font-weight: bold;
            border-radius: 12px;
            text-align: center;
            text-decoration: none;
            transition: 0.3s;
            margin-bottom: 8px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
        }
        .btn-1122 { background-color: #e74c3c; color: white; }
        .btn-police { background-color: #3498db; color: white; }
        .btn-fire { background-color: #e67e22; color: white; }
        .emergency-btn:hover { opacity: 0.9; transform: scale(1.03); }

        /* Header Bar */
        .header-bar {
            background-color: #ff4b4b;
            padding: 14px;
            text-align: center;
            border-radius: 8px;
            margin-bottom: 15px;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }

        /* Cards for Nearby Services */
        .card {
            border:1px solid #ddd;
            border-radius:12px;
            padding:15px;
            margin-bottom:15px;
            background-color:#f9f9f9;
            box-shadow: 1px 1px 6px rgba(0,0,0,0.1);
        }
        .card h4 { margin:0; }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
st.markdown('<div class="header-bar">🚨 Emergency Response App</div>', unsafe_allow_html=True)

# --- Top Emergency Call Buttons (now larger + equal width) ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.markdown('<a href="tel:1122" class="emergency-btn btn-1122">🚑 Call 1122</a>', unsafe_allow_html=True)
with col2:
    st.markdown('<a href="tel:15" class="emergency-btn btn-police">👮 Police (15)</a>', unsafe_allow_html=True)
with col3:
    st.markdown('<a href="tel:16" class="emergency-btn btn-fire">🔥 Fire Brigade (16)</a>', unsafe_allow_html=True)

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


def get_places_by_city(city):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """
        SELECT city, name, type, address, phone, lat, lon 
        FROM places 
        WHERE LOWER(city) = LOWER(?) 
        AND type IN ('Hospital', 'Police Station', 'Fire Station')
        """,
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
st.sidebar.header("🚑 Emergency Search")
query = st.sidebar.text_input("Enter emergency scenario:")
city = st.sidebar.text_input("Enter your city:")

if st.sidebar.button("Get Guidance"):
    guidance = gpt5_guidance(query)
    st.subheader(f"📝 Guidance for: {query}")
    st.info(guidance)

    if city:
        nearest = get_places_by_city(city)
    else:
        nearest = []

    if nearest:
        st.subheader("📍 Nearby Emergency Services")
        cols = st.columns(3)

        for i, place in enumerate(nearest):
            with cols[i % 3]:
                st.markdown(
                    f"""
                    <div class="card">
                        <h4>🏥 {place['name']}</h4>
                        <p><b>Type:</b> {place['type']}<br>
                        <b>Address:</b> {place['address']}<br>
                        <b>Phone:</b> {place['phone']}</p>
                        <a href="tel:{place['phone']}" class="emergency-btn btn-1122">📞 Call Now</a>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.warning("⚠️ No emergency services found for this city. Please try another.")
