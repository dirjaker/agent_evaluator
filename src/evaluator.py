"""
Evaluator 评估器模块
===================

实现多种评估策略：
- RuleEvaluator: 基于规则的评估
- LLMEvaluator: 基于 LLM 的评估
- CompositeEvaluator: 组合评估
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable
from enum import Enum
import time
import json


class EvalMetric(Enum):
    """评估指标"""
    ACCURACY = "accuracy"      # 准确性
    RELEVANCE = "relevance"    # 相关性
    COMPLETENESS = "completeness"  # 完整性
    COHERENCE = "coherence"    # 连贯性
    LATENCY = "latency"        # 延迟
    COST = "cost"              # 成本


@dataclass
class EvalResult:
    """评估结果"""
    metric: EvalMetric
    score: float  # 0-1
    explanation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric.value,
            "score": round(self.score, 3),
            "explanation": self.explanation
        }


@dataclass
class TestCase:
    """测试用例"""
    id: str
    input: str  # 用户输入
    expected_output: str  # 期望输出
    context: str = ""  # 上下文
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"  # easy, medium, hard

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "input": self.input[:100],
            "expected_output": self.expected_output[:100],
            "difficulty": self.difficulty,
            "tags": self.tags
        }


@dataclass
class EvalReport:
    """评估报告"""
    test_case: TestCase
    actual_output: str
    results: List[EvalResult] = field(default_factory=list)
    latency: float = 0.0
    tokens_used: int = 0
    total_score: float = 0.0

    def calculate_total(self, weights: Dict[EvalMetric, float] = None):
        """计算总分"""
        if not self.results:
            return 0.0

        if weights is None:
            # 默认权重
            weights = {
                EvalMetric.ACCURACY: 0.4,
                EvalMetric.RELEVANCE: 0.3,
                EvalMetric.COMPLETENESS: 0.2,
                EvalMetric.COHERENCE: 0.1
            }

        total = 0.0
        total_weight = 0.0
        for result in self.results:
            weight = weights.get(result.metric, 0.1)
            total += result.score * weight
            total_weight += weight

        self.total_score = total / total_weight if total_weight > 0 else 0.0
        return self.total_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_case_id": self.test_case.id,
            "total_score": round(self.total_score, 3),
            "latency": f"{self.latency:.2f}s",
            "tokens_used": self.tokens_used,
            "metrics": [r.to_dict() for r in self.results]
        }

    def summary(self) -> str:
        """生成摘要"""
        return f"""
测试用例: {self.test_case.id}
总分: {self.total_score:.2f}
延迟: {self.latency:.2f}s
Token: {self.tokens_used}
指标详情:
{chr(10).join([f"  {r.metric.value}: {r.score:.2f} - {r.explanation}" for r in self.results])}
"""


class RuleEvaluator:
    """
    基于规则的评估器

    使用预定义规则评估 Agent 输出
    """

    def __init__(self):
        self.rules: List[Callable] = []

    def add_rule(self, rule: Callable):
        """添加评估规则"""
        self.rules.append(rule)

    def evaluate(self, test_case: TestCase, actual_output: str) -> List[EvalResult]:
        """执行评估"""
        results = []

        # 准确性：检查关键词匹配
        accuracy = self._check_accuracy(test_case.expected_output, actual_output)
        results.append(EvalResult(
            metric=EvalMetric.ACCURACY,
            score=accuracy,
            explanation="基于关键词匹配的准确性评估"
        ))

        # 相关性：检查输入输出相关性
        relevance = self._check_relevance(test_case.input, actual_output)
        results.append(EvalResult(
            metric=EvalMetric.RELEVANCE,
            score=relevance,
            explanation="基于输入输出相关性评估"
        ))

        # 完整性：检查输出长度
        completeness = self._check_completeness(test_case.expected_output, actual_output)
        results.append(EvalResult(
            metric=EvalMetric.COMPLETENESS,
            score=completeness,
            explanation="基于输出完整性的评估"
        ))

        # 连贯性：检查输出连贯性
        coherence = self._check_coherence(actual_output)
        results.append(EvalResult(
            metric=EvalMetric.COHERENCE,
            score=coherence,
            explanation="基于输出连贯性的评估"
        ))

        return results

    def _check_accuracy(self, expected: str, actual: str) -> float:
        """检查准确性"""
        expected_words = set(expected.lower().split())
        actual_words = set(actual.lower().split())

        if not expected_words:
            return 1.0

        # 计算关键词匹配比例
        matches = expected_words.intersection(actual_words)
        return len(matches) / len(expected_words)

    def _check_relevance(self, input_text: str, output_text: str) -> float:
        """检查相关性"""
        input_words = set(input_text.lower().split())
        output_words = set(output_text.lower().split())

        if not input_words:
            return 1.0

        # 计算输入输出词汇重叠
        overlap = input_words.intersection(output_words)
        return min(len(overlap) / len(input_words) * 2, 1.0)

    def _check_completeness(self, expected: str, actual: str) -> float:
        """检查完整性"""
        expected_len = len(expected)
        actual_len = len(actual)

        if expected_len == 0:
            return 1.0

        # 长度比例，但不超过 1
        ratio = actual_len / expected_len
        return min(ratio, 1.0)

    def _check_coherence(self, text: str) -> float:
        """检查连贯性"""
        # 简单检查：是否有完整的句子
        sentences = text.split('。')
        complete_sentences = [s for s in sentences if len(s.strip()) > 5]

        if not complete_sentences:
            return 0.5

        return min(len(complete_sentences) / 3, 1.0)


class LLMEvaluator:
    """
    基于 LLM 的评估器

    使用 LLM 评估 Agent 输出质量
    """

    def __init__(self, llm_caller: Callable = None):
        self.llm_caller = llm_caller or self._mock_llm

    def evaluate(self, test_case: TestCase, actual_output: str) -> List[EvalResult]:
        """使用 LLM 评估"""
        prompt = self._build_prompt(test_case, actual_output)

        # 调用 LLM
        response = self.llm_caller(prompt)

        # 解析结果
        return self._parse_response(response)

    def _build_prompt(self, test_case: TestCase, actual_output: str) -> str:
        """构建评估提示"""
        return f"""请评估以下 AI Agent 的输出质量。

