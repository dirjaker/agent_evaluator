"""
Benchmark 基准测试模块
=====================

运行评估基准测试，生成报告
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
import time
import json

from .evaluator import (
    TestCase, EvalReport, EvalResult, EvalMetric,
    RuleEvaluator, LLMEvaluator, CompositeEvaluator
)
from .test_dataset import TestDataset


@dataclass
class BenchmarkConfig:
    """基准测试配置"""
    name: str = "Default Benchmark"
    repetitions: int = 1  # 每个测试重复次数
    timeout: float = 30.0  # 超时时间（秒）
    weights: Dict[EvalMetric, float] = field(default_factory=lambda: {
        EvalMetric.ACCURACY: 0.4,
        EvalMetric.RELEVANCE: 0.3,
        EvalMetric.COMPLETENESS: 0.2,
        EvalMetric.COHERENCE: 0.1
    })


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    config: BenchmarkConfig
    reports: List[EvalReport] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    def add_report(self, report: EvalReport):
        """添加评估报告"""
        self.reports.append(report)

    def finish(self):
        """完成测试"""
        self.end_time = datetime.now()

    def get_summary(self) -> Dict[str, Any]:
        """获取测试摘要"""
        if not self.reports:
            return {"error": "没有测试结果"}

        total_score = sum(r.total_score for r in self.reports) / len(self.reports)
        avg_latency = sum(r.latency for r in self.reports) / len(self.reports)
        total_tokens = sum(r.tokens_used for r in self.reports)

        # 按难度统计
        difficulty_stats = {}
        for report in self.reports:
            diff = report.test_case.difficulty
            if diff not in difficulty_stats:
                difficulty_stats[diff] = {"count": 0, "total_score": 0}
            difficulty_stats[diff]["count"] += 1
            difficulty_stats[diff]["total_score"] += report.total_score

        for diff in difficulty_stats:
            stats = difficulty_stats[diff]
            stats["avg_score"] = stats["total_score"] / stats["count"]

        # 按指标统计
        metric_stats = {}
        for report in self.reports:
            for result in report.results:
                if result.metric.value not in metric_stats:
                    metric_stats[result.metric.value] = []
                metric_stats[result.metric.value].append(result.score)

        metric_avg = {k: sum(v)/len(v) for k, v in metric_stats.items()}

        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0

        return {
            "name": self.config.name,
            "total_cases": len(self.reports),
            "total_score": round(total_score, 3),
            "avg_latency": round(avg_latency, 2),
            "total_tokens": total_tokens,
            "duration": round(duration, 2),
            "difficulty_stats": difficulty_stats,
            "metric_avg": metric_avg
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.get_summary(),
            "reports": [r.to_dict() for r in self.reports]
        }


class BenchmarkRunner:
    """
    基准测试运行器

    执行评估基准测试
    """

    def __init__(
        self,
        config: BenchmarkConfig = None,
        evaluator=None,
        agent_caller: Callable = None
    ):
        self.config = config or BenchmarkConfig()
        self.evaluator = evaluator or RuleEvaluator()
        self.agent_caller = agent_caller or self._mock_agent

    def run(self, dataset: TestDataset) -> BenchmarkResult:
        """
        运行基准测试

        Args:
            dataset: 测试数据集

        Returns:
            测试结果
        """
        result = BenchmarkResult(config=self.config)

        cases = dataset.get_cases()
        print(f"开始运行基准测试: {self.config.name}")
        print(f"测试用例数: {len(cases)}")
        print("=" * 60)

        for i, test_case in enumerate(cases, 1):
            print(f"\n[{i}/{len(cases)}] 执行测试: {test_case.id}")

            # 重复测试
            for rep in range(self.config.repetitions):
                report = self._run_single_test(test_case)
                result.add_report(report)

                if rep == 0:  # 只打印第一次
                    print(f"  得分: {report.total_score:.2f}")
                    print(f"  延迟: {report.latency:.2f}s")

        result.finish()

        print("\n" + "=" * 60)
        print("测试完成!")
        summary = result.get_summary()
        print(f"平均得分: {summary['total_score']:.2f}")
        print(f"平均延迟: {summary['avg_latency']:.2f}s")

        return result

    def _run_single_test(self, test_case: TestCase) -> EvalReport:
        """执行单个测试"""
        start_time = time.time()

        # 调用 Agent
        actual_output = self.agent_caller(test_case.input)

        latency = time.time() - start_time

        # 评估
        eval_results = self.evaluator.evaluate(test_case, actual_output)

        # 创建报告
        report = EvalReport(
            test_case=test_case,
            actual_output=actual_output,
            results=eval_results,
            latency=latency,
            tokens_used=len(actual_output.split())  # 简单估算
        )

        report.calculate_total(self.config.weights)
        return report

    def _mock_agent(self, input_text: str) -> str:
        """模拟 Agent 调用"""
        # 实际项目中这里调用真实的 Agent
        return f"关于 '{input_text[:20]}...' 的回答：这是一个模拟的回答。"


def run_benchmark(
    dataset: TestDataset,
    eval_type: str = "rule",
    agent_caller: Callable = None
) -> BenchmarkResult:
    """
    运行基准测试的便捷函数

    Args:
        dataset: 测试数据集
        eval_type: 评估器类型
        agent_caller: Agent 调用函数

    Returns:
        测试结果
    """
    from .evaluator import create_evaluator

    config = BenchmarkConfig(name=f"{dataset.name} 基准测试")
    evaluator = create_evaluator(eval_type)

    runner = BenchmarkRunner(
        config=config,
        evaluator=evaluator,
        agent_caller=agent_caller
    )

    return runner.run(dataset)
