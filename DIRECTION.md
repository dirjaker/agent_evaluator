# Agent Evaluator 项目方向指引

## 🎯 项目定位

Agent Evaluator 是一个**智能体评估学习项目**，目的是：
1. 理解 Agent 评估的方法论
2. 掌握自动化测试技术
3. 学习基准测试设计
4. 为面试提供可讲解的项目经验

---

## 📚 学习路径

### 阶段一：评估基础（Week 1）
- [x] 理解评估维度（准确性、相关性等）
- [x] 实现规则评估器
- [x] 创建测试数据集

### 阶段二：评估方法（Week 2）
- [x] 实现 LLM 评估器
- [x] 实现组合评估器
- [x] 设计评估权重

### 阶段三：基准测试（Week 3）
- [x] 实现基准测试框架
- [x] 生成测试报告
- [x] 统计分析功能

### 阶段四：真实集成（Week 4+）
- [ ] 集成 DeepSeek API
- [ ] 添加更多评估指标
- [ ] 实现 A/B 测试框架

---

## 🎓 面试要点

### 核心概念
1. **评估维度**：如何全面评估一个 Agent？
2. **评估方法**：规则 vs LLM vs 组合评估
3. **基准测试**：如何设计公平的测试？
4. **结果分析**：如何解读评估结果？

### 常见问题

**Q: 为什么需要 Agent 评估？**
> 评估是改进的基础。没有评估就无法：
> - 知道 Agent 的真实能力
> - 比较不同方案的优劣
> - 发现需要改进的地方

**Q: 如何选择评估方法？**
> - 规则评估：快速、确定性强，适合基础测试
> - LLM 评估：更智能，能理解语义，但成本高
> - 组合评估：平衡速度和准确性

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

---

## 🔗 技术关联

### 与其他项目的关系

```
agent_evaluator
├── 评估 agent_platform（Agent 性能）
├── 评估 multi_agent_crew（团队协作）
├── 评估 agent_memory_system（记忆效果）
└── 使用 knowledge_graph 提供知识
```

### 技术栈

- **核心**：Python 3.8+, dataclasses
- **可选**：pandas, matplotlib（数据可视化）
- **LLM**：DeepSeek API（真实评估）

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

### 博客/教程
- LLM 评估方法综述
- RAG 系统评估
- Agent 评估最佳实践

---

## ⚡ 快速命令

```bash
# 运行示例
python examples/eval_demo.py

# 测试代码
python -c "from src.evaluator import RuleEvaluator; print('OK')"
```
