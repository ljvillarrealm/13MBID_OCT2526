# Generado mediante pair programming (codigo asistido): Copilot (por defecto en VSCode)
# Revisado y adaptado por: Leonardo Villarreal

import pandas as pd
import pytest
from pandera.pandas import DataFrameSchema, Column, Check

@pytest.fixture
def datos_creditos():
    # Simulated data for testing
    df_creditos = pd.read_csv("data/raw/datos_creditos.csv", sep=";")
    return df_creditos

@pytest.fixture
def datos_tarjeta():
    df_tarjetas = pd.read_csv("data/raw/datos_tarjetas.csv", sep=";")
    return df_tarjetas


# ###################################
# Test de esquema
# ###################################

def test_esquema_creditos(datos_creditos):
    # Validar esquema de los datyos de credito
    schema_creditos = DataFrameSchema({
        "id_cliente": Column(float, nullable=False),
        "edad": Column(int, Check.greater_than_or_equal_to(18)),
        "importe_solicitado": Column(int, Check.greater_than(0)),
        "duracion_credito": Column(int, Check.greater_than(0)),
        "antiguedad_empleado": Column(float, Check.greater_than_or_equal_to(0), nullable=True),
        "situacion_vivienda": Column(str, nullable=False),  # Check.isin(["PROPIA", "ALQUILER", "FAMILIAR", "OTROS"])),
        "ingresos": Column(int, Check.greater_than_or_equal_to(0)),
        "objetivo_credito": Column(str, nullable=False),  # Check.isin(["EDUCACIÓN", "SALUD", "INVERSIONES", "PAGO_DEUDAS", "PERSONAL", "MEJORAS_HOGAR", "VACACIONES", "OTROS"])),
        "pct_ingreso": Column(float, Check.greater_than_or_equal_to(0)),
        "tasa_interes": Column(float, Check.greater_than_or_equal_to(0)),
        "estado_credito": Column(int, nullable=False), #Check.isin([0, 1])),
        "falta_pago": Column(int, nullable=False), #Check.isin([0, 1])),
    })

    schema_creditos.validate(datos_creditos)

def test_esquema_tarjeta(datos_tarjeta):
    # Validar esquema de los datos de tarjeta
    schema_tarjeta = DataFrameSchema({
        "id_cliente": Column(float, nullable=False),
        "antiguedad_cliente": Column(float, Check.greater_than_or_equal_to(0), nullable=True),
        "estado_civil": Column(str, nullable=False),  # Check.isin(["SOLTERO", "CASADO", "DIVORCIADO", "VIUDO"])),
        "estado_cliente": Column(str, nullable=False),  # Check.isin(["ACTIVO", "INACTIVO"])),
        "gastos_ult_12m": Column(float, Check.greater_than_or_equal_to(0)),
        "genero": Column(str, nullable=False),  # Check.isin(["MASCULINO", "FEMENINO"])),
        "limite_credito_tc": Column(float, Check.greater_than_or_equal_to(0)),
        "nivel_educativo": Column(str, nullable=False),  # Check.isin(["PRIMARIA", "SECUNDARIA", "SUPERIOR"])),
        "nivel_tarjeta": Column(str, nullable=False),  # Check.isin(["BASICA", "PREMIUM", "GOLD"])),
        "operaciones_ult_12m": Column(float, Check.greater_than_or_equal_to(0)),
        "personas_a_cargo": Column(float, Check.greater_than_or_equal_to(0)),
    })

    schema_tarjeta.validate(datos_tarjeta)


# ###################################
# Test de calidad de datos
# ###################################

