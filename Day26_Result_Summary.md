# Final result summary

| Method | Test MAE | Test RMSE |
|---|---:|---:|
| pH-only Linear Regression | 1.481534 | 1.900469 |
| Constant-mean baseline | 1.481718 | 1.901536 |

- Test rows: 416
- Linear Regression better absolute error rows: 221/416 (53.125%)
- Linear Regression artifact: 1,227 bytes (~1.20 KB)
- Median batch inference (416 rows): 1.086 ms; p95: 2.952 ms
- Maximum absolute test error: 7.0694

The model is retained as a simple reproducible prototype. Its aggregate performance is nearly tied with the constant baseline. Timestamps are synthetic and the target is next-row pH; this is not real underwater temporal validation.
