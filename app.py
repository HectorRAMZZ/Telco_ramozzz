import streamlit as st
import pandas as pd
import joblib

# 1. CONFIGURACIÓN DEL PANEL
st.set_page_config(page_title="Dashboard de Retención", layout="wide", page_icon="📊")

# ──────────────────────────────────────────────
# CSS GLOBAL — diseño oscuro profesional
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

/* ── Fondo general ── */
.stApp {
    background: #0d1117;
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #30363d;
}
section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #58a6ff !important;
    font-family: 'Syne', sans-serif;
}

/* ── Hero header ── */
.hero-box {
    background: linear-gradient(135deg, #1a237e 0%, #1565c0 55%, #0288d1 100%);
    border-radius: 14px;
    padding: 30px 36px;
    margin-bottom: 8px;
    box-shadow: 0 8px 40px rgba(21, 101, 192, 0.45);
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}
.hero-box::after {
    content: '';
    position: absolute;
    right: -60px; top: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(255,255,255,0.07) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 6px 0;
    letter-spacing: -0.3px;
}
.hero-sub {
    font-size: 13.5px;
    color: rgba(255,255,255,0.72);
    margin: 0;
    line-height: 1.55;
}

/* ── Divisor ── */
.divider {
    border: none;
    border-top: 1px solid #21262d;
    margin: 20px 0;
}

/* ── Etiqueta de sección ── */
.section-label {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #58a6ff;
    background: rgba(88,166,255,0.08);
    border: 1px solid rgba(88,166,255,0.2);
    border-radius: 20px;
    padding: 5px 14px;
    margin-bottom: 18px;
}

/* ── Widgets — labels ── */
label, .stSlider label, .stSelectbox label, .stNumberInput label {
    color: #8b949e !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
    text-transform: uppercase !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
    background: #1f6feb !important;
}

/* ── Selectbox & inputs ── */
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-size: 14px !important;
}
.stSelectbox > div > div:hover,
.stNumberInput > div > div > input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.15) !important;
}

/* ── Botón principal ── */
.stButton > button {
    background: linear-gradient(135deg, #1f6feb 0%, #0ea5e9 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 14px 0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    width: 100%;
    margin-top: 8px;
    box-shadow: 0 4px 20px rgba(31,111,235,0.4) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(31,111,235,0.55) !important;
}

/* ── Metric ── */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 20px 24px;
}
[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 12px !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stMetricValue"] {
    color: #e6edf3 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 36px !important;
    font-weight: 800 !important;
}

/* ── Progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #1f6feb, #0ea5e9) !important;
    border-radius: 4px !important;
}
.stProgress > div > div {
    background: #21262d !important;
    border-radius: 4px !important;
    height: 8px !important;
}

/* ── Alertas personalizadas ── */
.alert-critical {
    background: linear-gradient(135deg, rgba(220,38,38,0.12) 0%, rgba(239,68,68,0.06) 100%);
    border: 1px solid rgba(239,68,68,0.35);
    border-left: 4px solid #ef4444;
    border-radius: 10px;
    padding: 20px 22px;
    color: #fca5a5;
}
.alert-warning {
    background: linear-gradient(135deg, rgba(245,158,11,0.12) 0%, rgba(251,191,36,0.06) 100%);
    border: 1px solid rgba(251,191,36,0.35);
    border-left: 4px solid #f59e0b;
    border-radius: 10px;
    padding: 20px 22px;
    color: #fcd34d;
}
.alert-success {
    background: linear-gradient(135deg, rgba(16,185,129,0.12) 0%, rgba(52,211,153,0.06) 100%);
    border: 1px solid rgba(52,211,153,0.35);
    border-left: 4px solid #10b981;
    border-radius: 10px;
    padding: 20px 22px;
    color: #6ee7b7;
}
.alert-title {
    font-family: 'Syne', sans-serif;
    font-size: 15px;
    font-weight: 800;
    margin: 0 0 10px 0;
    letter-spacing: 0.2px;
}
.alert-body {
    font-size: 13.5px;
    line-height: 1.65;
    color: rgba(255,255,255,0.75);
    margin: 0;
}
.alert-body strong {
    color: rgba(255,255,255,0.92);
}

