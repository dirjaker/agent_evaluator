"""
Test Dataset 测试数据集模块
==========================

提供预定义的测试用例和数据集管理功能
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json

from .evaluator import TestCase


@dataclass
class TestDataset:
    """测试数据集"""
    name: str
    description: str = ""
    test_cases: List[TestCase] = field(default_factory=list)

    def add_case(self, test_case: TestCase):
        """添加测试用例"""
        self.test_cases.append(test_case)

    def get_cases(self, difficulty: str = None, tags: List[str] = None) -> List[TestCase]:
        """获取测试用例（可过滤）"""
        cases = self.test_cases

        if difficulty:
            cases = [c for c in cases if c.difficulty == difficulty]

        if tags:
            cases = [c for c in cases if any(t in c.tags for t in tags)]

        return cases

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "case_count": len(self.test_cases),
            "cases": [c.to_dict() for c in self.test_cases]
        }


def create_sample_dataset() -> TestDataset:
    """创建示例数据集"""
    dataset = TestDataset(
        name="通用问答测试集",
        description="用于测试问答类 Agent 的基础数据集"
    )

    # 简单问答
    dataset.add_case(TestCase(
        id="qa_001",
        input="什么是 Python？",
        expected_output="Python 是一种解释型、面向对象的高级编程语言",
        tags=["基础", "编程"],
        difficulty="easy"
    ))

    dataset.add_case(TestCase(
        id="qa_002",
        input="解释什么是机器学习",
        expected_output="机器学习是人工智能的一个分支，通过算法让计算机从数据中学习规律",
        tags=["AI", "基础"],
        difficulty="easy"
    ))

    # 中等问题
    dataset.add_case(TestCase(
        id="qa_003",
        input="Python 中的 GIL 是什么？它有什么影响？",
        expected_output="GIL 是全局解释器锁，它限制了同一时刻只有一个线程执行 Python 字节码，影响多线程性能",
        tags=["Python", "进阶"],
        difficulty="medium"
    ))

    dataset.add_case(TestCase(
        id="qa_004",
        input="解释 RESTful API 的设计原则",
        expected_output="RESTful API 遵循无状态、统一接口、资源导向等原则，使用 HTTP 方法进行 CRUD 操作",
        tags=["Web", "架构"],
        difficulty="medium"
    ))

    # 困难问题
    dataset.add_case(TestCase(
        id="qa_005",
        input="比较 Transformer 和 RNN 在序列建模中的优缺点",
        expected_output="Transformer 支持并行计算、捕捉长距离依赖，但计算复杂度高；RNN 顺序处理、适合流式数据，但存在梯度消失问题",
        tags=["深度学习", "NLP"],
        difficulty="hard"
    ))

    dataset.add_case(TestCase(
        id="qa_006",
        input="设计一个高并发的秒杀系统需要考虑哪些方面？",
        expected_output="需要考虑：流量削峰、库存预扣、分布式锁、缓存策略、限流降级、异步处理等方面",
        tags=["系统设计", "高并发"],
        difficulty="hard"
    ))

    return dataset


def create_coding_dataset() -> TestDataset:
    """创建编程测试数据集"""
    dataset = TestDataset(
        name="编程能力测试集",
        description="测试 Agent 的代码生成和解释能力"
    )

    dataset.add_case(TestCase(
        id="code_001",
        input="用 Python 实现二分查找",
        expected_output="def binary_search(arr, target): left, right = 0, len(arr)-1 ...",
        tags=["算法", "Python"],
        difficulty="medium"
    ))

    dataset.add_case(TestCase(
        id="code_002",
        input="解释 Python 装饰器的原理和用法",
        expected_output="装饰器是一个接收函数作为参数的高阶函数，返回一个新的函数，使用 @ 语法糖",
        tags=["Python", "进阶"],
        difficulty="medium"
    ))

    return dataset


def load_dataset_from_json(file_path: str) -> TestDataset:
    """从 JSON 文件加载数据集"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    dataset = TestDataset(
        name=data.get("name", "Unknown"),
        description=data.get("description", "")
    )

    for case_data in data.get("cases", []):
        dataset.add_case(TestCase(
            id=case_data["id"],
            input=case_data["input"],
            expected_output=case_data["expected_output"],
            tags=case_data.get("tags", []),
            difficulty=case_data.get("difficulty", "medium")
        ))

    return dataset
