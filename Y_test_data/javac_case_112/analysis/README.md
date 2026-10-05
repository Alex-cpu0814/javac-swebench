# Case 112 analysis

OpenJPEG Issue #571 reports that default lossless compression fails on Linux
x86 while the same input succeeds on x86-64. Pull request #579 adds the
`issue571.tif` regression input and an encode/decode/component-comparison test.
The production change is isolated in `src/lib/openjp2/tcd.c`; all upstream test
harness changes are isolated in `patches/test_patch.diff`.
