# Java-C SWE-bench Case 097 — JEP #22

Renumbered from case 096. The stable problem identity remains `ninia__jep-22`; issue number 22 and the upstream commits have not changed. Original issue: [ninia/jep#22](https://github.com/ninia/jep/issues/22).

A creator thread constructs a Jep interpreter and terminates. Another thread closes it. Base can use the terminated creator's JNIEnv and crash the JVM; the reference fix passes the current JNI environment into native close. The original report is Linux/amd64. This case reproduces that specific stale-environment defect on Linux, Java 8 and Python 3.4.10. The upstream warning that arbitrary cross-thread interpreter access remains unsafe is retained.

- Base: `e4f13ea277ce4809688dde766cc9fd173ec6f63d`.
- Fix: `767509de81f3a11b1ca54e23619d3226944a141e`.
- `gold_patch.diff` is the complete six-file upstream diff, including the generated Javadoc change.
- The model-facing input is only `official_swebench/public_task_097.json`.

## Protected tests and verification

There are 81 formal tests: one synthetic FAIL_TO_PASS, 78 existing upstream PASS_TO_PASS, and two added lifecycle PASS_TO_PASS tests. The target child JVM checks three terminated-creator closes and requires each CLOSE_STEP marker plus CLOSE_OK. Each child has a 60-second timeout and creator join has a 15-second timeout. Missing/duplicate completion markers fail even when the child exits zero. Child stdout/stderr and JVM crash reports are saved in the run directory.

The added lifecycle controls check same-thread close, use after close, repeated close, and successful interpreter reuse. A Python object's destructor writes a marker through captured os.write/os.close functions and an already-open descriptor, which remain usable during interpreter shutdown. Observing the marker checks native Python teardown side effects; memory consumption is not measured. Both an empty Java close and a close that only sets Java flags fail this observation.

Final controls: Base fails only the target regression and passes all 80 P2P; the exact upstream fix passes all 81. Both overbroad closes fail the target plus the two added lifecycle controls, while the original 78 tests pass. Candidate-supplied protected tests are rejected. Five process-helper checks cover successful completion, missing/duplicate markers, nonzero exit diagnostics, and timeout cleanup. Evidence is linked from `verification/local_evidence.json`.

## Docker and evaluation

The published environment is `yutu0814/javac-case-097-jep:benchmark-v3`, pinned in configuration to:

```text
yutu0814/javac-case-097-jep@sha256:8377bd71afd8d7673a7effb4473bbf204e57a1cad7c41fcc54caa11d3c7c1657
```

This is the same verified Base environment formerly published under 096, retagged under 097. The image audit confirms Base, a clean tree, no Fix object, no injected tests and no compiled project artifacts. Candidate code and protected tests are injected at runtime; Java and native sources are rebuilt with the original setup.py. The new repository was checked anonymously and the digest-pulled image passes all 81 tests with the reference fix.

From the repository root in PowerShell:

```powershell
python .\N_test_data\javac_case_097\evaluator\evaluate_model_patch.py --patch .\N_test_data\javac_case_097\patches\gold_patch.diff --run-id my-097-gold
python .\N_test_data\javac_case_097\analysis\verify_case.py
```

Use a fresh run ID. Exit codes are 0 resolved, 1 unresolved, 2 infrastructure failure. To repeat the full controls, use `analysis/verify_controls.py --suffix <fresh-name>`.

## Migration and provenance

Active directory, record filenames, configuration, root index and Docker repository use 097. Existing raw 096 logs keep their original identifiers as historical evidence. New runs use 097. The legacy 096 local archive and Docker repository have been removed; evaluation resolves the immutable 097 image. Test construction used the reference fix; no blinded test-generation claim is made. Official instance records and patch/verification directories contain grading material and should not be supplied to models in a blind repair task.
