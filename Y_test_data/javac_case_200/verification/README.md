# Case 200 verification evidence

Valid evidence consists of a clean evaluator-image build plus isolated Base
and Gold runs. Base must report `test-tdishr` as `ok` and
`test-treeshr-owner-id` as `FAIL`; Gold must report both as `ok`.

The exploratory Docker probe established the exact differential:
`4194368LU` on Base versus the official expected `64LU`, followed by a passing
Gold run.

- Final image build and clean-image audit: `case-200-build-2`
- Image ID: `sha256:77c71ce09d01e830e0b98f3607636f0ffb03abc24ad51498190f6e7e0fb961dd`
- Final Base control: `case-200-base-1`
- Final Gold control: `case-200-gold-1`

