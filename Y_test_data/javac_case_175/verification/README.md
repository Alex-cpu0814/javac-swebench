# Case 175 verification evidence

Valid evidence consists of a clean evaluator-image build plus isolated Base
and Gold runs. Base must report the existing small-response control as `ok` and
the official 512 KiB response regression as `FAIL`. Gold must report both as
`ok`.

- Initial build diagnostic: `case-175-build-1` (reactor artifacts omitted)
- Final image build and audit: `case-175-build-2`
- Image ID: `sha256:d5eaaed040c90536d22f0ef5548ad00d2ec61b59e698d725014695479df8a20d`
- Final Base control: `case-175-base-1`
- Final Gold control: `case-175-gold-1`

The initial build diagnostic is retained because it documents why the full
Jetty reactor must be installed with tests skipped rather than test compilation
disabled.
