# Case 062 — LWJGL clang_getCString (#496)

This is an **N_test_data** case: the original fix commit did not add a regression test; the protected Java test and its C input were derived from the issue. The source commits are pinned to `2c8811383487cd827f375abdc534a5d40a174edc` (Base) and `50869cf9638ef2225a5ca141bf89d617a920a762` (Fix). The full upstream diff is `patches/gold_patch.diff`.

The release comparison logs in `verification/release_comparison/` show LWJGL 3.2.2 returning an incorrect string and 3.2.3 returning the expected string on Linux amd64/Java 11. A separate clean-source evaluation of the exact Base/Fix pair confirms the same failure and repair: Base has F2P `FAILED`, P2P `PASSED`; the complete official Fix has both `PASSED`. Candidate precreation of the protected test is rejected.

The model-facing task is `official_swebench/public_task_062.json`. Keep `instance_062.json`, `patches/`, and the expected F2P/P2P outcomes out of the model prompt during a blind repair evaluation. The fixed source was visible during test construction, so no independent or blinded test-design claim is made.

Clone the published dataset and pull the immutable Base image:

```powershell
git clone https://github.com/Alex-cpu0814/javac-swebench.git
Set-Location .\javac-swebench\N_test_data\javac_case_062
docker pull yutu0814/javac-case-062-lwjgl3@sha256:a6b182c03068ba6e408878304674f3a8ae922f42b6399c3f1b82fd34166a40a5
```

Run Base and gold controls:

```powershell
python .\evaluator\evaluate_model_patch.py --patch .\verification\controls\base_control.patch --label base-1
python .\evaluator\evaluate_model_patch.py --patch .\patches\gold_patch.diff --label gold-1
```

The Base control is an empty valid patch in `verification/controls/base_control.patch`; F2P fails and P2P passes. Gold passes both. `verification/runs/<run-id>/` contains `summary.json`, `grading.json`, `events.jsonl`, raw build and test logs. Exit code `0` means resolved and `1` means unresolved; the expected Base result therefore exits `1`.

Evaluate a candidate patch with `python .\evaluator\evaluate_model_patch.py --patch C:\path\candidate.diff`. The evaluator defaults to the published digest and runs with no container network. Docker must be in Linux-container mode on `linux/amd64`; host Python 3.10+ and Git are required. The host does not need Java, Ant, GCC or Clang.

To rebuild the image from the pinned Base source instead of pulling it, prepare the declared 2019 Kotlin/Maven dependencies and run the image builder from this case directory:

```powershell
python .\evaluator\prepare_dependencies.py
python .\evaluator\build_model_evaluator.py
```

The image uses the project's Kotlin 1.3.50 compiler and Maven dependencies, plus dyncall source from LWJGL-CI commit `42de4c57115e34e8734c5b0c0e2cbe03244ab7b6` (2018 upstream rev. 291). The pinned dyncall archive is included; Kotlin/Maven artifacts are fetched once to `_work/lwjgl3-2019-deps` and verified by SHA-256. Ubuntu's libffi PIC archive and libclang 14 are explicit Linux build/runtime adaptations. Each evaluation runs with no container network and cold-builds the generator, Core/LLVM Java and current JNI from candidate source. The image contains no Base project binary, Fix object, gold patch, or protected test.

Published case: [GitHub](https://github.com/Alex-cpu0814/javac-swebench/tree/main/N_test_data/javac_case_062). Published image: [Docker Hub](https://hub.docker.com/r/yutu0814/javac-case-062-lwjgl3). `verification/publication/registry_audit.json` records anonymous manifest access, digest pull, and the clean-Base audit.