用户输入：{test_case.input}

期望输出：{test_case.expected_output}

实际输出：{actual_output}

请从以下维度评估（每项 0-1 分）：
1. 准确性：回答是否正确
2. 相关性：回答是否与问题相关
3. 完整性：回答是否完整
4. 连贯性：回答是否通顺连贯

请以 JSON 格式返回：
{{"accuracy": 0.0, "relevance": 0.0, "completeness": 0.0, "coherence": 0.0, "explanation": "评估说明"}}
"""

    def _mock_llm(self, prompt: str) -> str:
        """模拟 LLM 调用"""
        # 实际项目中这里调用真实的 LLM API
        return json.dumps({
            "accuracy": 0.8,
            "relevance": 0.9,
            "completeness": 0.7,
            "coherence": 0.85,
            "explanation": "模拟评估结果"
        })

    def _parse_response(self, response: str) -> List[EvalResult]:
        """解析 LLM 响应"""
        try:
            data = json.loads(response)
        except:
            data = {
                "accuracy": 0.5,
                "relevance": 0.5,
                "completeness": 0.5,
                "coherence": 0.5,
                "explanation": "解析失败"
            }

        return [
            EvalResult(EvalMetric.ACCURACY, data.get("accuracy", 0.5), data.get("explanation", "")),
            EvalResult(EvalMetric.RELEVANCE, data.get("relevance", 0.5), ""),
            EvalResult(EvalMetric.COMPLETENESS, data.get("completeness", 0.5), ""),
            EvalResult(EvalMetric.COHERENCE, data.get("coherence", 0.5), "")
        ]


class CompositeEvaluator:
    """
    组合评估器

    结合多种评估方法
    """

    def __init__(self):
        self.evaluators = []

    def add_evaluator(self, evaluator, weight: float = 1.0):
        """添加评估器"""
        self.evaluators.append((evaluator, weight))

    def evaluate(self, test_case: TestCase, actual_output: str) -> List[EvalResult]:
        """执行组合评估"""
        all_results = []

        for evaluator, weight in self.evaluators:
            results = evaluator.evaluate(test_case, actual_output)
            for result in results:
                result.score *= weight
                all_results.append(result)

        # 合并相同指标的结果
        merged = {}
        for result in all_results:
            if result.metric not in merged:
                merged[result.metric] = []
            merged[result.metric].append(result.score)

        # 计算平均分
        final_results = []
        for metric, scores in merged.items():
            avg_score = sum(scores) / len(scores)
            final_results.append(EvalResult(
                metric=metric,
                score=avg_score,
                explanation=f"综合 {len(scores)} 个评估器的结果"
            ))

        return final_results


def create_evaluator(eval_type: str = "rule") -> Any:
    """
    创建评估器的工厂函数

    Args:
        eval_type: 评估器类型 (rule, llm, composite)

    Returns:
        评估器实例
    """
    if eval_type == "rule":
        return RuleEvaluator()
    elif eval_type == "llm":
        return LLMEvaluator()
    elif eval_type == "composite":
        return CompositeEvaluator()
    else:
        raise ValueError(f"未知的评估器类型: {eval_type}")
