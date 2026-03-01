"""
app.py — MediGraph Streamlit Frontend (OGB-powered)
=====================================================
Run with:  streamlit run app.py
"""

import streamlit as st
import streamlit.components.v1 as components

import sys
import os
# Ensure the medigraph directory is in the Python path for Streamlit Cloud
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engines.data_loader import get_drug_names, get_num_drugs
from engines.interaction_engine import check_interactions
from engines.risk_engine import calculate_risk
from engines.graph_engine import build_graph

# ── Page config ────────────────────────────────────────────────────────────── #
st.set_page_config(
    page_title="MediGraph – Drug Interaction Checker",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS (Premium UI / Glassmorphism) ─────────────────────────────────── #
st.markdown("""
<style>
    /* ---- global ---- */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Force Dark Theme Background */
    .stApp, .stApp > header {
        background-color: #0f172a !important;
        background-image: radial-gradient(circle at top right, #1e293b, #0f172a) !important;
        color: #f8fafc !important;
    }
    
    /* Hide Streamlit default UI elements for a cleaner look */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Lock sidebar open — hide the collapse arrow */
    [data-testid="collapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"] { min-width: 280px !important; }

    /* ---- Animations ---- */
    @keyframes fadeInUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .animated-item {
        animation: fadeInUp 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
        opacity: 0;
    }
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }

    /* ---- gradient header ---- */
    .header-banner {
        background: linear-gradient(135deg, #09101f 0%, #172a45 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .header-banner::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%; width: 200%; height: 200%;
        background: radial-gradient(circle, rgba(41,121,255,0.1) 0%, transparent 60%);
        pointer-events: none;
    }
    .header-banner h1 {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(to right, #ffffff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 0.5rem 0;
        letter-spacing: -1px;
    }
    .header-banner p {
        color: #94a3b8;
        font-size: 1.15rem;
        font-weight: 300;
        margin: 0;
        letter-spacing: 0.5px;
    }

    /* ---- Glassmorphism Cards ---- */
    .glass-card {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    .metric-card {
        border-left: 4px solid #3b82f6;
    }
    .metric-card.warn  { border-left-color: #f59e0b; }
    .metric-card.error { border-left-color: #ef4444; }
    .metric-card.safe  { border-left-color: #10b981; }

    /* ---- severity badges ---- */
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .badge-moderate { background: linear-gradient(135deg, #f59e0b, #d97706); color:#fff; }
    .badge-severe   { background: linear-gradient(135deg, #ef4444, #b91c1c); color:#fff; }
    .badge-mild     { background: linear-gradient(135deg, #10b981, #059669); color:#fff; }
    .badge-contra   { background: linear-gradient(135deg, #8b5cf6, #6d28d9); color:#fff; }

    /* ---- risk score gauge ---- */
    .risk-gauge {
        text-align: center;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
    }
    .risk-low      { background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(5,150,105,0.2)); border: 1px solid rgba(16,185,129,0.3); }
    .risk-moderate { background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(217,119,6,0.2)); border: 1px solid rgba(245,158,11,0.3); }
    .risk-high     { background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(185,28,28,0.2)); border: 1px solid rgba(239,68,68,0.3); }
    
    .risk-gauge h2 { 
        color: #f8fafc; 
        font-size: 4.5rem; 
        font-weight: 700; 
        margin: 0; 
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    .risk-gauge p  { 
        font-size: 1.2rem; 
        font-weight: 500;
        margin: 0.5rem 0 0; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .risk-low p      { color: #34d399; }
    .risk-moderate p { color: #fbbf24; }
    .risk-high p     { color: #f87171; }

    /* ---- section titles ---- */
    .section-title {
        font-size: 1.4rem;
        font-weight: 600;
        color: #f1f5f9;
        margin: 2.5rem 0 1.2rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .section-title::after {
        content: '';
        height: 1px;
        flex-grow: 1;
        background: linear-gradient(to right, rgba(255,255,255,0.1), transparent);
    }

    /* ---- conflict row ---- */
    .conflict-row {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 0.8rem 0;
        border: 1px solid rgba(255,255,255,0.05);
        transition: all 0.2s ease;
    }
    .conflict-row:hover {
        background: rgba(30, 41, 59, 0.8);
        transform: scale(1.01);
    }
    .conflict-drug {
        font-size: 1.1rem;
        color: #e2e8f0;
    }
    .conflict-drug-highlight {
        color: #f87171;
        font-weight: 600;
    }

    /* ---- info box ---- */
    .info-box {
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        color: #94a3b8;
        font-size: 0.95rem;
        margin-top: 0.8rem;
        line-height: 1.5;
    }

    /* ---- custom streamlit overrides ---- */
    [data-testid="stSidebar"] {
        background: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    input {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.4) !important;
        background: linear-gradient(135deg, #60a5fa, #3b82f6) !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Header ───────────────────────────────────────────────────────────────────── #
st.markdown("""
<div class="header-banner animated-item">
    <h1>MediGraph</h1>
    <p>AI-powered Drug Interaction Checker — Powered by OGB</p>
</div>
""", unsafe_allow_html=True)


# ── Sidebar — Patient Info ───────────────────────────────────────────────────── #
with st.sidebar:
    st.markdown("<h2 style='color:#f8fafc; font-weight:600;'>Patient Information</h2>", unsafe_allow_html=True)
    patient_name = st.text_input("Patient Name", placeholder="eg : Nitya patel")
    patient_age  = st.number_input("Age (Years)", min_value=0, max_value=120, value=20)
    patient_gender = st.selectbox("Biological Sex", ["Male", "Female", "Other"])

    st.markdown("<br><hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    with st.expander("About the Dataset", expanded=True):
        st.markdown("""
        **OGB ogbl-ddi**  
        Open Graph Benchmark — Drug-Drug Interaction  
        
        <ul style="color:#94a3b8; font-size: 0.9rem; padding-left: 1rem;">
            <li><b>4,267</b> approved drugs</li>
            <li><b>1.3M+</b> known interactions</li>
            <li>Sourced from FDA records</li>
        </ul>
        """, unsafe_allow_html=True)


# ── Load OGB Data (cached) ───────────────────────────────────────────────────── #
@st.cache_resource(show_spinner="Connecting to OGB knowledge graph...")
def load_drug_list():
    return get_drug_names()

drug_names = load_drug_list()

# ── Main Section ─────────────────────────────────────────────────────────────── #
st.markdown("<div class='animated-item delay-1'>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h3 style='color:#e2e8f0; font-weight:500; font-size:1.3rem;'>Select Medications</h3>", unsafe_allow_html=True)
    selected_drugs = st.multiselect(
        "Search and select patient's current or prescribed drugs",
        options=drug_names,
        default=None,
        max_selections=15,
        placeholder="Type to search"
    )

with col2:
    st.markdown("<br><br>", unsafe_allow_html=True)
    check_btn = st.button("Check Interactions", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# ── Results ───────────────────────────────────────────────────────────────────── #
if check_btn and selected_drugs:
    if len(selected_drugs) < 2:
        st.warning("Please select at least 2 drugs to analyze potential interactions.")
    else:
        with st.spinner("Analyzing graph interactions..."):
            # Run engines
            conflicts = check_interactions(selected_drugs)
            patient_data = {"name": patient_name or "Unknown", "age": patient_age, "gender": patient_gender}

            # Validation (age/gender) against local drugs.json
            try:
                from engines.validation_engine import validate_patient
                import json, os
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                drugs_json_path = os.path.join(BASE_DIR, "data", "drugs.json")
                with open(drugs_json_path) as f:
                    drugs_db = json.load(f)
                age_warnings, gender_warnings = validate_patient(patient_data, selected_drugs, drugs_db)
            except Exception:
                age_warnings, gender_warnings = [], []

            risk_score, risk_level = calculate_risk(conflicts, age_warnings, gender_warnings)
            graph_html = build_graph(selected_drugs, conflicts)

        # ── Layout: Risk Gauge | Summary ─────────────────────────────── #
        st.markdown("<div class='animated-item delay-2'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns([1.2, 1, 1])

        with r1:
            gauge_cls = {"Low": "risk-low", "Moderate": "risk-moderate", "High": "risk-high"}.get(risk_level, "risk-low")
            st.markdown(f"""
            <div class="risk-gauge {gauge_cls}">
                <h2>{risk_score}</h2>
                <p>Risk: <strong>{risk_level}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="glass-card">
                <div style="color:#94a3b8; font-size:0.9rem; text-transform:uppercase;">Drugs Selected</div>
                <div style="font-size:2rem; font-weight:700; color:#f8fafc;">{len(selected_drugs)}</div>
            </div>
            <div class="glass-card">
                <div style="color:#94a3b8; font-size:0.9rem; text-transform:uppercase;">Interactions Found</div>
                <div style="font-size:2rem; font-weight:700; color:#f8fafc;">{len(conflicts)}</div>
            </div>
            """, unsafe_allow_html=True)

        with r3:
            st.markdown(f"""
            <div class="glass-card">
                <div style="color:#94a3b8; font-size:0.9rem; text-transform:uppercase;">Age Warnings</div>
                <div style="font-size:2rem; font-weight:700; color:#f8fafc;">{len(age_warnings)}</div>
            </div>
            <div class="glass-card">
                <div style="color:#94a3b8; font-size:0.9rem; text-transform:uppercase;">Gender Warnings</div>
                <div style="font-size:2rem; font-weight:700; color:#f8fafc;">{len(gender_warnings)}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Conflicts Table ───────────────────────────────────────────── #
        st.markdown("<div class='animated-item delay-3'>", unsafe_allow_html=True)
        if conflicts:
            st.markdown('<div class="section-title">Detected Drug Conflicts</div>', unsafe_allow_html=True)
            badge_map = {
                "Severe": "badge-severe",
                "Moderate": "badge-moderate",
                "Mild": "badge-mild",
                "Contraindicated": "badge-contra"
            }
            for c in conflicts:
                badge_cls = badge_map.get(c["severity"], "badge-moderate")
                st.markdown(f"""
                <div class="conflict-row">
                    <div class="conflict-drug">
                        <span class="conflict-drug-highlight">{c['drug1']}</span> interacts with <span class="conflict-drug-highlight">{c['drug2']}</span>
                        <span class="badge {badge_cls}">{c['severity']}</span>
                    </div>
                    <div class="info-box">{c['description']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            st.success("No known direct interactions detected between selected drugs.")

        # ── Age / Gender Warnings ─────────────────────────────────────── #
        if age_warnings:
            st.markdown('<div class="section-title">Age Contraindications</div>', unsafe_allow_html=True)
            for w in age_warnings:
                st.markdown(f'<div class="glass-card metric-card warn">{w}</div>', unsafe_allow_html=True)

        if gender_warnings:
            st.markdown('<div class="section-title">Gender Contraindications</div>', unsafe_allow_html=True)
            for w in gender_warnings:
                st.markdown(f'<div class="glass-card metric-card error">{w}</div>', unsafe_allow_html=True)

        # ── Interactive Graph ─────────────────────────────────────────── #
        st.markdown('<div class="section-title">Interaction Network</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="info-box" style="margin-bottom: 1rem; text-align: center;">
            <span style="color:#3b82f6;">●</span> Safe Medications &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
            <span style="color:#ef4444;">●</span> Interacting Medications &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
            <span style="color:#f59e0b;">—</span> Moderate Risk &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
            <span style="color:#ef4444;">—</span> Severe Risk
        </div>
        """, unsafe_allow_html=True)
        with st.container(border=True):
            components.html(graph_html, height=520, scrolling=False)
        st.markdown("</div>", unsafe_allow_html=True)

elif check_btn:
    st.info("Please select medications before checking interactions.")

# ── Footer ─────────────────────────────────────────────────────────────────── #
st.markdown("<br><br><hr style='border-color: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#64748b; font-size:0.85rem; font-weight: 300; padding-bottom: 2rem;">
    MediGraph Network Analyzer <br>
</div>
""", unsafe_allow_html=True)
