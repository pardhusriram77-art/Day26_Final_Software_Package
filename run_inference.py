"""Command-line example for the frozen pH model."""
import argparse
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from inference import predict_csv

parser = argparse.ArgumentParser(description="Predict next-row pH using the frozen pipeline.")
parser.add_argument("input_csv", help="CSV with a required 'ph' column")
parser.add_argument("output_csv", help="Destination CSV for predictions")
args = parser.parse_args()
Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
result = predict_csv(args.input_csv, args.output_csv)
print(result.to_string(index=False))
print(f"Saved predictions to: {args.output_csv}")
