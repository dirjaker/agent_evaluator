# Agent Evaluator 版本记录

## v1.0.0 (2026-05-30)

### 🎉 初始版本

#### 核心功能
- **Evaluator 模块**
  - RuleEvaluator 规则评估器
  - LLMEvaluator LLM 评估器
  - CompositeEvaluator 组合评估器
  - 支持 4 个评估维度

- **Test Dataset 模块**
  - TestCase 测试用例
  - TestDataset 数据集管理
  - 预定义数据集

- **Benchmark 模块**
  - BenchmarkConfig 配置
  - BenchmarkRunner 运行器
  - BenchmarkResult 结果统计

#### 示例代码
- `examples/eval_demo.py` - 评估演示

#### 文档
- `README.md` - 项目说明
- `TECHNICAL_DOC.md` - 技术文档
- `DIRECTION.md` - 方向指引

---

## 后续计划

### v1.1.0 (计划中)
- [ ] 集成 DeepSeek API 进行 LLM 评估
- [ ] 添加更多评估指标
- [ ] 支持 JSON 数据集导入

### v1.2.0 (计划中)
- [ ] A/B 测试框架
- [ ] 结果可视化
- [ ] 报告导出（PDF/HTML）

### v2.0.0 (远期)
- [ ] Web UI
- [ ] 多用户支持
- [ ] 与 CI/CD 集成
