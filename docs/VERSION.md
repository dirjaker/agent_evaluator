# Agent Evaluator 版本记录

## v1.0.0 (2026-05-30)

### 🎉 初始版本

#### 核心模块

- **Evaluator 评估器模块** (`src/evaluator.py`, ~350 行)
  - `EvalMetric` 评估指标枚举（6 个指标）
  - `EvalResult` 单项评估结果数据类
  - `TestCase` 测试用例数据类
  - `EvalReport` 评估报告（含加权总分计算）
  - `RuleEvaluator` 规则评估器（关键词匹配、词汇重叠、长度比、句子完整性）
  - `LLMEvaluator` LLM 评估器（支持自定义 `llm_caller` 注入）
  - `CompositeEvaluator` 组合评估器（权重缩放 + 同指标取均值融合）
  - `create_evaluator()` 工厂函数

- **Test Dataset 测试数据集模块** (`src/test_dataset.py`, ~150 行)
  - `TestDataset` 数据集类（支持难度和标签过滤）
  - `create_sample_dataset()` 通用问答测试集（6 个用例）
  - `create_coding_dataset()` 编程能力测试集（2 个用例）
  - `load_dataset_from_json()` JSON 文件导入

- **Benchmark 基准测试模块** (`src/benchmark.py`, ~220 行)
  - `BenchmarkConfig` 测试配置
  - `BenchmarkRunner` 测试运行器
  - `BenchmarkResult` 测试结果与多维统计
  - `run_benchmark()` 便捷函数

#### Web 服务

- **FastAPI Web Dashboard** (`src/web/app.py`, ~260 行)
  - 10 个 REST API 端点
  - Web 管理面板
  - CORS 跨域支持

#### 桌面应用

- **macOS 桌面应用** (`src/macos/app.py`, ~145 行)
  - tkinter GUI 界面
  - Web 服务启停控制
  - 浏览器快速打开

#### 示例与打包

- `examples/eval_demo.py` — 评估演示脚本
- `packaging/py2app_setup.py` — macOS 打包脚本

#### 文档

- `README.md` — 项目说明
- `docs/技术文档.md` — 详细技术设计文档
- `docs/TECHNICAL_DOC.md` — 技术文档
- `docs/DIRECTION.md` — 方向指引
- `docs/VERSION.md` — 版本记录
- `REVIEW.md` — 代码审查报告

---

## 后续计划

### v1.1.0 (计划中)

- [ ] 集成 DeepSeek API 进行 LLM 评估
- [ ] 添加更多评估指标（安全性、成本等）
- [ ] 支持 JSON 数据集导入（已完成，持续优化）
- [ ] 评估结果可视化图表

### v1.2.0 (计划中)

- [ ] A/B 测试对比报告
- [ ] 结果持久化（SQLite）
- [ ] 报告导出（PDF/HTML）
- [ ] 单元测试覆盖

### v2.0.0 (远期)

- [ ] Web UI 增强
- [ ] 多用户支持
- [ ] CI/CD 集成
- [ ] 分布式评估
