# Case 160 analysis

Issue #90 established that socket operations governed by `SO_TIMEOUT` should
raise `SocketTimeoutException` when the timeout expires. The parent commit had
already corrected the read side. The selected fix commit applies the same
behavior to a blocking native write.

On Base, two send-buffer-sized writes fill an AF_UNIX socket whose peer is not
reading. The second write remains blocked indefinitely even though the socket
timeout is 500 milliseconds. The native `write` path special-cases
`EAGAIN`/`EWOULDBLOCK` and returns without calling the helper that polls the
descriptor and raises the timeout exception.

The official fix routes the error through `checkNonBlocking`, which waits for
writability and throws `SocketTimeoutException` when polling expires. The exact
upstream test patch adds `testSocketTimeoutExceptionWrite` and retains the
read-side behavior as `testSocketTimeoutExceptionRead`.
