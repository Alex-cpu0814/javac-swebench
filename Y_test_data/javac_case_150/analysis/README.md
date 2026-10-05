# Case 150 analysis

Issue #116 reports that Linux abstract-namespace socket names regressed after
upgrading to junixsocket 2.5.1. The native layer supplied the full
`sockaddr_un` size instead of the actual abstract address length. As a result,
returned addresses contained many zero bytes and a C client using the real
name length could not connect to the Java server.

The upstream commit adds `AbstractNamespaceTest`, which binds and connects to
short abstract addresses and exercises meaningful trailing zero bytes. The
production fix is in `junixsocket-native/src/main/c/address.c`; the other
non-test edits from the same official commit remain in the gold patch.
