## Version UI con EXTRA
## Se capturan los datos originales y se hacen las transformaciones en vuelo antes de realizar la peticion al API con el modelo de porediccion\


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
    3. Revise los resultados y la información del modelo.
             
    Elaborado por (💜 DATA) ljvillarrealm para proyecto 13MBID
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

def calcular_atributos_derivados(raw: dict) -> dict:
    """Recibe los campos originales (tal como vienen de los datasets fuente)
    y devuelve el dict con el esquema esperado por la API/modelo."""

    importe_solicitado = raw["importe_solicitado"]
    ingresos = raw["ingresos"]
    operaciones_ult_12m = raw["operaciones_ult_12m"]
    gastos_ult_12m = raw["gastos_ult_12m"]
    duracion_credito = raw["duracion_credito"]
    antiguedad_empleado = raw["antiguedad_empleado"]
    edad = raw["edad"]

    return {
        # Atributos, tal cual
        "duracion_credito": duracion_credito,
        "situacion_vivienda": raw["situacion_vivienda"],
        "ingresos": ingresos,
        "objetivo_credito": raw["objetivo_credito"],
        "pct_ingreso": raw["pct_ingreso"],
        "tasa_interes": raw["tasa_interes"],
        "estado_credito": raw["estado_credito"],
        "antiguedad_cliente": raw["antiguedad_cliente"],
        "estado_civil": raw["estado_civil"],
        "estado_cliente": raw["estado_cliente"],
        "genero": raw["genero"],
        "limite_credito_tc": raw["limite_credito_tc"],
        "nivel_educativo": raw["nivel_educativo"],
        "personas_a_cargo": raw["personas_a_cargo"],

        # Atributos derivados
        "capacidad_pago": importe_solicitado / ingresos,
        "ratio_endeudamiento": importe_solicitado / (ingresos + importe_solicitado),
        "operaciones_mensuales": operaciones_ult_12m / 12,
        "gasto_transaccion_promedio": gastos_ult_12m / operaciones_ult_12m,
        "presion_financiera": (
            (gastos_ult_12m / 12 + importe_solicitado / duracion_credito * 12)
            / (ingresos / 12)
        ),
        "antiguedad_relativa": antiguedad_empleado / edad,
    }

# Formulario de entrada de datos
#with st.form("prediction_form"):
#    st.subheader("Datos del Cliente")
#    col1, col2, col3 = st.columns(3)
#
#    with col1:
#        antiguedad_cliente = st.number_input("Antigüedad del cliente (meses)", min_value=0, max_value=600, value=36)
#        genero = st.selectbox("Género", options=["M", "F"])
#        estado_civil = st.selectbox("Estado civil", options=["SOLTERO", "CASADO", "DIVORCIADO", "DESCONOCIDO"])
#
#    with col2:
#        nivel_educativo = st.selectbox(
#            "Nivel educativo",
#            options=["SECUNDARIO_COMPLETO", "UNIVERSITARIO_COMPLETO", "POSGRADO_COMPLETO", "SECUNDARIO_INCOMPLETO", "UNIVERSITARIO_INCOMPLETO", "POSGRADO_INCOMPLETO", "DESCONOCIDO"]
#        )
#        situacion_vivienda = st.selectbox("Situación de vivienda", options=["ALQUILER", "PROPIA", "HIPOTECA", "OTROS"])
#        personas_a_cargo = st.number_input("Personas a cargo", min_value=0, value=0, step=1, max_value=20)
#
#    with col3:
#        estado_cliente = st.selectbox("Estado del cliente", options=["ACTIVO", "INACTIVO"])
#        estado_credito = st.selectbox("Estado del crédito", options=[0, 1])
#
#    st.subheader("Información financiera y laboral")
#    col4, col5, col6 = st.columns(3)
#
#    with col4:
#        ingresos = st.number_input("Ingresos mensuales", min_value=0, value=50000, step=1000)
#        pct_ingreso = st.number_input("% del ingreso comprometido", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
#        capacidad_pago = st.number_input("Capacidad de pago", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
#
#    with col5:
#        duracion_credito = st.number_input("Duración del crédito (años)", min_value=1, max_value=20, value=3)
#        objetivo_credito = st.selectbox(
#            "Objetivo del crédito",
#            options=["PERSONAL", "EDUCACIÓN", "SALUD", "MEJORAS_HOGAR", "INVERSIONES", "PAGO_DEUDAS"]
#        )
#        tasa_interes = st.number_input("Tasa de interés (%)", min_value=0.0, max_value=40.0, value=12.0, step=0.1)
#
#    with col6:
#        ratio_endeudamiento = st.number_input("Ratio de endeudamiento", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
#        presion_financiera = st.number_input("Presión financiera", min_value=0.0, value=20.0, step=0.5)
#
#    st.subheader("Gastos, límites y otros")
#    col7, col8 = st.columns(2)
#
#    with col7:
#        limite_credito_tc = st.number_input("Límite de crédito (TC)", min_value=0, value=5000, step=100)
#        operaciones_mensuales = st.number_input("Operaciones mensuales", min_value=0.0, value=2.0, step=0.1)
#        gasto_transaccion_promedio = st.number_input("Gasto promedio por transacción", min_value=0.0, value=40.0, step=1.0)
#
#    with col8:
#        antiguedad_relativa = st.number_input("Antigüedad relativa del empleado", min_value=0.0, value=0.2, step=0.01)


