# Local evaluator

Build with `python evaluator/build_model_evaluator.py`; evaluate with `python evaluator/evaluate_model_patch.py --patch candidate.diff`. Requires Docker Linux engine and host Python3. Image contains exact clean Base and cached build dependencies/products. No Fix commit, gold patch, protected test patch or evaluation entrypoint is baked in.

At runtime the evaluator injects model patch, protected test patch and read-only helpers; runs with --network none; applies model first and rejects conflicts with protected tests; rebuilds current sources through standard Ant; compiles the C fixture and TestNG tests fresh; grades all 32 full test IDs. Missing/skipped tests cannot resolve. Model-induced build, test-compilation or JNI failures remain unresolved; missing tools and timeouts are infrastructure errors.

The unmodified conventional Ant tests target does not prepare the custom fixture. Always use the provided evaluator, which registers its absolute fixture path and current JNI path explicitly.

Published image: `yutu0814/javac-case-054-lwjgl3:benchmark-v1`; digest: `sha256:e3c1ac3197df69e047650a2806f0b923582058de8ca78b1c816657130f104bb4`. Use `docker pull yutu0814/javac-case-054-lwjgl3:benchmark-v1` before evaluation.
