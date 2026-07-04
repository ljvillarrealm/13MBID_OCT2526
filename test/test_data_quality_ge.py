# Generado mediante pair programming (codigo asistido): Copilot (por defecto en VSCode)
# Revisado y adaptado por: Leonardo Villarreal

import pandas as pd
import pytest
from pathlib import Path
import warnings

warnings.filterwarnings(
    "ignore",
    message = r".*`Number` field should not be instantiated.*",
    )

import great_expectations as ge

pytestmark = [
    pytest.mark.filterwarnings("ignore:.*Number.*should not be instantiated.*"),
    pytest.mark.filterwarnings("ignore:.*result_format.*Validator-level.*"),
    pytest.mark.filterwarnings("ignore:.*result_format.*Expectation-level.*"),
]

# Paths
PROJECT_DIR = Path(".").resolve()
DATA_DIR = PROJECT_DIR / "data"


def test_data_quality_ge():
    # Cargar los datos de créditos y tarjetas
    df_creditos = pd.read_csv(DATA_DIR / "raw/datos_creditos.csv", sep=";")
    df_tarjetas = pd.read_csv(DATA_DIR / "raw/datos_tarjetas.csv", sep=";")

    # Resultados de la validación
    results = {
        "success": True,
        "expectations": [],
        "statistics": {
            "total_expectations": 0,
            "successful_expectations": 0,
            "failed_expectations": 0,
            "pct_failed_expectations": 0.0,
        },
    }

    def add_expectation(expectation_name, condition, message=""):
        # Funcion para agregar resultados de expectativas

        # Determinar si la expectativa fue exitosa o fallida
        success = bool(condition)
        # Agregar el resultado de la expectation al diccionario de resultados
        results["expectations"].append({"expectation": expectation_name, "success": success, "message": message})
        # Actualizar estadísticas
        results["statistics"]["total_expectations"] += 1
        # Actualizar estadísticas de éxito o fallo
        if success:
            results["statistics"]["successful_expectations"] += 1
        else:
            results["statistics"]["failed_expectations"] += 1
            results["success"] = False
        # Calcular el porcentaje de expectativas fallidas
        results["statistics"]["pct_failed_expectations"] = (
            results["statistics"]["failed_expectations"] / results["statistics"]["total_expectations"]
        ) * 100

    # ##############################
    # Expectations
    # ##############################

    # Expectation 1: Verificar que la edad esta entre 18 y 100 años
    # Atributo a analizar: Exactitud (a nivel de rango)
    add_expectation(
        "rango_edad_es_valido",
        df_creditos["edad"].between(18.0, 100.0).all(),
        "La edad debe estar entre 18 y 100 años"
    )
    # Expectation 2: Verificar que la situacion de vivienda es una de las categorias validas
    # Atributo a analizar: Exactitud (a nivel de categoría)
    valid_vivienda = {"ALQUILER", "HIPOTECA", "PROPIA", "OTROS"}
    add_expectation(
        "situacion_vivienda_es_valida",
        df_creditos["situacion_vivienda"].isin(valid_vivienda).all(),
        f"La situacion de vivienda debe ser una de las siguientes: {valid_vivienda}"
    )

    # ############## (SECCION RETO/EXTRA PROPUESTO) ################
    # Expectation 3: Verificar que el ingreso es un valor positivo
    # Atributo a analizar: Consistencia/Exactitud (a nivel de rango)
    add_expectation(
        "ingreso_es_positivo",
        df_creditos["ingresos"].gt(0).all(),
        "El ingreso debe ser un valor positivo"
    )
    # Expectation 4: Verificar que el limite de credito esta entre 1000 y 100000
    # Atributo a analizar: Consistencia/Exactitud (a nivel de rango)
    add_expectation(
        "limite_credito_en_rango",
        df_tarjetas["limite_credito_tc"].between(1000.0, 100000.0).all(),
        "El limite de credito debe estar entre 1,000 y 100,000"
    )
    # Expectation 5: Verificar que la variable objetivo falta_pago solo contiene valores 'N' o 'S'
    # Atributo a analizar: Exactitud (a nivel de categoría)
    add_expectation(
        "falta_pago_es_binaria",
        df_creditos["falta_pago"].isin(['N', 'S']).all(),
        "La variable objetivo falta_pago debe contener solo valores 'N' o 'S'"
    )
    # Expectation 6: Verificar que estado del cliente es una de las categorias validas
    # Atributo a analizar: Exactitud (a nivel de categoría)
    valid_estado_cliente = {"ACTIVO", "PASIVO"}
    add_expectation(
        "estado_cliente_es_valido",
        df_tarjetas["estado_cliente"].isin(valid_estado_cliente).all(),
        f"El estado del cliente debe ser una de las siguientes: {valid_estado_cliente}"
    )
    # Expectation 7: Verificar que el id_cliente es unico en ambos datasets
    # Atributo a analizar: Consistencia (a nivel de unicidad de identificadores)
    add_expectation(
        "id_cliente_es_unico_creditos",
        df_creditos["id_cliente"].is_unique,
        "Existen identificadores de cliente duplicados en el dataset de créditos"
    )
    add_expectation(
        "id_cliente_es_unico_tarjetas",
        df_tarjetas["id_cliente"].is_unique,
        "Existen identificadores de cliente duplicados en el dataset de tarjetas"
    )
    # Expectation 8: Verificar que el esatdo civil es una de las categorias validas
    # Atributo a analizar: Exactitud (a nivel de categoría)
    valid_estado_civil = {"SOLTERO", "CASADO", "DIVORCIADO", "DESCONOCIDO"}
    add_expectation(
        "estado_civil_es_valido",
        df_tarjetas["estado_civil"].isin(valid_estado_civil).all(),
        f"El estado civil debe ser una de las siguientes: {valid_estado_civil}"
    )


    # Ejecutar las expectativas y mostrar los resultados
    print("\nResultados de la validación de datos:")
    for expectation in results["expectations"]:
        status = "Éxito" if expectation["success"] else "Fallo"
        print(f"- Expectativa: {expectation['expectation']}, Estado: {status}, Mensaje: {expectation['message']}")
    
    assert results["success"], "Algunas expectativas fallaron. Revisa los resultados de la validación."
