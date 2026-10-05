# Case 161 analysis

Issue #90 reported that an input read governed by `SO_TIMEOUT` could finish
without raising `SocketTimeoutException`. The defect is in the native
poll-based read path used upstream on Solaris and BSD-family platforms.

The parent implementation returned `-1` for every poll result below one. It
therefore conflated a blocking timeout, a native polling error, and a
non-blocking socket with end-of-stream. The official fix separates these
outcomes: native errors are propagated, a non-blocking socket returns zero,
and a blocking timeout raises `SocketTimeoutException`.

Docker Desktop supplies a Linux kernel, where junixsocket normally bypasses
this platform-specific branch. The evaluator therefore enables the upstream
`junixsocket_use_poll_for_read` compile-time path while compiling the unmodified
Base source. This produces the intended behavior split with the exact official
test: Base fails after the 500 ms timeout, and Gold passes.

The tracker contains the same fix commit twice. Case 161 represents the first
occurrence (workbook sequence 162); source case 162 (workbook sequence 163) is
recorded as a duplicate and is not materialized separately.
