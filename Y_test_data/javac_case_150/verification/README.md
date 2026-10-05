# Case 150 verification evidence

The final evidence records a clean image build plus isolated Base-control and
gold-control runs. A valid result shows both `AbstractNamespaceTest` methods
failing on Base, while the upstream gold patch passes them and the construction
control test.

- Final image: `case-150-build-2`
- Final Base control: `case-150-base-2`
- Final gold control: `case-150-gold-1`
- `case-150-base-1` records the pre-final dependency-cache diagnostic; no
  tests ran in that attempt, and it is not used as verification evidence.
