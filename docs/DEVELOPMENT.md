# Agent Evaluator — 开发环境搭建指南

本文档面向开发者，详细说明如何搭建 Agent Evaluator 的本地开发环境。

---

## 1. 环境要求

| 依赖 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 推荐 3.12 |
| Conda | 可选 | 推荐用于虚拟环境管理 |
| Git | 2.0+ | 版本管理 |
| macOS（可选） | 10.15+ | 桌面应用和 py2app 打包需要 |

## 2. 快速搭建

### 2.1 克隆项目

```bash
git clone https://github.com/dirjaker/agent_evaluator.git
cd agent_evaluator
git checkout dev
```

### 2.2 创建虚拟环境

**方式一：Conda（推荐）**

```bash
conda create -n agent_evaluator python=3.12 -y
conda activate agent_evaluator
```

**方式二：venv**

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
```

### 2.3 安装依赖

```bash
pip install -r requirements.txt
```

当前 `requirements.txt` 内容：

```
httpx==0.28.1
pydantic==2.13.4
pydantic_core==2.46.4
typing_extensions==4.15.0
```

> 核心评估模块（`src/evaluator.py`, `src/test_dataset.py`, `src/benchmark.py`）仅依赖 Python 标准库，无需安装额外包即可使用。

### 2.4 验证安装

```bash
# 验证核心模块可导入
python -c "from src.evaluator import RuleEvaluator, TestCase; print('✅ 核心模块正常')"

# 验证 Web 模块
python -c "from src.web.app import app; print('✅ Web 模块正常')"

# 运行评估演示
python examples/eval_demo.py
```

## 3. 开发工作流

### 3.1 项目结构

```
agent_evaluator/
├── src/                    # 核心源码
│   ├── __init__.py         # 包初始化
│   ├── evaluator.py        # 评估器模块
│   ├── test_dataset.py     # 数据集模块
│   ├── benchmark.py        # 基准测试模块
│   ├── web/                # Web 服务
│   │   ├── app.py          # FastAPI 应用
│   │   └── static/         # 前端静态文件
│   └── macos/              # macOS 桌面应用
│       └── app.py          # tkinter GUI
├── examples/               # 示例代码
│   └── eval_demo.py        # 评估演示脚本
├── packaging/              # 打包脚本
│   └── py2app_setup.py     # macOS 打包配置
├── docs/                   # 项目文档
├── assets/                 # 静态资源（banner 等）
├── requirements.txt        # Python 依赖
└── README.md
```

### 3.2 运行 Web 服务

```bash
# 启动 FastAPI 服务（默认端口 8004）
python -m src.web.app

# 访问 Web 面板
# http://localhost:8004
```

API 端点一览：

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | `/api/health` | 健康检查 |
| GET | `/api/stats` | 系统统计 |
| POST | `/api/evaluate` | 单条评估 |
| GET | `/api/evaluations` | 评估历史 |
| POST | `/api/benchmark` | 基准测试 |
| GET | `/api/datasets` | 数据集列表 |
| GET | `/` | Web 管理面板 |

### 3.3 运行 macOS 桌面应用

```bash
# 仅 macOS 可用
python -m src.macos.app
```

### 3.4 运行评估演示

```bash
python examples/eval_demo.py
```

该脚本演示了：
1. 规则评估器基本用法
2. LLM 评估器基本用法
3. 组合评估器配置
4. 基准测试运行

## 4. 代码规范

### 4.1 编码风格

- 遵循 PEP 8 规范
- 使用类型注解（Type Hints）
- 数据类使用 `dataclass` 装饰器
- 公共方法和类必须有 docstring

### 4.2 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 类名 | PascalCase | `RuleEvaluator`, `TestCase` |
| 函数名 | snake_case | `create_evaluator()`, `run_benchmark()` |
| 常量 | UPPER_SNAKE_CASE | `CORS_ORIGINS` |
| 私有方法 | `_前缀` | `_check_accuracy()`, `_mock_llm()` |

### 4.3 类型注解

```python
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass, field

def evaluate(self, test_case: TestCase, actual_output: str) -> List[EvalResult]:
    ...
```

## 5. 扩展开发

### 5.1 添加新评估指标

1. 在 `src/evaluator.py` 的 `EvalMetric` 枚举中添加新指标：

```python
class EvalMetric(Enum):
    SAFETY = "safety"  # 新增
```

2. 在 `RuleEvaluator.evaluate()` 中添加计算逻辑：

```python
def _check_safety(self, output: str) -> float:
    # 实现安全性检查
    ...
```

3. 如果使用 LLM 评估器，更新 `_build_prompt()` 中的评分维度。

### 5.2 添加新评估策略

实现统一接口即可：

```python
class MyEvaluator:
    def evaluate(self, test_case: TestCase, actual_output: str) -> List[EvalResult]:
        # 实现评估逻辑
        ...
```

然后在 `create_evaluator()` 工厂函数中注册。

### 5.3 添加新数据集

在 `src/test_dataset.py` 中添加工厂函数：

```python
def create_my_dataset() -> TestDataset:
    dataset = TestDataset(name="我的测试集", description="...")
    dataset.add_case(TestCase(...))
    return dataset
```

或使用 JSON 文件：

```json
{
  "name": "自定义测试集",
  "description": "...",
  "cases": [
    {
      "id": "test_001",
      "input": "用户输入",
      "expected_output": "期望输出",
      "difficulty": "medium",
      "tags": ["tag1"]
    }
  ]
}
```

```python
from src.test_dataset import load_dataset_from_json
dataset = load_dataset_from_json("path/to/dataset.json")
```

### 5.4 添加新 API 端点

在 `src/web/app.py` 中添加路由：

```python
@app.get("/api/my-endpoint")
async def my_endpoint():
    return {"result": "..."}
```

## 6. macOS 打包

使用 py2app 将项目打包为 macOS 桌面应用：

```bash
# 安装 py2app
pip install py2app

# 打包
python packaging/py2app_setup.py py2app

# 产出目录
# dist/Agent评估框架.app
```

## 7. 常见问题

### Q: 导入模块报错 `ModuleNotFoundError`

确保在项目根目录下运行，或设置 `PYTHONPATH`：

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python examples/eval_demo.py
```

### Q: Web 服务端口被占用

```python
# 修改 src/web/app.py 中的默认端口
def run_server(host: str = "0.0.0.0", port: int = 8080):
    ...
```

### Q: 如何接入真实 LLM API？

参见 `docs/TECHNICAL_DOC.md` 第 4.4 节"接入真实 LLM"。

## 8. 参考资源

- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [Python dataclasses 文档](https://docs.python.org/3/library/dataclasses.html)
- [py2app 文档](https://py2app.readthedocs.io/)
