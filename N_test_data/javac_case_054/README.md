# Case 054: LWJGL Vulkan debug naming

Human-approved Linux x86_64/JDK17 runtime adaptation of Issue #755. Protected public Java API tests use a freshly compiled controlled native provider: naming VkInstance and VkPhysicalDevice fails on Base and succeeds on official Fix; device naming remains a passing control.

2 F2P; 30 P2P (29 existing core tests + 1 new device-naming control). Initial and fresh network-none validation each repeated twice per revision. No skip/xfail or infrastructure failure.

Current JNI and Vulkan sources are built by standard Ant. Ubuntu libffi-dev 3.4.2-4 PIC archive is an explicit offline dependency adaptation. Base source version is 3.3.2; Issue reported 3.3.1. This does not reproduce the Windows driver crash, use a real GPU, or establish complete Vulkan/libffi compatibility.

See analysis/human_approval.json, analysis/review.json, and verification/ for scope and evidence. The published evaluator image is `yutu0814/javac-case-054-lwjgl3:benchmark-v1`; digest: `sha256:e3c1ac3197df69e047650a2806f0b923582058de8ca78b1c816657130f104bb4`.

```powershell
python evaluator/build_model_evaluator.py
python evaluator/evaluate_model_patch.py --patch C:\path\candidate.diff
```

Only official_swebench/public_task_054.json is model task input. Gold/test patches, private records and verification materials are grading assets.

Formal evaluator verified: Base unresolved (2 F2P failed, all 30 P2P passed); official Fix resolved (32/32 passed); pre-created protected test rejected with candidate_conflicts_with_test_patch. Clean image audit and target layout/checksums passed.
