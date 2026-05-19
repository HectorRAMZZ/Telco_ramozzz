import streamlit as st
import pandas as pd
import joblib

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Predicción de Churn", layout="centered")

# --- REQUISITOS DE LA EVALUACIÓN (PA2) ---
st.title("📊 Predicción de Abandono de Clientes (Telco Churn)")
st.markdown("### Desarrollado por: Hector Felipe Ramos Zurita")
st.markdown("**Cuaderno de Google Colab:** https://colab.research.google.com/drive/1O8Vaf_UeqlfcWgerPqejh4XtM6frVfDT?usp=sharing")

st.write("---")
st.write("Ingrese los datos del cliente para predecir si abandonará el servicio:")

# --- INTERFAZ DE USUARIO ---
col1, col2 = st.columns(2)

with col1:
    tenure = st.slider("Meses en la empresa (Tenure):", min_value=0, max_value=72, value=12)
    monthly_charges = st.number_input("Cargo Mensual ($):", min_value=18.0, max_value=120.0, value=50.0)

with col2:
    contract = st.selectbox("Tipo de Contrato:", ["Month-to-month", "One year", "Two year"])
    internet = st.selectbox("Servicio de Internet:", ["DSL", "Fiber optic", "No"])

# --- LÓGICA DE PREDICCIÓN ---
if st.button("Realizar Predicción"):
    try:
        # 1. Cargar el modelo desde la carpeta 'modelos'
        modelo = joblib.load('modelos/modelo_random_forest.pkl')
        
        # 2. Crear un DataFrame con los datos de entrada
        # (Se incluyen las variables que pide el modelo. Las demás asumen valores por defecto de la mayoría)
        input_data = {
            'SeniorCitizen': 0, 'tenure': tenure, 'MonthlyCharges': monthly_charges, 'TotalCharges': tenure * monthly_charges,
            'gender_Male': 1, 'Partner_Yes': 0, 'Dependents_Yes': 0, 'PhoneService_Yes': 1, 'MultipleLines_No phone service': 0,
            'MultipleLines_Yes': 0, 'InternetService_Fiber optic': 1 if internet == "Fiber optic" else 0,
            'InternetService_No': 1 if internet == "No" else 0, 'OnlineSecurity_No internet service': 0,
            'OnlineSecurity_Yes': 0, 'OnlineBackup_No internet service': 0, 'OnlineBackup_Yes': 0,
            'DeviceProtection_No internet service': 0, 'DeviceProtection_Yes': 0, 'TechSupport_No internet service': 0,
            'TechSupport_Yes': 0, 'StreamingTV_No internet service': 0, 'StreamingTV_Yes': 0,
            'StreamingMovies_No internet service': 0, 'StreamingMovies_Yes': 0,
            'Contract_One year': 1 if contract == "One year" else 0,
            'Contract_Two year': 1 if contract == "Two year" else 0,
            'PaperlessBilling_Yes': 1, 'PaymentMethod_Credit card (automatic)': 0,
            'PaymentMethod_Electronic check': 1, 'PaymentMethod_Mailed check': 0
        }
        
        df_input = pd.DataFrame([input_data])
        
        # 3. Predecir
        prediccion = modelo.predict(df_input)
        
        # 4. Mostrar el resultado
        st.write("---")
        if prediccion[0] == 1:
            st.error("⚠️ **ALERTA RIESGO ALTO:** Es muy probable que este cliente cancele el servicio (CHURN = SÍ).")
        else:
            st.success("✅ **CLIENTE SEGURO:** Es probable que este cliente se mantenga en la empresa (CHURN = NO).")
            
    except FileNotFoundError:
        st.error("❌ Error: No se encuentra el archivo 'modelo_random_forest.pkl' dentro de la carpeta 'modelos/'. Asegúrate de haberlo subido correctamente a GitHub.")
