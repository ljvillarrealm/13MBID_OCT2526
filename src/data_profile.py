"""
Máster en Big Data y Data Science
Metodologías de gestión y diseño de proyectos de big data

Sesión Práctica 01 - Reporte de verificación de datos con ydata-profiling

Genera reportes HTML de perfilado (profiling) de los datasets de créditos
y de otros productos (tarjetas), para su uso como salida dentro del
pipeline de DVC.

Generado con apoyo de IA: Claude Sonnet 5.0
Revisado y adaptado por: Leonardo Villarreal
"""

import pandas as pd
from ydata_profiling import ProfileReport


def main():
    # Lectura de los conjuntos de datos.
    # Rutas relativas a la raíz del proyecto (ejecución vía "dvc repro").
    df_creditos = pd.read_csv("data/raw/datos_creditos.csv", sep=";")
    df_tarjetas = pd.read_csv("data/raw/datos_tarjetas.csv", sep=";")

    # Generación y exportación del reporte - Créditos.
    profile_creditos = ProfileReport(
        df_creditos, title="Reporte de verificación - Créditos"
    )
    profile_creditos.to_file("docs/output/reporte_verificacion_creditos.html")

    # Generación y exportación del reporte - Otros productos (tarjetas).
    profile_tarjetas = ProfileReport(
        df_tarjetas, title="Reporte de verificación - Tarjetas"
    )
    profile_tarjetas.to_file("docs/output/reporte_verificacion_tarjetas.html")


if __name__ == "__main__":
    main()