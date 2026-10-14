# 架构模型、DSL 与长期维护：系统查漏补充

审阅日期：2026-10-15（北京时间）。本组补足原报告中“从共享模型维护多张架构视图”和“从基础设施配置生成架构图”的缺口。结论来自官方文档、GitHub REST API 与固定提交的实现代码，**只做静态源码审阅，没有安装或执行任何上游代码、Skill、MCP、渲染器、Terraform 或更新器**。上游 `AGENTS.md`、`SKILL.md` 均只作为研究材料。

新增源码均位于本项目 `Research/repos/<owner>/<repo>`，采用浅克隆、部分对象下载及稀疏检出；已阅读范围见各条目。SHA 对应审阅时默认分支，可能含发布版之后的变化。源码存在某能力不代表每一个已发布安装包都含该能力。本组没有把每个仓库声称的支持范围全部跑通。

GitHub 原始数据与取舍见 [候选及 API 快照](../evidence/architecture-modeling-candidates.json)。Star、fork 是仓库级数值；不等于使用人数、图形质量、正确率或教学效果。旧 Structurizr 仓库只记录迁移证据，不作为多个独立工具增加推荐数量。

## 收录与分工

| 工具 / 正式仓库 | Stars / forks | 本次固定 SHA | 最新正式 GitHub Release | 核心缺口 |
|---|---:|---|---|---|
| [LikeC4](https://github.com/likec4/likec4) | 5,875 / 400 | `5385c577042988691f66cd82e65d60d13121d468` | v1.59.4，2026-09-21 | 自定义架构语言、单一模型、多视图、交互站点 |
| [Structurizr](https://github.com/structurizr/structurizr) | 463 / 68 | `da99caf2f2857e5373f7b58569152274f1725ba3` | v2026.09.19，2026-09-19 | C4 模型及现行统一工具链 |
| [C4-PlantUML](https://github.com/plantuml-stdlib/C4-PlantUML) | 7,433 / 1,170 | `f998c46833daac592f3283ff08d7b8cd7e1558fb` | v2.14.0，2026-08-26 | PlantUML 的 C4 语义和图形约定 |
| [Archi](https://github.com/archimatetool/archi) | 1,286 / 344 | `fbfa4474c414477ce88257c956999fb9efdf9e69` | 此源码仓 API 返回空；官网正式版为 5.10.0 | ArchiMate 企业架构模型与人工建模 |
| [TerraVision](https://github.com/patrickchugh/terravision) | 1,655 / 175 | `7abacaab1483ccdcd4e59470b0097d23d9a05955` | v0.52.0，2026-10-02 | Terraform 计划 / 依赖图到云基础设施图 |

前四仓 API 采集时间为 `2026-10-14T20:53:31Z`；TerraVision 为 `2026-10-14T20:55:38Z`。Archi 的官网明确提供 2026-09-03 发布的 5.10.0，支持 ArchiMate 3.2；因此源码仓 `latest_release: null` 不能解释为没有发行版。[官方下载页](https://www.archimatetool.com/download/)

## 1. LikeC4：把架构知识维护成模型，再按问题生成视图

[正式仓库](https://github.com/likec4/likec4) · [官网](https://likec4.dev/) · [语言入门](https://likec4.dev/dsl/intro/) · [视图定义](https://likec4.dev/dsl/views/)

**基本功能与输入输出。** 输入 `.c4` / `.likec4` 文件：定义元素类型、嵌套结构、关系，以及各张视图的选择条件；再生成可浏览的架构站点、图像和其他导出形式。它借鉴 C4 与 Structurizr，但允许自定义类型和层级，不能直接当作无需约定即可严格遵守 C4 的工具。“从代码生成”在这里首先指从架构 DSL 生成，不能理解成自动分析任意业务仓库并保证模型随实现同步。

**帮助理解的价值。** 同一个服务可以出现在全局图、某条业务交互图和部署视图中，复用的是模型实体和关系。对于持续更新的系统知识库，这比手工维护多张互不关联的方框图更容易保持术语一致。开发者可以先看全局，再选与问题相关的子集。

**源码核实。**

1. 模型构建器收集项目文档并交给 `buildModelData`，还区分跨项目导入的合并阶段；视图计算器针对元素、部署、动态视图使用同一模型。[多文件模型构建](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/language-server/src/model/model-builder.ts#L179-L217) · [模型到多视图](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/core/src/compute-view/compute-view.ts#L33-L84)
2. 布局器实际将视图打印为 DOT，调用 Graphviz 得到 JSON 坐标再解析成 diagram；默认使用 WASM 适配器，动态视图还计算时序布局。这里确有拓扑驱动的布局链，区别于 Archify 架构图主要由作者给节点位置。[布局实现](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/layouts/src/graphviz/GraphvizLayoter.ts#L71-L151)
3. `build` 从工作目录创建语言服务，再调用 Vite 生成静态站点；CLI 默认选 WASM，也能切换本机 dot。PNG/JPEG 路径另用 Playwright 启动 Chromium 截图。[站点构建](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/likec4/src/cli/build/index.ts#L79-L104) · [图像导出](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/likec4/src/cli/export/png/handler.ts#L90-L115)
4. 当前源码有官方 MCP Apps `render-view`，返回布局数据并绑定交互 UI 资源；需要宿主支持 MCP Apps 才能在聊天里交互。不能照抄服务器描述中的“所有工具只读”：已注册的 `apply-semantic-layout` 会请求 MCP sampling，并调用 `editor.applyChange` 保存布局快照。[交互视图工具](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/mcp/src/tools/render-view.ts#L17-L62) · [布局工具会写快照](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/mcp/src/tools/apply-semantic-layout.ts#L66-L130)

**运行、许可与局限。** 本次 HEAD 的 CLI 要求 Node `>=22.22.3`；图像导出还依赖浏览器环境。主项目 MIT；实际查读了 `packages/likec4/LICENSE`。模型仍需人或 Agent 维护，模型检查和自动排版不证明系统实现符合模型。[Node 条件](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/likec4/package.json#L244-L246) · [MIT 许可](https://github.com/likec4/likec4/blob/5385c577042988691f66cd82e65d60d13121d468/packages/likec4/LICENSE#L1-L21)

**与 Archify 的关系。** 优先用于“一个系统需要长期维护多张一致视图”；Archify 更适合围绕当前问题迅速交付一份解释材料。两者可以互补，但本次没有验证自动互转或直接集成，不能当作现成功能。

## 2. Structurizr：现行 C4 参考实现，必须避开过时仓库入口

[当前主仓](https://github.com/structurizr/structurizr) · [官方文档](https://docs.structurizr.com/) · [在线 Playground](https://playground.structurizr.com/) · [官方迁移 / EOL 说明](https://docs.structurizr.com/eol)

**身份与现状。** Structurizr 由 C4 模型作者创建，当前主仓是 `structurizr/structurizr`。API 显示该仓创建于 2025-11-30；463 Stars 是这个新仓的关注度，不能代表整个产品从零开始。`structurizr/cli`、`lite`、`java`、`ui`、`onpremises` 当前均 `archived: true`，精确快照已保留。旧 `structurizr/dsl` API 返回 HTTP 404；404 本身不足以推断是删除、改名还是转私有。本次推荐以新仓及官方迁移表为准，不继续把旧 Lite / CLI 当作当前首选安装入口。

官方明确：Lite 由 `local` 取代，旧 CLI 功能并入 `pull` / `push` / `export` 等统一命令，on-premises 由 `server` 取代；旧 cloud service 没有替代产品。[官方 EOL](https://docs.structurizr.com/eol)

**基本功能与输入输出。** 输入 Structurizr DSL，也可由 Java API 构建 workspace；同一 workspace 保存模型、视图和文档。输出系统上下文、容器、组件、动态和部署等视图，可以本地浏览、发布到自托管服务，或导出静态站点及 PlantUML / C4-PlantUML / Mermaid 表达。它解决的是结构与视图的一致性，尤其适合 C4 体系；不是通用的业务代码逆向分析器。

**源码核实。**

1. `Workspace` 实际持有 `Model`、`ViewSet`、`Documentation`，不是只收集多张独立图片。`ViewSet.createDefaultViews` 遍历同一模型建立系统上下文、容器、组件等视图。[模型、视图与文档](https://github.com/structurizr/structurizr/blob/da99caf2f2857e5373f7b58569152274f1725ba3/structurizr-core/src/main/java/com/structurizr/Workspace.java#L20-L76) · [从模型建立多视图](https://github.com/structurizr/structurizr/blob/da99caf2f2857e5373f7b58569152274f1725ba3/structurizr-core/src/main/java/com/structurizr/view/ViewSet.java#L1191-L1218)
2. DSL parser 按所在上下文创建 software system / container / component，并登记标识符。C4 层次有具体对象和上下文约束，而非仅靠不同颜色模拟。[DSL 语义处理](https://github.com/structurizr/structurizr/blob/da99caf2f2857e5373f7b58569152274f1725ba3/structurizr-dsl/src/main/java/com/structurizr/dsl/StructurizrDslParser.java#L486-L524)
3. `ExportCommand` 注册 JSON、PlantUML、C4-PlantUML、Mermaid 等 exporter，遍历 workspace 的视图写文件；PNG/SVG 分支会检查是否包含 Playwright 实现，缺少时明确拒绝。不能把所有下载包说成导出能力相同，也不能假定导出后保留原 Viewer 的所有交互和样式。[导出后端](https://github.com/structurizr/structurizr/blob/da99caf2f2857e5373f7b58569152274f1725ba3/structurizr-application/src/main/java/com/structurizr/command/ExportCommand.java#L43-L64) · [图像导出条件](https://github.com/structurizr/structurizr/blob/da99caf2f2857e5373f7b58569152274f1725ba3/structurizr-application/src/main/java/com/structurizr/command/ExportCommand.java#L123-L132)
4. 当前主仓有官方 MCP 模块：`validate` 真正调用 DSL parser，`parse` 返回 workspace JSON，`inspect` 运行 `DefaultInspector` 汇集违反项。这些检查面向模型和语法，不能证明部署现场与模型一致。[MCP 实现](https://github.com/structurizr/structurizr/blob/da99caf2f2857e5373f7b58569152274f1725ba3/structurizr-mcp/src/main/java/com/structurizr/mcp/DslTools.java#L29-L92)

**运行与许可。** 公共主仓为 Apache-2.0；构建目标 Java 21，官方提供 Java WAR / Docker。务必区分开源核心与官方预编译 server：官方说明自编译 open core 可免费用，但预编译 server 的企业扩展需要许可；open core 的认证为 None、没有角色权限、workspace 为 Public。其他统一命令的免费使用说明不能推导成“整个官方 server 免费”。本次不报具体价格，避免把会变化的商业报价写死。[Java 与源码许可声明](https://github.com/structurizr/structurizr/blob/da99caf2f2857e5373f7b58569152274f1725ba3/pom.xml#L11-L21) · [官方 server 版本差异](https://docs.structurizr.com/server) · [官方发行包及 Playwright 条件](https://docs.structurizr.com/binaries)

**与 Archify 的关系。** 系统结构需要严格按 C4 组织、多个团队长期维护一份模型时，Structurizr 更合适；临时讲解一个调用链或整理一份交互读物时，Archify 更直接。导出 Mermaid / C4-PlantUML 是已有实现；自动导出 Archify 本次未发现或验证，不作承诺。

## 3. C4-PlantUML：值得单独介绍的领域扩展，不重复推荐引擎

[正式仓库](https://github.com/plantuml-stdlib/C4-PlantUML) · [说明与例子](https://github.com/plantuml-stdlib/C4-PlantUML#readme) · [C4 官方工具目录](https://c4model.com/tooling)

**基本功能与输入输出。** 这是 PlantUML 宏库：用 `Person`、`System`、`Container`、`Component`、`Rel`、边界和标签等约定写 `.puml`，由 PlantUML 渲染成图。还提供动态交互编号与部署图形。这里的“Container”是 C4 的应用 / 数据存储抽象，不等于只指 Docker 容器。

**帮助理解的价值。** 它把“谁使用系统、系统包含什么、组件怎样依赖”整理成一致的视觉语言；适合已经使用 PlantUML 的团队把架构图纳入代码评审和文档构建。主报告应把它标为 PlantUML 领域扩展，避免让人以为又多了一套独立渲染引擎。

**源码核实。**

1. `Container` 等宏调用 `$getElementLine`，后者把类型、标题、技术说明、属性、标签和链接组装成 PlantUML 元素声明。[容器宏](https://github.com/plantuml-stdlib/C4-PlantUML/blob/f998c46833daac592f3283ff08d7b8cd7e1558fb/C4_Container.puml#L73-L97) · [宏展开机制](https://github.com/plantuml-stdlib/C4-PlantUML/blob/f998c46833daac592f3283ff08d7b8cd7e1558fb/C4.puml#L1234-L1244)
2. 普通关系宏生成箭头，动态图的 `Rel` 增加交互序号前缀。这提供表达约定，不是从程序运行中采集真实调用序列。[动态编号实现](https://github.com/plantuml-stdlib/C4-PlantUML/blob/f998c46833daac592f3283ff08d7b8cd7e1558fb/C4_Dynamic.puml#L29-L47)
3. `Lay_D/Up/Right/Left` 通过隐藏连接向底层布局器施加相对位置约束。布局仍依赖 PlantUML 及所选后端；本库不是一个另行实现的自动布局器。[位置约束](https://github.com/plantuml-stdlib/C4-PlantUML/blob/f998c46833daac592f3283ff08d7b8cd7e1558fb/C4.puml#L1922-L1947)
4. 顶层文件默认远程 include `master` 上的下一层文件，配置 `RELATIVE_INCLUDE` 才改为本地相对 include。因此只把最外层 URL 固定到 SHA，不能保证整个依赖链固定；可使用同一版本的本地完整库，或固定包含相应标准库的 PlantUML 版本。[默认远程依赖链](https://github.com/plantuml-stdlib/C4-PlantUML/blob/f998c46833daac592f3283ff08d7b8cd7e1558fb/C4_Component.puml#L1-L6) · [基础库 include](https://github.com/plantuml-stdlib/C4-PlantUML/blob/f998c46833daac592f3283ff08d7b8cd7e1558fb/C4_Context.puml#L1-L6)

**运行、许可与局限。** 库本身 MIT；PlantUML 引擎及附加图标的许可需分别看待。需要 PlantUML 运行环境或兼容服务，本地 Java 路径、引擎版本和布局后端由使用者配置。它没有 LikeC4 / Structurizr 那样独立的“单一架构模型到多张查询视图”模型层；可以人工拆分、复用 include，但跨图一致性仍需额外管理。宏生成成功不代表符合真实架构，也不等于自动验证 C4 建模质量。[库的 MIT 许可](https://github.com/plantuml-stdlib/C4-PlantUML/blob/f998c46833daac592f3283ff08d7b8cd7e1558fb/LICENSE#L1-L21)

**与 Archify 的关系。** 适合现有 PlantUML 文档链、明确需要 C4 风格和文本差异评审的场景；Archify 的独立 HTML 探索体验更丰富。若先维护 Structurizr 模型，再导出 C4-PlantUML，可同时获得共享模型和成熟渲染链，这条路线已有 exporter 支撑。

## 4. Archi：ArchiMate 企业架构模型编辑器，不是 Archify

[正式仓库](https://github.com/archimatetool/archi) · [官网](https://www.archimatetool.com/) · [下载](https://www.archimatetool.com/download/)

**基本功能与输入输出。** Archi 是桌面 ArchiMate 建模器，用元素、关系和视点描述业务、应用、技术、动机、实施迁移等层次。输入主要是人工建立 / 导入的模型；保存 `.archimate` 模型，能导出 HTML 报告与 ArchiMate Model Exchange XML。它与 Archify 名字相近，但并非同一项目：Archi 重在持续维护企业架构模型，Archify 重在 Agent 图解生成与交付。

**帮助理解的价值。** 当问题从“哪个服务调用哪个服务”扩展为“哪个业务能力依赖哪些应用、迁移会影响哪些技术与目标”时，共享元素、多视图和关系规则比单张技术架构图更有价值。它也要求读者学习 ArchiMate 语义，不宜作为每次日常问答的默认工具。

**源码核实。**

1. 图上的 `DiagramModelArchimateObject` 引用底层 `IArchimateElement`；读写名称会转发到模型元素，并登记该元素对应的图对象。多个视图可以复用同一个模型实体，区别于各画一份独立文本。[图对象与共享模型](https://github.com/archimatetool/archi/blob/fbfa4474c414477ce88257c956999fb9efdf9e69/com.archimatetool.model/src/com/archimatetool/model/impl/DiagramModelArchimateObject.java#L255-L297)
2. Validator 收集元素、关系和视图，并可按偏好启用非法关系、未使用元素、空视图、重复和视点检查。具体非法关系检查会将源、目标和关系类型交给 ArchiMate 规则判断；这验证模型规则，不验证业务事实。[模型检查链](https://github.com/archimatetool/archi/blob/fbfa4474c414477ce88257c956999fb9efdf9e69/com.archimatetool.hammer/src/com/archimatetool/hammer/validation/Validator.java#L71-L138) · [关系校验实现](https://github.com/archimatetool/archi/blob/fbfa4474c414477ce88257c956999fb9efdf9e69/com.archimatetool.hammer/src/com/archimatetool/hammer/validation/checkers/InvalidRelationsChecker.java#L43-L65)
3. HTML exporter 复制页面骨架，分别生成模型说明、元素、视图和图片，输出可供其他人浏览的报告目录。它不是单纯截图导出。[HTML 报告](https://github.com/archimatetool/archi/blob/fbfa4474c414477ce88257c956999fb9efdf9e69/com.archimatetool.reports/src/com/archimatetool/reports/html/HTMLReportExporter.java#L229-L274)
4. XML exporter 分别写模型元素、关系、属性定义及视图。跨工具交换的是结构化模型；本次没有运行导入导出往返，不能保证与任意 ArchiMate 工具无损互通。[模型交换格式](https://github.com/archimatetool/archi/blob/fbfa4474c414477ce88257c956999fb9efdf9e69/org.opengroup.archimate.xmlexchange/src/org/opengroup/archimate/xmlexchange/XMLModelExporter.java#L217-L250)

**运行、许可与局限。** 主代码 MIT，桌面发行支持 Windows、macOS 和 Linux，具体最低系统版本以官方下载页为准；Eclipse / Java 生态依赖保留各自条款。它不是轻量浏览器白板，也不是自然语言直接生成事实模型的 Skill；本次未检查协作插件或声称主仓自带 Git 协作。[主仓 MIT 许可](https://github.com/archimatetool/archi/blob/fbfa4474c414477ce88257c956999fb9efdf9e69/License.txt#L1-L21)

**与 Archify 的关系。** 面向企业架构治理和长期变更影响分析时优先考虑 Archi；围绕代码阅读或短期主题进行解释时优先 Archify / LikeC4。不能把两者品牌、星数、安装方式混用。

## 5. TerraVision：从 Terraform 计划生成云基础设施架构图

[正式仓库](https://github.com/patrickchugh/terravision) · [官方文档](https://patrickchugh.github.io/terravision/) · [示例画廊](https://patrickchugh.github.io/terravision/gallery/)

**基本功能与输入输出。** 核心有两条入口：Terraform 目录 / Git URL 或预先导出的 plan JSON + graph DOT；以及人工 / Agent 编写的 `.tvg.json` 云资源图。输出 PNG、SVG、PDF、可编辑 draw.io 文件，Terraform 路线还可生成带资源元数据的交互 HTML。AWS、Azure、GCP 有各自映射及处理逻辑；这里不把 README 的资源覆盖数量视为全部经过本次测试。

**帮助理解的价值。** 它补足“架构图的节点从哪里来”这个缺口：当基础设施已经以 Terraform 描述，计划数据能提供比纯语言描述更明确的资源、变量、模块和部署分组依据。可以据此阅读网络、子网、服务依赖，并在配置变化时重新生成文档。它呈现的是配置 / 计划与绘图规则的结果，**不是云端运行态扫描，也不是漂移检测**。

**源码核实。**

1. 普通 Terraform 路线会运行 `init`，再以 `plan -refresh=false` 生成计划，通过 `show -json` 和 `graph` 取数据。临时覆盖本地 backend、处理 Terraform Cloud 配置并在 finally 恢复。它不只是静态读取 HCL；`init` 会下载模块 / provider，计划可能需要网络和云凭据。JSON 图和预生成 plan/graph 路线可跳过这些执行步骤。[初始化](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/tfwrapper.py#L267-L297) · [计划与图数据](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/tfwrapper.py#L320-L387) · [数据组装及恢复](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/tfwrapper.py#L430-L466) · [预生成数据入口](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/terravision/terravision.py#L218-L226)
2. 处理后的架构图不是 Terraform 图的逐节点无损副本。`consolidate_nodes` 会按配置合并资源、删去 `null_resource`，并去除合并节点内部连接；边还经过资源类型处理和推断。因此不采纳宣传中的“provably accurate”作为审查结论。[资源省略](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/graphmaker.py#L1588-L1603) · [资源合并](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/graphmaker.py#L1624-L1653)
3. draw.io 导出不是把 PNG 塞进画布：程序读取 Graphviz xdot 坐标，结合云厂商 shape 映射生成 mxGraph XML。交互 HTML 则内嵌预渲染 SVG、资源 metadata 与仓库内的 d3.js。[可编辑 draw.io 导出](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/drawing.py#L2232-L2268) · [独立 HTML 组装](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/html_renderer.py#L496-L533)
4. 当前包含官方 MCP 和 Agent Skill；MCP 封装真实 Terraform / 图形生成路径，普通 JSON 图不自动变成含真实资源属性的交互 HTML。“图到 Terraform”目前主要是 Skill 让 Agent 按图写代码的工作流，不能说已经实现确定性、无损的图形到 IaC 编译器。[交互 HTML 工具条件](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/modules/mcp_server.py#L516-L550) · [反向代码生成约定](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/skills/terravision-cloud-diagrams/SKILL.md#L198-L203)

**运行、许可与局限。** 主许可是 **AGPL-3.0-only**，不能与 MIT 工具混写；Python ≥3.11，渲染需要 Graphviz，Terraform 路线还需要相应 Terraform / OpenTofu 工具链。HEAD 的 `pyproject.toml` 声明 0.53.0，而 API 最新正式 Release 为 v0.52.0，本文审阅的是前述固定 HEAD。JSON 描述图的正确性依然取决于作者；“不用云访问”只能对相应无凭据入口作有条件表述。上游自己的 Skill 明确承认运行计划常需要凭据，与 README 无条件宣传有差异。[版本、Python 与许可](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/pyproject.toml#L5-L12) · [Terraform 条件](https://github.com/patrickchugh/terravision/blob/7abacaab1483ccdcd4e59470b0097d23d9a05955/skills/terravision-cloud-diagrams/SKILL.md#L65-L80)

**与 Archify 的关系。** 用户已有 Terraform 时先考虑 TerraVision 提取基础设施视图，再依据实际问题选择是否补一张 Archify 讲解图；业务代码调用链、一般知识结构仍更适合 Archify 等工具。本次未验证两者的格式互转。TerraVision 的同一张云图更接近工程配置来源，Archify 的类型和讲解对象更广。

## 如何纳入原报告而不过度堆工具

- “现在就理解这个系统”：保留 Archify 的优先位置，配合 ShowMe 选择表达形式。
- “同一系统要维护多张一致视图”：加入 LikeC4 / Structurizr，分别说明自定义建模与 C4 约束。
- “团队已经用 PlantUML”：加入 C4-PlantUML 扩展入口，不重复介绍 PlantUML 引擎。
- “业务、应用、技术和迁移要一起治理”：加入 Archi。
- “基础设施以 Terraform 为事实材料”：加入 TerraVision，并保留计划态、推断边、资源合并和运行依赖边界。

这些是基于实现机制的适用性判断，**不是实测效果排名**。没有哪一项可以仅凭渲染成功、规则校验通过或高 Star 数证明架构事实正确。
