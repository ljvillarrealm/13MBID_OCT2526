import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title = "Predicción de Mora en Créditos",
    page_icon = ":credit_card:",
    layout="wide"
)

with st.sidebar:
    st.header("Instrucciones")
    st.write("""
    1. Ingrese los datos de cliente en el formulario.
    2. Haga click en el botón "Predecir"  para obtener la probabilidad de mora en créditos.
    3. Revise los resultados y la infdromación del modelo.
    """)
    st.header("Configuración de la API")
    api_url = st.text_input(
        "URL de la API",
        value="http://localhost:8000",
        help="Ingrese la URL donde está alojada la API de predicción."
    )
    st.divider()
    if st.button("Probar conexión a la API"):
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                st.success("Conexión exitosa de la API.")
            else:
                st.error(f"Error al coenctar con la API: {response.status_code}")
        except Exception as e:
            st.error(f"Error al conectar con la API: {e}")

# Titulo y descripciion de la app
st.title("Predicción de Mora en Créditos")
st.write("Ingrese los datos del cliente para estimar la probabilidad de mora en créditos.")

# Formulario de entrada de datos
with st.form("prediction_form"):
    st.subheader("Datos del Cliente")
    col1, col2, col3 = st.columns(3)

    with col1:
        antiguedad_cliente = st.number_input("Antigüedad del cliente (meses)", min_value=0, max_value=600, value=36)
        genero = st.selectbox("Género", options=["M", "F"])
        estado_civil = st.selectbox("Estado civil", options=["SOLTERO", "CASADO", "DIVORCIADO", "DESCONOCIDO"])

    with col2:
        nivel_educativo = st.selectbox(
            "Nivel educativo",
            options=["SECUNDARIO_COMPLETO", "UNIVERSITARIO_COMPLETO", "POSGRADO_COMPLETO", "SECUNDARIO_INCOMPLETO", "UNIVERSITARIO_INCOMPLETO", "POSGRADO_INCOMPLETO", "DESCONOCIDO"]
        )
        situacion_vivienda = st.selectbox("Situación de vivienda", options=["ALQUILER", "PROPIA", "HIPOTECA", "OTROS"])
        personas_a_cargo = st.number_input("Personas a cargo", min_value=0, value=0, step=1, max_value=20)

    with col3:
        estado_cliente = st.selectbox("Estado del cliente", options=["ACTIVO", "INACTIVO"])
        estado_credito = st.selectbox("Estado del crédito", options=[0, 1])

    st.subheader("Información financiera y laboral")
    col4, col5, col6 = st.columns(3)

    with col4:
        ingresos = st.number_input("Ingresos mensuales", min_value=0, value=50000, step=1000)
        pct_ingreso = st.number_input("% del ingreso comprometido", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
        capacidad_pago = st.number_input("Capacidad de pago", min_value=0.0, max_value=1.0, value=0.5, step=0.01)

    with col5:
        duracion_credito = st.number_input("Duración del crédito (años)", min_value=1, max_value=20, value=3)
        objetivo_credito = st.selectbox(
            "Objetivo del crédito",
            options=["PERSONAL", "EDUCACIÓN", "SALUD", "MEJORAS_HOGAR", "INVERSIONES", "PAGO_DEUDAS"]
        )
        tasa_interes = st.number_input("Tasa de interés (%)", min_value=0.0, max_value=40.0, value=12.0, step=0.1)

    with col6:
        ratio_endeudamiento = st.number_input("Ratio de endeudamiento", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
        presion_financiera = st.number_input("Presión financiera", min_value=0.0, value=20.0, step=0.5)

    st.subheader("Gastos, límites y otros")
    col7, col8 = st.columns(2)

    with col7:
        limite_credito_tc = st.number_input("Límite de crédito (TC)", min_value=0, value=5000, step=100)
        operaciones_mensuales = st.number_input("Operaciones mensuales", min_value=0.0, value=2.0, step=0.1)
        gasto_transaccion_promedio = st.number_input("Gasto promedio por transacción", min_value=0.0, value=40.0, step=1.0)

    with col8:
        antiguedad_relativa = st.number_input("Antigüedad relativa del empleado", min_value=0.0, value=0.2, step=0.01)

    st.subheader("")
    submitted = st.form_submit_button(
        "▶️ Predecir",
        use_container_width=True
    )

if submitted:
    input_data = {
        "duracion_credito": duracion_credito,
        "situacion_vivienda": situacion_vivienda,
        "ingresos": ingresos,
        "objetivo_credito": objetivo_credito,
        "pct_ingreso": pct_ingreso,
        "tasa_interes": tasa_interes,
        "estado_credito": estado_credito,
        "antiguedad_cliente": antiguedad_cliente,
        "estado_civil": estado_civil,
        "estado_cliente": estado_cliente,
        "genero": genero,
        "limite_credito_tc": limite_credito_tc,
        "nivel_educativo": nivel_educativo,
        "personas_a_cargo": personas_a_cargo,
        "capacidad_pago": capacidad_pago,
        "ratio_endeudamiento": ratio_endeudamiento,
        "operaciones_mensuales": operaciones_mensuales,
        "gasto_transaccion_promedio": gasto_transaccion_promedio,
        "presion_financiera": presion_financiera,
        "antiguedad_relativa": antiguedad_relativa
    }

    try:
        with st.spinner("Calculando predicción..."):
            resp = requests.post(f"{api_url}/predict", json=input_data, timeout=10)
            resp.raise_for_status()
            result = resp.json()

        st.divider()
        st.subheader("📊 Resultado de la predicción")

        prediction = result["prediction"]
        prob = result.get("probability", {})
        labels = result.get("class_labels", {"0": "No entra en mora", "1": "Entra en mora"})

        label_text = labels.get(str(prediction), prediction)

        col_res1, col_res2 = st.columns(2)

        with col_res1:
            if str(prediction) == "1":
                st.error(f"**⚠️ Riesgo de falta de pago: {label_text}**")
            else:
                st.success(f"**✅ Bajo riesgo de falta de pago: {label_text}**")

        with col_res2:
            prob_mora = prob.get("1", prob.get(str(prediction), 0))
            prob_no_mora = prob.get("0", 1 - prob_mora)
            st.metric("Probabilidad de mora", f"{prob_mora * 100:.1f}%")
            st.metric("Probabilidad de no mora", f"{prob_no_mora * 100:.1f}%")

        with st.expander("Ver respuesta completa de la API"):
            st.json(result)

    except requests.exceptions.ConnectionError:
        st.error("No se pudo conectar con la API. Verifica la URL en el panel lateral.")
    except requests.exceptions.HTTPError as e:
        st.error(f"Error de la API ({resp.status_code}): {resp.json().get('detail', str(e))}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")

