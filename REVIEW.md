# Agent Evaluator — 代码审查报告

> 审查日期：2026-06-21  
> 项目路径：`/home/dirjaker/myprojects/agent_evaluator`  
> 审查范围：10 个 Python 源文件

---

## 🔴 致命问题

### 1. CORS 配置允许所有来源
- **文件**：`src/web/app.py` **第 29-31 行**
- **问题**：`allow_origins=["*"]` 允许任意域名跨域请求，配合无认证的 API 端点，任何网站均可调用评估接口、清空数据。
- **修复建议**：限制为实际前端域名，如 `allow_origins=["http://localhost:8004"]`，生产环境使用环境变量配置。

### 2. 服务绑定 0.0.0.0 且无认证
- **文件**：`src/web/app.py` **第 255 行**
- **问题**：`run_server(host="0.0.0.0")` 将服务暴露到所有网络接口，且所有 API 端点（`/api/evaluate`、`/api/benchmarks/clear` 等）均无任何认证和授权机制。
- **修复建议**：默认绑定 `127.0.0.1`；添加 API Key 或 Bearer Token 认证中间件。

### 3. 裸 except 捕获所有异常
- **文件**：`src/evaluator.py` **第 274 行**
- **问题**：`except:` 会捕获 `KeyboardInterrupt`、`SystemExit` 等不应被捕获的异常，掩盖真正的错误。
- **修复建议**：改为 `except (json.JSONDecodeError, ValueError) as e:`，并记录日志。

---

## 🟡 警告问题

### 4. 内存存储，数据持久性为零
- **文件**：`src/web/app.py` **第 52-53 行**
- **问题**：`benchmark_results` 和 `evaluation_history` 使用 Python 列表存储，进程重启后全部丢失，且无上限控制，长时间运行可能导致内存溢出。
- **修复建议**：使用 SQLite 或文件持久化；添加最大条目数限制。

### 5. 无线程安全保护
- **文件**：`src/web/app.py` **第 52-53 行**
- **问题**：FastAPI 的异步端点并发访问共享列表 `evaluation_history` 和 `benchmark_results`，`list.append()` 虽然在 CPython 中是原子的，但 `list.clear()` 和切片操作（`[-limit:]`）在并发场景下不安全。
- **修复建议**：使用 `asyncio.Lock` 保护共享状态，或改用线程安全的数据结构。

### 6. sys.path 操作方式不规范
- **文件**：`src/web/app.py` **第 20 行**，`src/macos/app.py` **第 14 行**，`examples/eval_demo.py` **第 10 行**
- **问题**：多处使用 `sys.path.insert(0, ...)` 修改模块搜索路径，容易导致模块冲突和导入混乱。
- **修复建议**：使用 `pyproject.toml` + `pip install -e .` 可编辑安装，消除 sys.path hack。

### 7. load_dataset_from_json 缺少文件路径验证
- **文件**：`src/test_dataset.py` **第 134-153 行**
- **问题**：`load_dataset_from_json(file_path)` 直接打开用户传入的路径，无路径白名单或沙箱限制，存在路径穿越风险。
- **修复建议**：限制文件路径在指定数据目录下，使用 `Path.resolve()` 检查前缀。

### 8. macOS GUI 无法真正停止服务
- **文件**：`src/macos/app.py` **第 123-128 行**
- **问题**：`_stop_server()` 仅设置 `self.server_running = False` 和更新 UI 状态，但 daemon 线程中的 uvicorn 服务器并未被真正终止。
- **修复建议**：保存 uvicorn server 引用，调用 `server.should_exit = True` 来停止。

---

## 🔵 建议

### 9. 评估器工厂函数返回类型不精确
- **文件**：`src/evaluator.py` **第 335 行**
- **问题**：`create_evaluator()` 返回类型标注为 `Any`，丧失类型检查优势。
- **修复建议**：定义 `Evaluator` Protocol 或基类，返回类型标注为 `RuleEvaluator | LLMEvaluator | CompositeEvaluator`。

### 10. CompositeEvaluator 直接修改传入结果的 score
- **文件**：`src/evaluator.py` **第 312 行**
- **问题**：`result.score *= weight` 直接修改了原始 EvalResult 对象，可能产生副作用。
- **修复建议**：创建新的 EvalResult 副本或使用不可变设计。

### 11. 缺少日志系统
- **问题**：整个项目使用 `print()` 输出信息，无法控制日志级别和输出目标。
- **修复建议**：使用 `logging` 模块替代 `print()`。

### 12. 缺少测试用例
- **问题**：项目无单元测试。
- **修复建议**：为核心评估逻辑添加 pytest 测试用例。

### 13. 依赖版本未锁定
- **文件**：`requirements.txt`
- **问题**：使用 `>=` 范围指定版本，可能导致不同环境安装不同版本。
- **修复建议**：使用 `pip freeze` 生成锁定文件或使用 `pyproject.toml` + lock 文件。

---

## 总结评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 🔒 安全 | **4/10** | CORS 全开、无认证、裸 except、路径验证缺失 |
| 📊 质量 | **6/10** | 代码结构清晰，但缺少错误处理、日志和测试 |
| 🏗️ 架构 | **6/10** | 模块划分合理，但内存存储、sys.path hack 影响可维护性 |
