# 来源与研究边界

原始候选 056（Excel 第 57 行），057 为同提交重复记录。官方修复不含测试。
issue_original.json 为 GitHub 原始报告；两个结构体测试通过讨论生成，Fix 在设计时已知。
没有盲生成或独立审查声明。

base_materials/ 保存固定 Base 的源码，包含官方补丁涉及的全部文件。
fix_materials_manifest.json 保存对应 Fix blob 的 SHA256，供补丁一致性验证。
test_sources/ 为实际运行的新增测试；原始工作区 root 副本缺少版权头不作为归档来源。
reproduction/ 和 local_prototype/ 保留早期单类验证程序/工具，仅作历史记录。

新 evaluator 在独立镜像中重新编译 Kotlin、所有启用的 Core/Vulkan Java 和当前 JNI，
使用真实 TestNG 执行两个 F2P 与一个项目原有 P2P。
外部 libffi PIC 适配、无真实 Vulkan 创建调用、validator 缺失时通过的测试边界详见
environment_spec.json。不能将局部 Java 状态解释成完整合法的 Vulkan 创建对象。
