# Java-C SWE-bench Case 069

This case is derived from LWJGL commit `94f8bd69e176be3e48b4376281fed778e76ab8df`, which fixes Issue #409 by using the buffer's base address when decoding text from a non-zero `ByteBuffer.position()`.

## Identity

- Instance: `LWJGL__lwjgl3-409`
- Repository: `LWJGL/lwjgl3`
- Base: `427e278dc2402aca025cacd58a80eb4eaa8c4832`
- Fix: `94f8bd69e176be3e48b4376281fed778e76ab8df`
- Issue: [#409](https://github.com/LWJGL/lwjgl3/issues/409)
- Candidate: `JC-009` from the Java-C official-test candidate table

## Test and environment

The protected test is the upstream `MemoryUtilTest.testTextDecoding` addition. It exercises ASCII, UTF-8, and UTF-16 decoding from buffers whose position is non-zero. The evaluator builds only LWJGL core and runs `MemoryUtilTest` through TestNG. It does not start a display server or invoke GLFW/OpenGL/OpenAL.

The Docker image contains the exact Base checkout and historical JDK 8/Ant toolchain. Candidate and protected patches are mounted at runtime.
