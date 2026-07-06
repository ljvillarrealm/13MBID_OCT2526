# Se importan las librerías necesarias y se suprimen las advertencias
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder

from sklearn.dummy import DummyClassifier

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score

import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=UserWarning)


from pathlib import Path
import joblib
import json


from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import cross_validate


# #################### (EXTRA) #########################
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

# Implementacion de MLFlow
from datetime import datetime
import numpy as np


from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature


def load_data():

    # Lectura de los datos
    df = pd.read_csv('./data/processed/datos_integrados.csv')

    # Preprocesameinto de datos
    # Ajuste customizado de datos
    # Ajuste de dato: falta_pago debe convertirse explicitamente a binaria para que sea mas facil a los algoritmos hacer la clasificacion
    # Se convierte la variable objetivo a binaria: 1 = falta de pago (Y), 0 = sin falta (N)
    df["falta_pago"] = df["falta_pago"].map({"Y": 1, "N": 0})

    # Se divide el dataset en variables predictoras y variable objetivo
    target = "falta_pago"

    features_X = df.drop(columns=[target])
    labels_y = df[target]

    # Se genera el conjunto de entrenamiento, validación y test con estratificación
    # Primero separar test final (10%)
    X_temp, X_test, y_temp, y_test = train_test_split(
        features_X,
        labels_y,
        test_size=0.10,
        random_state=42,
        stratify=labels_y
    )
    # Luego separar train y validation (22% del 90% es aprox. el 20% del total)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp,
        y_temp,
        test_size=0.22,
        random_state=42,
        stratify=y_temp
    )


    return df, X_train, X_val, X_test, y_train, y_val, y_test, features_X, labels_y


