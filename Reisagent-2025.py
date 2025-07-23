# Reisagent 2025 – Webversie (Streamlit UI met echte weersvoorspellingen)

import streamlit as st
import requests

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
            {"locatie": "Kempten (Allgäu, DE)", "reden": "Alpen, Romeinse historie, kastelen"},
            {"locatie": "Regensburg (DE)", "reden": "Middeleeuwse stad, Romeinse resten, Walhalla"},
            {"locatie": "Ptuj, Slovenië", "reden": "Romeins erfgoed, wijn, thermen"},
            {"locatie": "Maribor, Slovenië", "reden": "Historische stad, wijnroutes, Alpen"}
        ]

    def check_weer_echt(self, locatie):
        try:
            url = f"https://wttr.in/{locatie}?format=j1"
            response = requests.get(url)
            data = response.json()
            forecast = data['weather'][:5]
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

    def samenvatting_whatsapp(self):
        return (
            "🌄 Vakantie-idee: \n"
            "Week 1: Kempten – bergen, Romeinen, kastelen\n"
            "Week 2: Regensburg + Ptuj/Maribor – geschiedenis en wijn\n"
            "→ Droog, max 27°C, en goede hotels."
        )

st.set_page_config(page_title="Reisagent 2025", page_icon="🌍")
st.title("🌍 Reisagent 2025")
st.write("Plan je ideale vakantie met suggesties binnen 1200 km van Woudenberg")

agent = Reisagent2025()
suggesties = agent.suggestie_route()

locatie_keuze = st.selectbox("👉 Kies een bestemming:", [s['locatie'] for s in suggesties])

if st.button("Toon weer en advies"):
    reden = next((s['reden'] for s in suggesties if s['locatie'] == locatie_keuze), "")
    weer = agent.check_weer_echt(locatie_keuze)
    st.success(f"🎯 Bestemming: {locatie_keuze}\n\n📌 Reden: {reden}\n\n🌤 Weer:")
    st.text(weer)

st.markdown("---")
st.write("Of stuur dit idee door naar Elina:")
st.code(agent.samenvatting_whatsapp(), language='markdown')
