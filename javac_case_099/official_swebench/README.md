# Case 099 SWE-bench record

This record uses the upstream source fix and a dataset-owned regression test. The upstream commit did not modify an official test file, so the test patch isolates the ClassLoader-specific cache regression in a child JVM.
