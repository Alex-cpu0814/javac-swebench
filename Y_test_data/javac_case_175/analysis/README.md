# Case 175 analysis

Issue #135 reports corrupted responses from `AFSocketServerConnector` when a
Jetty response is larger than 32 KiB. The server reports HTTP 200, but each
subsequent chunk repeats bytes from the beginning of the response. The
official 512 KiB regression test detects the first mismatch at offset 32768.

`AFCore.write` copies a non-direct source into a reusable direct buffer before
calling the native send path. The Base implementation temporarily sets the
source limit to the direct buffer's absolute limit. After the first chunk, that
limit no longer describes the remaining slice of the source, so the wrong data
is copied. The official fix copies while both buffers have remaining bytes and
adds the same defensive loop to the non-direct read path.

The tracker contains the fix commit twice. Case 175 represents the first
occurrence (workbook sequence 176); source case 176 (workbook sequence 177) is
recorded as a duplicate and is not materialized separately.
