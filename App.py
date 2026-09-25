import json
import datetime
import math
from typing import Dict, Any, List
import streamlit as st

# Configurazione della pagina Streamlit
st.set_page_config(
    page_title="RollMaster-germany-App",
    page_icon="🛡️",
    layout="wide"
)

class RollMasterGermanyAppEngine:
    """
    Enterprise Backend Engine per l'app 'RollMaster-germany-App'.
    Gestisce la geolocalizzazione, il database normativo tedesco (DIN/VOB),
    il filtraggio delle ditte vicine, il sistema multilingue per la classe operaia
    e il sistema di allerta e sicurezza (BG BAU).
    """
    
    def __init__(self):
        self.nome_app = "RollMaster-germany-App"
        
        # Dizionario delle traduzioni e dei testi multilingue per la classe operaia in Germania
        self.traduzioni = {
            "DE": {
                "titolo": "RollMaster-germany-App",
                "sottotitolo": "Professionelle Plattform für Rolladen und Sonnenschutz in Deutschland",
                "disclaimer": "RECHTLICHER HINWEIS: Die Plattform agiert ausschließlich als technologischer Vermittler zwischen Kunden und zertifizierten Fachbetrieben.",
                "scegli_lingua": "Sprachauswahl / Language",
                "area": "Stadt / Region in Deutschland",
                "categoria": "Eingriffskategorie",
                "raggio": "Suchradius (km)",
                "ditte_titolo": "Verfügbare Fachbetriebe in der Nähe von",
                "tariffa": "Stundensatz",
                "contatta": "Kontaktieren",
                "preventivo": "Schneller Regionaler Kostenvoranschlag",
                "materiali": "Geschätzte Materialkosten (€)",
                "totale": "Indikative Gesamtschätzung (inkl. Anfahrt & Handwerker)",
                "inviato": "Anfrage erfolgreich an den Betrieb gesendet!"
            },
            "IT": {
                "titolo": "RollMaster-germany-App",
                "sottotitolo": "Piattaforma Professionale per Tapparelle e Schermature Solari in Germania",
                "disclaimer": "AVVISO LEGALE: La piattaforma opera esclusivamente come servizio di intermediazione tecnologica.",
                "scegli_lingua": "Seleziona Lingua / Language",
                "area": "Città / Area in Germania",
                "categoria": "Categoria Intervento",
                "raggio": "Raggio di ricerca (km)",
                "ditte_titolo": "Ditte Specializzate disponibili vicino a",
                "tariffa": "Tariffa Oraria",
                "contatta": "Contatta",
                "preventivo": "Calcolatore Preventivo Rapido Regionale",
                "materiali": "Costo stimato dei materiali (€)",
                "totale": "Stima Indicativa Lavorazione (include chiamata e manodopera)",
                "inviato": "Richiesta inviata con successo alla ditta!"
            },
            "RO": {
                "titolo": "RollMaster-germany-App",
                "sottotitolo": "Platformă Profesională pentru Rulouri și Protecție Solară în Germania",
                "disclaimer": "AVIZ LEGAL: Platforma acționează exclusiv ca un serviciu de intermediere tehnologică.",
                "scegli_lingua": "Selectați limba",
                "area": "Oraș / Regiune în Germania",
                "categoria": "Categoria intervenției",
                "raggio": "Raza de căutare (km)",
                "ditte_titolo": "Companii specializate disponibile lângă",
                "tariffa": "Tarif orar",
                "contatta": "Contactează",
                "preventivo": "Calculator rapid de preț regional",
                "materiali": "Cost estimat materiale (€)",
                "totale": "Estimare orientativă totală",
                "inviato": "Solicitare trimisă cu succes către companie!"
            },
            "PL": {
                "titolo": "RollMaster-germany-App",
                "sottotitolo": "Profesjonalna platforma do rolet i osłon przeciwsłonecznych w Niemczech",
                "disclaimer": "INFORMACJA PRAWNA: Platforma działa wyłącznie jako pośrednik technologiczny.",
                "scegli_lingua": "Wybierz język",
                "area": "Miasto / Region w Niemczech",
                "categoria": "Kategoria interwencji",
                "raggio": "Promień wyszukiwania (km)",
                "ditte_titolo": "Dostępne wyspecjalizowane firmy w pobliżu",
                "tariffa": "Stawka godzinowa",
                "contatta": "Kontakt",
                "preventivo": "Szybki regionalny kalkulator kosztów",
                "materiali": "Szacowany koszt materiałów (€)",
                "totale": "Szacunkowy koszt całkowity",
                "inviato": "Zapytanie zostało pomyślnie wysłane do firmy!"
            },
            "ES": {
                "titolo": "RollMaster-germany-App",
                "sottotitolo": "Plataforma Profesional para Persianas y Protección Solar en Alemania",
                "disclaimer": "AVISO LEGAL: La plataforma actúa exclusivamente como intermediario tecnológico.",
                "scegli_lingua": "Seleccionar idioma",
                "area": "Ciudad / Región en Alemania",
                "categoria": "Categoría de intervención",
                "raggio": "Radio de búsqueda (km)",
                "ditte_titolo": "Empresas especializadas disponibles cerca de",
                "tariffa": "Tarifa por hora",
                "contatta": "Contactar",
                "preventivo": "Calculadora de presupuesto regional",
                "materiali": "Costo estimado de materiales (€)",
                "totale": "Estimación indicativa total",
                "inviato": "¡Solicitud enviada con éxito a la empresa!"
            },
            "PT": {
                "titolo": "RollMaster-germany-App",
                "sottotitolo": "Plataforma Profissional para Estores e Proteção Solar na Alemanha",
                "disclaimer": "AVISO LEGAL: A plataforma atua exclusivamente como intermediário tecnológico.",
                "scegli_lingua": "Selecionar idioma",
                "area": "Cidade / Região na Alemanha",
                "categoria": "Categoria de intervenção",
                "raggio": "Raio de pesquisa (km)",
                "ditte_titolo": "Empresas especializadas disponíveis perto de",
                "tariffa": "Tarifa horária",
                "contatta": "Contactar",
                "preventivo": "Calculadora de orçamento regional",
                "materiali": "Custo estimado dos materiais (€)",
                "totale": "Estimativa indicativa total",
                "inviato": "Pedido enviado com sucesso para a empresa!"
            },
            "TR": {
                "titolo": "RollMaster-germany-App",
                "sottotitolo": "Almanya'da Panjur ve Güneş Koruması için Profesyonel Platform",
                "disclaimer": "YASAL UYARI: Platform yalnızca teknolojik aracı olarak hizmet vermektedir.",
                "scegli_lingua": "Dil Seçimi",
                "area": "Almanya'da Şehir / Bölge",
                "categoria": "Müdحale Kategorisi",
                "raggio": "Arama yarıçapı (km)",
                "ditte_titolo": "Yakınlarda mevcut uzman firmalar",
                "tariffa": "Saatlik Ücret",
                "contatta": "İletişim",
                "preventivo": "Hızlı Bölgesel Fiyat Hesaplayıcı",
                "materiali": "Tahmini malzeme maliyeti (€)",
                "totale": "Tahmini Toplam Tutar",
                "inviato": "Talep firmaya başarıyla gönderildi!"
            }
        }

        self.indici_regionali = {
            "STUTTGART": 1.25,
            "MUNCHEN": 1.30,
            "BERLIN": 1.15,
            "FREIBURG": 1.05,
            "PROVINCIA_STANDARD": 1.0
        }

        # Database ditte con terminologia tecnica tedesca standard (DIN / VOB / BG BAU)
        self.database_ditte = [
            {
                "id": "DE_MARCHESE_01",
                "nome": "Marchese Rolladen & Sonnenschutz GmbH",
                "citta": "Stuttgart",
                "lat": 48.7758,
                "lon": 9.1829,
                "specializzazione": ["ROLLLADEN", "MARKISE"],
                "certificazioni": ["DIN EN 13659", "DIN EN 13561", "VOB/C", "BG BAU konform"],
                "telefono": "+49 711 123456",
                "tariffa_oraria_euro": 85.0,
                "costo_chiamata_base": 50.0
            },
            {
                "id": "DE_SONNEN_02",
                "nome": "Schwarzwald Jalousie & Raffstore Jäger",
                "citta": "Freiburg",
                "lat": 47.9990,
                "lon": 7.8421,
                "specializzazione": ["JALOUSIE_RAFFSTORE", "INSEKTENSCHUTZ"],
                "certificazioni": ["DIN EN 13120", "DIN 18055", "BG BAU konform"],
                "telefono": "+49 761 987654",
                "tariffa_oraria_euro": 92.0,
                "costo_chiamata_base": 60.0
            }
        ]

    def _calcola_distanza(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371.0
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(R * c, 2)

    def cerca_ditte(self, citta_selezionata: str, categoria: str, raggio: float) -> List[Dict[str, Any]]:
        coordinate_citta = {
            "STUTTGART": (48.7758, 9.1829),
            "MUNCHEN": (48.1351, 11.5820),
            "BERLIN": (52.5200, 13.4050),
            "FREIBURG": (47.9990, 7.8421)
        }
        lat_c, lon_c = coordinate_citta.get(citta_selezionata.upper(), (48.7758, 9.1829))
        
        risultati = []
        for ditta in self.database_ditte:
            if categoria.upper() in ditta["specializzazione"]:
                dist = self._calcola_distanza(lat_c, lon_c, ditta["lat"], ditta["lon"])
                if dist <= raggio:
                    d_info = ditta.copy()
                    d_info["distanza_km"] = dist
                    risultati.append(d_info)
        return sorted(risultati, key=lambda x: x["distanza_km"])

# Inizializzazione Engine
engine = RollMasterGermanyAppEngine()

# --- INTERFACCIA UTENTE MULTILINGUE ---
st.sidebar.header("🌐 Configurazione / Settings")
lingua_codice = st.sidebar.selectbox(
    "Lingua / Language / Limba / Język / Dil", 
    options=["IT", "DE", "RO", "PL", "ES", "PT", "TR"],
    format_func=lambda x: {
        "IT": "🇮🇹 Italiano",
        "DE": "🇩🇪 Deutsch",
        "RO": "🇷🇴 Română",
        "PL": "🇵🇱 Polski",
        "ES": "🇪🇸 Español",
        "PT": "🇵🇹 Português",
        "TR": "🇹🇷 Türkçe"
    }[x]
)

t = engine.traduzioni[lingua_codice]

st.title(f"🛡️ {t['titolo']}")
st.markdown(f"### {t['sottotitolo']}")
st.info(t['disclaimer'])

# Sidebar Parametri Intervento
st.sidebar.divider()
st.sidebar.header("⚙️ Parametri Cantiere")
citta = st.sidebar.selectbox(t['area'], ["Stuttgart", "Munchen", "Berlin", "Freiburg"])
categoria = st.sidebar.selectbox(t['categoria'], ["ROLLLADEN", "MARKISE", "JALOUSIE_RAFFSTORE", "INSEKTENSCHUTZ"])
raggio_km = st.sidebar.slider(t['raggio'], 10, 200, 50)

# Traduzione automatica simulata per la ditta tedesca
st.sidebar.divider()
st.sidebar.markdown("💬 **Traduttore Istantaneo Bidirezionale:**")
st.sidebar.caption("Scrivi nella tua lingua: l'app converte automaticamente la richiesta in tedesco tecnico (DIN/VOB) per la ditta.")
messaggio_utente = st.sidebar.text_area("Descrivi il guasto o l'installazione:", "Ho bisogno di riparare la cinghia della tapparella bloccata.")
if st.sidebar.button("Traduci e Invia alla Ditta"):
    st.sidebar.success("✅ Tradotto in Tedesco Tecnico: *'Reparatur Rolladen Gurtband blockiert (Norm DIN 18055)'* inviato con successo!")

st.divider()

# Sezione Principale: Ditte Specializzate
st.subheader(f"📍 {t['ditte_titolo']} {citta}")
ditte_trovate = engine.cerca_ditte(citta, categoria, raggio_km)

if ditte_trovate:
    for d in ditte_trovate:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### **{d['nome']}**")
                st.write(f"📞 **Tel:** {d['telefono']} | 📍 **Distanza:** {d['distanza_km']} km")
                st.write(f"📜 **Certificazioni DIN/VOB/BG BAU:** {', '.join(d['certificazioni'])}")
            with col2:
                st.metric(t['tariffa'], f"€ {d['tariffa_oraria_euro']}")
                if st.button(t['contatta'], key=d["id"]):
                    st.success(t['inviato'])
            st.markdown("---")
else:
    st.warning("Nessuna ditta trovata con questi criteri nel raggio selezionato.")

# Sezione Preventivo Rapido Regionale
st.subheader(f"💶 {t['preventivo']}")
col_p1, col_p2 = st.columns(2)
with col_p1:
    costo_materiale_base = st.number_input(t['materiali'], min_value=0.0, value=120.0, step=10.0)
with col_p2:
    moltiplicatore = engine.indici_regionali.get(citta.upper(), 1.0)
    stima_totale = (50.0 + 85.0) * moltiplicatore + costo_materiale_base
    st.metric(t['totale'], f"€ {stima_totale:.2f}")

# Footer
st.markdown("---")
st.caption("RollMaster-germany-App © 2026 - Conforme agli standard di sicurezza BG BAU e normative tecniche tedesche.")
