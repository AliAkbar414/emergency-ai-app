import sqlite3
import streamlit as st

DB_PATH = "lifeline.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # --- Emergencies ---
    c.execute("DROP TABLE IF EXISTS emergencies")
    c.execute("""
        CREATE TABLE emergencies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            steps TEXT NOT NULL
        )
    """)

    emergencies = [
        ("Heart Attack",
         "Call 1122 immediately. Keep the patient calm, seated, and loosen tight clothing. "
         "Give one aspirin (if conscious and not allergic). Monitor breathing and pulse. "
         "If the person becomes unresponsive, start CPR (30 compressions and 2 breaths) until help arrives."),
        ("CPR (Adult)",
         "Call 1122 first. Place the heel of one hand on the center of the chest, the other hand on top. "
         "Push hard and fast at 100–120 compressions per minute, depth about 5 cm. "
         "After every 30 compressions, give 2 rescue breaths. Continue until medical help arrives or the patient breathes."),
        ("CPR (Child)",
         "Call 1122. Use one hand for compressions on the chest. Push about 5 cm deep at 100–120 compressions per minute. "
         "Give 30 compressions followed by 2 rescue breaths. Continue until the child breathes or help arrives."),
        ("CPR (Infant)",
         "Call 1122. Use two fingers at the center of the chest. Compress about 4 cm deep at 100–120 per minute. "
         "Give 30 compressions followed by 2 gentle rescue breaths. Continue until the infant resumes breathing or help arrives."),
        ("Choking (Adult/Child)",
         "Ask loudly 'Are you choking?'. If they cannot speak or cough, give 5 back blows between the shoulder blades. "
         "If not relieved, give 5 abdominal thrusts (Heimlich maneuver). Alternate until the object is expelled or the person becomes unresponsive. "
         "If unresponsive, begin CPR and call 1122."),
        ("Choking (Infant)",
         "If the infant cannot cry or breathe, support the head and neck, turn face down, and deliver 5 back blows. "
         "If not relieved, turn face up and give 5 chest thrusts with two fingers at the breastbone. "
         "Alternate until breathing returns or emergency help arrives. Call 1122 immediately."),
        ("Severe Bleeding",
         "Call 1122. Apply firm, direct pressure on the wound with a clean cloth or bandage. "
         "If blood soaks through, place another cloth on top—do not remove the original one. "
         "Keep the injured area elevated if possible. If bleeding does not stop, apply pressure to nearby artery points."),
        ("Burns",
         "Immediately cool the burn with running cool (not ice-cold) water for at least 20 minutes. "
         "Remove rings, watches, or tight clothing before swelling begins. "
         "Cover the burn with a clean, non-stick cloth or plastic wrap. "
         "Do not apply butter, oil, or toothpaste. Call 1122 for serious or large burns."),
        ("Fracture",
         "Call 1122 if the fracture appears severe. Keep the injured limb still and supported. "
         "Do not try to straighten or push back the bone. Apply a cold pack to reduce swelling. "
         "Immobilize with a splint if trained. Keep patient calm until medical help arrives."),
        ("Stroke",
         "Use the FAST method: Face drooping, Arm weakness, Speech difficulty, Time to call 1122 immediately. "
         "Keep the person safe and calm. Note the time symptoms started. "
         "Do not give food, drink, or medication. Wait with the patient until professional help arrives."),
    ]

    c.executemany("INSERT INTO emergencies (name, steps) VALUES (?, ?)", emergencies)

    # --- Places ---
    c.execute("DROP TABLE IF EXISTS places")
    c.execute("""
        CREATE TABLE places (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        )
    """)

    # --- Sample Places (10+ Pakistani Cities) ---
    city_places = [
        ("Karachi","JPMC","Hospital","Rafiqui Shaheed Rd","1122",24.8617,67.0360),
        ("Lahore","Mayo Hospital","Hospital","Nisbat Rd","1122",31.5680,74.3090),
        ("Islamabad","PIMS Hospital","Hospital","G-8/3","1122",33.7073,73.0554),
        ("Rawalpindi","Holy Family Hospital","Hospital","Satellite Town","1122",33.6450,73.0620),
        ("Faisalabad","Allied Hospital","Hospital","People's Colony","1122",31.4278,73.0794),
        ("Multan","Nishtar Hospital","Hospital","Nishtar Rd","1122",30.1964,71.4687),
        ("Peshawar","Lady Reading Hospital","Hospital","Soekarno Rd","1122",34.0106,71.5700),
        ("Quetta","Civil Hospital Quetta","Hospital","Jinnah Rd","1122",30.1897,67.0183),
        ("Hyderabad","Civil Hospital Hyderabad","Hospital","Station Rd","1122",25.3960,68.3578),
        ("Sialkot","Allama Iqbal Hospital","Hospital","Sialkot","1122",32.4936,74.5310),
    ]

    c.executemany("INSERT INTO places (city,name,type,address,phone,lat,lon) VALUES (?,?,?,?,?,?,?)", city_places)

    conn.commit()
    conn.close()

# --- Optional: Sidebar Button in Streamlit to manually create DB ---
st.sidebar.header("⚙️ Database Setup")
if st.sidebar.button("Initialize Database"):
    setup_database()
    st.success("✅ Database created successfully with emergencies + places.")
