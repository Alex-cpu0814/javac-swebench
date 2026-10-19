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

使用要求：Docker（Linux 容器模式）、Git、宿主机 Python 3.10 或更新版本。
镜像平台为 `linux/amd64`，ARM64/Apple Silicon 尚未验证。宿主机无需安装 Java、
Ant、GCC 或 Vulkan 驱动。第一次拉取镜像需要网络，拉取后评测容器断网编译、测试。

从公开仓库下载文件，并按不可变 digest 拉取已发布镜像：

```powershell
git clone https://github.com/Alex-cpu0814/javac-swebench.git
cd javac-swebench/N_test_data/javac_case_056
docker pull yutu0814/javac-case-056-lwjgl3@sha256:866ae42ecde1bbcaa0581fabe2380bdea159ed944f565066b7abe1c2922a7669
```

先用官方修复补丁验证环境：

```powershell
python evaluator/evaluate_model_patch.py --patch patches/gold_patch.diff
```

预期 `status=resolved`，两个 FAIL_TO_PASS 和一个 PASS_TO_PASS 全部通过，退出码为 0。
评测模型补丁时，将补丁保存为文件，再执行（替换为实际路径）：

```powershell
python evaluator/evaluate_model_patch.py --patch C:/path/candidate.diff
```

结果保存在 `verification/runs/<run-id>/`；`summary.json` 给出状态及计数，
`grading.json` 给出逐项结果，`project-build.raw.log` 和 `tests.raw.log` 保存构建和测试日志。
退出码 0 表示 resolved，1 表示 unresolved，2 表示基础设施错误。

评测器默认使用上述 digest；即使 `benchmark-v1` 标签以后改变，也不会跟随改变。
`--image` 可显式指定其他镜像，结果会记录实际引用。镜像默认入口是 Bash，
直接 `docker run` 不会自动评测；完整评测由上述脚本注入补丁、受保护测试和评测器。
镜像自身不包含修复补丁或受保护测试。

Docker Hub：[yutu0814/javac-case-056-lwjgl3](https://hub.docker.com/r/yutu0814/javac-case-056-lwjgl3)。

Base: `307ebed6ef6ba420b2165ddb2ec21dd9a37479df`  
Fix: `ce56fc6c805ea671a4cf4e79abbd331688adfb6d`  
Issue: https://github.com/LWJGL/lwjgl3/issues/673

镜像提供独立运行所需 Base 和依赖；不依赖原实验目录。
构建镜像时可选复用已有源码对象/第三方依赖缓存，详细命令见 `evaluator/README.md`。
模型输入仅使用 `official_swebench/public_task_056.json`，其余记录含评测答案。
原始候选 056/057 为同提交重复数据，合并为这一个 instance。
发布状态和镜像 digest 见 `verification/publication.json`（如已发布）。
