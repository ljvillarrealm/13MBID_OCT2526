"""
Máster en Big Data y Data Science

Metodologías de gestión y diseño de proyectos de big data

AP1 - Limpieza de los datos
---
En este script se realiza una evaluación básica de calidad de los datos del
escenario y se ejecutan acciones de limpieza.

Generado con apoyo de IA: Claude Sonnet 5.0
Revisado y adaptado por: Leonardo Villarreal
"""

# Se importan las librerías necesarias y se suprimen las advertencias
import pandas as pd
#import numpy as np
from ydata_profiling import ProfileReport
import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)


def process_data():

    # -------------------------------------------------------------------
    # Lectura del mismo dataset inicial
    # -------------------------------------------------------------------
    df_creditos = pd.read_csv("data/raw/datos_creditos.csv", sep=";")
    # print(df_creditos.head(5))

    df_tarjetas = pd.read_csv("data/raw/datos_tarjetas.csv", sep=";")
    # print(df_tarjetas.head(5))

    # -------------------------------------------------------------------
    # Transformaciones sobre los datos
    # -------------------------------------------------------------------

    # Verificación de nulos
    # Se verifica la cantidad de valores nulos en cada columna
    # print("Valores nulos en el dataset de créditos:")
    # for col in df_creditos.columns:
    #     print(f"Atributo: {col} - Valores nulos: {df_creditos[col].isna().sum()} "
    #           f"({df_creditos[col].isna().sum()/len(df_creditos)*100:.2f}%)")

    # Se verifica la cantidad de valores nulos en cada columna
    # print("Valores nulos en el dataset de tarjetas:")
    # for col in df_tarjetas.columns:
    #     print(f"Atributo: {col} - Valores nulos: {df_tarjetas[col].isna().sum()} "
    #           f"({df_tarjetas[col].isna().sum()/len(df_tarjetas)*100:.2f}%)")

    # Selección de datos (filtro de columnas)
    # Se establece qué columnas se eliminan
    col_eliminar_creditos = []
    col_eliminar_tarjetas = ['nivel_tarjeta']

    # Se ejecuta la operación
    df_creditos.drop(col_eliminar_creditos, inplace=True, axis=1)
    df_tarjetas.drop(col_eliminar_tarjetas, inplace=True, axis=1)

    # Limpieza de datos (filtro de filas)
    #
    # Modificacion:
    # 1. Se descarta la eliminacion directa de los valores nulos con la
    #    finalidad de procesarlos y realizar la imputacion mas adecuada al
    #    momento: Mediana.

    # Checkpoint
    df_creditos_filtrado = df_creditos.copy()

    # Se filtran los datos para eliminar registros con edades superiores a 90 años
    df_creditos_filtrado = df_creditos_filtrado[df_creditos_filtrado['edad'] < 90]

    # Tratamiento de valores nulos
    # Eliminar todo registro con algun valor nulo (deprecado. Ver Modificacion 1).
    # df_creditos_filtrado.dropna(inplace=True)

    # Tratamiento de valores nulos para tasa_interes, se reemplaza por la
    # media de la columna, agrupada por objetivo_credito
    df_creditos_filtrado['tasa_interes'] = df_creditos_filtrado.groupby('objetivo_credito')['tasa_interes'].transform(lambda x: x.fillna(x.mean()))

    # Tratamiento de nulos para antiguedad_empleado, se reemplaza por la
    # mediana de la columna, agrupada por edad
    df_creditos_filtrado['antiguedad_empleado'] = df_creditos_filtrado.groupby('edad')['antiguedad_empleado'].transform(lambda x: x.fillna(x.median()))

    # -------------------------------------------------------------------
    # Integración de ambos datasets en uno solo
    # -------------------------------------------------------------------
    df_integrado = pd.merge(df_creditos_filtrado, df_tarjetas, on='id_cliente', how='inner')

    # print(f"Filas del dataset integrado con los filtros realizados: {df_integrado.shape[0]}")
    # print(f"Columnas del dataset integrado post integración: {df_integrado.shape[1]}")
    # print(f"El dataset original tenía {df_creditos.shape[0]} filas en Créditos y "
    #       f"{df_tarjetas.shape[0]} filas en Tarjetas.")
    # print(f"Se han eliminado {df_creditos.shape[0] - df_creditos_filtrado.shape[0]} filas en total.")
    # print(df_integrado.head(5))

    # -------------------------------------------------------------------
    # Generacion de atributos
    #
    # En esta seccion se realiza la creacion de atributos derivados, de
    # interes para el negocio.
    # -------------------------------------------------------------------

    # Atributo generado 1: capacidad de pago = importe solicitado / ingresos
    df_integrado['capacidad_pago'] = df_integrado['importe_solicitado'] / df_integrado['ingresos']

    # Atributo generado 2: ratio de endeudamiento = importe solicitado / (ingresos + importe solicitado)
    df_integrado['ratio_endeudamiento'] = df_integrado['importe_solicitado'] / (df_integrado['ingresos'] + df_integrado['importe_solicitado'])

    # Atributo generado 3: operaciones mensuales promedio = operaciones totales / 12 meses
    df_integrado['operaciones_mensuales'] = df_integrado['operaciones_ult_12m'] / 12

    # Atributo generado 4: gasto por transacción promedio = gasto total / operaciones totales
    df_integrado['gasto_transaccion_promedio'] = df_integrado['gastos_ult_12m'] / df_integrado['operaciones_ult_12m']

    # Atributo generado 5: Presion financiera
    df_integrado['presion_financiera'] = (
        (df_integrado['gastos_ult_12m'] / 12 + df_integrado['importe_solicitado'] / (df_integrado['duracion_credito']) * 12)
        / (df_integrado['ingresos'] / 12)
    )

    # Atributo generado 6: Antiguedad relativa del empleado = antiguedad_empleado / edad
    df_integrado['antiguedad_relativa'] = df_integrado['antiguedad_empleado'] / df_integrado['edad']

    # -------------------------------------------------------------------
    # Transformaciones sobre atributos
    #
    # Modificacion:
    # 1. Se descarta el mapping de estado civil
    # 2. Se descarta el mapping de estado de credito
    # 3. Se descarta la transformacion de Antiguedad del empleado
    # 4. Se descarta la transformacion de edad
    # -------------------------------------------------------------------

    # Columna: estado_civil
    # cambios_estado_civil = {
    #     'CASADO': 'C',
    #     'SOLTERO': 'S',
    #     'DESCONOCIDO': 'N',
    #     'DIVORCIADO': 'D',
    # }
    #
    # Columna: estado_credito
    # cambios_estado_credito = {
    #     0: 'P',
    #     1: 'C',
    # }
    #
    # estado_civil_N = df_integrado.loc[:, ('estado_civil')].map(cambios_estado_civil).rename('estado_civil_N')
    # estado_credito_N = df_integrado.loc[:, ('estado_credito')].map(cambios_estado_credito).rename('estado_credito_N')

    # Antiguedad del empleado
    # etiquetas_a_e = ['menor_5', '5_a_10', 'mayor_10']
    # rangos_a_e = [0, 4, 10, 50]
    # valor_para_nan = 'NA'
    # antiguedad_empleados_N = pd.cut(df_integrado['antiguedad_empleado'],
    #                                 bins=rangos_a_e,
    #                                 labels=etiquetas_a_e,
    #                                 right=False).cat.add_categories(valor_para_nan).fillna(valor_para_nan)
    #
    # print(antiguedad_empleados_N.value_counts())

    # edad
    # etiquetas_e = ['menor_25', '25_a_30']
    # rangos_e = [0, 24, 50]
    # edad_N = pd.cut(df_integrado['edad'],
    #                 bins=rangos_e,
    #                 labels=etiquetas_e)
    #
    # print(edad_N.value_counts())

    # Se eliminan las columnas originales y se integran las nuevas columnas procesadas
    columnas_a_eliminar = [
        # 'estado_civil', 'estado_credito', 'antiguedad_empleado', 'edad',
        'id_cliente',
        'importe_solicitado',
        'operaciones_ult_12m',
        'gastos_ult_12m',
        'antiguedad_empleado',
        'edad',
    ]
    df_integrado.drop(columnas_a_eliminar, inplace=True, axis=1)
    # df_integrado = pd.concat([df_integrado, estado_civil_N, estado_credito_N, antiguedad_empleados_N, edad_N], axis=1)
    # print(df_integrado.head(5))

    # -------------------------------------------------------------------
    # Validaciones finales
    # -------------------------------------------------------------------

    # Se verifica la cantidad de valores nulos en cada columna del dataset integrado
    # print("Valores nulos en el dataset integrado:")
    # for col in df_integrado.columns:
    #     print(f"Atributo: {col} - Valores nulos: {df_integrado[col].isna().sum()} "
    #           f"({df_integrado[col].isna().sum()/len(df_integrado)*100:.2f}%)")

    # Se verifica la presencia de valores duplicados en el dataset integrado
    # num_duplicados = df_integrado.duplicated().sum()
    # print(f"\nNúmero de filas duplicadas en el dataset integrado: {num_duplicados}")

    # Resumen general del dataset integrado
    resumen = pd.DataFrame({
        'Atributo': df_integrado.columns,
        'Tipo de dato': df_integrado.dtypes,
        'Valores unicos': df_integrado.nunique(),
        'Valores nulos': df_integrado.isna().sum(),
        'Porcentaje nulos': df_integrado.isna().sum() / len(df_integrado) * 100
    })
    print(resumen)

    # -------------------------------------------------------------------
    # Exportación del dataset unificado a un archivo nuevo (en el
    # directorio de procesados)
    # -------------------------------------------------------------------
    df_integrado.to_csv('data/processed/datos_integrados.csv', index=False)

    # ############## (SECCION RETO/EXTRA PROPUESTO) ################
    # Generación y exportación del reporte
    profile_integrado = ProfileReport(
        df_integrado, title="Reporte de verificación - Integración de datos: Etapa de Procesado"
    )
    profile_integrado.to_file("docs/output/reporte_verificacion_integracion.html")

if __name__ == "__main__":
    process_data()