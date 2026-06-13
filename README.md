<div align="center">

# 📊 Agent Evaluator

### Agent 性能评估框架

[![评估维度](https://img.shields.io/badge/评估维度-5+-blue?style=flat-square)]()
[![指标](https://img.shields.io/badge/指标-10+-green?style=flat-square)]()
[![框架](https://img.shields.io/badge/框架-Pydantic-orange?style=flat-square)]()
[![更新](https://img.shields.io/badge/更新-2025.06-red?style=flat-square)]()

*多维度 Agent 评估 · 响应质量 · 安全性 · 成本分析 · 自动化测试*

</div>

---

> 智能体评估框架 - 自动化评估 AI Agent 的性能

## ✨ 特性

- 📏 **多维度评估**：准确性、相关性、完整性、连贯性
- 🔧 **多种评估方法**：规则评估、LLM 评估、组合评估
- 📦 **测试数据集管理**：预定义数据集、自定义数据集
- 📊 **基准测试**：自动化运行测试、生成报告

## 🚀 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/dirjaker/agent_evaluator.git
cd agent_evaluator

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 基础用法

```python
from src.evaluator import RuleEvaluator, TestCase
from src.test_dataset import create_sample_dataset

# 创建评估器
evaluator = RuleEvaluator()

# 创建测试用例
test_case = TestCase(
    id="test_001",
    input="什么是 Python？",
    expected_output="Python 是一种编程语言"
)

# 评估
results = evaluator.evaluate(test_case, "Python 是一种流行的编程语言")

for result in results:
    print(f"{result.metric.value}: {result.score:.2f}")
```

## 📁 项目结构

```
agent_evaluator/
├── src/
│   ├── __init__.py       # 包初始化
│   ├── evaluator.py      # 评估器实现
│   ├── test_dataset.py   # 测试数据集
│   └── benchmark.py      # 基准测试
├── examples/
│   └── eval_demo.py      # 评估演示
├── TECHNICAL_DOC.md      # 技术文档
├── DIRECTION.md          # 方向指引
├── VERSION.md            # 版本记录
├── requirements.txt      # 依赖列表
└── README.md             # 项目说明
```

## 📏 评估维度

| 维度 | 说明 | 权重 |
|------|------|------|
| **Accuracy** | 回答是否正确 | 40% |
| **Relevance** | 回答是否相关 | 30% |
| **Completeness** | 回答是否完整 | 20% |
| **Coherence** | 回答是否连贯 | 10% |

## 🔧 评估方法

### 1. 规则评估 (RuleEvaluator)

基于预定义规则评估，快速、确定性强。

```python
from src.evaluator import RuleEvaluator

evaluator = RuleEvaluator()
results = evaluator.evaluate(test_case, actual_output)
```

### 2. LLM 评估 (LLMEvaluator)

使用 LLM 进行智能评估。

```python
from src.evaluator import LLMEvaluator

evaluator = LLMEvaluator(llm_caller=my_llm_function)
results = evaluator.evaluate(test_case, actual_output)
```

### 3. 组合评估 (CompositeEvaluator)

结合多种评估方法。

```python
from src.evaluator import CompositeEvaluator, RuleEvaluator, LLMEvaluator

evaluator = CompositeEvaluator()
evaluator.add_evaluator(RuleEvaluator(), weight=0.6)
evaluator.add_evaluator(LLMEvaluator(), weight=0.4)
```

## 📊 运行基准测试

```python
from src.benchmark import run_benchmark
from src.test_dataset import create_sample_dataset

# 创建数据集
dataset = create_sample_dataset()

# 定义 Agent
def my_agent(input_text):
    return f"回答：{input_text}"

# 运行测试
result = run_benchmark(dataset, agent_caller=my_agent)

# 打印摘要
summary = result.get_summary()
print(f"平均得分: {summary['total_score']:.2f}")
```

## 📦 测试数据集

### 预定义数据集

```python
from src.test_dataset import create_sample_dataset, create_coding_dataset

# 通用问答数据集
qa_dataset = create_sample_dataset()

# 编程能力数据集
code_dataset = create_coding_dataset()
```

### 自定义数据集

```python
from src.test_dataset import TestDataset
from src.evaluator import TestCase

dataset = TestDataset(name="我的测试集")
dataset.add_case(TestCase(
    id="custom_001",
    input="自定义问题",
    expected_output="期望答案"
))
```

## 📊 运行示例

```bash
python examples/eval_demo.py
```

## 🎯 应用场景

- 🧪 **性能测试**：评估 Agent 的回答质量
- 🔄 **A/B 测试**：对比不同 Agent 版本
- 🔁 **回归测试**：确保更新不降低性能
- 📈 **模型选型**：选择最佳模型

## 📚 文档

- [技术文档](TECHNICAL_DOC.md) - 架构设计、模块详解
- [方向指引](DIRECTION.md) - 项目规划、学习路径
- [版本记录](VERSION.md) - 更新日志

## Web 评估面板

提供基于 FastAPI 的 Web 评估面板，可通过浏览器执行评估、运行基准测试和查看历史记录。

```bash
# 启动评估面板
python src/web/app.py

# 访问 Dashboard
# http://localhost:8004
```

### Web API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/evaluate` | POST | 执行单个评估 |
| `/api/evaluations` | GET | 获取评估历史 |
| `/api/benchmark` | POST | 运行基准测试 |
| `/api/benchmarks` | GET | 获取基准测试历史 |
| `/api/datasets` | GET | 列出可用数据集 |
| `/api/datasets/{name}` | GET | 获取数据集详情 |
| `/api/stats` | GET | 获取统计信息 |

## macOS 桌面应用

提供基于 tkinter 的本地桌面窗口，可一键启动 Web 服务。

```bash
python src/macos/app.py
```

## 打包 macOS .app

```bash
pip install py2app
python packaging/py2app_setup.py py2app
# 产出: dist/Agent评估框架.app
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

## 📄 License

MIT License

