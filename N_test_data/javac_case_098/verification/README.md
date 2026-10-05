# Case 098 Verification

The gold and protected test patches apply cleanly to the exact Base commit. The protected test invokes the official JEP `TestMemoryLeaks` Java stress class from the normal `jep.Run` test framework and checks that the child JVM completes under a bounded heap.

The final status will be recorded after the Base negative control and Fix gold control both run in the clean Docker image.
