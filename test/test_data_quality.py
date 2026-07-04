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



def test_esquema_creditos(datos_creditos):
    # Validar esquema de los datyos de credito
    schema_creditos = DataFrameSchema({
        "id_cliente": Column(int, nullable=False),
        "edad": Column(int, Check.greater_than_or_equal_to(18)),
        "ingresos": Column(float, Check.greater_than_or_equal_to(0)),
        "situacion_vivienda": Column(str, Check.isin(["ALQUILER", "HIPOTECA", "PROPIA", "OTROS"])),
        "objetivo_credito": Column(str, Check.isin(["EDUCACIÓN", "SALUD", "INVERSIONES", "PAGO_DEUDAS", "PERSONAL", "MEJORAS_HOGAR", "VACACIONES", "OTROS"])),
        "falta_pago": Column(int, nullable=False), #Check.isin([0, 1])),
    })

    # Validate the dataframe against the schema
    schema_creditos.validate(datos_creditos)
