"""Inference helpers for the frozen pH-only next-row pH model."""
from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "Day22_Final_Linear_Regression_Pipeline.joblib"


def load_model(model_path=MODEL_PATH):
    """Load the frozen scikit-learn pipeline."""
    return joblib.load(model_path)


def predict_next_ph(ph_values, model=None):
    """Predict next-row pH from current-row pH values; None is median-imputed."""
    if model is None:
        model = load_model()
    frame = pd.DataFrame({"ph": ph_values})
    return model.predict(frame[["ph"]])


def predict_csv(input_csv, output_csv, model=None):
    """Read a CSV containing a 'ph' column and write predictions."""
    frame = pd.read_csv(input_csv)
    if "ph" not in frame.columns:
        raise ValueError("Input CSV must contain a column named 'ph'.")
    if model is None:
        model = load_model()
    result = frame.copy()
    result["predicted_next_ph"] = predict_next_ph(result["ph"], model=model)
    result.to_csv(output_csv, index=False)
    return result