with st.form("prediction_form"):
    st.subheader("Datos del cliente")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.text("Información personal")
        edad = st.number_input("Edad", min_value=18, max_value=100, value=30)
        antiguedad_cliente = st.number_input("Antigüedad como cliente (meses)", min_value=0, max_value=600, value=36)
        genero = st.selectbox("Género", options=["M", "F"])
        estado_civil = st.selectbox("Estado civil", options=["SOLTERO", "CASADO", "DIVORCIADO", "DESCONOCIDO"])
        nivel_educativo = st.selectbox(
            "Nivel educativo",
            options=["SECUNDARIO_COMPLETO", "UNIVERSITARIO_COMPLETO", "POSGRADO_COMPLETO",
                     "SECUNDARIO_INCOMPLETO", "UNIVERSITARIO_INCOMPLETO", "POSGRADO_INCOMPLETO", "DESCONOCIDO"]
        )
        personas_a_cargo = st.number_input("Personas a cargo", min_value=0, max_value=20, value=0)
        estado_cliente = st.selectbox("Estado del cliente", options=["ACTIVO", "INACTIVO"])

    with col2:
        st.text("Información financiera")
        ingresos = st.number_input("Ingresos anuales", min_value=0, value=50000, step=1000)
        pct_ingreso = st.number_input("% del ingreso comprometido", min_value=0.0, max_value=1.0, value=0.3, step=0.01)
        limite_credito_tc = st.number_input("Límite de crédito (TC)", min_value=0, value=5000, step=100)
        situacion_vivienda = st.selectbox("Situación de vivienda", options=["ALQUILER", "PROPIA", "HIPOTECA", "OTROS"])
        estado_credito = st.selectbox("Estado del crédito", options=[0, 1])
        operaciones_ult_12m = st.number_input("Operaciones (últimos 12 meses)", min_value=0.0, value=24.0, step=1.0)
        gastos_ult_12m = st.number_input("Gastos (últimos 12 meses)", min_value=0.0, value=500.0, step=10.0)
        

    with col3:
        st.text("Información del crédito")
        importe_solicitado = st.number_input("Importe solicitado del crédito", min_value=0, value=10000, step=500)
        duracion_credito = st.number_input("Duración del crédito (años)", min_value=1, max_value=20, value=3)
        tasa_interes = st.number_input("Tasa de interés (%)", min_value=0.0, max_value=40.0, value=12.0, step=0.1)
        objetivo_credito = st.selectbox(
            "Objetivo del crédito",
            options=["PERSONAL", "EDUCACIÓN", "SALUD", "MEJORAS_HOGAR", "INVERSIONES", "PAGO_DEUDAS"]
        )
    
    st.subheader("Información interna")
    col4, col5, col6 = st.columns(3)

    with col4:
        st.text("Información del empleado")
        antiguedad_empleado = st.number_input("Antigüedad laboral (años)", min_value=0.0, value=5.0, step=0.5)
    
    with col5:
        pass

    with col6:
        pass

    st.subheader("")
    submitted = st.form_submit_button(
        "▶️ Predecir",
        use_container_width=True
    )

if submitted:
    raw = {
        "edad": edad,
        "antiguedad_empleado": antiguedad_empleado,
        "antiguedad_cliente": antiguedad_cliente,
        "genero": genero,
        "estado_civil": estado_civil,
        "nivel_educativo": nivel_educativo,
        "personas_a_cargo": personas_a_cargo,
        "ingresos": ingresos,
        "importe_solicitado": importe_solicitado,
        "duracion_credito": duracion_credito,
        "tasa_interes": tasa_interes,
        "objetivo_credito": objetivo_credito,
        "situacion_vivienda": situacion_vivienda,
        "estado_credito": estado_credito,
        "pct_ingreso": pct_ingreso,
        "limite_credito_tc": limite_credito_tc,
        "operaciones_ult_12m": operaciones_ult_12m,
        "gastos_ult_12m": gastos_ult_12m,
        "estado_cliente": estado_cliente,
    }

    input_data = calcular_atributos_derivados(raw)

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

