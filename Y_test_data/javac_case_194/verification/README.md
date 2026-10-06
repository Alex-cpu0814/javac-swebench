# Case 194 verification evidence

Valid evidence consists of a clean evaluator-image build plus isolated Base
and Gold runs. Base must report `test-tdishr` as `ok` and `test-treeshr` as
`FAIL`; Gold must report both as `ok`.

The exploratory Docker probe established that exact differential before the
formal evaluator assets were generated.

- Final image build and clean-image audit: `case-194-build-1`
- Image ID: `sha256:d12be7067ce51c31c085739c3a3fc4c69d273b8751059234700870a2ce9e5606`
- Final Base control: `case-194-base-1`
- Final Gold control: `case-194-gold-1`
