# Verification evidence

generation_evidence/ 保留用户早期执行的单类局部构建日志，不能单独作为完整构建证据。
builds/case-056-build-1/ 保存标准 Ant Base 构建、依赖清单与干净镜像审计。
runs/case-056-base-1/：冷构建后两个 F2P 失败，一个 P2P 通过。
runs/case-056-gold-1/：完整官方补丁应用后冷构建，三个测试全部通过。
runs/case-056-tamper-1/：预先创建受保护测试的候选被拒绝。
各目录包含原始编译日志、真实 TestNG XML、结构化事件和 grading。
Docker 评测断网，JNI 库从当前源码编译；镜像没有 Fix/测试/评测脚本。
publication.json（如存在）记录 Docker Hub 与 GitHub 发布状态。
