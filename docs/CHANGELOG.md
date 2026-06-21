# Agent Evaluator — 更新日志

本文件记录 Agent Evaluator 的所有重要变更。格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [1.0.0] - 2026-05-30

### 🎉 首次发布

#### 核心功能

- **评估器模块** (`src/evaluator.py`)
  - `RuleEvaluator`：基于规则的评估器（关键词匹配、长度比、句子完整性）
  - `LLMEvaluator`：基于 LLM 的评估器（支持自定义 `llm_caller` 注入）
  - `CompositeEvaluator`：组合评估器（权重缩放 + 同指标取均值融合）
  - `create_evaluator()` 工厂函数
  - 四维评估指标：Accuracy、Relevance、Completeness、Coherence
  - `EvalReport` 加权总分计算

- **测试数据集模块** (`src/test_dataset.py`)
  - `TestDataset` 数据集类（支持难度和标签过滤）
  - `create_sample_dataset()`：通用问答测试集（6 个用例，覆盖 easy/medium/hard）
  - `create_coding_dataset()`：编程能力测试集（2 个用例）
  - `load_dataset_from_json()`：从 JSON 文件加载自定义数据集

- **基准测试模块** (`src/benchmark.py`)
  - `BenchmarkConfig`：测试配置（名称、重复次数、超时、权重）
  - `BenchmarkRunner`：测试运行器（支持自定义 `agent_caller`）
  - `BenchmarkResult`：测试结果与多维统计（按难度分组、按指标聚合）
  - `run_benchmark()` 便捷函数

- **Web 服务** (`src/web/app.py`)
  - FastAPI REST API（10 个端点）
  - Web 管理面板（Dashboard）
  - CORS 跨域支持（限制为本地访问）

- **macOS 桌面应用** (`src/macos/app.py`)
  - tkinter GUI 界面
  - 内嵌 Web 服务启停控制
  - 一键打开浏览器访问 Web 面板

#### 示例与打包

- `examples/eval_demo.py`：评估演示脚本（覆盖三种评估器和基准测试）
- `packaging/py2app_setup.py`：macOS py2app 打包脚本

#### 文档

- `README.md`：项目说明与快速开始
- `docs/技术文档.md`：详细技术设计文档（中文）
- `docs/TECHNICAL_DOC.md`：技术文档
- `docs/DIRECTION.md`：项目方向指引
- `docs/VERSION.md`：版本记录

#### 代码审查

- `REVIEW.md`：代码审查报告（安全、质量、架构三维度评估）

---

## [未发布] — 计划中

### 计划新增

- 集成 DeepSeek / GPT API 进行真实 LLM 评估
- A/B 测试对比报告生成
- 评估结果可视化图表（Matplotlib / Plotly）
- 数据持久化（SQLite）
- 单元测试覆盖（pytest）
- CI/CD 集成与自动化回归测试
- 更多评估指标（安全性、成本等）
- 分布式评估支持

### 计划改进

- 使用 `pyproject.toml` 替代 `sys.path` hack
- 添加日志系统（`logging` 模块替代 `print()`）
- 锁定依赖版本
- 添加 API 认证机制
