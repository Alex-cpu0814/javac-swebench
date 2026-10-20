# Verification

`builds/case-068-build-final/summary.json` records a successful clean Base image audit. The image ID is `sha256:30a5258e746b1190c9b5d6c6aacbbaa04bdd0f11f4aff0b5605a3eeb8445dfaa`.

`runs/case-068-base-final/`: null-game-pose F2P failed with NPE and zero stub calls; non-null P2P passed with one native call.

`runs/case-068-gold-final/`: both tests passed; null-game-pose call reached the stub with address `0` and count `0`.

`runs/case-068-tamper-final/`: the candidate attempted to add the protected Java test path and was rejected during test-patch injection with `candidate_conflicts_with_test_patch`.

`source_overlay_comparison/` preserves the earlier Docker reproduction using exact generated Java files from Base and Fix compiled against the matching 3.2.0/3.2.1 release dependencies. Formal evaluator results above are the grading evidence.

`publication/registry_audit.json` records the published image digest, successful anonymous registry access, digest pull, and clean Base audit of the pulled image.

The original issue was observed on Windows with a real SteamVR application. The local tests cover the Java/native argument boundary on Linux using a stub; they make no claim about the real compositor or hardware.
