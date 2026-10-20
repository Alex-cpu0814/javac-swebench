#include <jni.h>
#include <stdint.h>

static int last_calls;
static uintptr_t last_render_address;
static uint32_t last_render_count;
static uintptr_t last_game_address;
static uint32_t last_game_count;

static int wait_get_poses_stub(void *render, uint32_t render_count, void *game, uint32_t game_count) {
    ++last_calls;
    last_render_address = (uintptr_t)render;
    last_render_count = render_count;
    last_game_address = (uintptr_t)game;
    last_game_count = game_count;
    return 418;
}

#define JNI_PROBE(name) Java_org_lwjgl_openvr_VRCompositorNullGamePoseTest_##name

JNIEXPORT jlong JNICALL JNI_PROBE(stubFunction)(JNIEnv *env, jclass cls) {
    (void)env; (void)cls;
    return (jlong)(intptr_t)&wait_get_poses_stub;
}
JNIEXPORT jint JNICALL JNI_PROBE(callCount)(JNIEnv *env, jclass cls) {
    (void)env; (void)cls;
    return last_calls;
}
JNIEXPORT jlong JNICALL JNI_PROBE(renderAddress)(JNIEnv *env, jclass cls) {
    (void)env; (void)cls;
    return (jlong)last_render_address;
}
JNIEXPORT jint JNICALL JNI_PROBE(renderCount)(JNIEnv *env, jclass cls) {
    (void)env; (void)cls;
    return (jint)last_render_count;
}
JNIEXPORT jlong JNICALL JNI_PROBE(gameAddress)(JNIEnv *env, jclass cls) {
    (void)env; (void)cls;
    return (jlong)last_game_address;
}
JNIEXPORT jint JNICALL JNI_PROBE(gameCount)(JNIEnv *env, jclass cls) {
    (void)env; (void)cls;
    return (jint)last_game_count;
}
