# Verification

Generation evidence contains sanitized repeated Base/Fix and fresh network-none results. builds/ and runs/ contain the successful formal image audit and evaluator checks. Controls verified: noop.patch leaves exactly the two target failures while all 30 P2P pass; the official Fix passes all 32 tests; test_tamper.patch is rejected with candidate_conflicts_with_test_patch before execution. Official Fix is an execution-only reference. Neither real Vulkan hardware nor original Windows crash behavior is claimed.

final_summary.json records the local completed case. layout_validation.json covers the target case only. Docker Hub image and GitHub case publication are complete; publication.json records the registry digest and verified default-tag run.
