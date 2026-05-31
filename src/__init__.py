"""
Agent Evaluator
===============

智能体评估框架，用于自动化评估 Agent 的性能。

评估维度：
1. 准确性（Accuracy）：回答是否正确
2. 相关性（Relevance）：回答是否相关
3. 完整性（Completeness）：回答是否完整
4. 延迟（Latency）：响应时间
5. 成本（Cost）：Token 消耗

评估方法：
- 规则评估：基于预定义规则
- LLM 评估：使用 LLM 进行评判
- 人工评估：人工打分

作者：dirjaker
创建日期：2026-05-30
版本：1.0.0
"""

__version__ = "1.0.0"
__author__ = "dirjaker"
