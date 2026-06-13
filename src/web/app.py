"""
Agent Evaluator - Web Dashboard
FastAPI 服务，暴露评估框架的 REST API
"""

import sys
import uuid
from pathlib import Path
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# 确保项目根目录在 sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ============================================================
# 初始化
# ============================================================

app = FastAPI(title="Agent Evaluator", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# 导入核心模块
from src.evaluator import (
    RuleEvaluator, LLMEvaluator, CompositeEvaluator,
    TestCase, EvalMetric, EvalResult, EvalReport,
    create_evaluator,
)
from src.test_dataset import (
    TestDataset, create_sample_dataset, create_coding_dataset,
)
from src.benchmark import (
    BenchmarkConfig, BenchmarkRunner, BenchmarkResult, run_benchmark,
)

# 存储运行结果
benchmark_results: list[dict] = []
evaluation_history: list[dict] = []


# ============================================================
# 请求模型
# ============================================================

class EvaluateRequest(BaseModel):
    test_id: str
    input_text: str
    expected_output: str
    actual_output: str
    eval_type: str = "rule"
    difficulty: str = "medium"
    tags: list[str] = []


class BenchmarkRunRequest(BaseModel):
    dataset_name: str = "sample"
    eval_type: str = "rule"
    repetitions: int = 1
    agent_output: Optional[str] = None


class TestCaseRequest(BaseModel):
    id: str
    input: str
    expected_output: str
    difficulty: str = "medium"
    tags: list[str] = []


# ============================================================
# API 路由
# ============================================================

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@app.get("/api/stats")
async def get_stats():
    """获取统计信息"""
    return {
        "total_evaluations": len(evaluation_history),
        "total_benchmarks": len(benchmark_results),
        "available_metrics": [m.value for m in EvalMetric],
        "available_evaluators": ["rule", "llm", "composite"],
        "available_datasets": ["sample", "coding"],
    }


# ---- 评估 ----

@app.post("/api/evaluate")
async def evaluate(request: EvaluateRequest):
    """执行单个评估"""
    test_case = TestCase(
        id=request.test_id,
        input=request.input_text,
        expected_output=request.expected_output,
        difficulty=request.difficulty,
        tags=request.tags,
    )

    evaluator = create_evaluator(request.eval_type)
    results = evaluator.evaluate(test_case, request.actual_output)

    report = EvalReport(
        test_case=test_case,
        actual_output=request.actual_output,
        results=results,
        latency=0.0,
        tokens_used=len(request.actual_output.split()),
    )
    report.calculate_total()

    record = {
        "id": str(uuid.uuid4())[:8],
        "test_id": request.test_id,
        "eval_type": request.eval_type,
        "total_score": round(report.total_score, 3),
        "metrics": [r.to_dict() for r in results],
        "timestamp": datetime.now().isoformat(),
    }
    evaluation_history.append(record)

    return record


@app.get("/api/evaluations")
async def list_evaluations(limit: int = 50):
    """获取评估历史"""
    return {"evaluations": evaluation_history[-limit:], "total": len(evaluation_history)}


@app.post("/api/evaluations/clear")
async def clear_evaluations():
    """清空评估历史"""
    evaluation_history.clear()
    return {"status": "cleared"}


# ---- 基准测试 ----

@app.post("/api/benchmark")
async def run_benchmark_api(request: BenchmarkRunRequest):
    """运行基准测试"""
    # 选择数据集
    if request.dataset_name == "coding":
        dataset = create_coding_dataset()
    else:
        dataset = create_sample_dataset()

    # 创建 Agent 调用函数
    if request.agent_output:
        def agent_caller(input_text: str) -> str:
            return request.agent_output
    else:
        def agent_caller(input_text: str) -> str:
            return f"关于 '{input_text[:30]}' 的回答: 这是一个模拟的 Agent 回答。"

    config = BenchmarkConfig(
        name=f"{dataset.name} 基准测试",
        repetitions=request.repetitions,
    )

    evaluator = create_evaluator(request.eval_type)
    runner = BenchmarkRunner(
        config=config,
        evaluator=evaluator,
        agent_caller=agent_caller,
    )

    result = runner.run(dataset)

    record = {
        "id": str(uuid.uuid4())[:8],
        "summary": result.get_summary(),
        "reports": [r.to_dict() for r in result.reports],
        "timestamp": datetime.now().isoformat(),
    }
    benchmark_results.append(record)

    return record


@app.get("/api/benchmarks")
async def list_benchmarks(limit: int = 20):
    """获取基准测试历史"""
    return {"benchmarks": benchmark_results[-limit:], "total": len(benchmark_results)}


@app.post("/api/benchmarks/clear")
async def clear_benchmarks():
    """清空基准测试历史"""
    benchmark_results.clear()
    return {"status": "cleared"}


# ---- 数据集 ----

@app.get("/api/datasets")
async def list_datasets():
    """列出可用数据集"""
    sample = create_sample_dataset()
    coding = create_coding_dataset()
    return {
        "datasets": [
            {"name": "sample", "display_name": sample.name, "description": sample.description, "cases": len(sample.test_cases)},
            {"name": "coding", "display_name": coding.name, "description": coding.description, "cases": len(coding.test_cases)},
        ]
    }


@app.get("/api/datasets/{name}")
async def get_dataset(name: str):
    """获取数据集详情"""
    if name == "coding":
        dataset = create_coding_dataset()
    elif name == "sample":
        dataset = create_sample_dataset()
    else:
        raise HTTPException(404, f"数据集不存在: {name}")
    return dataset.to_dict()


# ============================================================
# Web UI
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def web_ui():
    html_path = Path(__file__).parent / "static" / "index.html"
    return html_path.read_text(encoding="utf-8")


# ============================================================
# 启动入口
# ============================================================

def run_server(host: str = "0.0.0.0", port: int = 8004):
    import uvicorn
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    run_server()
