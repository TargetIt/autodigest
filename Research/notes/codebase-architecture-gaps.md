# 架构图与代码理解补漏：从仓库提取关系，再核对图的事实依据

本轮补入 **5 个具有独立代码实现的项目**，覆盖“仓库概览 → 静态关系 → 语义架构 → 图文解释”。它们补的是 Archify 上游的事实采集与解释能力：Archify 可以渲染与检查输入图，但一个输入合法、布局合格的箭头，并不自动等于真实调用或部署关系。

**审阅范围：**2026-10-15（北京时间），对下表固定 SHA 进行静态源码审阅；已将真实 Git 浅检出保存到 `Research/repos/<owner>/<repo>`。没有安装依赖、运行分析器/模型/项目测试、连接 MCP 或调用付费服务。Stars/Forks 来自本仓现有 `collect_github_metadata.py` 的 `collect()`，原始字段与时间保存在 [候选及证据快照](../evidence/codebase-architecture-candidates.json)。Stars 是仓库关注度，不能替代准确率、速度、维护质量或语言覆盖实测。

| 项目 / 官方入口 | 精确 Stars / Forks | 分层与典型输出 | 模型依赖 | 固定源码 |
| --- | ---: | --- | --- | --- |
| [GitDiagram](https://github.com/ahmedkhaleel2004/gitdiagram) · [网站](https://gitdiagram.com) | 18,202 / 1,403 | 仓库 → 可点击架构图、说明、Mermaid | 新图生成需要 LLM；已存图可以直接阅读 | [310e2e696b19](https://github.com/ahmedkhaleel2004/gitdiagram/tree/310e2e696b1953cec0e76560cad5e9cd7ca5d964) |
| [CodeBoarding](https://github.com/CodeBoarding/CodeBoarding) · [网站](https://www.codeboarding.org) | 2,577 / 213 | 静态符号/调用关系 + 语义分组 → 分层架构说明、Mermaid/HTML | 完整语义分析需要配置模型，可接本地 Ollama | [57ac725575a8](https://github.com/CodeBoarding/CodeBoarding/tree/57ac725575a82562a27e1b12302afaa337232b23) |
| [GitNexus](https://github.com/abhigyanpatwari/GitNexus) · [Web UI](https://gitnexus.vercel.app) | 47,882 / 5,197 | 源码 → 可查询知识图谱、调用候选路径、影响分析上下文 | 结构索引本身不要求 LLM；wiki/聊天另需模型能力 | [cae60c2bd49e](https://github.com/abhigyanpatwari/GitNexus/tree/cae60c2bd49ed9176544d0d1a0810db6a552f2cc) |
| [DeepWiki-open](https://github.com/AsyncFuncAI/deepwiki-open) | 18,197 / 2,014 | 代码检索 → 带图 wiki、问答、问题驱动 codemap | 需要生成模型与 embedding；可配置本地后端 | [d92819a9c9f3](https://github.com/AsyncFuncAI/deepwiki-open/tree/d92819a9c9f3b99416e3580ff235fc9d3adf8b89) |
| [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) · [官方手册](https://github.com/sverweij/dependency-cruiser/tree/main/doc) | 7,291 / 301 | JS/TS 模块依赖 → JSON、图、规则违反报告 | 无 LLM | [c580daf6477a](https://github.com/sverweij/dependency-cruiser/tree/c580daf6477aa5619bacad9c9091c9b7cc81882d) |

前四项 API 采集时间为 `2026-10-14T20:53:23–28Z`，dependency-cruiser 为 `2026-10-14T20:55:28Z`，均对应北京时间 10 月 15 日。以下“接入 Archify”是本次提出的组合使用方法，**不是已实现或实测的原生适配器**。

## 1. GitDiagram：快速建立仓库概览，并回到文件核对

**基本功能与理解价值。**输入 GitHub 仓库，生成一张组件分组、连接关系和可点击源码入口的图，附带解释与 Mermaid。适合刚接触仓库、希望先知道主要模块在哪里的人。当前版本不是只看 README：源码有受预算约束的文件采样、引用列表与边证据处理。它仍然主要是 **LLM 生成的高层概览**，不是完整静态调用图。

**实际代码链：**

1. [fetchSourceContext](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/source-context.ts#L225-L258) 为私有仓库检查 token，选择用于摘要的源文件，并限制进一步读取的引用文件数量；因此不是逐文件完整理解所有代码。
2. [generateValidatedGraph](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/graph-planner.ts#L119-L221) 调用结构化模型输出，验证图，遇到可修复的错误源码路径时会清掉链接/引用后继续，结构问题才触发重试。图生成成功不能被解释成所有节点都有源码锚点。
3. [applyEdgeEvidence](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/edge-evidence.ts#L26-L90) 对一般源码引用检查是否已读取、是否覆盖端点或引用相关文件；根 README 单独允许作为引用。它会移除不合适引用、尝试补充引用。**没有引用的边并未被一律删除**，而且文件级引用也没有证明边上的业务解释。
4. [compileDiagramGraph](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/src/server/generate/graph.ts#L450-L512) 将组、节点和边编译成 Mermaid，并为有源码路径的节点附加 GitHub 跳转。这是实际的图描述编译实现，返回 Mermaid 字符串；最终 SVG 渲染属于前端的另一步。

**模型/服务与成本。**新图生成有模型调用与 token 成本，当前 diagram provider 配置为 OpenAI/OpenRouter；网站运营方提供的额度不等于自托管无成本。私有仓库还需要 GitHub 访问凭据。此轮没有发送任何仓库到这些服务。根许可为 [MIT](https://github.com/ahmedkhaleel2004/gitdiagram/blob/310e2e696b1953cec0e76560cad5e9cd7ca5d964/LICENSE#L1-L21)。

**如何用于 Archify。**把它作为候选组件与关系的初稿；只把已经打开源码验证过的路径/边转成 Archify JSON，对无引用边标注“待核实”。不要把“图有可点击链接”当作“架构经过完整验证”。动态加载、配置注入、多服务部署关系和未采样代码仍需要其他证据。

## 2. CodeBoarding：静态符号关系与 LLM 语义结构分工明确

**基本功能与理解价值。**输入本地或远程仓库，通过语言分析获得符号、调用、继承和依赖，再用模型组织组件名称、职责、分层说明及关系标签；输出可展开的架构资料。相对只有文件树的工具，它更适合回答“这几个文件为何属于一个组件、从哪一层继续读”。

**实际代码链：**

1. [CallGraphBuilder.build](https://github.com/CodeBoarding/CodeBoarding/blob/57ac725575a82562a27e1b12302afaa337232b23/static_analyzer/engine/call_graph_builder.py#L49-L132) 发现符号、建立索引，通过语言适配器/LSP 构建边与类层次，再计算包依赖，并把文件和行号写入 references。这个阶段提供的是可追溯结构信息。
2. [ScopeAnalysisAgent.analyze](https://github.com/CodeBoarding/CodeBoarding/blob/57ac725575a82562a27e1b12302afaa337232b23/agents/scope_analysis_agent.py#L178-L244) 把 scope 文件、方法、静态图交给 agent；可调用读文件与查方法调用工具，受输入 token/工具/模型调用预算限制，输出结构化语义分析。组件职责和说明并不是静态分析器自动证明的事实。
3. [ScopeAssembler 的关系合并](https://github.com/CodeBoarding/CodeBoarding/blob/57ac725575a82562a27e1b12302afaa337232b23/diagram_analysis/scope_assembly.py#L255-L293) 是必须写清的边界：若没有静态边和关键符号边，但模型给出 evidence 文本，代码仍允许保留该语义关系，并记 `is_static=false`。因此应区分静态支持边与语义解释边；不能概括为“全部箭头均经静态调用验证”。
4. [Mermaid 生成器](https://github.com/CodeBoarding/CodeBoarding/blob/57ac725575a82562a27e1b12302afaa337232b23/output_generators/markdown.py#L9-L40) 从结构化 components 和 relations 输出节点、带标签的边及组件详情跳转；同仓还提供 HTML 等输出。

**模型/服务与成本。**固定提交的 `pyproject.toml` 要求 Python 3.12，分析还涉及语言服务器/解析器及模型配置；不是装一个 Markdown skill 就完成所有分析。`agents/llm_config.py` 有 Ollama 接口，因此可以选择本地模型，但仍需准备模型和计算资源；远程模型的调用另计。根许可为 [MIT](https://github.com/CodeBoarding/CodeBoarding/blob/57ac725575a82562a27e1b12302afaa337232b23/LICENSE#L1-L21)。

**如何用于 Archify。**优先提取静态 references 的文件/行号和 `is_static` 标记，核对后再提升为少量业务组件。对于 `is_static=false` 关系保留推断说明或另找代码/配置依据。语言适配器、语言服务器分辨率、动态行为及模型 scope 预算都会影响覆盖；静态分析结合 LLM 能改善阅读路径，但不能自动确认生产运行拓扑。

## 3. GitNexus：给人和 Agent 查询的代码知识图谱

**基本功能与理解价值。**把文件、符号、引用/调用等关系写入本地图谱，再提供图浏览、查询、上下游影响与候选执行路径。它适合在架构图之外追问“这个入口会经过哪些模块”“修改这个符号影响哪里”，也可以给 Agent 提供结构化上下文。它与 GitDiagram 的主要区别是可查询的结构索引，不能仅按谁画图更漂亮比较。

**实际代码链：**

1. [parseSourceSafe](https://github.com/abhigyanpatwari/GitNexus/blob/cae60c2bd49ed9176544d0d1a0810db6a552f2cc/gitnexus/src/core/tree-sitter/safe-parse.ts#L211-L249) 实际调用 Tree-sitter parser，将源码解析为树，并处理输入长度/解析预算。结构分析不是先把所有源码发送给 LLM。
2. [分析阶段注册](https://github.com/abhigyanpatwari/GitNexus/blob/cae60c2bd49ed9176544d0d1a0810db6a552f2cc/gitnexus/src/core/ingestion/pipeline.ts#L330-L365) 明确串起解析、跨文件与作用域解析，以及 community/process 等派生阶段；这些是独立实现的代码处理流程。
3. [process tracing 实现](https://github.com/abhigyanpatwari/GitNexus/blob/cae60c2bd49ed9176544d0d1a0810db6a552f2cc/gitnexus/src/core/ingestion/process-processor.ts#L440-L679) 只用满足 confidence 与 reason 条件的 CALLS 边构图，再按深度优先路径搜索，受 trace 深度、分支和数量预算约束。它是从静态图提取的候选路径，**不是实际运行采样，也不保证枚举所有路径**；源码会统计深度截断和遗漏分支。
4. [wiki 模型配置](https://github.com/abhigyanpatwari/GitNexus/blob/cae60c2bd49ed9176544d0d1a0810db6a552f2cc/gitnexus/src/core/wiki/llm-client.ts#L94-L140) 另行解析 provider、API key 或已有模型 CLI。需要把无 LLM 的结构索引与需要生成模型的解释/wiki 功能分开理解。

**模型/服务与成本。**结构索引可以本地进行；依赖包含原生 parser 与 LadybugDB，有安装、内存和磁盘成本。Embedding 在该提交的 CLI 中是显式选项，启用时还涉及模型/runtime；本地 Web UI 并不意味着任意聊天后端都本地。默认 `analyze` 还可能生成 Agent 上下文/集成文件，不能把它当成对工作区毫无写入的查询操作；本次未运行。

**许可必须单列。**固定 SHA 根文件是 [PolyForm Noncommercial 1.0.0](https://github.com/abhigyanpatwari/GitNexus/blob/cae60c2bd49ed9176544d0d1a0810db6a552f2cc/LICENSE#L1-L41)，GitHub API 返回 `NOASSERTION`。这里按“源码可审阅的候选”收录，不标为 MIT，也不把它与无此用途限制的项目等同。

**如何用于 Archify。**查询选定入口/符号的调用和文件依据，检查边的置信信息与是否截断，再把少量确认过的关系转成 Archify 输入。图谱里一条边存在，不代表部署中每次都会经过它；缺边也可能来自解析能力、动态分派或索引版本，而不是证明“没有依赖”。应同时记录被分析仓库的 commit，防止拿旧索引解释新代码。

## 4. DeepWiki-open：值得补入，但定位是代码图文解释与 codemap

**基本功能与理解价值。**这是独立的仓库 wiki/问答实现，不是把 Cognition 的商业 DeepWiki 代码开源。它通过代码分块与检索，让模型生成文档、Mermaid 和回答。当前固定版本还存在问题驱动的 **codemap**：例如围绕“请求如何到达数据库”组织步骤、代码引用、图和说明。因此应收录到代码理解邻接层，不能仅当普通笔记库；也不能把它当静态调用图分析器。

**实际代码链：**

1. [RAG 文档转换器](https://github.com/AsyncFuncAI/deepwiki-open/blob/d92819a9c9f3b99416e3580ff235fc9d3adf8b89/api/rag/pipeline.py#L230-L245) 组合带行号追踪的 splitter 与 `ToEmbeddings`，形成切块 → embedding 的数据管线。
2. [codemap 生成流程](https://github.com/AsyncFuncAI/deepwiki-open/blob/d92819a9c9f3b99416e3580ff235fc9d3adf8b89/api/services/codemap.py#L224-L297) 先检索相关代码，再调用模型生成 skeleton，第二阶段补 diagrams/guides；若后者失败，会回退到没有完整图文增强的 skeleton，并标 degraded。不能承诺每次请求都有完整架构图。
3. [引用定位](https://github.com/AsyncFuncAI/deepwiki-open/blob/d92819a9c9f3b99416e3580ff235fc9d3adf8b89/api/services/codemap.py#L164-L208) 尝试用 snippet 在真实文件中找行号；完整片段匹配失败还可能以第一条非空行定位，找不到则没有在此处强制拒绝引用。因此这是一种可追溯性补强，不能称为完整语义核验。
4. [实际 Mermaid renderer](https://github.com/AsyncFuncAI/deepwiki-open/blob/d92819a9c9f3b99416e3580ff235fc9d3adf8b89/src/components/Mermaid.tsx#L356-L388) 调用 `mermaid.render` 得到 SVG，并处理失败状态；不是仅在 README 贴了一张示意图。

**模型/服务与成本。**生成与 embedding 是两条模型需求；`api/config/embedder.json` 有 OpenAI、Ollama 等后端。选择本地生成模型时，也要确认 embedding 的配置，不能由“支持 Ollama”推导全链路默认离线。部署还有 Python API、前端、索引存储等成本。根许可为 [MIT](https://github.com/AsyncFuncAI/deepwiki-open/blob/d92819a9c9f3b99416e3580ff235fc9d3adf8b89/LICENSE#L1-L21)。

**如何用于 Archify。**适合先围绕具体问题找阅读路线，查看引用和 Mermaid，再人工确认关键路径并生成简洁的 Archify 图。需要检查检索是否漏掉调用另一端、snippet 是否确实支持解释、链接是否固定到同一个 commit。它提供图文叙事；检索相关性与引用存在都不等于箭头含义正确。

## 5. dependency-cruiser：JS/TS 模块依赖的独立事实层

**基本功能与理解价值。**扫描 JavaScript/TypeScript 等模块依赖，生成依赖图和结构化结果，并按允许、禁止、必须等规则检测架构约束；可用于发现循环依赖、跨层依赖和不应耦合的目录。它无需模型，特别适合作为前端/Node 仓库架构说明的核对来源。

**实际代码链：**

1. [ES module 依赖提取](https://github.com/sverweij/dependency-cruiser/blob/c580daf6477aa5619bacad9c9091c9b7cc81882d/src/extract/acorn/extract-es6-deps.mjs#L10-L66) 遍历 AST 中的 import/export；在这个 Acorn 抽取路径中，动态 import 只在字符串字面量或不含插值模板等可识别条件下抽取。代码本身就体现了静态覆盖边界。
2. [cruise 主流程](https://github.com/sverweij/dependency-cruiser/blob/c580daf6477aa5619bacad9c9091c9b7cc81882d/src/main/cruise.mjs#L76-L108) 规范化文件和解析选项，再执行 extract → analyze → report；这是依赖分析和报告工具，不是 LLM 从 README 猜架构。
3. [规则验证器](https://github.com/sverweij/dependency-cruiser/blob/c580daf6477aa5619bacad9c9091c9b7cc81882d/src/validate/index.mjs#L20-L101) 对依赖运行 allowed / forbidden / required 匹配并返回 severity 和规则名称，支持把组织约束变成可检查规则。
4. [Mermaid reporter](https://github.com/sverweij/dependency-cruiser/blob/c580daf6477aa5619bacad9c9091c9b7cc81882d/src/report/mermaid.mjs#L158-L168) 从分析结果构建子图、边和重点高亮；同一份结果也有 JSON、DOT 等 reporter。这里的图表示模块依赖，不表示业务事件时序。

**模型/服务与成本。**无需 LLM API。需要 Node 和仓库的解析/tsconfig/别名等配置；当前包声明的 Node 范围为 `^22 || ^24 || >=26`。导出 DOT 后若要渲染成图，还需要对应渲染器；生成 JSON/Mermaid 与渲染图片是不同步骤。根许可为 [MIT](https://github.com/sverweij/dependency-cruiser/blob/c580daf6477aa5619bacad9c9091c9b7cc81882d/LICENSE#L1-L21)。

**如何用于 Archify。**先抽出模块/文件依赖，再有依据地聚合成业务组件；把“模块 imports”与“组件调用”“网络通信”分清。不能从 `A import B` 直接推导“请求必经 B”，也不能依靠静态 import 捕获运行时拼接路径、反射、跨服务网络关系或真实部署。适合有明确 JS/TS 代码范围和可解释边含义的仓库。

## 实际选型与事实核对次序

| 当前问题 | 优先使用 | 得到什么之后再画 Archify |
| --- | --- | --- |
| 第一次看陌生仓库，先建立整体概览 | GitDiagram | 打开并核对重点组件与边的源码入口，区分有引用/无引用 |
| JS/TS 的模块耦合、层间依赖、循环规则 | dependency-cruiser | 带文件路径的依赖结果、违反规则及可识别范围 |
| 要查看跨文件调用、候选执行链与改动影响 | GitNexus（先看许可） | 指定 commit 的图查询、置信信息、截断/遗漏提示 |
| 要从符号调用提升到分层职责与组件文档 | CodeBoarding | 静态 references，分别标出 static-backed 与 semantic-only 关系 |
| 围绕某个问题读代码，结合图、步骤与解释 | DeepWiki-open | 问题对应的引用片段、代码行与图文；核对模型解释后再整理 |

建议保留两份东西：一份是未经美化、可复核的关系与源码依据；另一份是经过筛选的教学/架构视图。对每条最终箭头记录“依赖/调用/消息/部署/模型推断”等类型及来源 commit，避免把不同语义都画成同样的线。

本轮没有为了数量继续收录 glato/emerge、mindwalk/adrenaline 等相邻候选；它们可留作后续专题观察，**本次未作源码结论**。以上 5 项也不包含自动互导 Archify 的成品适配器；实现转换前仍需确定组件聚合粒度、证据字段和人工核对方式。
