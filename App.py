import streamlit as st
import datetime
import math
from typing import Dict, Any, List

# --- BACKEND ENGINE (Logica Aziendale & Normativa Tedesca DIN/VOB) ---
class RollMasterEnterpriseEngine:
    def __init__(self):
        self.database_ditte = [
            {
                "id": "DE_MARCHESE_01",
                "nome": "Marchese Rolladen & Sonnenschutz GmbH",
                "citta": "Stuttgart",
                "lat": 48.7758,
                "lon": 9.1829,
                "specializzazione": ["ROLLLADEN", "MARKISE"],
                "certificazioni": ["DIN EN 13659", "DIN EN 13561", "VOB/C"],
                "telefono": "+49 711 123456",
                "disponibile_subito": True,
                "tariffa_oraria_euro": 85.0
            },
            {
                "id": "DE_SONNEN_02",
                "nome": "Schwarzwald Jalousie & Raffstore Jäger",
                "citta": "Freiburg",
                "lat": 47.9990,
                "lon": 7.8421,
                "specializzazione": ["JALOUSIE_RAFFSTORE", "INSEKTENSCHUTZ"],
                "certificazioni": ["DIN EN 13120", "DIN 18055"],
                "telefono": "+49 761 987654",
                "disponibile_subito": True,
                "tariffa_oraria_euro": 92.0
            },
            {
                "id": "DE_EXPRESS_03",
                "nome": "Hauptstadt Rollate & Insektenschutz Express",
                "citta": "Berlin",
                "lat": 52.5200,
                "lon": 13.4050,
                "specializzazione": ["ROLLLADEN", "INSEKTENSCHUTZ", "MARKISE"],
                "certificazioni": ["DIN EN 13659", "Meisterbetrieb"],
                "telefono": "+49 30 555666",
                "disponibile_subito": False,
                "tariffa_oraria_euro": 79.0
            },
            {
                "id": "DE_BAIER_04",
                "nome": "Münchener Beschattungssysteme & Jalousie Bauer",
                "citta": "München",
                "lat": 48.1351,
                "lon": 11.5820,
                "specializzazione": ["JALOUSIE_RAFFSTORE", "MARKISE"],
                "certificazioni": ["DIN EN 13561", "DIN EN 12101"],
                "telefono": "+49 89 112233",
                "disponibile_subito": True,
                "tariffa_oraria_euro": 98.0
            }
        ]

        self.catalogo_global_sonnenschutz = {
            "ROLLLADEN": {
                "normative": ["DIN EN 13659 (Windwiderstand)", "DIN 18055"],
                "materiali": ["PVC Standard Lamellen", "Aluminium Schäumung Eco", "Stahlpanzer V1"],
                "ricambi": ["Gurtband 14mm", "Gurtwickler Unterputz", "Walzenkapsel", "Stahlfeder"],
                "attrezzi": ["Langschraubendreher", "Federklemmenzange", "Magnetische Wasserwaage"]
            },
            "MARKISE": {
                "normative": ["DIN EN 13561 (Außenmarkisen)", "BG BAU Windklasse 2"],
                "materiali": ["Gelenkarmmarkise Premium", "Vollkassette", "Acrylgewebe imprägniert"],
                "ricambi": ["Gelenkarm", "Wandhalterung", "Somfy IO Rohrmotor"],
                "attrezzi": ["Drehmomentschlüssel", "Leitungsfinder", "Baustellenkompass"]
            },
            "JALOUSIE_RAFFSTORE": {
                "normative": ["DIN EN 13120", "DIN EN 14201"],
                "materiali": ["Raffstore 80mm gebördelt", "Innenjalousie Slim"],
                "ricambi": ["Aufzugsband", "Leiterkordel", "Elero WT Motor"],
                "attrezzi": ["Millimeter-Dickenmessgerät", "Crimpzange"]
            },
            "INSEKTENSCHUTZ": {
                "normative": ["DIN Spec 18055"],
                "materiali": ["Roll-Insektenschutz", "Plissee", "Magnetischer Alurahmen"],
                "ricambi": ["Fiberglasgewebe schwarz", "Bürstendichtung", "Zugfeder"],
                "attrezzi": ["Kederrolle", "Ersatzklingenmesser"]
            }
        }

    def _calcola_distanza(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        return round(R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))), 2)

    def cerca_ditte(self, lat_c, lon_c, categoria, raggio):
        risultati = []
        for ditta in self.database_ditte:
            if categoria.upper() in ditta["specializzazione"]:
                dist = self._calcola_distanza(lat_c, lon_c, ditta["lat"], ditta["lon"])
                if dist <= raggio:
                    item = ditta.copy()
                    item["distanza_km"] = dist
                    item["norme"] = self.catalogo_global_sonnenschutz[categoria.upper()]["normative"]
                    risultati.append(item)
        return sorted(risultati, key=lambda x: x["distanza_km"])

    def check_meteo(self, categoria, vento):
        if categoria.upper() == "MARKISE" and vento >= 38.0:
            return True, "🚨 CRITICAL BG BAU: Windstärke überschreitet DIN EN 13561 (38 km/h). Montage sofort einstellen!"
        elif categoria.upper() == "JALOUSIE_RAFFSTORE" and vento >= 45.0:
            return True, "⚠️ WARNING: Hoher Wind (45 km/h). Gefahr von Lamellenschäden."
        return False, "Sicherer Betrieb. DIN-konforme Arbeitsbedingungen."

