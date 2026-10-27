# Verification evidence

`final_summary.json` identifies six release runs (`*-170-published-v1`) and their summary/patch/evaluator/image hashes. `builds/build-170-published` holds the Base-only image build and audit; `runs/` holds runtime evidence. `discovery/` preserves construction logs; `base-junit-discovery-v4` is final discovery.

| Control | Verified result |
|---|---|
| Base plus unrelated marker | 2 target failures, all 41 preservation tests pass |
| Complete official Gold | All 43 pass |
| Equivalent attempt-count-based fallback repair | All 43 pass; no exact-patch matching |
| Gold plus native large-port regression | Targets and mount controls pass; upstream testLargePort fails |
| Candidate precreates protected probe | Rejected at test patch application |
| Gold plus original upstream test modification | Rejected by build's fingerprint guard |

Base and Gold share the audited image and protected assets. Actual noexec logs show `failed to map segment from shared object` without `perm`; failed initialization may additionally cause a secondary missing-native-method error. Normal loading works in both versions, distinguishing this from incompatible JNI dependencies. Gold maps from home/cwd as appropriate and performs three native bidirectional round trips per success. Both versions reject all-blocked loading.

Preliminary v1 runs had four classes/31 original tests; the large-port mutation was ineffective because that path lacked coverage. The original domain SocketAddressTest was added; final v2 runs have all 39 methods in five classes. Preliminary results are retained and excluded from final validation.

Recheck: `python analysis/verify_controls.py --docker <docker-executable>`. `official_swebench/SHA256SUMS.txt` protects release evidence. Linux noexec behavior is verified; complete SELinux/RHEL deployment, full Maven packaging and candidate C-source compilation are outside scope.

The release verification uses six `*-170-published-v1` runs against the immutable Docker Hub image. Earlier v2 runs are retained as prepublication evidence; `final_summary.json` points to the release runs.

Docker Hub publication is recorded in `docker_publication.json`, including the immutable reference and anonymous registry status. The release configuration and all six protection controls use the published image. The release run names are listed in `final_summary.json`; earlier local runs are historical.
