#include <jni.h>

/* Same JNI signatures and sizeof(void *) result as the two pinned C revisions. */
JNIEXPORT jint JNICALL Java_org_lwjgl_system_MemoryUtil_memGetPointerSize(JNIEnv *env, jclass clazz) {
    (void)env;
    (void)clazz;
    return (jint)sizeof(void *);
}

JNIEXPORT jint JNICALL Java_org_lwjgl_system_MemoryAccess_getPointerSize(JNIEnv *env, jclass clazz) {
    (void)env;
    (void)clazz;
    return (jint)sizeof(void *);
}
