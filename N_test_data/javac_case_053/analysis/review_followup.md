# 053 独立审查补充核对

审查结论以 `review.json` 为准：接受候选，无阻断问题，最终仍需人工确认。

## 编译命令对应关系

Base 的 `base_materials/config/linux/build.xml` 第 35–48 行定义 Linux C 编译阶段。候选使用其中的 `-c -std=gnu11`、`-O3 -fPIC`、`-pthread -DNDEBUG`、Linux/x64 平台宏、FORTIFY/GNU/大文件宏及真实 JDK/project include 目录；核心警告组对应同文件第 166 行的 `-Werror -Wfatal-errors -Wall -Wextra -pedantic`。

有意简化：候选省去影响链接/优化阶段的 LTO、在固定 x86_64 容器中省去默认同架构的 `-m64`、省去本翻译单元不使用的额外模块 include 目录。它直接编译对象，不执行 Ant 或最终链接，不能声称完整 native 构建通过。

有意适配：显式增加原报告中出现的 `-Wstrict-prototypes`，以在 upstream Clang 14 下稳定启用 Apple Clang 报告的同类诊断。原 macOS 的 Objective-C 模式、SDK、架构和 Apple Clang 默认诊断组未被精确复现，须保留此范围说明。

## 参考修复与执行入口

`verification/latest.json` 记录 Base/Fix 身份、两个完整官方变更文件的应用后 blob 校验、冻结候选 SHA256 及两轮结果。该元数据可核对参考身份，不需要向生成器或审查员公开修复源码。

执行入口明确为 `python3 config/tests/native_compilation.py`，由离线容器验证脚本调用；候选没有自动加入已有 TestNG/Ant 套件。

## 人工决定

确认是否接受这个有参考 Fix 验证的 Linux 编译适配候选，以及有限的回归覆盖。若要求原环境精确复现，则需要另行提供/准备 macOS Ventura 和 Apple Clang 14.0.3 环境，不能把当前 Linux 结果写成 macOS 验证。

设施错误处理缺少 subprocess 启动异常结构化输出与超时，是审查记录的非阻断改进项。当前已冻结并验证的候选未作修改；后续改进应以单独修订记录并重新验证。
