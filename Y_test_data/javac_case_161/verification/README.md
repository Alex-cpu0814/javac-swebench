# Case 161 verification evidence

Valid evidence consists of a clean evaluator-image build plus isolated Base
and Gold runs with the upstream poll-read path enabled. Base must report the
existing `issue14Pass` control as `ok` and the official
`testSocketTimeoutException` regression as `FAIL`. Gold must report both as
`ok`.

- Image build and audit: `case-161-build-1`
- Image ID: `sha256:969c2650967701f77c0d620466db2df05b0f5f8b6706167dbf117545f54a2ad3`
- Published image: `yutu0814/javac-case-161-junixsocket:benchmark-v1`
- Final Base control: `case-161-base-2`
- Final Gold control: `case-161-gold-1`
- Default-Linux platform diagnostic: `case-161-base-1`

The diagnostic run documents that default Linux bypasses the affected upstream
branch and therefore passes before the fix. It is retained as environment
evidence, but is not the final Base control.
