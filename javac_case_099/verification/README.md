# Case 099 Verification

The gold and protected test patches must apply cleanly to the exact Base commit. Verification requires Base + test patch to fail the child-JVM regression and Fix + test patch to pass it, with the existing regression suite remaining green.
