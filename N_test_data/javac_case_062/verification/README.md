# Verification

`release_comparison/` contains the verified LWJGL 3.2.2/3.2.3 release logs. `builds/case-062-build-final-default/` contains the clean Base image audit and dependency manifests. `runs/case-062-base-final/` records F2P `FAILED` and P2P `PASSED`; `runs/case-062-gold-final/` records both `PASSED`; `runs/case-062-tamper-final/` records rejection of candidate precreation of the protected test. All exact-commit controls used the same image ID and no container network. `publication/registry_audit.json` records verification of the published Docker Hub digest.
