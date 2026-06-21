<div align="center">

<img src="assets/banner.svg" width="100%" alt="Agent 评估框架">

<br>

### 📊 Agent 评估框架

[![Stars](https://img.shields.io/github/stars/dirjaker/agent_evaluator?style=flat-square&label=Stars&color=FFD700)](https://github.com/dirjaker/agent_evaluator/stargazers)
[![Forks](https://img.shields.io/github/forks/dirjaker/agent_evaluator?style=flat-square&label=Forks&color=4A90D9)](https://github.com/dirjaker/agent_evaluator/network/members)
[![Contributors](https://img.shields.io/github/contributors/dirjaker/agent_evaluator?style=flat-square&label=Contributors&color=8B4513)](https://github.com/dirjaker/agent_evaluator/graphs/contributors)
[![License](https://img.shields.io/github/license/dirjaker/agent_evaluator?style=flat-square&label=License&color=20B2AA)](https://github.com/dirjaker/agent_evaluator/blob/dev/LICENSE)

**一个自动化评估 AI Agent 输出质量的多维度评估框架**

</div>

---

## 📖 项目简介

Agent Evaluator 是一款轻量级、可扩展的 AI Agent 评估工具。它提供了**规则评估、LLM 评估、组合评估**三种策略，支持从准确性、相关性、完整性、连贯性等多个维度对 Agent 输出进行量化打分，并内置基准测试运行器，可一键完成数据集驱动的批量评估与统计分析。

适用于 Agent Prompt 调优、模型选型、A/B 对比、回归测试等场景。

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 📏 **多维评估** | 准确性、相关性、完整性、连贯性四维度量化打分 |
| 🧠 **三种评估策略** | 规则评估（快速确定）、LLM 评估（语义理解）、组合评估（融合两者） |
| 🧪 **自动化基准测试** | 内置 BenchmarkRunner，一键运行数据集并生成多维统计报告 |
| 📊 **测试数据集管理** | 预置通用问答与编程能力数据集，支持 JSON 文件导入自定义数据集 |
| ⚖️ **A/B 对比分析** | 通过替换 `agent_caller` 函数，对同一数据集进行版本对比 |
| 🌐 **Web 管理面板** | 基于 FastAPI 的 REST API 与 Web Dashboard |
| 🖥️ **macOS 桌面应用** | tkinter GUI，内嵌 Web 视图，一键启动评估服务 |
| 📈 **多维统计报告** | 按难度分组、按指标聚合、加权总分计算 |

## 🏗️ 项目结构

```
agent_evaluator/
├── src/
│   ├── __init__.py          # 包初始化，版本信息
│   ├── evaluator.py         # 核心评估器（Rule/LLM/Composite）
│   ├── test_dataset.py      # 测试数据集管理
│   ├── benchmark.py         # 基准测试运行器
│   ├── web/
│   │   ├── app.py           # FastAPI Web 服务
│   │   └── static/          # 前端静态文件
│   └── macos/
│       └── app.py           # macOS 桌面应用
├── examples/
│   └── eval_demo.py         # 评估演示脚本
├── packaging/
│   └── py2app_setup.py      # macOS 打包脚本
├── docs/                    # 项目文档
├── requirements.txt         # Python 依赖
└── README.md
```

## 🚀 快速开始

### 环境要求

- Python 3.10+
- 推荐使用 Conda 管理虚拟环境

### 安装与运行

```bash
# 克隆项目
git clone https://github.com/dirjaker/agent_evaluator.git
cd agent_evaluator

# 创建虚拟环境
conda create -n agent_evaluator python=3.12 -y
conda activate agent_evaluator

# 安装依赖
pip install -r requirements.txt

# 运行评估演示
python examples/eval_demo.py
```

### 启动 Web 服务

```bash
# 启动 FastAPI 服务（默认端口 8004）
python -m src.web.app

# 或通过 macOS 桌面应用启动
python -m src.macos.app
```

### 基本使用

```python
from src.evaluator import RuleEvaluator, TestCase
from src.test_dataset import create_sample_dataset
from src.benchmark import run_benchmark

# 1. 单条评估
evaluator = RuleEvaluator()
test_case = TestCase(
    id="test_001",
    input="什么是 Python？",
    expected_output="Python 是一种解释型、面向对象的高级编程语言"
)
results = evaluator.evaluate(test_case, "Python 是一种流行的编程语言")

# 2. 批量基准测试
dataset = create_sample_dataset()
result = run_benchmark(dataset, eval_type="rule", agent_caller=my_agent)
print(result.get_summary())
```

## 🛠️ 技术栈

| 层级 | 技术 |
|------|------|
| **核心评估** | Python 3.10+, dataclasses, enum, typing |
| **Web 服务** | FastAPI, Uvicorn, Pydantic |
| **桌面应用** | tkinter (macOS) |
| **数据处理** | JSON, Python 标准库 |
| **打包分发** | py2app (macOS) |

## 📐 评估维度

| 维度 | 英文 | 权重 | 说明 |
|------|------|------|------|
| 准确性 | Accuracy | 40% | 回答内容是否正确 |
| 相关性 | Relevance | 30% | 回答是否与问题相关 |
| 完整性 | Completeness | 20% | 回答是否覆盖了关键信息 |
| 连贯性 | Coherence | 10% | 回答是否通顺、逻辑连贯 |

> 权重可通过 `BenchmarkConfig.weights` 自定义配置。

## 📝 开发日志

- [x] 四维评估指标体系（v1.0.0）
- [x] 规则 / LLM / 组合三种评估策略（v1.0.0）
- [x] 测试数据集管理与 JSON 导入（v1.0.0）
- [x] 基准测试运行器与统计报告（v1.0.0）
- [x] FastAPI Web Dashboard（v1.0.0）
- [x] macOS 桌面应用（v1.0.0）
- [ ] 集成 DeepSeek / GPT API 进行真实 LLM 评估
- [ ] A/B 测试对比报告
- [ ] 评估结果可视化图表
- [ ] CI/CD 集成与自动化回归测试

## 📄 许可证

[MIT License](LICENSE)

---

<div align="center">

🔗 **GitHub**: [dirjaker/agent_evaluator](https://github.com/dirjaker/agent_evaluator)

⭐ 如果这个项目对你有帮助，请给一个 Star 支持一下！

</div>
