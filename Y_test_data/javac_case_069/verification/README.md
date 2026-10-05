# Case 100 verification

Verification must show that the exact Base plus the protected upstream test fails `testTextDecoding`, while the Fix plus the same test passes it. `testUTF8` is retained as a PASS_TO_PASS control. The image audit must confirm that the clean image contains neither candidate nor protected patches.
