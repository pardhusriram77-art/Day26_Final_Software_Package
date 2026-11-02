# Day 25 — Detailed Error / Failure Analysis

## Scope and protocol
This analysis inspects the same 416-row held-out chronological test set used on Day 23. The Day 22 frozen pH-only Linear Regression pipeline is not retrained or modified. The exact source CSV and saved test predictions are used to reconstruct the test rows.

## Overall held-out performance
- Test rows: 416
- MAE: **1.4815**
- RMSE: **1.9005**
- Mean residual (actual − predicted): **0.0373**
- Median absolute error: **1.2234**
- Maximum absolute error: **7.0694**
- Underpredictions: 205
- Overpredictions: 211

Positive residual means actual next-row pH was higher than predicted (underprediction). Negative residual means prediction was higher than actual (overprediction).

## Five largest individual errors
1. timestamp=2024-05-11 07:00:00; current pH=nan; actual next pH=0.0000; predicted=7.0694; absolute error=7.0694; direction=overprediction
2. timestamp=2024-05-04 23:00:00; current pH=7.1252; actual next pH=13.5412; predicted=7.0703; absolute error=6.4710; direction=underprediction
3. timestamp=2024-05-06 03:00:00; current pH=9.3961; actual next pH=13.3499; predicted=7.0930; absolute error=6.2569; direction=underprediction
4. timestamp=2024-05-07 12:00:00; current pH=8.2888; actual next pH=0.9756; predicted=7.0819; absolute error=6.1063; direction=overprediction
5. timestamp=2024-05-06 07:00:00; current pH=nan; actual next pH=1.4318; predicted=7.0694; absolute error=5.6377; direction=overprediction

See `Day25_Worst_20_Predictions.csv` for the top 20 and `Day25_All_Test_Predictions_With_Error_Analysis.csv` for all test rows.

## Error organisation by pH range
Groups are descriptive pH bins, not safety or regulatory thresholds.

- <6.5: n=149, MAE=1.9008, RMSE=2.2033, bias=-1.9008
- 6.5–7.0: n=57, MAE=0.2977, RMSE=0.3314, bias=-0.2977
- 7.0–7.5: n=40, MAE=0.2019, RMSE=0.2343, bias=0.1911
- 7.5–8.0: n=40, MAE=0.7005, RMSE=0.7148, bias=0.7005
- >8.0: n=130, MAE=2.1541, RMSE=2.4023, bias=2.1541

See `Day25_Error_by_Actual_pH_Range.csv` and `Day25_Error_by_Current_pH_Range.csv` for complete grouped statistics.

## Error magnitude and direction
Error bands are descriptive absolute-error intervals: <=0.5, 0.5–1.0, 1.0–2.0, 2.0–3.0, and >3.0. See `Day25_Error_Band_Distribution.csv` and `Day25_Error_Direction_Summary.csv`.

## Model explanation
The model has one predictor: current-row pH. Its fitted coefficient is **0.010011**, intercept **6.998942**, and median-imputation statistic **7.041665**. A one-unit increase in current pH changes the predicted next-row pH by the coefficient amount within this fitted linear relationship. There is no multi-feature importance ranking to provide because the model has only one feature.

## Baseline context
The constant-mean baseline has been compared row-by-row. Linear Regression has lower absolute error on 221 of 416 test rows (53.12%). The aggregate advantage is very small; the model should not be described as substantially better.

## Visual inspection
- `Day25_Actual_vs_Predicted.png`: prediction agreement and deviations from the ideal diagonal.
- `Day25_Residual_Distribution.png`: residual spread and skew.
- `Day25_Residuals_vs_Predicted.png`: possible systematic patterns.
- `Day25_Error_by_pH_Range.png`: descriptive MAE by actual pH range.

## Limitations and likely failure conditions
1. **Synthetic chronology:** timestamps were generated for pipeline testing; the original dataset is static. The next-row target is not a genuine future sensor reading.
2. **Single-feature model:** current pH alone cannot capture interactions involving hardness, solids, chloramines, sulfate, conductivity, organic carbon, trihalomethanes, or turbidity.
3. **Abrupt changes:** a linear mapping from current pH to next-row pH may miss sudden transitions or irregular jumps.
4. **Out-of-range inputs:** the fitted linear relationship may extrapolate poorly beyond the pH values represented in training.
5. **Missing input values:** median imputation gives a valid numeric input but hides the fact that the sensor value was missing; missingness itself is not modelled.
6. **No sensor context:** there are no dissolved-oxygen or pressure fields in the source dataset.
7. **No anomaly labels:** error cases cannot be called true anomalies or false alarms; there is no labelled anomaly ground truth.
8. **No causal diagnosis:** a large residual indicates prediction failure, not why it happened or whether it reflects a physical water event.

## Recommended final reporting
Report the largest individual errors, error direction and magnitude, grouped pH-range statistics, residual plots, coefficient interpretation, and the limitations above. Avoid causal claims about error groups without real sensor metadata and verified observations.
