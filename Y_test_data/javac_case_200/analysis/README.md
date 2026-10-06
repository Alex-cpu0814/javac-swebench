# Case 200 analysis

Issue #2375 reports that the NCI owner field historically packed a Unix GID
and UID into two 16-bit halves. Modern UIDs may exceed 16 bits, so this layout
can truncate or corrupt the owner identity.

The fix introduces an NCI flag for records that contain a full 32-bit UID.
New records with a high-word UID store that UID directly, while legacy packed
records remain readable by returning their low 16-bit UID. TCL directory
output is updated to describe the owner as a UID rather than a packed pair.

The upstream test change updates the existing `test-treeshr.tdi` oracle from
`4194368LU` (`64 << 16 | 64`) to `64LU`. Runtime validation as UID/GID 64
proves Base-fail/Fix-pass. The tracker maps this unique commit to source case
200 (workbook sequence 201).

