import streamlit as st
import pandas as pd
import joblib

# 1. CONFIGURACIÓN DEL PANEL (Diseño ancho y profesional)
st.set_page_config(page_title="Dashboard de Retención", layout="wide")

# Estilos visuales personalizados mediante Markdown
st.markdown("""
    <style>
    .main-title { font-size: 30px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .section-header { font-size: 20px; font-weight: bold; color: #1F2937; margin-top: 15px; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal del Dashboard Comercial
st.markdown('<div class="main-title">📊 Inteligencia de Clientes: Panel Estratégico de Retención</div>', unsafe_allow_html=True)
st.write("Herramienta analítica predictiva para la evaluación de riesgo de fuga de clientes en tiempo real.")

# 2. CUADRO ACADÉMICO OBLIGATORIO (Rúbrica de Evaluación PA2)
with st.sidebar:
    st.header("📋 Información Académica")
    st.markdown("**Estudiante:** Hector Felipe Ramos Zurita")
    st.markdown("**Código ISIL:** `[TU CÓDIGO ISIL AQUÍ]`")
    st.markdown("[🔗 Cuaderno de Google Colab (Modo Lector)](Pega_Aquí_Tu_Enlace_Real)")
    st.write("---")
    st.caption("Evaluación PA2 - Procesamiento, Modelado y Despliegue Web")

st.write("---")

# 3. INTERFAZ DE USUARIO: Términos comerciales y simples en español
st.markdown('<div class="section-header">👤 Variables del Perfil Comercial y Facturación</div>', unsafe_allow_html=True)

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

# 4. LÓGICA DE PROCESAMIENTO Y PREDICCIÓN COMERCIAL
if st.button("🚀 Evaluar Riesgo en Tiempo Real", use_container_width=True):
    try:
        # Cargar el modelo guardado desde la carpeta obligatoria
        modelo = joblib.load('modelos/modelo_random_forest.pkl')
        
        # MAPEO INTERNO: Traducimos las respuestas simples del español al estricto formato del modelo
        c_one_year = 1 if contrato_comercial == "Anual (1 Año)" else 0
        c_two_year = 1 if contrato_comercial == "Bianual (2 Años)" else 0
        
        int_fiber = 1 if servicio_internet == "Fibra Óptica" else 0
        int_no = 1 if servicio_internet == "Sin servicio de internet" else 0
        
        pay_electronic = 1 if canal_pago == "Banca Digital / Cheque Electrónico" else 0
        pay_card = 1 if canal_pago == "Tarjeta de Crédito (Débito Automático)" else 0
        pay_mailed = 1 if canal_pago == "Pago Manual / Cheque en Ventanilla" else 0

        # Construcción del DataFrame idéntico al entrenamiento en Colab (Mismo orden y columnas)
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
        
        # Cálculo de probabilidades en lugar de salida binaria para alimentar el Dashboard
        probabilidades = modelo.predict_proba(df_input)[0]
        riesgo_porcentaje = probabilidades[1] * 100  # Probabilidad de pertenecer a la clase 1 (Churn)
        
        st.write("---")
        st.markdown('<div class="section-header">📈 Diagnóstico Comercial y Plan de Acción</div>', unsafe_allow_html=True)
        
        # Despliegue visual de resultados mediante columnas
        res_col1, res_col2 = st.columns([1, 2])
        
        with res_col1:
            st.metric(label="Índice de Riesgo de Fuga", value=f"{riesgo_porcentaje:.1f}%")
            st.progress(riesgo_porcentaje / 100)
        
        with res_col2:
            # Segmentación de acciones comerciales según el nivel de riesgo matemático
            if riesgo_porcentaje >= 60:
                st.error("🚨 **ALERTA CRÍTICA: ALTO RIESGO DE FUGA DETECTADO**")
                st.markdown("**Acción Inmediata:** Transferir la cuenta de forma prioritaria al equipo de Retención Especializada. Se recomienda aplicar un beneficio del **20% de descuento automático** en sus próximos ciclos de facturación o una mejora de velocidad sin costo para asegurar la continuidad de la cuenta antes de que solicite la cancelación.")
            
            elif 30 <= riesgo_porcentaje < 60:
                st.warning("⚠️ **ALERTA MODERADA: PERFIL EN ZONA DE INESTABILIDAD**")
                st.markdown("**Acción Preventiva:** El cliente muestra señales intermedias de fricción (ej. contrato mensual o canales de pago manuales). Se recomienda enviar de forma proactiva una campaña digital de fidelización ofreciendo la migración a un plan estructurado a plazo fijo con tarifas preferenciales.")
            
            else:
                st.success("✅ **CLIENTE SALUDABLE: COMPORTAMIENTO ESTABLE**")
                st.markdown("**Acción de Mantenimiento:** El usuario cuenta con un perfil de alta lealtad y baja probabilidad de abandono. No se requiere asignar presupuesto de marketing ni descuentos directos. Continuar con el ciclo regular de facturación y soporte estándar de la compañía.")
                
    except FileNotFoundError:
        st.error("❌ Error del Sistema: No se encontró el archivo 'modelo_random_forest.pkl' dentro de la carpeta 'modelos/'. Confirma que se haya subido correctamente a tu repositorio de GitHub.")
    except Exception as e:
        st.error(f"❌ Ocurrió un error inesperado al procesar el diagnóstico: {e}")
