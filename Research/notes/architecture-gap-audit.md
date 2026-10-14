# 以 Archify 为起点的架构与绘图工具查漏

**结论：Archify 保持架构图、组件关系和请求流程图的默认首选；此次再补入 20 个主仓，使总报告覆盖 60 个主仓。** 它们补齐了架构建模、代码关系提取、Agent 操作可编辑画布、云基础设施、数据库结构和知识画布。每一项都有官方仓库入口、精确 Star 快照、固定源码版本、实际实现依据与使用边界。[60 仓总览](../README.md#3-仓库总览与关注度) · [新增项总览](../README.md#34-以-archify-为起点补齐的架构与绘图工具)

用户已明确“画架构图用 Archify”。该偏好已写入 [AutoDigest 工作流](../../tool/workflows/autodigest.md) 和 [工具说明](../../tool/README.md)。这里完成的是调研与默认选型规则，未把下载源码当成已安装或已启用 skill，也没有运行新增项目的模型服务。

## 1. 为什么上一版会漏，以及这次如何补

上一版围绕 ShowMe、解释型 skill、通用图形引擎和交互学习展开，虽然覆盖 Mermaid、draw.io、Excalidraw、D2 等基础工具，仍缺少几条完整的工程路线：**共享架构模型、从业务代码提取关系、从基础设施配置生成图，以及数据库结构专用工具。** 只在已有类别里继续找名字相近的项目，会继续漏掉这些路线。

本次从“我想画什么、关系从哪里来、图怎样修改、如何长期维护”反向拆分，再交叉检索官方工具目录、GitHub topic/仓库搜索、相关仓库生态与现有清单。GitHub REST 搜索保留了 7 条实际查询、时间、返回条目和是否截断；搜索按关注度发现候选，但低 Star 的 Structurizr 新主仓和 AWS 样例仍按实际能力收录。[原始搜索结果](../evidence/architecture-gap-search.json)

搜索中的 `stars` 阈值用于发现高关注线索，不是收录门槛。它会漏掉缺少 topic、新建仓、未提到关键词的实现，因此同时使用领域与官方迁移信息补足。**这是一轮可复核的系统查漏，不宣称穷尽 GitHub 所有绘图项目。** 未深读的相邻项目保留为候选，不会用“已排除”冒充质量判定。[逐项筛选记录](../evidence/architecture-gap-screening.json)

## 2. 按你的实际任务选工具

| 现在要解决的问题 | 默认或优先选择 | 需要交付、保留什么 |
| --- | --- | --- |
| 给我讲清这个系统、组件如何协作、一次请求怎么走 | **Archify** | JSON、HTML、每条关键关系的类型与出处；浏览器检查结果 |
| 同一个系统要长期维护多张一致的图 | LikeC4；需要 C4 体系时 Structurizr | 一份共享模型、多个问题视图、版本记录 |
| 团队已经使用 PlantUML，想统一 C4 表达 | C4-PlantUML | `.puml` 与固定版本依赖；不能只固定最外层 include |
| 企业业务、应用、技术及迁移影响一起建模 | Archi | ArchiMate 模型、共享元素与关系、可浏览报告 |
| 陌生代码仓库，先找主要组件 | GitDiagram | 概览初稿和可点击源码；无证据关系标待核实 |
| 查 JS/TS 的模块依赖、循环与跨层约束 | dependency-cruiser | 依赖 JSON、图、规则违反项；明确边表示模块依赖（import/require/export 等），不代表业务调用时序 |
| 查跨文件调用、影响范围和候选路径 | GitNexus；结合语义职责时 CodeBoarding | 指定 commit 的关系与引用，置信/截断或推断标记 |
| 围绕具体问题读代码并生成图文解释 | DeepWiki-open | 检索来源、片段、图与解释；区分引用定位和语义证明 |
| 已有 Terraform，想看基础设施结构 | TerraVision | 计划/graph 输入、生成图、资源合并及推断边说明 |
| 明确写 AWS 资源关系与布局，持续生成云图 | AWS Diagram as Code | YAML 与 PNG；工具不自动发现生产部署 |
| AWS 图需要引导讲解、交互或 draw.io 交付 | AWS 架构图 MCP 样例 | 结构 JSON、HTML / `.drawio` 与校验修复回执 |
| 想让 Agent 持续修改可编辑工程图 | drawio-skill、官方 draw.io MCP；按偏好选 Excalidraw MCP | 原生 XML / `.excalidraw` 与导出物，核对编辑结果 |
| 想亲手画、改、整理流程图与思维导图 | Drawnix、Excalidraw、draw.io | 原生可编辑图和必要的导出 |
| 已有 Mermaid 文本，想改善嵌入或终端展示 | Beautiful Mermaid | 支持子集内的 SVG / 文本图；超出语法另选渲染器 |
| 表结构怎么关联、怎样设计或阅读数据库 | drawDB / ChartDB / Liam ERD | SQL、schema/元数据、原生图或 ERD 站点 |
| 笔记、材料、脑图想放在一起长期整理 | AFFiNE | 文档与画布；按照具体功能准备应用与服务 |

这些选择基于源码机制，不是同一题目的速度、出图质量或学习效果排名。尤其不要把“分析代码”与“画出一张易懂的图”混为一项能力：Archify 的强项是组织和交付解释，真实关系仍需从材料取得。

一个可采用的过程是：**源码 / schema / 计划 → 提取并核对关系 → 选择与当前问题有关的少量内容 → Archify 图解 → 用图追问并回源修正。** 箭头至少区分静态依赖、调用、网络消息、设计意图和模型推断。上述工具与 Archify 的组合是本次提出的工作方法；除笔记明确确认的工具内导出外，不代表已有或实测了自动格式转换适配器。

## 3. 新增 20 项分组阅读

| 分组 | 本轮补入 | 逐项实现与限制 |
| --- | --- | --- |
| 共享架构模型、C4、企业架构、Terraform | LikeC4、Structurizr、C4-PlantUML、Archi、TerraVision（5） | [模型与基础设施源码笔记](architecture-modeling-gaps.md) |
| 从代码寻找架构依据与阅读路径 | GitDiagram、CodeBoarding、GitNexus、DeepWiki-open、dependency-cruiser（5） | [代码理解源码笔记](codebase-architecture-gaps.md) |
| Agent 绘图、渲染、白板与 AWS 云图 | drawio-skill、mcp_excalidraw、Beautiful Mermaid、Drawnix、AWS Diagram as Code、AWS 架构图 MCP 样例（6） | [绘图入口源码笔记](agent-diagram-gaps.md) |
| 数据库 ERD 与知识画布 | drawDB、ChartDB、Liam ERD、AFFiNE（4） | [数据库与画布源码笔记](database-and-canvas-gaps.md) |

基本功能与全部 Star 数直接放在[主报告新增表](../README.md#34-以-archify-为起点补齐的架构与绘图工具)，Fork、release、维护日期和许可证 API 检测值进入[统一元数据表](../evidence/repository-index.md)。没有用仓库搜索页的四舍五入数字替换 API 快照；原 40 仓数据原样保留，本轮增补各自标采集时间。

## 4. 会影响选择的纠正

1. **Structurizr 应看现行主仓。** 旧 CLI、Lite、Java、UI、on-premises 等仓已归档，新仓 Star 较少不能当作产品不成熟的证据。新 CLI/server 与旧教程的安装路径不同，官方 server 发行物和自编译核心能力也有区别。[迁移与源码核实](architecture-modeling-gaps.md#2-structurizr现行-c4-参考实现必须避开过时仓库入口)
2. **自动代码图有多种证据强度。** CodeBoarding 可以保留只有模型 evidence 的语义关系；GitDiagram 不会一律删除无源码引用的边；GitNexus 的候选路径受预算截断；DeepWiki 的片段定位也不是语义证明。最终图需要保留这些区别。[逐项代码依据](codebase-architecture-gaps.md)
3. **TerraVision 不只是读取 HCL。** 普通路径会执行 Terraform init/plan/show/graph，且存在资源合并和推断连接。它不等于云现场扫描，也不能仅凭宣传认定逐边完全准确。[Terraform 路径](architecture-modeling-gaps.md#5-terravision从-terraform-计划生成云基础设施架构图)
4. **AWS 旧绘图模块与整个 MCP 项目要分开。** `awslabs.aws-diagram-mcp-server` 的弃用不代表整个 `awslabs/mcp` 仓库停用；官方当前迁移建议见分组笔记。这里收录的 AWS Diagram as Code 与 AWS 样例也不冒称所有旧用法的无缝替代。[官方迁移与实现范围](agent-diagram-gaps.md)
5. **名字和许可要认真区分。** Archi 不是 Archify；Beautiful Mermaid 不是 Mermaid 官方完整引擎；第三方 drawio-skill 和 Excalidraw MCP 不等于官方服务。GitNexus 的 Noncommercial、TerraVision/drawDB/ChartDB 的 AGPL、AFFiNE 的目录划分，均按审阅版本记录。[模型组](architecture-modeling-gaps.md) · [代码组](codebase-architecture-gaps.md) · [数据库组](database-and-canvas-gaps.md)
6. **“校验成功”需要说清校验的对象。** 可能只证明 JSON/DSL 合法、引用位置存在、模型规则符合或图像成功渲染；这些都不能单独证明系统事实与箭头含义正确。Archify 已做的局部实测和未验证范围仍见[专项笔记](archify.md)。

## 5. 收录边界与可复核交付

已有关联能力的项目不重复充数：PlantUML 与 C4-PlantUML 分别是引擎和领域扩展；官方与第三方 MCP 单独列出，是因为接入方式、状态和编辑/导出实现确有区别。Structurizr 归档旧仓保留迁移证据，不加进 60 个主仓。Archify 的前身/相关项目与现行架构绘图候选在筛选记录中注明关系；相似名字和 fork 不能当作独立技术贡献的证据。

搜索还找到科学插图、PR 审查、交互面板、其他白板 SDK 和代码地图等相邻候选。这一轮优先补齐用户特别在意的架构图与工程绘图路径，对未深读的相邻项目保留名称、链接和状态，未给它们编造优缺点或测试结论。候选与新增主仓不是同一个统计口径。

20 份新增源码全部直接下载到 `Research/repos/<owner>/<repo>/`，与既有 41 份共同构成 61 个固定 Git 子模块；原工具内容仍在 `tool/`。大型项目采用稀疏检出，恢复方法和范围见[源码目录](../repos/README.md)。每条固定源码链接的提交、文件 SHA-256 和行号可由[验证脚本](../scripts/verify_source_checkouts.py)复核。

本轮新增项目均为静态源码审阅，未安装依赖、调用模型、连接云资源或运行完整应用。文档与证据的完整性检查另记在[验证记录](../evidence/validation.md)；不会把完整性校验写成“20 个工具全部亲测可用”。
