# Agent Evaluator — 技术文档

## 1. 项目概述

Agent Evaluator 是一个智能体评估框架，用于自动化评估 AI Agent 的输出质量。框架采用策略模式设计，支持规则评估、LLM 评估和组合评估三种策略，提供从单条评估到批量基准测试的完整工作流。

### 1.1 核心特性

- **多维度评估**：准确性、相关性、完整性、连贯性四维度量化打分
- **多种评估方法**：规则评估（快速确定）、LLM 评估（语义理解）、组合评估（融合策略）
- **测试数据集管理**：预置数据集、JSON 文件导入自定义数据集
- **基准测试**：自动化运行测试、按难度分组统计、生成多维报告
- **Web 管理面板**：FastAPI REST API + Web Dashboard
- **macOS 桌面应用**：tkinter GUI，内嵌 Web 视图

### 1.2 应用场景

- Agent Prompt 调优与迭代验证
- 不同模型/版本的 A/B 对比测试
- 代码变更后的回归测试
- 模型选型与性能评估

## 2. 架构设计

### 2.1 评估流程

```
测试数据集 (TestDataset)
    ↓
┌─────────────┐
│ Agent 调用  │  ← agent_caller 函数（可替换为任意 Agent）
└──────┬──────┘
       ↓
┌─────────────┐
│ 评估器      │
│ - Rule      │  ← 关键词匹配，快速确定
│ - LLM       │  ← LLM 语义评判
│ - Composite │  ← 加权融合多种评估器
└──────┬──────┘
       ↓
┌─────────────┐
│ 评估报告    │  ← EvalReport（各维度分数 + 加权总分）
└──────┬──────┘
       ↓
┌─────────────┐
│ 基准测试    │  ← BenchmarkResult（按难度/指标统计）
└─────────────┘
```

### 2.2 评估维度

| 维度 | 英文 | 权重 | 说明 |
|------|------|------|------|
| 准确性 | Accuracy | 40% | 回答内容是否正确（关键词匹配） |
| 相关性 | Relevance | 30% | 回答是否与问题相关（词汇重叠） |
| 完整性 | Completeness | 20% | 回答是否覆盖关键信息（长度比） |
| 连贯性 | Coherence | 10% | 回答是否通顺连贯（句子完整性） |

> 权重可通过 `BenchmarkConfig.weights` 自定义。缺失指标使用 0.1 作为兜底权重。

## 3. 模块详解

### 3.1 Evaluator 模块 (`src/evaluator.py`)

核心评估器模块，采用策略模式实现三种评估策略。

#### 数据模型

| 类 | 说明 |
|------|------|
| `EvalMetric` | 评估指标枚举（accuracy, relevance, completeness, coherence, latency, cost） |
| `EvalResult` | 单项评估结果（指标、分数、说明） |
| `TestCase` | 测试用例（id、输入、期望输出、难度、标签） |
| `EvalReport` | 评估报告（含加权总分计算） |

#### 评估器

**RuleEvaluator** — 基于规则的评估

```python
evaluator = RuleEvaluator()
results = evaluator.evaluate(test_case, actual_output)
```

- 准确性：期望输出与实际输出的关键词交集覆盖率
- 相关性：输入与输出的词汇重叠率（×2，上限 1.0）
- 完整性：输出长度与期望长度之比（上限 1.0）
- 连贯性：完整句子数 / 3（上限 1.0）

**LLMEvaluator** — 基于 LLM 的评估

```python
evaluator = LLMEvaluator(llm_caller=my_llm_function)
results = evaluator.evaluate(test_case, actual_output)
```

- 通过 Prompt 让 LLM 对输出质量进行语义级评判
- `llm_caller` 参数接受任意 Callable，可接入 DeepSeek、GPT-4 等
- 内置 `_mock_llm` 用于开发测试

**CompositeEvaluator** — 组合评估

```python
evaluator = CompositeEvaluator()
evaluator.add_evaluator(RuleEvaluator(), weight=0.6)
evaluator.add_evaluator(LLMEvaluator(), weight=0.4)
results = evaluator.evaluate(test_case, actual_output)
```

- 先按权重缩放各评估器分数
- 再对相同指标取算术平均
- 实现加权融合

#### 工厂函数

```python
from src.evaluator import create_evaluator
evaluator = create_evaluator("rule")     # 规则评估器
evaluator = create_evaluator("llm")      # LLM 评估器
evaluator = create_evaluator("composite") # 组合评估器
```

### 3.2 Test Dataset 模块 (`src/test_dataset.py`)

测试数据集管理模块。

