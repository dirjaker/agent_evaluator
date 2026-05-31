# Agent Evaluator - 技术文档

## 1. 项目概述

Agent Evaluator 是一个智能体评估框架，用于自动化评估 AI Agent 的性能。

### 1.1 核心特性

- **多维度评估**：准确性、相关性、完整性、连贯性
- **多种评估方法**：规则评估、LLM 评估、组合评估
- **测试数据集管理**：预定义数据集、自定义数据集
- **基准测试**：自动化运行测试、生成报告

### 1.2 应用场景

- Agent 性能测试
- A/B 测试对比
- 回归测试
- 模型选型

## 2. 架构设计

### 2.1 评估流程

```
测试数据集
    ↓
┌─────────────┐
│ Agent 调用  │
└──────┬──────┘
       ↓
┌─────────────┐
│ 评估器      │
│ - Rule      │
│ - LLM       │
│ - Composite │
└──────┬──────┘
       ↓
┌─────────────┐
│ 评估报告    │
└─────────────┘
```

### 2.2 评估维度

| 维度 | 说明 | 权重 |
|------|------|------|
| Accuracy | 回答是否正确 | 40% |
| Relevance | 回答是否相关 | 30% |
| Completeness | 回答是否完整 | 20% |
| Coherence | 回答是否连贯 | 10% |

## 3. 模块详解

### 3.1 Evaluator 模块 (`evaluator.py`)

#### 核心类

**RuleEvaluator** - 规则评估
```python
evaluator = RuleEvaluator()
results = evaluator.evaluate(test_case, actual_output)
```

**LLMEvaluator** - LLM 评估
```python
evaluator = LLMEvaluator(llm_caller=my_llm)
results = evaluator.evaluate(test_case, actual_output)
```

**CompositeEvaluator** - 组合评估
```python
evaluator = CompositeEvaluator()
evaluator.add_evaluator(RuleEvaluator(), weight=0.6)
evaluator.add_evaluator(LLMEvaluator(), weight=0.4)
```

### 3.2 Test Dataset 模块 (`test_dataset.py`)

测试数据集管理：
```python
dataset = create_sample_dataset()
cases = dataset.get_cases(difficulty="medium")
```

### 3.3 Benchmark 模块 (`benchmark.py`)

基准测试运行：
```python
result = run_benchmark(dataset, eval_type="rule", agent_caller=my_agent)
summary = result.get_summary()
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
```

### 4.2 运行基准测试

```python
from src.benchmark import run_benchmark
from src.test_dataset import create_sample_dataset

dataset = create_sample_dataset()

def my_agent(input_text):
    return f"回答：{input_text}"

result = run_benchmark(dataset, agent_caller=my_agent)
```

### 4.3 自定义评估器

```python
from src.evaluator import RuleEvaluator, EvalResult, EvalMetric

class MyEvaluator(RuleEvaluator):
    def _check_accuracy(self, expected, actual):
        # 自定义准确性检查逻辑
        return 1.0 if expected in actual else 0.0
```

## 5. 设计决策

### 5.1 为什么需要多种评估方法？

- **规则评估**：快速、确定性强，适合基础测试
- **LLM 评估**：更智能，能理解语义，但成本高
- **组合评估**：平衡速度和准确性

### 5.2 权重设计

基于重要性分配权重：
- 准确性最重要（40%）
- 相关性次之（30%）
- 完整性再次（20%）
- 连贯性最后（10%）

## 6. 扩展点

### 6.1 添加新的评估指标

在 `EvalMetric` 枚举中添加新指标。

### 6.2 集成真实 LLM

替换 `LLMEvaluator._mock_llm` 方法。

### 6.3 添加持久化

将测试结果保存到数据库。

## 7. 已知限制

- 使用模拟 LLM
- 评估规则较简单
- 无可视化界面

## 8. 后续计划

- [ ] 集成 DeepSeek API
- [ ] 添加更多评估指标
- [ ] 实现 A/B 测试框架
- [ ] 添加 Web UI
