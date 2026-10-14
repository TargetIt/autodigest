# 调研验证记录

日期：2026-10-15（Asia/Shanghai）。环境：Node.js `v22.23.2`、Python `3.9.6`。以下区分来源核查、程序行为检查与未执行范围，避免把“读过代码”写成“所有功能已实测”。

## 1. 首批元数据与源码引用（39 个主仓）

- 通过 GitHub REST API 采集 39 个主仓的仓库信息、默认分支 HEAD 和 latest release，保留 endpoint 及 UTC 时间；39 个源码审阅 SHA 均与本次 API 的 HEAD 一致。
- 汇总表的 39 个 Star 数逐行对照 JSON，仓库不重复；HumanLayer、Matt Pocock 明确标为合集 Star。
- 统一检查 **236 个去重后的固定 SHA 源码链接**：提交号、目标文件存在、行号不越界；同时记录源文件 SHA-256。[源码索引](source-index.json)
- 索引涉及 40 个仓库：39 个主工具，以及用于核对 D3 数据绑定实现的 `d3/d3-selection` 依赖。Graphviz 只核实官方来源，没有算入 GitHub 主工具数量。
- 代码链接的位置检查不等于证明引用支持全部结论。各分组另做静态审阅，并对主报告进行了交叉复核；修正了 ShowMe 文件链接、pixelviz 风格描述、Mafs 与 Attention 计算的职责、ELK 适用范围和 monorepo release 的解释。
- 仓库内相对链接和主报告目录锚点另做本地检查；外部官网/演示入口的可达性记录在 [入口链接检查](external-link-check.json)。HTTP 429 为限流，不能判成链接已失效；入口能打开也不代表应用已通过功能验证。

## 2. Ofori01/show-me 的引用与布局检查

固定 SHA：`62c8905665be8ff6f51df05eaccf6b38e1c183e1`。审阅导入与脚本后，在该源码目录执行，未安装依赖、未启动服务、未使用模型生成新地图。源码现位于 [`Research/repos/Ofori01/show-me/`](../repos/Ofori01/show-me/)。

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

固定 SHA：`3398377f740d47faa0245b107b886e856fa3930f`。在该仓库根目录运行；源码现位于 [`Research/repos/jgraph/drawio-mcp/`](../repos/jgraph/drawio-mcp/)：

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

## 6. 初次目录补全与源码迁移（Archify 增补前）

此前已将原有内容移入 `tool/`，但下载源码仍在临时缓存，`Research/` 中只有报告与证据。本次将 40 份源码移入 `Research/repos/<owner>/<repo>/`，以 Git 子模块固定到调研版本；根目录 `.gitmodules` 和父仓 gitlink 共同记录地址及版本。

- `tool/` 的 30 个受版本控制文件逐项核对，无缺失、无改动；其 Git 树与迁移提交 `42b1f0f` 完全相同。
- 27 个原 Git 检出保留所有文件内容、文件模式与符号链接；13 个归档快照保留原有文件字节，补齐固定版本缺失文件并恢复上游执行位。原下载快照信息移到 [`download-snapshots/`](download-snapshots/)。
- 逐项核对 40 个 HEAD、父仓 gitlink、子模块 URL 和干净状态；源码引用索引中的 236 条记录在新路径下重新核对 SHA-256 和行号。
- 部分原检出是稀疏检出，保留调研所需源码范围；具体状态在[检出清单](source-checkouts.json)。重新初始化子模块默认检出固定版本的完整受控文件；文档说明了现有稀疏检出的展开方法。
- 本次检查不执行上游代码，不重跑此前功能测试。父仓提交子模块引用，不把所有上游源码文件复制为父仓普通文件；普通 clone 或 ZIP 下载不能代替子模块初始化。

从 AutoDigest 仓库根目录复核源码位置、提交和引用文件：

```bash
python3 Research/scripts/verify_source_checkouts.py
```

## 7. Archify 增补

在首批 39 仓之外增加 `tt-a1i/archify`，当前共 40 个主仓、41 个源码子模块（含 `d3/d3-selection`）。Archify 的 API 快照采于 2026-10-14T20:41:13+00:00，原 39 仓的数字和采集时间保留不变。本次新增源码引用与首批引用统一保存在 [source-index.json](source-index.json)。

固定源码 SHA 为 `d0c8c7e9f4e06f303389f804208d387f27019ef5`，晚于所记录的 v3.1.0 release；没有对发行 ZIP 复测。9 次局部 CLI 调用符合预期：有效架构输入生成并交付 HTML，非法类型和未知连接端点被拒绝，渲染失败保留旧 HTML 且失效交付状态无法通过严格检查，恢复交付后通过。

环境为 Node `v22.23.2`；未安装依赖、未调用模型，更新检查显式禁用。没有测试浏览器显示、交互、导出、其余九类图或完整 `finalize`。已查看两张上游样例截图，未对本次生成的 HTML 做视觉验收。详细输入、退出码、哈希、源码依据和可重放脚本见 [Archify 实测记录](archify/README.md)。

## 8. 以 Archify 为重点的系统查漏

在已有 40 个主仓上增补 20 个，共 60 个主仓、61 个直接源码子模块（含 d3/d3-selection）。新增元数据逐条采于 2026-10-14T20:53:23+00:00 至 20:55:59+00:00（北京时间 2026-10-15 04:53–04:55）；原 40 条元数据记录逐字段与前一提交比较，完全保留。

- 7 条 GitHub 搜索查询、领域目录、迁移信息及相关仓库发现的线索，汇入 [65 项筛选记录](architecture-gap-screening.json)。这些包含已有项、20 个新增主仓、历史/重复入口及未深读的相邻候选，不能说 65 项都做了深入源码审查。
- 20 个新增项目均查看了固定版本实现，而非只看 README；本轮全部为静态审阅，没有安装依赖、运行上游测试/应用/模型服务或执行 Terraform。四组笔记列出各自审阅范围。
- `python3 Research/scripts/verify_source_checkouts.py` 通过：**61 个固定子模块、418 条固定源码引用**。核对父仓 gitlink、子仓 HEAD、地址、路径、干净状态、引用文件 SHA-256 与行号范围；不能由此推出工具端到端可用或架构事实正确。
- 新增 20 项主表 Star 与各自 API 快照一致；文档中 180 个本地路径/锚点链接检查通过；60 行仓库元数据表和61行源码入口表保持完整。18 个官方外部入口 HTTP 检查均返回200，状态与重定向另存 [链接检查](architecture-gap-external-links.json)；HTTP 成功只证明检查时入口可访问。
- 独立交叉复核发现并修正两处：ChartDB 部分跨方言转换可确定性本地执行；GitDiagram 的 Mermaid 字符串编译与前端 SVG 渲染分开描述。另核实 Structurizr 旧仓归档、AWS 旧绘图模块弃用，避免推荐过时入口。
- `tool/` 原有内容继续位于原目录。本轮有意修改 `tool/README.md` 和 `tool/workflows/autodigest.md`，持久记录用户的 Archify 架构绘图默认偏好；不再把这两个文件宣称为与迁移时逐字一致。其余原工具文件未改。

本轮只改变报告、证据、源码引用及工具使用说明，没有替换原工具程序。此前 Archify 的9次局部CLI检查属于上一轮，不能算作本轮新增20项的测试结果。