```python
from src.test_dataset import create_sample_dataset, create_coding_dataset, load_dataset_from_json

# 使用预置数据集
dataset = create_sample_dataset()       # 通用问答测试集（6 用例）
dataset = create_coding_dataset()       # 编程能力测试集（2 用例）

# 过滤用例
cases = dataset.get_cases(difficulty="medium")
cases = dataset.get_cases(tags=["Python"])

# 从 JSON 文件加载自定义数据集
dataset = load_dataset_from_json("my_dataset.json")
```

### 3.3 Benchmark 模块 (`src/benchmark.py`)

基准测试运行与统计模块。

```python
from src.benchmark import run_benchmark, BenchmarkConfig, BenchmarkRunner
from src.test_dataset import create_sample_dataset

# 方式一：便捷函数
dataset = create_sample_dataset()
result = run_benchmark(dataset, eval_type="rule", agent_caller=my_agent)

# 方式二：自定义配置
config = BenchmarkConfig(
    name="我的基准测试",
    repetitions=3,
    weights={EvalMetric.ACCURACY: 0.5, EvalMetric.RELEVANCE: 0.5}
)
runner = BenchmarkRunner(config=config, evaluator=my_evaluator, agent_caller=my_agent)
result = runner.run(dataset)

# 查看结果
summary = result.get_summary()
print(f"平均得分: {summary['total_score']}")
print(f"按难度统计: {summary['difficulty_stats']}")
print(f"按指标统计: {summary['metric_avg']}")
```

### 3.4 Web 服务模块 (`src/web/app.py`)

基于 FastAPI 的 REST API 服务。

主要端点：

| 方法 | 路径 | 功能 |
|------|------|------|
| POST | `/api/evaluate` | 执行单条评估 |
| POST | `/api/benchmark` | 运行基准测试 |
| GET | `/api/datasets` | 列出可用数据集 |
| GET | `/api/stats` | 系统统计信息 |
| GET | `/` | Web 管理面板 |

```bash
# 启动服务
python -m src.web.app
# 访问 http://localhost:8004
```

### 3.5 macOS 桌面应用 (`src/macos/app.py`)

基于 tkinter 的桌面 GUI 应用，提供：

- 启动/停止内嵌 FastAPI 服务
- 一键打开浏览器访问 Web 面板
- 实时状态显示

```bash
python -m src.macos.app
```

## 4. 使用指南

### 4.1 快速开始

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
for r in results:
    print(f"{r.metric.value}: {r.score:.2f}")
```

### 4.2 运行基准测试

```python
from src.benchmark import run_benchmark
from src.test_dataset import create_sample_dataset

dataset = create_sample_dataset()

def my_agent(input_text):
    return f"回答：{input_text}"

result = run_benchmark(dataset, agent_caller=my_agent)
summary = result.get_summary()
```

### 4.3 自定义评估器

```python
from src.evaluator import RuleEvaluator

class MyEvaluator(RuleEvaluator):
    def _check_accuracy(self, expected, actual):
        # 自定义准确性检查逻辑
        return 1.0 if expected in actual else 0.0
```

### 4.4 接入真实 LLM

```python
import httpx
from src.evaluator import LLMEvaluator

def deepseek_caller(prompt: str) -> str:
    response = httpx.post(
        "https://api.deepseek.com/chat/completions",
        headers={"Authorization": "Bearer YOUR_API_KEY"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    )
    return response.json()["choices"][0]["message"]["content"]

evaluator = LLMEvaluator(llm_caller=deepseek_caller)
```

## 5. 设计决策

### 5.1 为什么需要多种评估方法？

| 方法 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 规则评估 | 快速、零成本、确定性强 | 不理解语义 | 基础测试、快速验证 |
| LLM 评估 | 语义理解强、评估质量高 | 成本高、速度慢 | 精细评估、最终验收 |
| 组合评估 | 兼顾速度和质量 | 配置复杂 | 生产环境推荐 |

### 5.2 权重设计

基于业务重要性分配权重：

- 准确性最重要（40%）：回答必须正确
- 相关性次之（30%）：回答必须切题
- 完整性再次（20%）：回答需要覆盖关键信息
- 连贯性最后（10%）：回答需要通顺可读

### 5.3 为什么选择策略模式？

策略模式让三种评估器遵循统一接口，可以随时切换或组合，符合开闭原则。新增评估策略只需实现 `evaluate()` 方法，无需修改已有代码。

## 6. 已知限制

- Web 服务使用内存存储，进程重启后数据丢失
- 规则评估器的算法较简单，仅做词级匹配
- LLM 评估器默认使用 mock，需手动接入真实 API
- 暂无单元测试覆盖

## 7. 后续计划

- [ ] 集成 DeepSeek / GPT API 进行真实 LLM 评估
- [ ] 添加更多评估指标（安全性、成本等）
- [ ] A/B 测试对比报告
- [ ] 评估结果可视化图表
- [ ] 数据持久化（SQLite）
- [ ] CI/CD 集成
