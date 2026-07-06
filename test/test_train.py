from src.train_model import train_model
import json
from pathlib import Path
import pytest

def test_train_model(tmp_path):
    # Raiz del projecto


    
    project_root = Path(__file__).resolve().parents[1]

    baseline_path = project_root / "metrics" / "train_metrics.json"
    if not baseline_path.exists():
        pytest.skip("Baseline metyrics file not found . Run train_model.py to generate it.")

    with open(baseline_path, "r") as f:
        baseline = json.load(f)

    # Ejecutar entrenamioenot 
    data_path = project_root / "data" / "processed" / "datos_integrados.csv"
    model_output_path = tmp_path / "prod_model.pkl"
    preprocessor_output = tmp_path / "prod_preprocessor.pkl"
    metrics_output_path = tmp_path / "train_metrics.json"

    # Ejecutar entrenamiento
    _, _, metrics = train_model(
        data_path=str(data_path),
        model_path=str(model_output_path),
        preprocess_path=str(preprocessor_output),
        metrics_path=str(metrics_output_path)
    )

    # Ejecutar test
    assert set(metrics.keys()) == set(baseline.keys()), "Las metricas egenradas no coinciden con las metricas de referencia."

    mtol = 1e-9
    for k in baseline.keys():
        assert metrics[k] == pytest.approx(baseline[k], rel=0, abs=mtol), (
            f"La metrica {k} cambio: baseline={baseline[k]} nueva={metrics[k]}"
        )

if __name__ == "__main__":
    test_train_model()