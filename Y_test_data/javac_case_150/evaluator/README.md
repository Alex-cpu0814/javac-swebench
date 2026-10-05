# Case 150 evaluator

Build `image/Dockerfile`, then inject a candidate patch, the protected test
patch, `run_evaluation.sh`, `case_adapter.sh`, and `report_surefire.py` at
runtime. The image contains only the Base checkout and cached public build
dependencies; it contains neither the fix commit nor evaluation patches.