/* ── Texto genérico ── */
p, .stMarkdown p { color: #8b949e; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Información Académica")
    st.markdown("**Estudiante:** Hector Felipe Ramos Zurita")
    st.markdown("**Código ISIL:** `[6816.202610]`")
    st.markdown("[🔗 Cuaderno de Google Colab (Modo Lector)](https://colab.research.google.com/drive/1O8Vaf_UeqlfcWgerPqejh4XtM6frVfDT?usp=sharing)")
    st.write("---")
    st.caption("Evaluación PA2 - Procesamiento, Modelado y Despliegue Web")


# ──────────────────────────────────────────────
# HERO HEADER
# ──────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-title">📊 Inteligencia de Clientes: Panel Estratégico de Retención</div>
    <p class="hero-sub">Herramienta analítica predictiva para la evaluación de riesgo de fuga de clientes en tiempo real.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SECCIÓN 3 — INPUTS (variables sin cambios)
# ──────────────────────────────────────────────
st.markdown('<div class="section-label">👤 Variables del Perfil Comercial y Facturación</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    antiguedad = st.slider(
        "Antigüedad del Cliente (Meses):",
        min_value=0, max_value=72, value=12,
        help="Tiempo total transcurrido desde que el cliente contrató el servicio por primera vez."
    )
    pago_mensual = st.number_input(
        "Monto de Facturación Mensual ($):",
        min_value=18.0, max_value=120.0, value=50.0, step=5.0,
        help="Cargo fijo mensual registrado en el último ciclo."
    )

with col2:
    contrato_comercial = st.selectbox(
        "Modalidad de Contrato Actual:",
        ["Mes a mes", "Anual (1 Año)", "Bianual (2 Años)"],
        help="Tipo de vinculación legal vigente del cliente con la compañía."
    )
    servicio_internet = st.selectbox(
        "Tecnología de Internet Instalada:",
        ["Fibra Óptica", "DSL", "Sin servicio de internet"],
        help="Tipo de conexión de datos activa en el domicilio del cliente."
    )

with col3:
    canal_pago = st.selectbox(
        "Canal de Pago Habitual:",
        ["Banca Digital / Cheque Electrónico", "Tarjeta de Crédito (Débito Automático)", "Pago Manual / Cheque en Ventanilla"],
        help="Método de pago principal utilizado por el usuario."
    )

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ──────────────────────────────────────────────
# SECCIÓN 4 — BOTÓN Y PREDICCIÓN (lógica intacta)
# ──────────────────────────────────────────────
if st.button("🚀 Evaluar Riesgo en Tiempo Real", use_container_width=True):
    try:
        modelo = joblib.load('modelos/modelo_random_forest.pkl')

        # MAPEO INTERNO
        c_one_year = 1 if contrato_comercial == "Anual (1 Año)" else 0
        c_two_year = 1 if contrato_comercial == "Bianual (2 Años)" else 0

        int_fiber = 1 if servicio_internet == "Fibra Óptica" else 0
        int_no = 1 if servicio_internet == "Sin servicio de internet" else 0

        pay_electronic = 1 if canal_pago == "Banca Digital / Cheque Electrónico" else 0
        pay_card = 1 if canal_pago == "Tarjeta de Crédito (Débito Automático)" else 0
        pay_mailed = 1 if canal_pago == "Pago Manual / Cheque en Ventanilla" else 0

        input_data = {
            'SeniorCitizen': 0,
            'tenure': antiguedad,
            'MonthlyCharges': pago_mensual,
            'TotalCharges': antiguedad * pago_mensual,
            'gender_Male': 1, 'Partner_Yes': 0, 'Dependents_Yes': 0, 'PhoneService_Yes': 1,
            'MultipleLines_No phone service': 0, 'MultipleLines_Yes': 0,
            'InternetService_Fiber optic': int_fiber,
            'InternetService_No': int_no,
            'OnlineSecurity_No internet service': 0, 'OnlineSecurity_Yes': 0,
            'OnlineBackup_No internet service': 0, 'OnlineBackup_Yes': 0,
            'DeviceProtection_No internet service': 0, 'DeviceProtection_Yes': 0,
            'TechSupport_No internet service': 0, 'TechSupport_Yes': 0,
            'StreamingTV_No internet service': 0, 'StreamingTV_Yes': 0,
            'StreamingMovies_No internet service': 0, 'StreamingMovies_Yes': 0,
            'Contract_One year': c_one_year,
            'Contract_Two year': c_two_year,
            'PaperlessBilling_Yes': 1,
            'PaymentMethod_Credit card (automatic)': pay_card,
            'PaymentMethod_Electronic check': pay_electronic,
            'PaymentMethod_Mailed check': pay_mailed
        }

        df_input = pd.DataFrame([input_data])

        probabilidades = modelo.predict_proba(df_input)[0]
        riesgo_porcentaje = probabilidades[1] * 100

        # ── Resultados ──
        st.markdown('<div class="section-label">📈 Diagnóstico Comercial y Plan de Acción</div>', unsafe_allow_html=True)

        res_col1, res_col2 = st.columns([1, 2])

        with res_col1:
            st.metric(label="Índice de Riesgo de Fuga", value=f"{riesgo_porcentaje:.1f}%")
            st.progress(riesgo_porcentaje / 100)

        with res_col2:
            if riesgo_porcentaje >= 60:
                st.markdown("""
                <div class="alert-critical">
                    <p class="alert-title">🚨 ALERTA CRÍTICA: ALTO RIESGO DE FUGA DETECTADO</p>
                    <p class="alert-body"><strong>Acción Inmediata:</strong> Transferir la cuenta de forma prioritaria al equipo de Retención Especializada. Se recomienda aplicar un beneficio del <strong>20% de descuento automático</strong> en sus próximos ciclos de facturación o una mejora de velocidad sin costo para asegurar la continuidad de la cuenta antes de que solicite la cancelación.</p>
                </div>
                """, unsafe_allow_html=True)

            elif 30 <= riesgo_porcentaje < 60:
                st.markdown("""
                <div class="alert-warning">
                    <p class="alert-title">⚠️ ALERTA MODERADA: PERFIL EN ZONA DE INESTABILIDAD</p>
                    <p class="alert-body"><strong>Acción Preventiva:</strong> El cliente muestra señales intermedias de fricción (ej. contrato mensual o canales de pago manuales). Se recomienda enviar de forma proactiva una campaña digital de fidelización ofreciendo la migración a un plan estructurado a plazo fijo con tarifas preferenciales.</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.markdown("""
                <div class="alert-success">
                    <p class="alert-title">✅ CLIENTE SALUDABLE: COMPORTAMIENTO ESTABLE</p>
                    <p class="alert-body"><strong>Acción de Mantenimiento:</strong> El usuario cuenta con un perfil de alta lealtad y baja probabilidad de abandono. No se requiere asignar presupuesto de marketing ni descuentos directos. Continuar con el ciclo regular de facturación y soporte estándar de la compañía.</p>
                </div>
                """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("❌ Error del Sistema: No se encontró el archivo 'modelo_random_forest.pkl' dentro de la carpeta 'modelos/'. Confirma que se haya subido correctamente a tu repositorio de GitHub.")
    except Exception as e:
        st.error(f"❌ Ocurrió un error inesperado al procesar el diagnóstico: {e}")
