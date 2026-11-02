# Day 26 — Final Software Package
## AI-Based Underwater Environmental Analytics

This repository packages the frozen pH-only Linear Regression pipeline, preprocessing/inference interface, example input/output, final validation evidence, report and presentation drafts.

> **Scope warning:** The source water-potability dataset is static. Timestamps were synthetically generated for pipeline experiments. The target is the next row's pH, not a verified future underwater sensor measurement. This is an academic prototype, **not validated for operational underwater deployment**.

## Selected method
- Model: Linear Regression
- Input: current-row `ph`
- Target: next-row pH (`ph.shift(-1)`)
- Preprocessing: parse timestamps, drop invalid timestamps, stable ascending sort, median imputation inside saved pipeline
- No scaling
- Frozen model: `models/Day22_Final_Linear_Regression_Pipeline.joblib`

The model was retained as the simplest candidate with the lowest reported validation RMSE. Its test advantage over the constant-mean baseline is extremely small.

## Repository layout
```text
data/       example_input.csv, water_potability_temporal_synthetic.csv
models/     frozen Linear Regression pipeline, constant-mean baseline
src/        inference.py, run_inference.py
outputs/    example_predictions.csv
reports/    result summary, report draft, presentation draft, figures
README.md   setup and usage
requirements.txt
```

## Setup
Recommended environment matches recorded experiments: Python 3.13.5.
```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\\Scripts\\activate      # Windows
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run example inference
From repository root:
```bash
python src/run_inference.py data/example_input.csv outputs/my_predictions.csv
```
Input CSV must contain a numeric `ph` column. Missing `ph` values are median-imputed by the saved pipeline. Output retains input columns and adds `predicted_next_ph`.

Python API:
```python
from src.inference import load_model, predict_next_ph
model = load_model()
print(predict_next_ph([7.1, 8.2, 6.4], model=model))
```

## Evaluation
Chronological split without shuffle: 1,939 train / 416 validation / 416 held-out test rows. Test set was not used for selection or tuning.

| Method | Test MAE | Test RMSE |
|---|---:|---:|
| pH-only Linear Regression | 1.481534 | 1.900469 |
| Constant-mean baseline | 1.481718 | 1.901536 |

Linear Regression had lower absolute error on 221/416 rows (53.125%). The aggregate gain is marginal and should not be interpreted as strong predictive evidence.

## Performance
Recorded on the Day 23 execution environment:
- Linear Regression model artifact: 1,227 bytes (~1.20 KB)
- 416-row batch inference median: 1.086 ms; p95: 2.952 ms
- Constant-mean baseline: 655 bytes; median 0.034 ms
Timings are machine-dependent.

## Error analysis
Day 25 inspected all 416 held-out rows. Maximum absolute error was 7.0694. The model coefficient for current pH is approximately 0.010011, so predictions remain close to a near-constant value. See `reports/figures/` and the detailed Day 25 report included in `reports/`.

## Limitations
1. Static source data with synthetic timestamps.
2. Next-row pH is a pseudo-temporal target, not a genuine future sensor reading.
3. Single-feature model ignores multivariate interactions.
4. No dissolved oxygen or pressure fields.
5. No labelled anomaly ground truth.
6. Residuals do not prove sensor faults or physical causes.
7. Not validated for operational underwater deployment.

## Security
Only load the supplied `.joblib` artifacts from a trusted source. Joblib/pickle files can execute code if maliciously crafted.

## Status
Final software package, README, and report/PPT drafts are prepared. Mentor approval, real time-stamped sensor data, and deployment validation remain pending.
