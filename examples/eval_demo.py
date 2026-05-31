"""
示例：评估器基础用法
==================

演示如何使用评估框架评估 Agent
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.evaluator import (
    RuleEvaluator, LLMEvaluator, CompositeEvaluator,
    TestCase, EvalMetric
)
from src.test_dataset import create_sample_dataset
from src.benchmark import run_benchmark


def demo_rule_evaluator():
    """规则评估器演示"""
    print("=" * 60)
    print("示例1：规则评估器")
    print("=" * 60)

    # 创建评估器
    evaluator = RuleEvaluator()

    # 创建测试用例
    test_case = TestCase(
        id="test_001",
        input="什么是 Python？",
        expected_output="Python 是一种解释型、面向对象的高级编程语言",
        difficulty="easy"
    )

    # 模拟 Agent 输出
    actual_output = "Python 是一种流行的编程语言，它是解释型的，支持面向对象编程。"

    # 执行评估
    results = evaluator.evaluate(test_case, actual_output)

    print(f"\n测试用例: {test_case.id}")
    print(f"输入: {test_case.input}")
    print(f"期望: {test_case.expected_output}")
    print(f"实际: {actual_output}")
    print(f"\n评估结果:")
    for result in results:
        print(f"  {result.metric.value}: {result.score:.2f} - {result.explanation}")


def demo_llm_evaluator():
    """LLM 评估器演示"""
    print("\n" + "=" * 60)
    print("示例2：LLM 评估器")
    print("=" * 60)

    # 创建评估器
    evaluator = LLMEvaluator()

    # 创建测试用例
    test_case = TestCase(
        id="test_002",
        input="解释机器学习",
        expected_output="机器学习是人工智能的分支，通过算法从数据中学习",
        difficulty="medium"
    )

    # 模拟 Agent 输出
    actual_output = "机器学习是 AI 的一个重要分支，它让计算机能够从数据中自动学习规律和模式。"

    # 执行评估
    results = evaluator.evaluate(test_case, actual_output)

    print(f"\n测试用例: {test_case.id}")
    print(f"输入: {test_case.input}")
    print(f"\n评估结果:")
    for result in results:
        print(f"  {result.metric.value}: {result.score:.2f}")


def demo_composite_evaluator():
    """组合评估器演示"""
    print("\n" + "=" * 60)
    print("示例3：组合评估器")
    print("=" * 60)

    # 创建组合评估器
    evaluator = CompositeEvaluator()
    evaluator.add_evaluator(RuleEvaluator(), weight=0.6)
    evaluator.add_evaluator(LLMEvaluator(), weight=0.4)

    # 测试用例
    test_case = TestCase(
        id="test_003",
        input="什么是 GIL？",
        expected_output="GIL 是 Python 的全局解释器锁",
        difficulty="medium"
    )

    actual_output = "GIL（Global Interpreter Lock）是 Python 的全局解释器锁，它限制同一时刻只有一个线程执行 Python 字节码。"

    # 执行评估
    results = evaluator.evaluate(test_case, actual_output)

    print(f"\n测试用例: {test_case.id}")
    print(f"\n评估结果:")
    for result in results:
        print(f"  {result.metric.value}: {result.score:.2f}")


def demo_benchmark():
    """基准测试演示"""
    print("\n" + "=" * 60)
    print("示例4：基准测试")
    print("=" * 60)

    # 创建数据集
    dataset = create_sample_dataset()

    # 定义模拟 Agent
    def mock_agent(input_text: str) -> str:
        """模拟 Agent"""
        return f"关于 '{input_text[:15]}...' 的回答：这是模拟的详细解答。"

    # 运行基准测试
    result = run_benchmark(
        dataset=dataset,
        eval_type="rule",
        agent_caller=mock_agent
    )

    # 打印摘要
    print("\n测试摘要:")
    summary = result.get_summary()
    print(f"  总用例数: {summary['total_cases']}")
    print(f"  平均得分: {summary['total_score']:.2f}")
    print(f"  平均延迟: {summary['avg_latency']:.2f}s")


if __name__ == "__main__":
    demo_rule_evaluator()
    demo_llm_evaluator()
    demo_composite_evaluator()
    demo_benchmark()
