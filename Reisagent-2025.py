# Reisagent 2025 – Webversie (Streamlit UI met uitbreidingen)

import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

class Reisagent2025:
    def __init__(self):
        self.max_afstand_km = 1200
        self.voorkeuren = {
            "klimaat": "droog, onder 30 graden",
            "regio": "geen westen van Nederland",
            "thema": ["bergen", "vestingstadjes", "geschiedenis", "Romeinen", "Tempeliers"],
            "verblijf_duur": {"min": 3, "max": 7},
            "startlocatie": "Woudenberg",
            "comfort": ["goede bedden", "niet te hard matras", "uitgebreid ontbijt"]
        }

    def suggestie_route(self):
        return [
            {"locatie": "Kempten (Allgäu, DE)", "reden": "Alpen, Romeinse historie, kastelen", "coords": (47.7265, 10.3139), "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Kempten_Rathaus_und_St.-Lorenz-Basilika.jpg/320px-Kempten_Rathaus_und_St.-Lorenz-Basilika.jpg"},
            {"locatie": "Regensburg (DE)", "reden": "Middeleeuwse stad, Romeinse resten, Walhalla", "coords": (49.0134, 12.1016), "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Regensburg_Steinerne_Br%C3%BCcke_2014.jpg/320px-Regensburg_Steinerne_Br%C3%BCcke_2014.jpg"},
            {"locatie": "Ptuj, Slovenië", "reden": "Romeins erfgoed, wijn, thermen", "coords": (46.4190, 15.8700), "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Ptuj_s_kapelskim_hribom_in_gradom.jpg/320px-Ptuj_s_kapelskim_hribom_in_gradom.jpg"},
            {"locatie": "Maribor, Slovenië", "reden": "Historische stad, wijnroutes, Alpen", "coords": (46.5547, 15.6459), "foto": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Maribor_Riverbank.JPG/320px-Maribor_Riverbank.JPG"}
        ]

    def check_weer_echt(self, locatie):
        try:
            url = f"https://wttr.in/{locatie}?format=j1"
            response = requests.get(url)
            data = response.json()
            forecast = data['weather'][:14]
            dagen = []
            for dag in forecast:
                datum = dag['date']
                max_temp = dag['maxtempC']
                min_temp = dag['mintempC']
                kans_op_regen = dag['hourly'][4]['chanceofrain']
                dagen.append(f"📅 {datum}: {min_temp}–{max_temp}°C, kans op regen: {kans_op_regen}%")
            return "\n".join(dagen)
        except:
            return "⚠ Weerdata kon niet worden opgehaald."

# Streamlit UI
st.set_page_config(page_title="Reisagent 2025", page_icon="🌍")
st.title("🌍 Reisagent 2025")
st.write("Plan je ideale vakantie met suggesties binnen 1200 km van Woudenberg")

agent = Reisagent2025()
suggesties = agent.suggestie_route()

locatie_namen = [s['locatie'] for s in suggesties]
locatie_keuze = st.selectbox("👉 Kies een bestemming:", locatie_namen)
selectie = next(s for s in suggesties if s['locatie'] == locatie_keuze)

st.image(selectie['foto'], width=400, caption=locatie_keuze)

if st.button("Toon weer en advies"):
    reden = selectie['reden']
    weer = agent.check_weer_echt(locatie_keuze)
    st.success(f"🎯 Bestemming: {locatie_keuze}\n\n📌 Reden: {reden}\n\n🌤 Weer:")
    st.text(weer)
    maps_url = f"https://www.google.com/maps/search/?api=1&query={locatie_keuze.replace(' ', '+')}"
    st.markdown(f"📍 [Bekijk op Google Maps]({maps_url})")

# Toon kaart met pins
m = folium.Map(location=[48.5, 11.5], zoom_start=5)
for s in suggesties:
    folium.Marker(s['coords'], popup=s['locatie']).add_to(m)
st.write("🗺️ Bestemmingen op de kaart:")
st_folium(m, width=700)
