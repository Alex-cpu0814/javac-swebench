# Case 160 verification evidence

Valid evidence consists of a clean evaluator-image build plus isolated Base
and Gold runs. Base must report the read-timeout control as `ok` and the
write-timeout regression as `ERROR` after its bounded wait. Gold must report
both methods as `ok`.

The standard evaluator confirmed that split:

- First build diagnostic: `case-160-build-1` (Ubuntu package mirror timeout)
- Final image build: `case-160-build-2`
- Image ID: `sha256:15fcd1b85e32e2b60df81e65888a891648cf05421aece7b8fbaa0e829be75e24`
- Published image: `yutu0814/javac-case-160-junixsocket:benchmark-v1`
- Final Base control: `case-160-base-1`
- Final Gold control: `case-160-gold-1`
