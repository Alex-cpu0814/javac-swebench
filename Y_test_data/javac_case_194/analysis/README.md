# Case 194 analysis

Issue #1423 reports that malformed tree names beginning with `\\null` can
crash TDI callers. The official regression expresses the invalid name as a
newline-starting lookup and expects the normal `TreeNNF` diagnostic rather than
process termination.

The Base parser can leave its search-term array null and then dereference it in
`Search`; its whitespace trimmer can also move before an empty buffer. The fix
rejects the invalid path early, guards the missing term, and makes trimming
safe. The gold patch preserves the complete non-test upstream commit diff,
including the regenerated Flex source.

The tracker maps this unique commit to source case 194 (workbook sequence 195).
