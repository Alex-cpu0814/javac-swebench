# Isolated compilation evaluator

Pull `yutu0814/javac-case-053-lwjgl3:benchmark-v1` and evaluate with `python evaluate_model_patch.py --patch candidate.diff`. Maintainers may rebuild with `python build_model_evaluator.py`. One clean Base image contains the historical repository and Clang/JDK/Python tools, without Fix history, patches, grading data or test entrypoints. Patches and adapter are injected at runtime.

The protected test prints structured compilation JSON. The grader maps its four actual test statuses to PASSED/FAILED, treats missing nodes as unresolved, and separates infrastructure failures. Exit codes: 0 resolved, 1 unresolved, 2 infrastructure error. The host --timeout also stops a hung container. The compilation oracle covers a generated JNI C object and selected controls, not a full Ant/TestNG suite.
