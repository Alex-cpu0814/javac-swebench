# Case 152 verification evidence

Valid evidence consists of a clean evaluator image build plus isolated Base and
Gold runs. Base must report `testForkedVMRedirectStdin` as `ERROR` while the
stdout descriptor control remains `ok`. Gold must report both methods as `ok`.

The standard evaluator confirmed that semantic split:

- Final image build: `case-152-build-1`
- Image ID: `sha256:34489d29f08f54938761edd96b22ef7638687867c33e37101fec92a777fbc973`
- Published image: `yutu0814/javac-case-152-junixsocket:benchmark-v1`
- Final Base control: `case-152-base-1`
- Final Gold control: `case-152-gold-1`
