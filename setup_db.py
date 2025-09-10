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
         "If the person becomes unresponsive, start CPR until help arrives."),
        ("CPR (Adult)",
         "Call 1122 first. Place the heel of one hand on the center of the chest, the other hand on top. "
         "Push hard and fast at 100–120 compressions per minute, depth about 5 cm. "
         "After every 30 compressions, give 2 rescue breaths."),
        ("Severe Bleeding",
         "Call 1122. Apply firm, direct pressure on the wound with a clean cloth or bandage. "
         "If blood soaks through, place another cloth on top—do not remove the original one."),
        ("Burns",
         "Cool the burn with running cool (not ice-cold) water for at least 20 minutes. "
         "Remove rings, watches, or tight clothing. Cover with a clean cloth. Do not apply oil or toothpaste. "
         "Call 1122 for serious or large burns."),
        ("Stroke",
         "Use the FAST method: Face drooping, Arm weakness, Speech difficulty, Time to call 1122 immediately. "
         "Keep the person safe and calm. Note the time symptoms started."),
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

    # --- Hospitals + Police + Fire Stations for 10 major cities ---
    city_places = [
        # Karachi
        ("Karachi","JPMC","Hospital","Rafiqui Shaheed Rd","021-99201300",24.8617,67.0360),
        ("Karachi","Karachi Police HQ","Police Station","Garden Rd","021-99212609",24.8735,67.0331),
        ("Karachi","Fire Brigade Saddar","Fire Station","Saddar","021-99215007",24.8582,67.0303),

        # Lahore
        ("Lahore","Mayo Hospital","Hospital","Nisbat Rd","042-99211100",31.5680,74.3090),
        ("Lahore","Civil Lines Police","Police Station","Civil Lines","042-99202805",31.5652,74.3141),
        ("Lahore","Fire Station Shadman","Fire Station","Shadman","042-99203456",31.5497,74.3255),

        # Islamabad
        ("Islamabad","PIMS Hospital","Hospital","G-8/3","051-9261170",33.7073,73.0554),
        ("Islamabad","Aabpara Police","Police Station","Aabpara","051-9222596",33.7110,73.0667),
        ("Islamabad","Fire Brigade HQ","Fire Station","H-9","051-9253012",33.6844,73.0481),

        # Rawalpindi
        ("Rawalpindi","Holy Family Hospital","Hospital","Satellite Town","051-9290320",33.6450,73.0620),
        ("Rawalpindi","Ganjmandi Police","Police Station","Ganjmandi","051-5552221",33.6021,73.0495),
        ("Rawalpindi","Fire Station Committee Chowk","Fire Station","Committee Chowk","051-9292900",33.6354,73.0680),

        # Faisalabad
        ("Faisalabad","Allied Hospital","Hospital","People's Colony","041-9200123",31.4278,73.0794),
        ("Faisalabad","Rail Bazaar Police","Police Station","Rail Bazaar","041-9200101",31.4185,73.0790),
        ("Faisalabad","Fire Station D Ground","Fire Station","D Ground","041-9200456",31.4160,73.1000),

        # Multan
        ("Multan","Nishtar Hospital","Hospital","Nishtar Rd","061-9200231",30.1964,71.4687),
        ("Multan","Cantt Police","Police Station","Cantt Area","061-9200120",30.1920,71.4670),
        ("Multan","Fire Station Chungi","Fire Station","Chungi No. 6","061-9200345",30.2001,71.4700),

        # Peshawar
        ("Peshawar","Lady Reading Hospital","Hospital","Soekarno Rd","091-9211430",34.0106,71.5700),
        ("Peshawar","Faqirabad Police","Police Station","Faqirabad","091-9211120",34.0050,71.5620),
        ("Peshawar","Fire Station Kohati","Fire Station","Kohati Gate","091-9211456",34.0120,71.5730),

        # Quetta
        ("Quetta","Civil Hospital","Hospital","Jinnah Rd","081-9200123",30.1897,67.0183),
        ("Quetta","City Police","Police Station","City Area","081-9200101",30.1820,67.0100),
        ("Quetta","Fire Station Jinnah Rd","Fire Station","Jinnah Rd","081-9200456",30.1900,67.0150),

        # Hyderabad
        ("Hyderabad","Civil Hospital Hyderabad","Hospital","Station Rd","022-9200123",25.3960,68.3578),
        ("Hyderabad","Market Police","Police Station","Market Area","022-9200101",25.3920,68.3600),
        ("Hyderabad","Fire Station Latifabad","Fire Station","Latifabad","022-9200456",25.4000,68.3650),

        # Sialkot
        ("Sialkot","Allama Iqbal Hospital","Hospital","Daska Rd","052-9200123",32.4936,74.5310),
        ("Sialkot","Cantt Police","Police Station","Cantt Area","052-9200101",32.5000,74.5350),
        ("Sialkot","Fire Station Cantt","Fire Station","Cantt","052-9200456",32.4960,74.5330),
    ]

    c.executemany("INSERT INTO places (city,name,type,address,phone,lat,lon) VALUES (?,?,?,?,?,?,?)", city_places)

    conn.commit()
    conn.close()

# --- Optional: Sidebar Button in Streamlit to manually create DB ---
st.sidebar.header("⚙️ Database Setup")
if st.sidebar.button("Initialize Database"):
    setup_database()
    st.success("✅ Database created successfully with emergencies + hospitals + police + fire stations.")
