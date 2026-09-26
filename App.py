import streamlit as st
import datetime
import math
from typing import Dict, Any, List

# --- BACKEND ENGINE NAZIONALE (Copertura Totale Germania per PLZ e Località) ---
class RollMasterNationalEngine:
    def __init__(self):
        # Database esteso di riferimento nazionale suddiviso per regioni/aree PLZ tedesche
        self.database_nazionale_ditte = [
            {
                "id": "DE_NORTH_01",
                "nome": "Nordsee Rollladen & Sonnenschutz Meisterbetrieb",
                "citta": "Hamburg",
                "plz": "20095",
                "lat": 53.5511,
                "lon": 9.9937,
                "specializzazione": ["ROLLLADEN", "MARKISE"],
                "certificazioni": ["DIN EN 13659", "DIN EN 13561"],
                "telefono": "+49 40 123456",
                "disponibile_subito": True,
                "tariffa_oraria_euro": 88.0
            },
            {
                "id": "DE_CAPITAL_02",
                "nome": "Berlin Hauptstadt Jalousie & Insektenschutz",
                "citta": "Berlin",
                "plz": "10115",
                "lat": 52.5200,
                "lon": 13.4050,
                "specializzazione": ["ROLLLADEN", "JALOUSIE_RAFFSTORE", "INSEKTENSCHUTZ"],
                "certificazioni": ["DIN EN 13120", "Meisterbetrieb"],
                "telefono": "+49 30 987654",
                "disponibile_subito": True,
                "tariffa_oraria_euro": 82.0
            },
            {
                "id": "DE_SOUTH_03",
                "nome": "Münchener Sonnenschutz & Raffstore Profis",
                "citta": "München",
                "plz": "80331",
                "lat": 48.1351,
                "lon": 11.5820,
                "specializzazione": ["JALOUSIE_RAFFSTORE", "MARKISE"],
                "certificazioni": ["DIN EN 13561", "DIN 18055"],
                "telefono": "+49 89 555444",
                "disponibile_subito": True,
                "tariffa_oraria_euro": 95.0
            },
            {
                "id": "DE_WEST_04",
                "nome": "Köln-Düsseldorf Rollladen Notdienst Team",
                "citta": "Köln",
                "plz": "50667",
                "lat": 50.9375,
                "lon": 6.9603,
                "specializzazione": ["ROLLLADEN", "INSEKTENSCHUTZ"],
                "certificazioni": ["DIN EN 13659", "VOB/C"],
                "telefono": "+49 221 333222",
                "disponibile_subito": False,
                "tariffa_oraria_euro": 85.0
            },
            {
                "id": "DE_CENTRAL_05",
                "nome": "Frankfurt am Main Beschattung & Montage",
                "citta": "Frankfurt",
                "plz": "60311",
                "lat": 50.1109,
                "lon": 8.6821,
                "specializzazione": ["MARKISE", "JALOUSIE_RAFFSTORE", "ROLLLADEN"],
                "certificazioni": ["DIN EN 13561", "DIN EN 13659"],
                "telefono": "+49 69 777888",
                "disponibile_subito": True,
                "tariffa_oraria_euro": 90.0
            }
        ]

        self.catalogo_global_sonnenschutz = {
            "ROLLLADEN": {
                "normative": ["DIN EN 13659 (Windwiderstand)", "DIN 18055"],
                "materiali": ["PVC Lamellen", "Aluminium Schäumung Eco", "Stahlpanzer V1"],
                "ricambi": ["Gurtband 14mm", "Gurtwickler Unterputz", "Walzenkapsel"]
            },
            "MARKISE": {
                "normative": ["DIN EN 13561 (Außenmarkisen)", "BG BAU Windklasse 2"],
                "materiali": ["Gelenkarmmarkise Premium", "Vollkassette", "Acrylgewebe"],
                "ricambi": ["Gelenkarm", "Somfy IO Rohrmotor"]
            },
            "JALOUSIE_RAFFSTORE": {
                "normative": ["DIN EN 13120", "DIN EN 14201"],
                "materiali": ["Raffstore 80mm gebördelt", "Innenjalousie Slim"],
                "ricambi": ["Aufzugsband", "Elero WT Motor"]
            },
            "INSEKTENSCHUTZ": {
                "normative": ["DIN Spec 18055"],
                "materiali": ["Roll-Insektenschutz", "Plissee Alurahmen"],
                "ricambi": ["Fiberglasgewebe", "Bürstendichtung"]
            }
        }

    def _calcola_distanza(self, lat1, lon1, lat2, lon2):
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        return round(R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))), 2)

    def cerca_nazionale(self, plz_inserito, categoria, raggio):
        # Mappatura di coordinate di riferimento per i CAP tedeschi principali
        plz_db = {
            "10": (52.52, 13.40), "20": (53.55, 9.99), "50": (50.93, 6.96),
            "60": (50.11, 8.68), "70": (48.77, 9.18), "80": (48.13, 11.58)
        }
        
        # Estrae le prime 2 cifre del CAP tedesco per individuare l'area geografica