# --- FRONTEND STREAMLIT (Interfaccia Utente & SaaS Monetizzazione) ---
def run_app():
    st.set_page_config(page_title="RollMaster Germany", page_icon="🛡️", layout="wide")
    engine = RollMasterEnterpriseEngine()

    st.title("🛡️ RollMaster-Germany-App")
    st.markdown("### Das Enterprise SaaS Portal für Sonnenschutz-Fachbetriebe & Montage-Notdienste")

    # Banner promozionale primi 100 clienti (Offerta Founder 49€ / Early Bird)
    st.info("🔥 **Gründer-Aktion (Early Bird):** Die ersten 100 Meisterbetriebe erhalten das Enterprise-Paket für nur **49 € / Monat** im ersten Jahr (Gutscheincode: `EARLY100`)!")

    st.sidebar.header("📍 Standort & Parameter")
    citta_scelta = st.sidebar.selectbox("Wähle Standort", ["Stuttgart", "München", "Berlin", "Freiburg"])
    
    coords = {
        "Stuttgart": (48.7800, 9.1800),
        "München": (48.1300, 11.5700),
        "Berlin": (52.5100, 13.4000),
        "Freiburg": (47.9900, 7.8300)
    }
    lat, lon = coords[citta_scelta]

    categoria = st.sidebar.selectbox("Produkt / Kategorie", ["ROLLLADEN", "MARKISE", "JALOUSIE_RAFFSTORE", "INSEKTENSCHUTZ"])
    raggio = st.sidebar.slider("Suchradius (km)", 10, 200, 50)
    vento = st.sidebar.slider("Aktuelle Windgeschwindigkeit (km/h)", 0, 80, 15)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🛠️ Notdienst & Ditte-Matching", 
        "📋 Technische Kataloge & DIN", 
        "⚠️ BG BAU Sicherheits-Monitor",
        "💳 SaaS Abonnement & Gründer-Rabatt"
    ])

    with tab1:
        st.subheader(f"Verfügbare Meisterbetriebe in der Nähe von {citta_scelta}")
        ditte_trovate = engine.cerca_ditte(lat, lon, categoria, raggio)
        
        if ditte_trovate:
            for d in ditte_trovate:
                with st.expander(f"🏢 {d['nome']} ({d['distanza_km']} km entfernt) - {d['citta']}"):
                    st.write(f"📞 **Telefon:** {d['telefono']}")
                    st.write(f"💵 **Stundensatz:** {d['tariffa_oraria_euro']} € / Std.")
                    st.write(f"📜 **Zertifizierungen:** {', '.join(d['certificazioni'])}")
                    st.write(f"⚖️ **Angewandte Normen:** {', '.join(d['norme'])}")
                    st.success("Sofort verfügbar" if d["disponibile_subito"] else "Zur Zeit ausgelastet")
        else:
            st.warning("Keine Betriebe im gewählten Radius gefunden. Erweitern Sie den Suchradius.")

    with tab2:
        st.subheader(f"Strukturierte DIN-Daten für: {categoria}")
        cat_info = engine.catalogo_global_sonnenschutz[categoria]
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📜 Relevante Normen (DIN / VOB)")
            for n in cat_info["normative"]:
                st.markdown(f"- {n}")
            st.markdown("#### ⚙️ Standard Ersatzteile")
            for r in cat_info["ricambi"]:
                st.markdown(f"- {r}")
        with col2:
            st.markdown("#### 🧱 Typische Materialien")
            for m in cat_info["materiali"]:
                st.markdown(f"- {m}")
            st.markdown("#### 🧰 Benötigte Werkzeuge")
            for a in cat_info["attrezzi"]:
                st.markdown(f"- {a}")

    with tab3:
        st.subheader("⚠️ BG BAU Arbeitsschutz & Wind-Sensorik")
        blocco, msg = engine.check_meteo(categoria, vento)
        if blocco:
            st.error(msg)
        else:
            st.success(msg)
        st.info("Das System gleicht die Baustellendaten automatisch mit den Richtlinien der Berufsgenossenschaft der Bauwirtschaft (BG BAU) ab.")

    with tab4:
        st.subheader("💳 Enterprise SaaS Lizenz & Gründer-Aktion")
        st.markdown("Sichern Sie sich den vollen Zugriff auf alle regionalen Schnittstellen und DIN-Datenbanken.")
        
        coupon = st.text_input("Gutscheincode eingeben (z.B. EARLY100)")
        if coupon.upper() == "EARLY100":
            st.success("🎉 Gutschein erfolgreich angewendet! Gründer-Rabatt für die ersten 100 Kunden aktiviert (Nur **49 € / Monat**).")
            if st.button("Jetzt kostenpflichtig abonnieren (Stripe Checkout Simulation)"):
                st.balloons()
                st.success("Abonnement erfolgreich abgeschlossen! Willkommen im RollMaster Netzwerk.")
        elif coupon:
            st.error("Ungültiger oder abgelaufener Gutscheincode.")
        else:
            st.warning("Geben Sie den Code **EARLY100** ein, um die 49€-Aktion für die ersten 100 Unternehmen zu beanspruchen.")

if __name__ == "__main__":
    run_app()
