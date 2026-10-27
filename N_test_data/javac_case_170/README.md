# Case 170 — junixsocket #140

此目录是独立的 SWE-bench-compatible 数据，实例为 `kohlschutter__junixsocket-140`，属于 `N_test_data`：上游 Fix 没有新增回归测试，本数据的保护测试根据 issue 构造。原始探索证据已整理进正式目录；发布后清理探索工作目录和可重建缓存。

问题：临时目录可写但以 `noexec` 挂载时，提取 `.so` 成功，真实 `System.load` 却报 `failed to map segment from shared object`。Base 按异常文本中有无 `perm` 判断是否回退，因而没有尝试仍可用的后续目录。测试验证真实 Java/JNI 加载和 Unix-domain socket 双向传输。

- Base：`71a134bce58a22fb17a7a14f00799196c0c71a60`
- Fix：[`09548dadf52ba6b4f939d0260c391503f478a6a5`](https://github.com/kohlschutter/junixsocket/commit/09548dadf52ba6b4f939d0260c391503f478a6a5)
- Issue：[#140](https://github.com/kohlschutter/junixsocket/issues/140)
- Gold：完整上游提交的原始差异；测试和驱动由数据制作补充，制作时已查看 Fix。

| 最终测试 | 数量 | Base | Gold |
|---|---:|---|---|
| 临时目录 noexec，回退 home | 1 | FAIL | PASS |
| 临时目录和 home 均 noexec，回退 cwd | 1 | FAIL | PASS |
| 正常加载、全部目录 noexec 时仍拒绝 | 2 | PASS | PASS |
| 五个原项目 JUnit 类中的全部用例 | 39 | PASS | PASS |
| 合计 | 43 | 41 PASS / 2 FAIL | 43 PASS |

每个加载场景使用独立 JVM。成功须完成三轮真实 socket 双向数据校验，并由 `/proc/self/maps` 确认库映射来自预期目录；负面对照须保留真实 `UnsatisfiedLinkError`。测试检查 `/proc/self/mountinfo` 中的实际挂载标志，同时证明所有候选目录可写。

Docker Hub 镜像为 `yutu0814/javac-case-170-junixsocket:benchmark-v1`，评测默认固定到 `yutu0814/javac-case-170-junixsocket@sha256:1a70b55b3d05b7f18257b238ba0ab246f055b03023eb9483d1cafc58703fbde3`，已验证 ID 为 `sha256:1a70b55b3d05b7f18257b238ba0ab246f055b03023eb9483d1cafc58703fbde3`。镜像只含干净 Base、公开依赖和工具链；Gold、Fix Git 对象、保护测试、评测驱动和项目编译产物均不在镜像内。每次评测通过只读挂载注入驱动/测试，在新容器中应用候选补丁后重新编译。

在 PowerShell 中复核官方补丁：

```powershell
Set-Location 'E:\CLB_Swe-bench\javac-swebench\N_test_data\javac_case_170'
$python = 'C:\Users\玉兔\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$docker = 'C:\Users\玉兔\AppData\Local\Programs\DockerDesktop\resources\bin\docker.exe'
& $python .\evaluator\evaluate_model_patch.py --docker $docker --patch .\patches\gold_patch.diff --run-id manual-gold-170
```

换成自己的补丁路径即可评测候选解，每次使用新的 `--run-id`。结果在 `verification/runs/<run-id>/`。`summary.json` 为 `resolved` 且退出码 0 表示全部通过；未解决为 1，基础设施错误为 2。

重建镜像与核验现有记录：

```powershell
& $python .\evaluator\build_model_evaluator.py --docker $docker --run-id manual-build-170
& $python .\analysis\verify_controls.py --docker $docker
```

镜像构建需要联网获取固定摘要的基础镜像、Base 提交、带 SHA256 的 Maven 依赖和 Ubuntu 系统包；评测容器使用 `--network none`。Docker Desktop 需运行 Linux containers，并支持 `--tmpfs` 的 `exec/noexec` 挂载。可重建的镜像上下文与 Git 工作副本已忽略。系统包版本可能改变重建后的镜像 ID，新镜像须重新验证；历史结果绑定本次确切 ID。

构建范围：重编候选补丁下的 92 个核心 Java 8 源文件（含上游兼容层和按上游模板生成的 BuildProperties），再编译 74 个测试源码。JNI 运行库固定为 Maven Central 的官方 `junixsocket-native-common:2.8.0`，SHA256 见 `analysis/toolchain_assets.json`。此任务修复 Java 加载逻辑；候选 C 修改、多模块 Maven 打包和现代 JDK 实现不在当前评分范围。没有声明完整 native 源码重编或完整 RHEL/SELinux 策略复刻。

公开给模型的是 `official_swebench/public_task_170.json` 和干净 Base；其余补丁、测试及日志属于私有评测材料。六组最终对照见 `verification/final_summary.json`。Docker Hub 已发布并通过匿名清单校验；GitHub 发布及复核记录见 `verification/`。

Published-image quick start (Docker executable on PATH):

```powershell
docker pull yutu0814/javac-case-170-junixsocket@sha256:1a70b55b3d05b7f18257b238ba0ab246f055b03023eb9483d1cafc58703fbde3
python .\evaluator\evaluate_model_patch.py --patch .\patches\gold_patch.diff --run-id consumer-gold-170
```
