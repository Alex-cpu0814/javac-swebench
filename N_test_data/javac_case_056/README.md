# Case 056: LWJGL imageless framebuffer

Instance: `LWJGL__lwjgl3-673`; repo: `LWJGL/lwjgl3`; source version: `3.3.0`.

两个 issue-derived TestNG 测试覆盖 NULL pAttachments 保留 attachmentCount，以及
旧版生成校验器错误抛出 NPE。1 个项目原有 `VulkanTest.testParse` 为 P2P。
在独立断网容器中：Base 两目标失败、P2P 通过；官方 Fix 三个测试全部通过。
候选补丁预先创建受保护测试时被拒绝。

Core/Vulkan 使用标准 Ant 冷构建：Kotlin 生成器和模板、生成 Java/C、所有启用的 Java
模块及当前源码 JNI。评测时不复用 Base 项目二进制或 Maven JNI 成品。
Ubuntu libffi-dev 3.4.2-4 PIC 静态库是明确记录的外部依赖适配。
测试覆盖 Java 结构体/校验语义，没有真实 VkDevice、Vulkan 驱动或 GPU 调用。
Fix 在测试设计时已知；没有独立盲生成/评审声明。

```text
analysis/          来源、研究边界、源码快照、历史复现程序
patches/           完整官方修复和受保护测试补丁
official_swebench/ JSON、JSONL、模型任务输入、校验和
evaluator/         干净 Base 镜像构建、运行时注入、标准 Ant 评测
verification/      历史日志及独立镜像的构建、审计、Base/Fix/篡改控制
```

镜像已发布到 Docker Hub，按不可变 digest 拉取及干净 Base 审计均通过：

```powershell
docker pull yutu0814/javac-case-056-lwjgl3:benchmark-v1
python evaluator/evaluate_model_patch.py --patch C:\path\candidate.diff
```

镜像 digest：`sha256:866ae42ecde1bbcaa0581fabe2380bdea159ed944f565066b7abe1c2922a7669`。

Base: `307ebed6ef6ba420b2165ddb2ec21dd9a37479df`  
Fix: `ce56fc6c805ea671a4cf4e79abbd331688adfb6d`  
Issue: https://github.com/LWJGL/lwjgl3/issues/673

镜像提供独立运行所需 Base 和依赖；不依赖原实验目录。
构建镜像时可选复用已有源码对象/第三方依赖缓存，详细命令见 `evaluator/README.md`。
模型输入仅使用 `official_swebench/public_task_056.json`，其余记录含评测答案。
原始候选 056/057 为同提交重复数据，合并为这一个 instance。
发布状态和镜像 digest 见 `verification/publication.json`（如已发布）。
