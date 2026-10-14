# 调研验证记录

日期：2026-10-15（Asia/Shanghai）。环境：Node.js `v22.23.2`、Python `3.9.6`。以下区分来源核查、程序行为检查与未执行范围，避免把“读过代码”写成“所有功能已实测”。

## 1. 元数据与源码引用

- 通过 GitHub REST API 采集 39 个主仓的仓库信息、默认分支 HEAD 和 latest release，保留 endpoint 及 UTC 时间；39 个源码审阅 SHA 均与本次 API 的 HEAD 一致。
- 汇总表的 39 个 Star 数逐行对照 JSON，仓库不重复；HumanLayer、Matt Pocock 明确标为合集 Star。
- 统一检查 **236 个去重后的固定 SHA 源码链接**：提交号、目标文件存在、行号不越界；同时记录源文件 SHA-256。[源码索引](source-index.json)
- 索引涉及 40 个仓库：39 个主工具，以及用于核对 D3 数据绑定实现的 `d3/d3-selection` 依赖。Graphviz 只核实官方来源，没有算入 GitHub 主工具数量。
- 代码链接的位置检查不等于证明引用支持全部结论。各分组另做静态审阅，并对主报告进行了交叉复核；修正了 ShowMe 文件链接、pixelviz 风格描述、Mafs 与 Attention 计算的职责、ELK 适用范围和 monorepo release 的解释。
- 仓库内相对链接和主报告目录锚点另做本地检查；外部官网/演示入口的可达性记录在 [入口链接检查](external-link-check.json)。HTTP 429 为限流，不能判成链接已失效；入口能打开也不代表应用已通过功能验证。

## 2. Ofori01/show-me 的引用与布局检查

固定 SHA：`62c8905665be8ff6f51df05eaccf6b38e1c183e1`。审阅导入与脚本后，在该源码目录执行，未安装依赖、未启动服务、未使用模型生成新地图。

```bash
node skills/show-me/scripts/self-test.mjs --repo skills/show-me
node skills/show-me/scripts/layout-test.mjs --repo skills/show-me
node skills/show-me/scripts/validate.mjs skills/show-me/examples/show-me.system-map.json --repo skills/show-me
```

三个进程退出码均为 `0`。以下是从本次工具执行结果转录的输出要点，不是另行保存的原始运行日志。

```text
self-test:
  clean fixture passes
  fabricated evidence string is rejected
  real string cited at the wrong line is rejected
  a line past the end of the file is rejected
  citation to a file that does not exist is rejected
  a flow that teleports between nodes is rejected
  a branch step does not advance the path
  a branch step wrongly treated as a hop breaks the chain
  a glob matching nothing is rejected
  an unknown node id on an edge is rejected
  prose too thin to be an explanation is rejected
  all 11 gate tests passed

layout-test:
  28 routes stay in the corridors
  19 footprints are disjoint
  all routed points fall inside the viewBox
  6 districts are contiguous and pure
  layout is deterministic
  all layout invariants hold (1 map checked)

validate:
  resolved 19 nodes -> 19 source files, 6,046 LOC, 3 test files
  scope coverage: 19/19 files claimed (100%)
  1 non-blocking craft note: one 32-word sentence
  OK — 19 nodes, 28 edges, 3 flows, all citations verified.
```

这能支持“样例与这些错误输入的校验行为符合预期”，不能支持“任意仓库都能被正确理解”“所有调用关系自动提取正确”或“每个真实引文都支持 Agent 的解释”。引用、几何布局与语义正确性是三个层次。[实现与测试源码](../notes/showme-skills.md)

## 3. draw.io MCP 的图形查询测试

固定 SHA：`3398377f740d47faa0245b107b886e856fa3930f`。在该仓库根目录运行：

```bash
node --test mcp-tool-server/test/shape-search.test.js
```

结果：**3 tests，3 pass，0 fail，退出码 0**。覆盖相对图像 URL 转换、绝对 URL/data URI 与非图像样式保留、强匹配标记。这组测试只调用 Node 标准库与已审阅的 shape-search 模块，不启动 MCP、浏览器或图标网络服务。

不能据此推断自动布局质量、模型生成效果或宿主内嵌兼容性已经验证。[集成与辅助函数分析](../notes/agent-diagram-integrations.md)

## 4. Excalidraw Diagram Skill 的结构校验边界

固定 SHA：`8646fcc9f74f38539c6cdb4c969723336a96ddcd`。完整阅读 `references/render_excalidraw.py` 后，用 Python 的 `importlib.util` 导入模块，仅调用不依赖 Playwright 的函数。

| 输入或操作 | 预期与实际结果 |
| --- | --- |
| 空字典 `{}` | 返回 type 错误与缺失 elements 错误 |
| `type=excalidraw`，elements 为空数组 | 返回空数组错误 |
| elements 是字符串 | 返回必须为数组的错误 |
| elements 含一个矩形 | 顶层结构检查通过 |
| elements 含 `type=invented_invalid_type` | 也通过，证实此函数不检查元素类型语义 |
| 一个矩形加带负坐标箭头的包围盒 | 得到预期 `(-5, 0, 12, 20)` |

六项针对性断言通过，退出码 0。没有执行浏览器渲染；这个小检查也不代表该项目声明的 Python ≥3.11 完整运行环境已在 Python 3.9 上验证兼容。

因此报告把“自动顶层结构检查”和“Agent 按 skill 进行渲染、看图、修复”分开写，不把后者说成渲染器自动检测所有重叠或事实错误。[验证实现与渲染模板](../notes/agent-diagram-integrations.md)

## 5. 没有由本次检查证明的能力

本次没有运行其余上游测试全套，没有连接远端 MCP/云工作区，没有调用付费模型或语音服务，没有为 39 个项目逐一构建最终产物。对这些路径使用“源码存在、静态确认、官方说明”等强度，不使用“亲测全部可用”。

尤其没有测量真实学习者的成绩、保持率或迁移能力。功能与代码审查能够帮助选择值得试用的工具；证明学习收益还需要同材料、同问题和新例子的对照实践。
