/* A loadable 64-bit library to make the wrong 32-bit selection observable. */
int jemalloc_probe_stub(void) { return 64; }
