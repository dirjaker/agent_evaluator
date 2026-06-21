# Agent Evaluator 项目方向指引

## 🎯 项目定位

Agent Evaluator 是一个**智能体评估框架项目**，目标是：

1. 提供一套**开箱即用的 AI Agent 评估工具**
2. 支持多种评估策略（规则 / LLM / 组合），满足不同场景需求
3. 提供基准测试与统计分析能力，支撑 Agent 迭代优化
4. 为面试提供可深入讲解的项目经验

---

## 🏗️ 架构设计原则

### 策略模式

三种评估器遵循统一的 `evaluate(test_case, actual_output) -> List[EvalResult]` 接口，可随时切换或组合。

### 工厂模式 + 依赖注入

- `create_evaluator()` 集中创建逻辑
- `LLMEvaluator` 和 `BenchmarkRunner` 通过参数注入外部依赖

### 核心逻辑零外部依赖

核心评估模块仅依赖 Python 标准库，便于集成到任意项目。

---

## 📚 学习路径

### 阶段一：评估基础（Week 1）

- [x] 理解评估维度（准确性、相关性、完整性、连贯性）
- [x] 实现规则评估器
- [x] 创建测试数据集

### 阶段二：评估方法（Week 2）

- [x] 实现 LLM 评估器
- [x] 实现组合评估器
- [x] 设计评估权重体系

### 阶段三：基准测试（Week 3）

- [x] 实现基准测试框架
- [x] 生成测试报告
- [x] 多维统计分析（按难度、按指标）

### 阶段四：应用层（Week 4）

- [x] FastAPI Web Dashboard
- [x] macOS 桌面应用
- [x] JSON 数据集导入

### 阶段五：真实集成（Week 5+）

- [ ] 集成 DeepSeek / GPT API
- [ ] 添加更多评估指标
- [ ] A/B 测试对比报告
- [ ] 数据持久化

---

## 🎓 面试要点

### 核心概念

1. **评估维度**：如何全面评估一个 Agent？
2. **评估方法**：规则 vs LLM vs 组合评估的优劣对比
3. **策略模式**：为什么选择策略模式？如何扩展？
4. **基准测试**：如何设计公平的测试？如何统计分析？
5. **结果解读**：如何从评估结果中发现 Agent 的薄弱环节？

### 常见问题

**Q: 为什么需要 Agent 评估？**

> 评估是改进的基础。没有评估就无法知道 Agent 的真实能力、比较不同方案的优劣、发现需要改进的地方。

**Q: 如何选择评估方法？**

> - 规则评估：快速、确定性强，适合基础测试和快速验证
> - LLM 评估：语义理解强，适合精细评估，但成本高
> - 组合评估：推荐方案，兼顾速度和质量

**Q: 如何设计好的测试用例？**

> 1. 覆盖不同难度（简单、中等、困难）
> 2. 覆盖不同场景（问答、推理、创作）
> 3. 有足够的数量（统计意义）
> 4. 有明确的评判标准

**Q: 如何解读评估结果？**

> - 看总分：整体表现
> - 看分项：哪个维度需要改进
> - 看分布：不同难度的表现差异
> - 看趋势：多次测试的变化

**Q: CompositeEvaluator 的融合策略是什么？**

> 采用"权重缩放 + 同指标取均值"的两步策略，比直接加权平均更灵活。

---

## 🔗 技术关联

### 与其他项目的关系

```
agent_evaluator
├── 可评估 agent_platform（Agent 性能）
├── 可评估 multi_agent_crew（团队协作）
├── 可评估 agent_memory_system（记忆效果）
└── 可使用 knowledge_graph 提供知识
```

### 技术栈

- **核心**：Python 3.10+, dataclasses, enum, typing
- **Web 服务**：FastAPI, Uvicorn, Pydantic
- **桌面应用**：tkinter (macOS)
- **打包**：py2app
- **外部依赖**：httpx, pydantic（Web 服务用）

---

## 📖 参考资源

### 论文

- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685)
- [Chatbot Arena](https://arxiv.org/abs/2306.05685)
- [MT-Bench](https://arxiv.org/abs/2306.05685)

### 开源项目

- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- [LangSmith](https://github.com/langchain-ai/langsmith)
- [Ragas](https://github.com/explodinggradients/ragas)

### 技术文档

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Python dataclasses](https://docs.python.org/3/library/dataclasses.html)

---

## ⚡ 快速命令

```bash
# 运行评估演示
python examples/eval_demo.py

# 启动 Web 服务
python -m src.web.app

# 启动 macOS 桌面应用
python -m src.macos.app

# 验证核心模块
python -c "from src.evaluator import RuleEvaluator; print('OK')"
```