def test_basicos_creditos(datos_creditos):
    df = datos_creditos.copy()

    # Validar dataset no vacio
    # Atributo a analizar: Exactitud (a nivel de estructura)
    assert not df.empty, "El dataset de créditos está vacío"

    # Validar la cantidad de filas y columnas
    # Atributo a analizar: Completitud (en general)
    assert df.shape[0] > 0, "El dataset de créditos no tiene filas"
    assert df.shape[1] == 12, "El dataset de créditos no tiene 12 columnas"

    # Validar que no hay valores nulos en el dataset
    # Atributo a analizar: Completitud (en general)
    assert df.notnull().all().all(), "El dataset de créditos contiene valores nulos"

    # Validar que no hay valores nulos en las columnas
    # Atributo a analizar: Completitud (en columnas específicas)
    assert df["id_cliente"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'id_cliente'"
    assert df["edad"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'edad'"
    assert df["importe_solicitado"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'importe_solicitado'"
    assert df["duracion_credito"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'duracion_credito'"
    assert df["antiguedad_empleado"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'antiguedad_empleado'"
    assert df["situacion_vivienda"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'situacion_vivienda'"
    assert df["ingresos"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'ingresos'"
    assert df["objetivo_credito"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'objetivo_credito'"
    assert df["pct_ingreso"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'pct_ingreso'"
    assert df["tasa_interes"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'tasa_interes'"
    assert df["estado_credito"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'estado_credito'"
    assert df["falta_pago"].notnull().all(), "El dataset de créditos contiene valores nulos en la columna 'falta_pago'"

def test_basicos_tarjeta(datos_tarjeta):
    df = datos_tarjeta.copy()

    # Validar dataset no vacio
    # Atributo a analizar: Exactitud (a nivel de estructura)
    assert not df.empty, "El dataset de tarjetas está vacío"

    # Validar la cantidad de filas y columnas
    # Atributo a analizar: Completitud (en general)
    assert df.shape[0] > 0, "El dataset de tarjetas no tiene filas"
    assert df.shape[1] == 11, "El dataset de tarjetas no tiene 11 columnas"

    # Validar que no hay valores nulos en el dataset
    # Atributo a analizar: Completitud (en general)
    assert df.notnull().all().all(), "El dataset de tarjetas contiene valores nulos"

    # Validar que no hay valores nulos en las columnas
    # Atributo a analizar: Completitud (en columnas específicas)
    assert df["id_cliente"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'id_cliente'"
    assert df["antiguedad_cliente"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'antiguedad_cliente'"
    assert df["estado_civil"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'estado_civil'"
    assert df["estado_cliente"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'estado_cliente'"
    assert df["gastos_ult_12m"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'gastos_ult_12m'"
    assert df["genero"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'genero'"
    assert df["limite_credito_tc"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'limite_credito_tc'"
    assert df["nivel_educativo"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'nivel_educativo'"
    assert df["nivel_tarjeta"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'nivel_tarjeta'"
    assert df["operaciones_ult_12m"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'operaciones_ult_12m'"
    assert df["personas_a_cargo"].notnull().all(), "El dataset de tarjetas contiene valores nulos en la columna 'personas_a_cargo'" 


# ###################################
# Test de integridad y consistencia referencial
# ###################################

def test_integridad_referencial(datos_creditos, datos_tarjeta):
    # Validar integridad referencial entre los datasets de créditos y tarjetas
    # Atributo a analizar: Consistencia (a nivel de relación entre datasets)
    assert set(datos_creditos["id_cliente"]).issubset(set(datos_tarjeta["id_cliente"])), "Existen clientes en el dataset de créditos que no están presentes en el dataset de tarjetas"
    assert set(datos_tarjeta["id_cliente"]).issubset(set(datos_creditos["id_cliente"])), "Existen clientes en el dataset de tarjetas que no están presentes en el dataset de créditos"



    # ############## (SECCION RETO/EXTRA PROPUESTO) ################
    # Validar unicidad de los identificadores de cliente en ambos datasets
    # Atributo a analizar: Consistencia (a nivel de unicidad de identificadores)
    assert datos_creditos["id_cliente"].is_unique, "Existen identificadores de cliente duplicados en el dataset de créditos"
    assert datos_tarjeta["id_cliente"].is_unique, "Existen identificadores de cliente duplicados en el dataset de tarjetas"

    # Validar rangos y valores validos
    # Atributo a analizar: Consistencia (a nivel de domino)

    ## Edad de los clientes
    assert datos_creditos["edad"].min() >= 0, "Existen valores negativos en la columna 'edad' del dataset de créditos"
    assert datos_creditos["edad"].max() <= 100, "Existen valores fuera del rango válido en la columna 'edad' del dataset de créditos"

    ## Antiguedad del empleado
    assert datos_creditos["antiguedad_empleado"].min() >= 0, "Existen valores negativos en la columna 'antiguedad_empleado' del dataset de créditos"
    assert datos_creditos["antiguedad_empleado"].max() <= 50, "Existen valores fuera del rango válido en la columna 'antiguedad_empleado' del dataset de créditos"

    ## Antiguedad del cliente
    assert datos_tarjeta["antiguedad_cliente"].min() >= 0, "Existen valores negativos en la columna 'antiguedad_cliente' del dataset de tarjetas"
    assert datos_tarjeta["antiguedad_cliente"].max() <= 50, "Existen valores fuera del rango válido en la columna 'antiguedad_cliente' del dataset de tarjetas"

    ## Porcentaje de ingreso
    assert datos_creditos["pct_ingreso"].min() >= 0, "Existen valores negativos en la columna 'pct_ingreso' del dataset de créditos"
    assert datos_creditos["pct_ingreso"].max() <= 100, "Existen valores fuera del rango válido en la columna 'pct_ingreso' del dataset de créditos"

    ## Tasa de interes
    assert datos_creditos["tasa_interes"].min() >= 0, "Existen valores negativos en la columna 'tasa_interes' del dataset de créditos"
    assert datos_creditos["tasa_interes"].max() <= 100, "Existen valores fuera del rango válido en la columna 'tasa_interes' del dataset de créditos"

    ## Estado del credito
    assert datos_creditos["estado_credito"].isin([0, 1]).all(), "Existen valores inválidos en la columna 'estado_credito' del dataset de créditos"

    ## Estado del pago (falta de pago)
    assert datos_creditos["falta_pago"].isin([0, 1]).all(), "Existen valores inválidos en la columna 'falta_pago' del dataset de créditos"
