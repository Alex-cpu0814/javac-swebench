# Java-C SWE-bench Case 099

This case is derived from JEP commit `778b516930bdc11ecbb7751d560d373964009639`, which fixes Issue #17 by moving the Java-method cache from a process-global dictionary to the cache owned by each Jep interpreter.

The protected test builds two versions of the same Java class name with different ClassLoaders. It exercises the first version in one Jep instance, closes it, and then exercises the second version in a new Jep instance. Base reuses the stale global method list; the fix keeps the method cache isolated.

## Identity

- Instance: `ninia__jep-17-cache`
- Base: `b1ab138dd6d492c7547e24d0b117aeafb112613d`
- Fix: `778b516930bdc11ecbb7751d560d373964009639`
- Issue: #17

## Verification

The test runs inside a child JVM so a native failure cannot terminate the Python test runner. The Docker evaluator uses OpenJDK 8 and Python 3.4.10, matching the Base tree's supported environment.