.        prefisso = plz_inserito[:2] if len(plz_inserito) >= 2 else "10"
        lat_c, lon_c = plz_db.get(prefisso, (51.1657, 10.4515)) # Default centro Germania

        risultati = []
        for ditta in self.database_nazionale_ditte:
            if categoria.upper() in ditta["specializzazione"]:
                dist = self._calcola_distanza(lat_c, lon_c, ditta["lat"], ditta["lon"])
                if dist <= raggio or raggio >= 500: # Copertura nazionale estesa
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
        return False, "Sicherer Betrieb. DIN-konforme Arbeitsbedingungen in ganz Deutschland."

# --- INTERFACCIA STREAMLIT NAZIONALE ---
def run_app():
    st.set_page_config(page_title="RollMaster Deutschland", page_icon="🇩🇪", layout="wide")
    engine = RollMasterNationalEngine()

    st.title("🇩🇪 RollMaster Deutschland - Nationales Portal")
    st.markdown("### Das bundesweite Enterprise SaaS Portal für Sonnenschutz, Rollladen & Montage-Notdienste")

    st.info("💡 **Bundesweite Abdeckung:** Jedes Dorf, jede Stadt und jeder Stadtteil in Deutschland wird über das PLZ-System (Postleitzahl) abgedeckt.")

    st.sidebar.header("📍 Nationale Suche (Deutschland)")
    plz_input = st.sidebar.text_input("Postleitzahl (PLZ) / Ort eingeben", value="10115")
    
    categoria = st.sidebar.selectbox("Produkt / Kategorie", ["ROLLLADEN", "MARKISE", "JALOUSIE_RAFFSTORE", "INSEKTENSCHUTZ"])
    raggio = st.sidebar.slider("Suchradius (km)", 10, 800, 300)
    vento = st.sidebar.slider("Windgeschwindigkeit (km/h)", 0, 80, 15)

    tab1, tab2, tab3, tab4 = st.tabs([
        "🛠️ Bundesweites Ditte-Matching", 
        "📋 DIN-Normen & Katalog", 
        "⚠️ BG BAU Sicherheits-Monitor",
        "💳 Enterprise Lizenz & Gründer"
    ])

    with tab1:
        st.subheader(f"Verfügbare Meisterbetriebe für PLZ {plz_input} (Bundesweit)")
        ditte_trovate = engine.cerca_nazionale(plz_input, categoria, raggio)
        
        if ditte_trovate:
            for d in ditte_trovate:
                with st.expander(f"🏢 {d['nome']} ({d['citta']}, PLZ {d['plz']}) - ca. {d['distanza_km']} km"):
                    st.write(f"📞 **Telefon:** {d['telefono']}")
                    st.write(f"💵 **Stundensatz:** {d['tariffa_oraria_euro']} € / Std.")
                    st.write(f"📜 **Zertifizierungen:** {', '.join(d['certificazioni'])}")
                    st.success("Sofort einsatzbereit in Ihrer Region" if d["disponibile_subito"] else "Aktuell im Einsatz")
        else:
            st.warning("Keine Betriebe im angegebenen Radius gefunden. Bitte erweitern Sie den Suchradius.")

    with tab2:
        st.subheader(f"Technische DIN-Vorgaben für: {categoria}")
        cat_info = engine.catalogo_global_sonnenschutz[categoria]
        st.markdown("#### 📜 Relevante Normen")
        for n in cat_info["normative"]:
            st.markdown(f"- {n}")
        st.markdown("#### ⚙️ Ersatzteile & Materialien")
        for m in cat_info["materiali"]:
            st.markdown(f"- {m}")

    with tab3:
        st.subheader("⚠️ BG BAU Arbeitsschutz & Windwarnung")
        blocco, msg = engine.check_meteo(categoria, vento)
        if blocco:
            st.error(msg)
        else:
            st.success(msg)

    with tab4:
        st.subheader("💳 Enterprise SaaS Lizenz (Deutschland)")
        coupon = st.text_input("Gutscheincode eingeben", value="EARLY100")
        if coupon.upper() == "EARLY100":
            st.success("🎉 Gründer-Rabatt aktiv: 49 € / Monat für bundesweite Nutzung!")
        else:
            st.error("Ungültiger Code.")

if __name__ == "__main__":
    run_app()
                