def preprocess(features_X):

    # Se identifican las columnas numéricas y categóricas
    num_cols = features_X.select_dtypes(include=["int64","float64"]).columns.tolist()
    cat_cols = features_X.select_dtypes(include=["object","category"]).columns.tolist()

    # Se crea un pipeline para preprocesamiento de datos
    numeric_transformer = Pipeline([
        ("scaler", StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", numeric_transformer, num_cols),
        ("cat", categorical_transformer, cat_cols)
    ])

    return preprocessor


def train_model(
    data_path = "./data/processed/datos_integrados.csv",
    model_path = "./models/prod_model.pkl",
    preprocess_path = "./models/prod_processor.pkl",
    metrics_path = "./metrics/train_metrics.pkl"
):
    """"Se entrena el modelo objetivo"""
    
    # Implementacion de MLFlow
    mlflow.set_tracking_uri("sqlite:///mlflow.db") # La version mas reciente de MLFlow (3.14.0 actualemente) recomeinda migrar al uso de la base de datos.
    mlflow.set_experiment("Proyecto 13MBID - Entrenamiento de modelo PROD")

    # Cargar los datos
    df, X_train, X_val, X_test, y_train, y_val, y_test, features_X, labels_y = load_data()

    # Codificacion de la variablle objetivo
    if set(y_train.dropna().unique()) == {"N", "Y"}:
        y_train_eval = y_train.map({"N": 0, "Y": 1})
        y_val_eval = y_val.map({"N": 0, "Y": 1})
        y_test_eval = y_test.map({"N": 0, "Y": 1})
    else:
        y_train_eval = y_train.copy()
        y_val_eval = y_val.copy()
        y_test_eval = y_test.copy()

    # Preparacion del pipeline con el modelo
    model = HistGradientBoostingClassifier(
        random_state=42,
        class_weight="balanced"   # permite compensar de manera interna el desbalance en 1 (Y) vs 0 (N)
    )

    # Invocar preprocessor
    preprocessor = preprocess(features_X)

    # Levantar pipeline
    pipeline = ImbPipeline([
        ("prep", preprocessor),
        ("undersample", RandomUnderSampler(random_state=42)),
        ("model", model)
    ])

    # Entrenamiento del modelo
    ## Fase 1 de optimizacion de hiperparametros: RandomizedSearchCV
    param_distributions = {
        "model__max_iter": [100, 200, 300, 500],
        "model__max_depth": [None, 3, 5, 8, 12],
        "model__learning_rate": [0.01, 0.05, 0.1, 0.2],
        "model__max_leaf_nodes": [15, 31, 63, 127],
        "model__l2_regularization": [0.0, 0.1, 0.5, 1.0]
    }

    random_search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_distributions,
        n_iter=20,             # cantidad de combinaciones aleatorias a probar
        scoring="roc_auc",
        cv=5,
        random_state=42,
        n_jobs=-1
    )

    random_search.fit(X_train, y_train)
    print("Mejores parámetros (fase 1):", random_search.best_params_)

    ## Fase 2 de optimizacion de hiperparametros: RandomizedSearchCV
    best = random_search.best_params_

    param_grid = {
        "model__max_iter": [best["model__max_iter"]],
        "model__max_depth": [best["model__max_depth"]],
        "model__learning_rate": [best["model__learning_rate"] * 0.5,
                                best["model__learning_rate"],
                                best["model__learning_rate"] * 1.5],
        "model__max_leaf_nodes": [max(best["model__max_leaf_nodes"] - 16, 2),
                                    best["model__max_leaf_nodes"],
                                    best["model__max_leaf_nodes"] + 16],
        "model__l2_regularization": [best["model__l2_regularization"]]
    }

    grid_search = GridSearchCV(
        pipeline,
        param_grid=param_grid,
        scoring="roc_auc",
        cv=5,
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)
    print("Mejores parámetros (fase 2):", grid_search.best_params_)

    ##pipeline.fit(X_train, y_train)  # entrenamiento simple de antes
    pipeline = grid_search.best_estimator_

    # Evaluacion del modelo
    y_test_pred = pipeline.predict(X_test)
    y_test_score = (
        pipeline.predict_proba(X_test)[:, 1]
        if hasattr(pipeline, "predict_proba")
        else pipeline.decision_function(X_test)
    )

    # Metricas
    metrics = {
        "test_accuracy": accuracy_score(y_test_eval, y_test_pred),
        "test_precision": precision_score(y_test_eval, y_test_pred, zero_division=0),
        "test_recall": recall_score(y_test_eval, y_test_pred, zero_division=0),
        "test_f1": f1_score(y_test_eval, y_test_pred, zero_division=0),
        "test_roc_auc": roc_auc_score(y_test_eval, y_test_score)
    }

    for i, j in metrics.items():
        print(f"{i}: {j:.4f}")

    # Se genera una matriz de confusión para el conjunto de test
    cm = confusion_matrix(y_test, y_test_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot(cmap="Blues")
    cm_path = "./docs/training_output/confusion_matrix.png"
    Path(cm_path).parent.mkdir(parents=True, exist_ok=True)
    plt.title("Matriz de Confusión - OPTIM")
    plt.savefig(cm_path, bbox_inches="tight")
    plt.close()

    # Registro en MLFlow
    signature = infer_signature(X_train, pipeline.predict(X_train))

    with mlflow.start_run(run_name="Pipeline (prod)- HistGradientBoostingClassifier"):
        mlflow.log_params(model.get_params())
        mlflow.log_params({
            "train_samples":    len(X_train),
            "validation_samples": len(X_val),
            "test_samples":     len(X_test),
            "balancing_method": "undersampling",
        })
        mlflow.log_metrics(metrics)
        mlflow.log_artifact(cm_path)
        mlflow.sklearn.log_model(
            pipeline,
            name="model",
            signature=signature,
            skops_trusted_types=[ # De esta maner se evita el error: MlflowException: The saved sklearn model references untrusted types. If you are sure loading these types is safe, set the 'skops_trusted_types' parameter when calling 'log_model' or 'save_model' to the list of trusted types.
                "imblearn.pipeline.Pipeline",
                "imblearn.under_sampling._prototype_selection._random_under_sampler.RandomUnderSampler"
            ]
        )

        run_id = mlflow.active_run().info.run_id
        print(f"Modelo registrado en MLflow. run_id: {run_id}")

    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    Path(preprocess_path).parent.mkdir(parents=True, exist_ok=True)
    Path(metrics_path).parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(pipeline, model_path)
    joblib.dump(pipeline.named_steps["prep"], model_path)

    # Guardar métricas
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)

    return pipeline, pipeline.named_steps["prep"], metrics

if __name__ == "__main__":
    train_model()


### EXTRA
## Se ha elegido el modelo con mejor scorering por ROC_AUC
## Se ha implementado la optimizacion de hiperparametros en 2 fases:
#   1) RandomizedSearchCV
#   2) GridSearchCV