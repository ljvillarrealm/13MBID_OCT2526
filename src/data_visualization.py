"""
Máster en Big Data y Data Science
Metodologías de gestión y diseño de proyectos de big data

AP1 - Visualización de los datos

Script ejecutable generado a partir de la libreta 'CD01_Visualizacion.ipynb'.
Realiza una visualización básica de los datos del escenario y guarda todas
las imágenes (gráficas) generadas en la carpeta de salida indicada.

Uso:
    python CD01_Visualizacion.py

Los datos se leen desde ../data/raw/ (rutas relativas al script, igual que
en la libreta original). Las imágenes se guardan en la carpeta 'output/'
(se puede cambiar modificando la variable OUTPUT_DIR).

Generado con apoyo de IA: Claude Sonnet 5.0
Revisado y adaptado por: Leonardo Villarreal
"""

import os
import warnings
from datetime import datetime
 
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sin interfaz gráfica, ideal para scripts/servidores
import matplotlib.pyplot as plt
import seaborn as sns
 
# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------
sns.set(style="whitegrid", palette="muted")
plt.rcParams["figure.figsize"] = (8, 5)
 
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)
 
# Carpeta donde se guardarán las imágenes generadas: docs/output_<fecha>_<hora>
# Ruta relativa al script: ../docs/output_YYYYMMDD_HHMMSS
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#OUTPUT_DIR = os.path.join(BASE_DIR, "..", "docs", f"output_{TIMESTAMP}")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "docs", f"output")
OUTPUT_DIR = os.path.normpath(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)
 
 
def guardar_figura(nombre_archivo):
    """Guarda la figura actual de matplotlib en OUTPUT_DIR y la cierra."""
    ruta = os.path.join(OUTPUT_DIR, nombre_archivo)
    plt.savefig(ruta, bbox_inches="tight", dpi=150)
    plt.close()
    print(f"Imagen guardada en: {ruta}")
 
 
def main():
    # -----------------------------------------------------------------------
    # Lectura de los datos desde el directorio data/raw
    # -----------------------------------------------------------------------
 
    # Lectura de los datos de créditos
    df_creditos = pd.read_csv("data/raw/datos_creditos.csv", sep=";")
    print(df_creditos.head(5))
 
    # Lectura de los datos de tarjetas
    df_tarjetas = pd.read_csv("data/raw/datos_tarjetas.csv", sep=";")
    print(df_tarjetas.head(5))
 
    # -----------------------------------------------------------------------
    # Visualización de algunas propiedades del dataset
    # -----------------------------------------------------------------------
 
    # Dimensiones del dataset
    print("Dimensiones del dataset de creditos:")
    print(f"El dataset tiene {df_creditos.shape[0]} filas y {df_creditos.shape[1]} columnas.")
    print("\nDimensiones del dataset de tarjetas:")
    print(f"El dataset tiene {df_tarjetas.shape[0]} filas y {df_tarjetas.shape[1]} columnas.")
 
    # Descripción estadística de las columnas numéricas de cada DataFrame
    print("\nDescripción general del dataset de créditos:")
    print(df_creditos.describe())
    print("\nDescripción general del dataset de tarjetas:")
    print(df_tarjetas.describe())
 
    # Descripción estadística de las columnas categóricas del DataFrame
    print("\nDescripción de las columnas categóricas del dataset de créditos:")
    print(df_creditos.describe(include="object"))
    print("\nDescripción de las columnas categóricas del dataset de tarjetas:")
    print(df_tarjetas.describe(include="object"))
 
    # Información del DataFrame de créditos
    print("\nInformación del dataset de créditos:")
    df_creditos.info()
 
    # Información del DataFrame de tarjetas
    print("\nInformación del dataset de tarjetas:")
    df_tarjetas.info()
 
    # -----------------------------------------------------------------------
    # Distribución de la variable objetivo
    # -----------------------------------------------------------------------
    sns.countplot(x="falta_pago", data=df_creditos)
    plt.title("Distribución de la variable objetivo (mora)")
    plt.xlabel("¿Presentó mora el cliente?")
    plt.ylabel("Cantidad de clientes")
    guardar_figura("01_distribucion_variable_objetivo.png")
 
    print(df_creditos["falta_pago"].value_counts(normalize=True).mul(100).round(2))
 
    # -----------------------------------------------------------------------
    # Distribución de variables categóricas - créditos
    # -----------------------------------------------------------------------
    categorical_cols = df_creditos.select_dtypes(include=["object"]).columns.drop("falta_pago")
 
    print("\nDistribución de las variables categóricas del dataset de créditos:")
 
    for col in categorical_cols:
        plt.figure(figsize=(8, 4))
        order = df_creditos[col].value_counts().index
        sns.countplot(y=col, data=df_creditos, order=order)
        plt.title(f"Distribución de {col}")
        plt.xlabel("Cantidad")
        plt.ylabel(col)
        guardar_figura(f"02_creditos_distribucion_{col}.png")
 
    # -----------------------------------------------------------------------
    # Distribución de variables categóricas - tarjetas
    # -----------------------------------------------------------------------
    categorical_cols_tarjetas = df_tarjetas.select_dtypes(include=["object"])
 
    print("\nDistribución de las variables categóricas del dataset de tarjetas:")
 
    for col in categorical_cols_tarjetas:
        plt.figure(figsize=(8, 4))
        order = df_tarjetas[col].value_counts().index
        sns.countplot(y=col, data=df_tarjetas, order=order)
        plt.title(f"Distribución de {col}")
        plt.xlabel("Cantidad")
        plt.ylabel(col)
        guardar_figura(f"03_tarjetas_distribucion_{col}.png")
 
    # -----------------------------------------------------------------------
    # Correlación entre variables numéricas - créditos
    # -----------------------------------------------------------------------
    num_df = df_creditos.select_dtypes(include=["float64", "int64"])
    corr = num_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de correlaciones - Créditos")
    guardar_figura("04_correlaciones_creditos.png")
 
    # -----------------------------------------------------------------------
    # Correlación entre variables numéricas - tarjetas
    # -----------------------------------------------------------------------
    num_df = df_tarjetas.select_dtypes(include=["float64", "int64"])
    corr = num_df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Matriz de correlaciones - Tarjetas")
    guardar_figura("05_correlaciones_tarjetas.png")
 
    # -----------------------------------------------------------------------
    # Listado de columnas de cada dataset
    # -----------------------------------------------------------------------
    def reporte_descripcion_dataset(df):
        columnas = df.columns
        print("Columnas del dataset:\n")
        for col in columnas:
            print(col)
 
    print("Descripción del dataset 'datos_creditos'")
    reporte_descripcion_dataset(df_creditos)
 
    print("Descripción del dataset 'datos_tarjetas'")
    reporte_descripcion_dataset(df_tarjetas)
 
    print(f"\nProceso finalizado. Todas las imágenes se guardaron en: {OUTPUT_DIR}")
 
 
if __name__ == "__main__":
    main()
