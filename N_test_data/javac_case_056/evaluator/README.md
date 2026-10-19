# Independent Base-image evaluator

镜像已发布到 Docker Hub，并完成按 digest 拉取和断网审计。

```powershell
docker pull yutu0814/javac-case-056-lwjgl3:benchmark-v1
python evaluator/evaluate_model_patch.py --patch C:\path\candidate.diff
```

结果位于 verification/runs/<run-id>/；0 表示 resolved，1 表示 unresolved，2 表示基础设施错误。
模型补丁、受保护测试补丁、评测适配器在运行时注入；容器断网。
先应用模型补丁，再检查受保护测试是否仍可完整应用；冲突则拒绝。

每次执行标准 Ant clean-kotlin / clean-java / clean-native / compile-templates / compile-native。
启用 Core/Vulkan；其余可选绑定关闭，Ant 的 Linux native 目标仍会构建两个无关小库。
JNI 从当前源码编译，链接已固定 SHA256 的 Ubuntu libffi PIC 静态依赖。
使用真实 TestNG 和显式 XMLReporter，避开旧版 HTML 报告器缺少 jquery.min.js 的问题。
两个新增测试与项目已有 VulkanTest.testParse 一起运行。

重新构建：

```powershell
python evaluator/build_model_evaluator.py
```

构建需网络访问 apt/GitHub/Ant 依赖。若本地原实验工作区存在，脚本可复用其中 Base 的
Git 对象和 Base 声明的 Java/Kotlin 第三方依赖缓存；只导出 depth-one Base，不带 Fix。
也可通过 --source-repo / --dependency-cache 显式指定这些可选缓存。
发布镜像的使用不需要这些本地文件。

测试范围为 Java 结构体与生成校验器，不执行真实 Vulkan framebuffer 创建。
不宣称完整上游可选模块、GPU 或所有 libffi ABI 路径的兼容性。
