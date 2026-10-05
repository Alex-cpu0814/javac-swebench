# Case 152 analysis

Issue #97 reports that a bound AF_UNIX socket inherited as standard input
(file descriptor 0) cannot be used by junixsocket. This is a FastCGI-style
launch pattern: the parent process owns the listening socket and supplies it to
the Java process through stdin.

The upstream commit introduces `FileDescriptorCast` support for
`ProcessBuilder.Redirect` and changes native descriptor validation so descriptor
zero is accepted as valid. Its official regression test passes an AF_UNIX
socket to a forked JVM as stdin and expects the child to send `Hello world`
back through that socket.

Because the same commit also performs a broad API/test-package reorganization,
the protected patch keeps the official regression behavior in a small isolated
harness. This avoids unrelated pre-refactor tests failing to compile against
the post-refactor production tree while testing the same JNI behavior.
