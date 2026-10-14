# 帮助理解知识的 ShowMe 类 Skill 与可视化工具调研

调研日期：**2026 年 10 月 15 日，Asia/Shanghai**。覆盖 **39 个 GitHub 仓库**，包括解释型 skill、Agent 绘图集成、结构图工具、数学动画、交互实验和数据探索工具。

**目录入口：**原有 AutoDigest 内容在 [`../tool/`](../tool/)，本次报告、证据和下载源码都在 `Research/` 下。下载的 40 份源码（39 个主仓库 + `d3/d3-selection`）位于 [`repos/<owner>/<repo>/`](repos/README.md)，以固定提交的 Git 子模块保存。首次克隆后需初始化子模块才能在本地查看源码，具体命令见[源码目录说明](repos/README.md)。

**优先建议：用 ShowMe 选择恰当的表达方式，用 Mermaid 或 Excalidraw 讲清结构，用 Mafs 或 marimo 检验参数变化，用带追问的教学流程确认自己真的理解了。** 工具各有分工，装得多不等于理解得深；最值得保留的是可修改的源文件、可复算的例子和能回到材料的依据。

导航：[ShowMe 的身份](#1-showme-具体指什么) · [按问题选工具](#2-先按自己的理解障碍选工具) · [39 个仓库总览](#3-仓库总览与关注度) · [重点项目](#4-最值得深入看的几条路线) · [源码核实发现](#5-源码核实后需要纠正的印象) · [接入 AutoDigest](#6-如何用于-autodigest) · [方法与证据](#7-调研方法-证据与复核)

## 1. ShowMe 具体指什么

仅凭“ShowMe / showme / 烧密”这个名字，无法唯一确定你此前使用的是哪个项目。本次找到最贴近“让 AI 用可视化帮助理解当前主题”的实现是 **HumanLayer 的 `show-me` skill**。它位于一个 skills 合集内，而不是独立的 ShowMe 绘图应用。[直接打开 SKILL.md](https://github.com/humanlayer/skills/blob/653b6411c1f70c275a18e37673b042ff99f67ceb/plugins/show-me/skills/show-me/SKILL.md)

它的主要价值是选择表达方式：算法用伪代码，调用顺序用调用树，组件关系用组件树，文件职责用目录树，跨组件交互用 Mermaid，改动用 diff，复杂布局再使用 HTML。这里的“可视化”包括代码形状和结构表达，不只意味着图片。它本身没有独立的布局引擎、教学效果评分器或事实校验器。[固定版本的源码分析](notes/showme-skills.md)

还发现了几个需要分开的近名项目：

| 名称 | 实际侧重点 | 与 HumanLayer ShowMe 的区别 |
| --- | --- | --- |
| [Ofori01/show-me](https://github.com/Ofori01/show-me) | 把代码仓库画成可交互的等距系统地图，附文件、行号和引用文本 | 有 schema、引用校验、布局代码和测试；更偏代码理解 |
| [theolundqvist/justshowme](https://github.com/theolundqvist/justshowme) | 交互解释页、手绘风动画幻灯片及配音视频 | 当前版本不止一个简单 HTML skill，部分路径需要更多依赖 |
| [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | 把解释、方案、差异等组织成视觉页面和相关产物 | 当前版本已有渲染与导出实现，不能仍按早期纯提示词介绍 |
| [ericblue/visual-explainer-skill](https://github.com/ericblue/visual-explainer-skill) | 调用图像生成服务制作解释图 | 主要输出图片，与上一项不是同一项目，也不是可操作的数学模型 |

检索到的技能目录和介绍文章只用于发现线索；判断采用原作者仓库与固定版本源码，没有把聚合站的安装量或旧 Star 数当作事实。

## 2. 先按自己的理解障碍选工具

下表是结合代码能力与 AutoDigest 目标提出的选型建议，不是对学习效果做过实验后的排名。

| 我现在卡在哪里 | 优先工具 | 应该得到什么 | 怎样检查是否真的有帮助 |
| --- | --- | --- | --- |
| 一段解释太密，看不出主干 | HumanLayer ShowMe、visual-explainer | 一个聚焦的结构视图或解释页 | 隐藏正文后，能否用图复述关键机制 |
| 材料很多，不知道概念分几层 | Markmap | 可折叠的知识层级 | 能否说清上下位关系；交叉依赖另画关系图 |
| 不知道组件之间如何协作 | Mermaid、draw.io、D2 | 有方向、标签、边界的结构或时序图 | 每条边究竟代表调用、数据、依赖还是因果 |
| 图不对，想边学边改 | Excalidraw、draw.io、Next AI Draw.io | 保留源格式的可编辑图 | 能否改一个节点并同步修正相关连接 |
| 看不懂实际代码怎么运行 | Ofori Show-me、OpenHop、交互架构 skill | 可逐步走读的路径，最好有源码引用 | 图中的路径是否真的在源码中存在 |
| 不懂变量变了为什么结果会变 | Mafs、marimo、Observable Framework | 滑块、拖拽点、真实重算、边界输入 | 先预测变化，再操作验证；允许得到反直觉结果 |
| 数学变换太抽象 | Manim Community、ManimGL、Motion Canvas | 分步骤变换或时间轴动画 | 暂停时能否解释每一步，不只记住画面 |
| 不理解反馈与连锁影响 | LOOPY | 可干预的正负反馈模型 | 能否解释回路；不把简化模型当现实预测 |
| 有实验数据，但看不出规律 | Plot、Vega-Lite、ECharts；特殊需求用 D3 | 有单位、尺度、筛选条件的数据图 | 能否回到原始数据，是否把相关关系误读成因果 |
| 希望以后复习或给别人讲 | teach、Quarto、marimo、Framework | 解释、练习、代码和输出放在一起 | 换一个例子还能否作出正确判断 |

## 3. 仓库总览与关注度

以下 **Star 均为 GitHub REST API 在北京时间 2026-10-15 03:11 左右采集的精确快照**，不是搜索摘要中的近似值。Fork、默认分支提交日期、release、归档状态和许可证检测值见 [仓库元数据表](evidence/repository-index.md) 与 [JSON 证据](evidence/github-metadata.json)。

Star 反映关注度，不能直接代表教学质量、正确率、维护承诺或实际用户数量。**HumanLayer 和 Matt Pocock 的数字是整个 skills 合集的 Star，不能当成 `show-me` 或 `teach` 单项的热度。** 低 Star 的项目仍可能有值得借鉴的验证机制；高 Star 的基础库也未必能直接作为 skill 使用。

### 3.1 ShowMe 类 Skill 与 Agent 绘图入口

本组更接近“我向 AI 提问，它直接给我一个更容易理解的表达”。[解释型 skill 源码笔记](notes/showme-skills.md) · [绘图集成源码笔记](notes/agent-diagram-integrations.md)

| 工具与仓库 | Star | 基本功能与理解价值 | 使用条件与主要边界 |
| --- | ---: | --- | --- |
| [HumanLayer ShowMe](https://github.com/humanlayer/skills/tree/main/plugins/show-me/skills/show-me) | 5,268¹ | 从树、伪代码、Mermaid、diff、HTML 中选择最小有效视图，降低解释负担 | 以 Agent 指令为主；绘图和正确性取决于宿主及生成内容 |
| [Visual Explainer](https://github.com/nicobailon/visual-explainer) | 10,427 | 解释页、方案与差异对照；当前版本还含渲染器、MCP 和多种导出 | 功能路径有不同依赖；HTML 页面不自动等于可复算模型 |
| [visualise](https://github.com/bentossell/visualise) | 484 | 生成内嵌 SVG、HTML 控件和解释图的设计指令 | `visualizer` 代码围栏需宿主实现渲染，复制 skill 不会自动获得该能力 |
| [OpenHop](https://github.com/naorsabag/openhop) | 48 | 让 Agent 生成可逐步播放的数据流，检查流程定义中的节点引用与步骤一致性 | 有前端运行时；公网 Pages 的统计配置与本地模式需分开判断 |
| [Ofori Show-me](https://github.com/Ofori01/show-me) | 6 | 带源码引用的交互代码地图，适合理解仓库结构和调用链 | 引用文本真实不代表解释必然正确；项目规模尚小 |
| [Architecture Diagram Skill](https://github.com/konraddzbik/architecture-diagram-skill) | 118 | 生成可点击、逐步播放数据包流向的架构解释页 | 特别适合系统流程，不是任意领域的通用仿真引擎 |
| [Visualizer Skill](https://github.com/NickyLam/Visualizer-Skill) | 0 | SVG/HTML 图解、结构图和图表的设计规范及参考素材 | 主要是指令和资源，不能据此认定有独立的渲染服务 |
| [JustShowMe](https://github.com/theolundqvist/justshowme) | 9 | 解释页、幻灯片，以及不同动画/视频流程 | 复杂输出需要额外工具；生成视频比日常图解成本高 |
| [Matt Pocock teach](https://github.com/mattpocock/skills/tree/main/skills/productivity/teach) | 290,977¹ | 对话式教学与练习，结合视觉材料组织学习过程 | 学习流程型 skill；全集 Star 不能证明单个教学 skill 的效果 |
| [Excalidraw Diagram Skill](https://github.com/coleam00/excalidraw-diagram-skill) | 5,014 | Agent 写原生图文件，再渲染看图修正 | Python/Playwright/浏览器；该版本未见 LICENSE；自动校验范围有限 |
| [Excalidraw 官方 MCP App](https://github.com/excalidraw/excalidraw-mcp) | 5,520 | 在支持 MCP Apps 的宿主内流式展示和编辑手绘图 | 宿主需支持交互 UI；checkpoint 与分享路径有服务端行为 |
| [draw.io 官方 MCP / Plugins](https://github.com/jgraph/drawio-mcp) | 5,642 | 自然语言经 Agent 产生 XML/Mermaid，搜索形状、布局并继续编辑 | App、Tool Server、skill 是不同接入方式；按输出要求选择 |
| [Excalidraw 官方 CLI](https://github.com/excalidraw/cli) | 149 | 本地图转 PNG，或管理 Excalidraw+ 工作区 | 本地渲染免账号；云工作区需凭据；中文字体可能首次下载 |
| [Next AI Draw.io](https://github.com/DayuanJiang/next-ai-draw-io) | 36,245 | 完整聊天绘图应用，支持按节点编辑、XML 修复与可选视觉复查 | 需要部署或桌面应用、模型 provider；验证不能证明知识正确 |
| [Eric Blue Visual Explainer](https://github.com/ericblue/visual-explainer-skill) | 56 | 图像生成型白板、信息图、思维导图和多帧图片 | 有模型调用成本；主要产物是图片，精确编辑和事实核对较弱 |

¹ 合集仓库总 Star。

### 3.2 结构图 白板 思维导图与绘图基础设施

本组提供真正的解析、布局、编辑、绘制或渲染能力。Agent 通常负责生成输入，工具负责按规则呈现。[逐项源码笔记与许可核对](notes/diagram-tools.md)

| 工具与仓库 | Star | 基本功能与理解价值 | 使用条件与主要边界 |
| --- | ---: | --- | --- |
| [Mermaid](https://github.com/mermaid-js/mermaid) | 90,653 | 文本生成流程、时序、状态、类等图；便于版本管理和正文嵌入 | 图表达的是写入的关系，不会自动证明关系真实；不同宿主支持版本不同 |
| [Excalidraw](https://github.com/excalidraw/excalidraw) | 133,875 | 手绘风白板与可嵌入编辑器，适合边讲边改、保留草图思考 | 编辑器与官方 MCP/CLI 是不同仓库；布局与教学设计仍需人或 Agent |
| [draw.io](https://github.com/jgraph/drawio) | 8,763 | 丰富图形和原生 XML 编辑，适合正式架构、流程和工程图 | 代码与图形资产许可要区分；本次版本 README 不承诺实时协作 |
| [D2](https://github.com/d2lang/d2) | 25,616 | 用结构化文本描述图，编译、自动布局并导出 | 当前官方仓已从 terrastruct 重定向至 d2lang；布局引擎能力随版本变化 |
| [PlantUML](https://github.com/plantuml/plantuml) | 13,364 | 文本生成 UML、时序和状态等工程图；当前同仓还含 MCP 实现 | Java 渲染器与 Node/TeaVM MCP 能力不完全相同，许可也要看所用变体 |
| [Markmap](https://github.com/markmap/markmap) | 13,167 | Markdown 层级转可折叠、缩放的思维导图 | 适合目录和上下位关系；无法用树自然表达所有跨层关系 |
| [Diagrams](https://github.com/mingrammer/diagrams) | 42,725 | 用 Python 编写云服务/系统架构图，以节点和集群组织系统 | 主要依靠 Graphviz 布局；不会从 Python 代码自动推断实际部署 |
| [React Flow / Svelte Flow](https://github.com/xyflow/xyflow) | 38,665 | 构建可拖拽、连接、缩放的节点编辑器 | 是开发组件，不是现成知识解释产品；需自己定义数据语义和交互 |
| [Kroki](https://github.com/yuzutech/kroki) | 4,368 | 以统一 API 调用多种文本绘图后端 | 属于渲染网关；具体图种、依赖和许可由各引擎决定 |
| [AntV Infographic](https://github.com/antvis/Infographic) | 6,996 | 结构化内容生成信息图，结合模板、图形元素和编辑能力；同仓含 creator skill | 很适合关系、顺序、对比的概览；模板不能替代事实和论证 |
| [tldraw](https://github.com/tldraw/tldraw) | 50,919 | 可扩展画布和白板 SDK，可做自定义学习界面 | 当前为 tldraw 自有许可，生产使用需相应许可，不能写成 MIT 工具 |

### 3.3 数学动画 可操纵解释与数据探索

本组帮助理解“变化”和“规律”。播放动画、拖动变量、重新执行计算是不同能力。[逐项源码笔记](notes/interactive-learning.md) · [ECharts 补充](notes/agent-diagram-integrations.md)

| 工具与仓库 | Star | 基本功能与理解价值 | 使用条件与主要边界 |
| --- | ---: | --- | --- |
| [Manim Community](https://github.com/ManimCommunity/manim) | 41,533 | Python 编排数学对象、变换和动画，适合逐步推导 | 学习和渲染成本较高；默认产物是动画，不自动成为滑块实验 |
| [3Blue1Brown ManimGL](https://github.com/3b1b/manim) | 95,073 | 数学动画与 OpenGL 场景，接近原作者创作工具链 | 与 Manim Community 是不同 API 和安装包，教程不能随意混用 |
| [Motion Canvas](https://github.com/motion-canvas/motion-canvas) | 19,327 | 用 TypeScript、生成器和时间轴制作解释动画 | 适合程序员控制节奏与转场；仍需亲自编写解释逻辑 |
| [Mafs](https://github.com/stevenpetryk/mafs) | 3,444 | React 数学图形组件，可拖拽点、画函数、观察几何关系 | 适合数学交互小实验；依赖 React；当前 HEAD 日期较早 |
| [MathBox](https://github.com/unconed/mathbox) | 1,505 | 基于 WebGL/Three.js 的数学场景和数据变换 | 适合复杂空间解释；当前 HEAD 为 2023 年，需额外核对依赖兼容性 |
| [Observable Plot](https://github.com/observablehq/plot) | 5,404 | 用 marks、尺度和数据转换快速构建统计图 | 轻于手写 D3，适合数据证据；不自动建立因果机制 |
| [Observable Framework](https://github.com/observablehq/framework) | 3,663 | Markdown、JavaScript 和数据加载器组成可交互解释站点 | 适合长期维护课程/实验页；部署和数据加载需设计 |
| [marimo](https://github.com/marimo-team/marimo) | 23,173 | Python 响应式笔记本，控件变化带动依赖单元重新计算 | 适合可复算的知识实验；计算逻辑、环境和数据仍由作者负责 |
| [LOOPY](https://github.com/ncase/loopy) | 1,749 | 用带正负关系的节点和信号展示反馈循环 | 很适合形成系统直觉；不是已校准的定量系统动力学求解器 |
| [Quarto](https://github.com/quarto-dev/quarto-cli) | 6,086 | 把文字、代码执行结果和图表发布成文章、书籍或报告 | 更偏组织、执行和出版；具体交互由嵌入内容及执行引擎提供 |
| [D3](https://github.com/d3/d3) | 113,752 | 数据绑定、尺度、布局等基础模块，能构建高度定制的解释图 | 自由度高、工程量大；顶层包是多个子模块的集合 |
| [Vega-Lite](https://github.com/vega/vega-lite) | 5,517 | 声明式统计图语法，编译为 Vega 运行时规格，支持选择交互 | 适合可复用数据表达；超出语法的交互需要下沉到其他层 |
| [Apache ECharts](https://github.com/apache/echarts) | 67,509 | 成熟交互图表库，适合实验曲线、对比和数据探索 | 需要自己定义数据和交互；图表丰富不等于解释自动准确 |

## 4. 最值得深入看的几条路线

### 4.1 先学 ShowMe 的表达选择 再考虑大型生成器

ShowMe 最值得借鉴的不是某一种图，而是“当前问题需要什么视图”。例如研究函数调用，调用树可能已经足够；研究请求往返，时序图比通用方框图更容易暴露先后关系。这样可以减少把所有知识都塞进同一种信息图模板的问题。

如果需要一份独立解释页，`nicobailon/visual-explainer` 值得进一步试用；如果需要围绕已有理解反复提问、练习，`mattpocock/skills` 中的 `teach` 更接近学习流程。它们承担的角色不同：一个加强表达和产物，另一个组织学习互动。[源码依据与版本边界](notes/showme-skills.md)

### 4.2 精确技术图保留 Mermaid Excalidraw 或 draw.io 源文件

对于架构、算法和工程知识，能够检查节点、修改箭头、保留版本差异，通常比只有一张漂亮图片更实用。

Mermaid 的文本适合嵌入 GitHub 文档。Excalidraw 适合自由草图和人工调整。draw.io 适合有正式图形、容器、工程符号需求的图。Agent 集成可以分别选择 Excalidraw Diagram Skill、官方 MCP、draw.io 官方插件或 Next AI Draw.io；**编辑器、skill、MCP 服务和 CLI 不应被当成同一个安装对象。** [绘图基础层](notes/diagram-tools.md) · [Agent 集成层](notes/agent-diagram-integrations.md)

用于理解代码时，Ofori Show-me 的引用校验尤其值得借鉴：让图中重要论断关联文件和原文，再用程序检查引用存在。这能拦住一部分凭空编造，但仍需人判断“这段代码是否真的支持该解释”。本次其引用门禁和示例布局通过了针对性本地检查，详见 [验证记录](evidence/validation.md)。

### 4.3 要理解因果和参数 就给读者可操作的变量

“看过动画”和“能预测变化”之间还有距离。比如学习注意力机制，只播放 Q/K/V 流程不一定能理解缩放因子；可以固定一组并非全部相同的 logits，改变它们共同乘上的正数，观察系数增大时权重更集中、减小时更平缓。这个实验只展示分数尺度的影响；要讨论维度与 `√dₖ`，应另列清楚分量的均值、方差和独立性等统计假设。

Mafs 适合拖拽点、几何和函数关系；marimo 适合有 Python 计算的实验；Framework 适合把交互实验组织成长期维护的网页；Manim 和 Motion Canvas 适合精心编排的过程演示。具体选择取决于需要“操作并重算”还是“按节奏观察”。[对应机制的代码依据](notes/interactive-learning.md)

LOOPY 很适合直观体会正反馈、负反馈和传播，但其代码是简化的信号模型。若问题是库存量、真实时间尺度、物理守恒或政策效果，需要建立相应数学模型和数据校准，不能因为画面有动态就把它当仿真结论。

### 4.4 图像生成适合辅助表达 精确论证另留底稿

Eric Blue 的 skill 把内容转成详细图像提示并调用图片 API，适合做白板风插图和视觉摘要。但它与可编辑 XML、Excalidraw JSON 或可执行数学代码有不同的可验证性。公式、标签、数值、箭头和限定条件应另有可检查的文本/代码来源；多帧图片也不代表变量之间真的被计算过。[图片生成路径与版本问题](notes/agent-diagram-integrations.md)

## 5. 源码核实后需要纠正的印象

这些细节会直接影响选型，不能只看项目简介。

1. **“装了 skill 就能在聊天里交互”并不普遍成立。** bentossell/visualise 的输出约定依赖宿主识别 `visualizer` 围栏；MCP App 也需要宿主的相应 UI 能力。普通 Markdown 阅读器不会自动获得这些能力。[skill 代码依据](notes/showme-skills.md)
2. **“有 validator 就保证正确”不成立。** coleam00 渲染器的程序校验主要检查顶层结构；看图修复靠 Agent 执行工作流。Ofori 的引用检查确认原文存在，也不证明推理成立。[集成审阅](notes/agent-diagram-integrations.md) · [ShowMe 审阅](notes/showme-skills.md)
3. **OpenHop 的本地模式和官方 Pages 构建需要区分。** 本次所审 Pages 配置启用统计，统计代码把 URL hash 纳入上报内容；因此不能照抄 README 中“片段留在浏览器”的表述，推论公开分享内容一定不会上传。本次未对生产站点做网络抓包。[配置与代码证据](notes/showme-skills.md)
4. **TALA 的旧结论已经不适用于所审 D2 版本。** 当前源码包含可选的 TALA 布局实现，并有相应许可说明；不能继续把它笼统写成只能额外购买的闭源组件。[D2 具体版本依据](notes/diagram-tools.md)
5. **公开仓库不等于所有资产都能按 MIT 使用。** tldraw 是自有许可；draw.io 图标模板另有条件；coleam00 项目未见 LICENSE；Excalidraw MCP 的 MIT 声明与单独许可文件的缺失也如实记录。这里只报告源码状态，不替代具体用途的授权核实。[许可证检查](notes/diagram-tools.md) · [集成许可细节](notes/agent-diagram-integrations.md)
6. **GitHub 自动检测可能与实际文件不一致。** Quarto API 返回 `NOASSERTION`，但其 CLI 的 COPYING.md 写明 MIT；PlantUML 有多种许可变体，不能只用 API 的一个字段概括所有发行物。[Quarto](notes/interactive-learning.md) · [PlantUML](notes/diagram-tools.md)
7. **最近有人点 Star 或仓库被推送，不代表核心实现最近更新。** 所采集默认分支 HEAD：MathBox 为 2023-01-25，LOOPY 为 2019-04-17，Mafs 为 2025-03-30。成熟且变化少不等于不可用，但选为长期技术底座前应单独验证依赖与运行环境。[提交快照](evidence/repository-index.md)
8. **宣传中的外部模型名和调用代码需要对齐。** Eric Blue 项目对 Gemini 后端的称呼与实际请求模型 ID 不一致，本次没有执行其外部 API，不能保证照抄就能运行。[具体行号](notes/agent-diagram-integrations.md)

## 6. 如何用于 AutoDigest

结合 [现有 AutoDigest 工作流](../tool/workflows/autodigest.md)，建议把可视化作为回答当前问题的手段，保留“核心解释—反馈—修复”的主线。下面是建议方案，本次调研没有改写现有工具流程。

| AutoDigest 阶段 | 可以加入的能力 | 应保留的产物 |
| --- | --- | --- |
| 输入锚定 | 写清读者卡在分类、机制、时序、数学还是证据 | 具体问题、材料位置和成功标准 |
| 核心解释 | 用 ShowMe 选择一幅最能回答问题的图；复杂机制用原生可编辑格式 | 解释正文、图的源文件、关键论断的出处 |
| 用户反馈 | 让用户指出哪条边不懂，或在改变参数前先预测结果 | 原话反馈、预测与实际结果的差别 |
| 修复 | 修改图和正文；必要时补一个可运行的小实验 | 与正文一致的图、计算代码和边界输入 |
| 检视 | 分别检查事实、计算、视觉布局和运行条件 | 哪些已验证、哪些仍是简化或推测 |
| 输出 | 根据用途保留 Markdown、HTML、原生图、动画或报告 | 可复查版本、依赖说明、可点击来源 |

可以用三个具体题目做后续小规模选型，而不是一次安装全部工具：

- **Transformer Attention**：Mermaid/Excalidraw 解释投影与矩阵形状；marimo，或 Framework 配合显式 JavaScript 计算，做小规模权重实验；Mafs 可辅助理解 Q/K 向量几何。检查维度、归一化、mask 和解释中的条件是否一致。
- **一个仓库的请求链路**：比较 ShowMe 的时序图与 Ofori/OpenHop 的逐步走读。检查每个节点和连接能否定位到真实实现，能否覆盖异常路径。
- **反馈系统**：LOOPY 帮助形成正负反馈直觉，再用明确的数学模型检查量纲和时间演化。分开标注示意关系与定量结果。

建议的验收问题是：**我能否不看原文复述机制，预测一个新输入的结果，指出一个不适用边界，并找到图中关键结论的依据？** 如果只能说“图很好看”，还没有完成知识消化。

## 7. 调研方法 证据与复核

本次完成了候选发现、官方仓定位、固定版本代码审阅、GitHub 元数据采集和部分针对性本地验证。39 个主仓均有源码或 skill 实体审阅；没有把仓库首页当成全部依据，也没有为所有项目安装依赖、连接模型服务或做完整端到端测试。

**证据文件：**

- [ShowMe 与解释型 skill 笔记](notes/showme-skills.md)：入口指令、运行时、引用校验、具体限制。
- [绘图基础工具笔记](notes/diagram-tools.md)：解析、布局、编辑、渲染机制与许可差异。
- [数学与交互学习笔记](notes/interactive-learning.md)：动画、拖拽、响应式执行和数据图语法。
- [Agent 绘图集成笔记](notes/agent-diagram-integrations.md)：官方 MCP/CLI、Excalidraw skill、AI 绘图应用与 ECharts。
- [仓库元数据表](evidence/repository-index.md)：Star、Fork、默认分支提交、API 许可检测、固定源码版本。
- [原始字段快照](evidence/github-metadata.json) 与 [仓库清单](evidence/repositories.json)：保留采集时间和每个 API endpoint。
- [验证记录](evidence/validation.md)：执行了什么、通过了什么，以及不能从测试推出什么。
- [源码引用索引](evidence/source-index.json)：汇集固定 commit 的源码链接，用于复核文件与行号。
- [下载源码与恢复方法](repos/README.md)：40 个本地源码入口及子模块初始化说明；[检出清单](evidence/source-checkouts.json)记录路径、固定版本和迁移核验结果。

源码笔记中的链接尽量固定到 **commit SHA + 文件 + 行号**。主文的仓库首页链接便于继续探索；后续版本可能变化，应以固定版本证据理解本报告的判断。**默认分支源码中的功能，不代表当前 npm/PyPI 包或 GitHub release 已包含。** 多包仓库的 `latest_release` 还可能是其中一个子包：本次 Mermaid 的该字段对应 tiny，xyflow 对应 Svelte，不能把它们当成整个仓库所有包的最新版本。

Graphviz 是 Diagrams 等工具的重要依赖，但其官方主开发仓在 GitLab，因此没有把任意 GitHub 镜像作为第 40 个独立主仓统计。D3 的具体数据绑定实现额外读了 `d3/d3-selection`，它作为支撑依赖进入源码索引，不另计主工具数量。闭源服务和只有聚合列表、缺少实现可检查的项目没有混进这 39 个仓库。

复采 Star 和仓库状态可在仓库根目录运行：

```bash
python3 Research/scripts/collect_github_metadata.py
```

脚本使用已认证的 `gh api` 读取公共元数据，不安装被调研工具。复采会更新 JSON 快照，**不会自动更新本文数字和判断**；需要同步更新表格、日期，并在关键版本变化后重看源码。`open_issues_count` 包括 PR，不能拿它当缺陷数量；`latest_release` 为空也不等于项目停止维护。

本次选型结论建立在功能与源码机制上，没有测量这些工具对真实学习者的理解提升幅度。要验证学习收益，应使用同一材料、同一组具体问题和新的迁移题比较；不能把 Star 或演示页面的视觉效果当作这种证据。
