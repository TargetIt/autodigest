# ShowMe 与交互知识解释工具：源码核查笔记

调研日期：2026-10-15。范围：9 个 GitHub 仓库的视觉解释、交互流程、教学类 skill。先网页搜索确认来源，再浅克隆当前默认分支，固定提交后读源码。全部源码链接固定到本次检查的完整 commit SHA；未发现仓库迁移。

本页记录“工具是什么、代码做了什么、没有证明什么”。星数、fork 和更新时间以汇总文档的 GitHub API 集中快照为准；`humanlayer/skills`、`mattpocock/skills` 的星数属于整个合集，不能当成单独 `show-me` 或 `teach` 的使用量。

除 Ofori01/show-me 的三组本地校验外，本页均为静态源码核查。未安装外来 skill、未修改全局 agent 配置、未启动服务、未调用付费 API，也未把宣传截图当成亲测结果。外部 README/SKILL 的指令仅是研究材料。

## 先识别 ShowMe 的身份

用户没有提供原始链接，不能断言之前用过的是哪一个。结合“一个帮助理解的 showme skill”的描述，**HumanLayer 的 `show-me` 最贴近这个名字与用途**：官方于 2026-08-12 发布，并致谢 Matt Pocock `/teach` 的 HTML 教学页。另一个同名 `Ofori01/show-me` 是带源码引用校验的等距代码地图，不应混为一谈。[HumanLayer 官方发布文章](https://www.humanlayer.com/blog/show-me-skill)

| 名称 | 交付内容 | 是否自带运行时代码 | 适合解决的问题 |
|---|---|---|---|
| HumanLayer show-me | 伪代码、调用树、组件树、diff、Mermaid 或 HTML | show-me 子目录没有渲染器/校验器 | 把当前解释压缩成最小可理解形状 |
| Ofori01/show-me | 带来源的等距系统地图、流程及 Markdown 文本版 | 有：Node 校验、计量、布局与渲染 | 看懂代码库并回查图中关系 |
| theolundqvist/justshowme | 交互讲解、动画幻灯片、讲解视频三种 skill | 有：模板、截图、帧检查、视频流水线 | 做出能操作、展示、逐步观看的解释材料 |
| nicobailon/visual-explainer | HTML 图解、审查、方案和幻灯片，另有导出工具 | 当前有可选 MCP、JSON/计划渲染器、视频/PPTX | 将抽象机制和比较结果做成解释页 |

## 固定版本清单

| 仓库 | 本次审查提交 | 许可证状态 |
|---|---|---|
| [humanlayer/skills](https://github.com/humanlayer/skills) | [`653b6411c1f7`](https://github.com/humanlayer/skills/commit/653b6411c1f70c275a18e37673b042ff99f67ceb) | MIT（已读仓库 LICENSE） |
| [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | [`33a6b4d43958`](https://github.com/nicobailon/visual-explainer/commit/33a6b4d43958d2d152c9cb13762af802062fade5) | MIT（已读仓库 LICENSE） |
| [bentossell/visualise](https://github.com/bentossell/visualise) | [`35cd185b58af`](https://github.com/bentossell/visualise/commit/35cd185b58af5db2f9d0fe13d9872b544a467483) | README 声明 MIT；未见独立 LICENSE |
| [naorsabag/openhop](https://github.com/naorsabag/openhop) | [`927015aebbee`](https://github.com/naorsabag/openhop/commit/927015aebbeeb2559e6296946b57b2594c9a1d37) | MIT（已读仓库 LICENSE） |
| [Ofori01/show-me](https://github.com/Ofori01/show-me) | [`62c8905665be`](https://github.com/Ofori01/show-me/commit/62c8905665be8ff6f51df05eaccf6b38e1c183e1) | MIT（已读仓库 LICENSE） |
| [konraddzbik/architecture-diagram-skill](https://github.com/konraddzbik/architecture-diagram-skill) | [`cd94e972682d`](https://github.com/konraddzbik/architecture-diagram-skill/commit/cd94e972682dfacd7c741f9096cacc90d5cc5c41) | MIT（已读仓库 LICENSE） |
| [NickyLam/Visualizer-Skill](https://github.com/NickyLam/Visualizer-Skill) | [`409cc699c56b`](https://github.com/NickyLam/Visualizer-Skill/commit/409cc699c56bbdfc2b52a70509c24642585c0d5f) | MIT（已读仓库 LICENSE） |
| [theolundqvist/justshowme](https://github.com/theolundqvist/justshowme) | [`b7e20e8966d8`](https://github.com/theolundqvist/justshowme/commit/b7e20e8966d852f95c470179ee0b23f5abbab936) | MIT（已读仓库 LICENSE） |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [`49dd158d1076`](https://github.com/mattpocock/skills/commit/49dd158d1076134a641b33efb035946536778336) | MIT（已读仓库 LICENSE） |

## 1. HumanLayer show-me：最轻的“换一种方式讲清楚”

**基本功能与输入输出。** 输入当前对话、算法、代码修改或困惑，输出伪代码、运行时调用树、UI 组件树、文件职责树、Mermaid 时序图及增删 diff；遇到布局或过密概念才写一个聚焦 HTML 文件。核心是挑出回答当前问题所需的少数结构。[仓库](https://github.com/humanlayer/skills) · [表达方式](https://github.com/humanlayer/skills/blob/653b6411c1f70c275a18e37673b042ff99f67ceb/plugins/show-me/skills/show-me/SKILL.md#L7-L118)

**如何帮助理解。** “谁调用谁”“前后哪里不同”“状态归谁拥有”等问题，可以直接用树和差异图露出顺序与边界。适合作为 AutoDigest 核心解释的默认小工具，不必给每个问题都创建网站。前置信息为 `disable-model-invocation: true`，对应显式 `/show-me` 调用。[入口](https://github.com/humanlayer/skills/blob/653b6411c1f70c275a18e37673b042ff99f67ceb/plugins/show-me/skills/show-me/SKILL.md#L1-L7)

**源码核实。** 本体只有一份 128 行 `SKILL.md`、agent 元数据及插件清单；没找到 show-me 专用解析器、渲染引擎、引用校验或回归测试。仓库根目录其他技能的测试不能算成 show-me 的正确性验证。HTML 由宿主模型生成、由宿主浏览器打开；仓库没有打包可视化聊天客户端。[HTML 与最小范围原则](https://github.com/humanlayer/skills/blob/653b6411c1f70c275a18e37673b042ff99f67ceb/plugins/show-me/skills/show-me/SKILL.md#L118-L128)

**局限、成本、审查深度。** 主要成本是模型生成与上下文；复杂输出需 Mermaid 支持或浏览器。没有事实门禁，精简也可能漏条件。已完整阅读 show-me 本体及元数据，未运行模型生成。[MIT 许可证](https://github.com/humanlayer/skills/blob/653b6411c1f70c275a18e37673b042ff99f67ceb/LICENSE#L1-L13)

## 2. nicobailon/visual-explainer：从概念到完整交互解释页

**基本功能与输入输出。** 输入概念、架构、git diff、方案或项目回顾，得到 SVG、步骤播放器和图表组成的单页 HTML，也可按需生成幻灯片。当前包为 `0.12.0`：普通模式仍以模型编写 HTML 为主，另有 JSON quick 模式、交互计划渲染、MCP、PPTX/MP4 导出。[仓库](https://github.com/nicobailon/visual-explainer) · [命令与 quick 模式](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/README.md#L432-L451) · [包版本](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/package.json#L1-L8)

**如何帮助理解。** 一幅图表达一个结论，边标注行为；stepper 分步揭示机制，滑块/开关改变共同模型、数字和图形同步更新。适合缓存命中、TTL、权衡曲线和方案差异的反事实探索。**当前默认已改成手工编排 SVG**，仅在用户要求或提供源码时选 Mermaid；旧评测的默认 Mermaid 描述已不适用。[表达规则](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/SKILL.md#L31-L67) · [联动高亮和步骤播放](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/references/diagrams.md#L76-L89)

**源码核实。**

- `quick/render.mjs` 真正校验字段、枚举、表格列数及 flow 节点引用并转义文本；但它是有限 JSON 到 HTML 模板，`flow` 实际输出节点卡片和文本化边列表，不能误写为任意拓扑自动布局。[校验](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/quick/render.mjs#L55-L147) · [实际 flow 渲染](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/quick/render.mjs#L175-L188)
- `plan/render.mjs` 读取仓库文件、检查路径和行范围，抽取源码片段，并接受 `read/inferred/guess` 证据等级。它能查“文件/行存在”，不能证明自然语言结论在语义上正确。[读文件](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/plan/render.mjs#L123-L149) · [证据与片段抽取](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/plan/render.mjs#L234-L277)
- `/fact-check` 是让 agent 提取主张、对照代码、修订页面的提示词，不是独立事实验证算法。MCP 是本地 stdio，接收 HTML 或 quick JSON；写入范围约束和临时文件重命名属于文件安全机制。[fact-check 本体](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/commands/fact-check.md#L1-L13) · [MCP 写入检查](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/mcp/server.mjs#L135-L162)

**局限和成本。** 普通 HTML 需要模型、文件写入与浏览器，字体/部分库可用 CDN，不能笼统称完全离线。可选 MCP/PPTX 要 Node 依赖；视频要浏览器、Playwright、ffmpeg，配音可另需语音 API。PPTX 是有损静态输出，不保留 SVG/Canvas/动态图表、动画及响应布局。[依赖](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/package.json#L51-L70) · [PPTX 边界](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/pptx/README.md#L1-L13) · [视频成本](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/plugins/visual-explainer/references/video.md#L59-L76)

**审查深度。** 读 README、完整 skill、quick/MCP/计划关键实现、fact-check、视频/PPTX 说明及依赖；未生成成品或执行浏览器 QA。根 `package.json` 仅列版本检查脚本，本次文件树未发现独立测试套件；校验代码不等于完整测试覆盖。[MIT 许可证](https://github.com/nicobailon/visual-explainer/blob/33a6b4d43958d2d152c9cb13762af802062fade5/LICENSE#L1-L13)

## 3. bentossell/visualise：对话内视觉规范，渲染端另接

**基本功能与输入输出。** 输入机制、流程、方案比较或数据问题，输出 `visualizer` 围栏包裹的 SVG/HTML 片段。设计资料拆为颜色排版、图解、交互组件、Chart.js 模块按需读取。[仓库](https://github.com/bentossell/visualise) · [模块和生成规则](https://github.com/bentossell/visualise/blob/35cd185b58af5db2f9d0fe13d9872b544a467483/SKILL.md#L21-L39)

**如何帮助理解。** 按“机制/部件/步骤/差异”选表达形式；滑块处理本地数值变化，图上点击可借宿主 `sendPrompt` 追问。这个桥接函数不是 skill 自己提供的。[追问和图形路由](https://github.com/bentossell/visualise/blob/35cd185b58af5db2f9d0fe13d9872b544a467483/SKILL.md#L60-L79)

**源码核实。** README 明确没有附带 renderer。`references/client-implementation.md` 是 iframe 接入示例文档，不是已发布可启动客户端；仓库无 package manifest、构建系统或测试。复制 skill 不会使普通终端/Markdown 自动得到内嵌交互。[作者声明的客户端边界](https://github.com/bentossell/visualise/blob/35cd185b58af5db2f9d0fe13d9872b544a467483/README.md#L45-L51) · [renderer 代码示例](https://github.com/bentossell/visualise/blob/35cd185b58af5db2f9d0fe13d9872b544a467483/references/client-implementation.md#L23-L63)

**局限、成本、审查深度。** 宿主不识别围栏时要文件浏览或自行开发；主题、CSS 变量、CSP、`sendPrompt` 都是宿主契约，不是 skill 自身强制出的能力。主要成本为模型，部分图表加载 CDN。已读完整 skill、README、客户端示例和资源结构，未实装。许可证应准确写为“[README 声明 MIT](https://github.com/bentossell/visualise/blob/35cd185b58af5db2f9d0fe13d9872b544a467483/README.md#L53-L55)，本次快照未见独立 LICENSE”。

## 4. OpenHop：带真实运行时的逐跳流程讲解

**基本功能与输入输出。** 输入 agent 阅读得到的流程或手写 YAML，输出可播放、暂停、步进、下钻子流程、查看 payload 字段的图；适合 OAuth、订单链路、消息管道或参与者明确的业务流程。[仓库](https://github.com/naorsabag/openhop) · [在线演示](https://naorsabag.github.io/openhop/) · [使用模型](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/skills/openhop/SKILL.md#L21-L46)

**如何帮助理解。** 把“全图太复杂”变成“当前谁把什么送给谁”，再逐层展开。更适合离散事件及节点间传递；对连续数学参数的影响未必是合适表示。

**源码核实。** TypeScript monorepo 真正包含 CLI、Fastify 服务、React/React Flow 界面、ELK 布局和共享 Zod schema。校验器检查重复 ID、端点和嵌套引用并建议相近拼写；没有逐条对照目标仓库的源码证据。流程持久化到本地 `~/.openhop/flows`，可用环境变量更改。[引用一致性校验](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/packages/shared/src/validator.ts#L53-L179) · [前端依赖](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/packages/web/package.json#L38-L64) · [本地存储](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/packages/server/src/store.ts#L25-L73)

**必须区分本地与公网分享。** README 宣称无遥测、hash 分享不上传；本次源码却显示 Pages 工作流已配置 Umami，运行代码把 `pathname + search + hash` 放进统计事件，而分享 hash 本身装有压缩 YAML。“fragment 通常不随 HTTP 请求发送”不能推出网页脚本不会主动发它。这里是源码可确认的冲突，未对生产站点抓包；不能把公网演示模式等同于私有流程的无上传分享。本地普通构建不满足统计启用条件，须分开评价。[README 分享描述](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/README.md#L88-L94) · [Pages 已启用统计](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/.github/workflows/pages.yml#L34-L42) · [启用条件](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/packages/web/src/lib/umami-gating.ts#L1-L7) · [事件明确包含 hash](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/packages/web/src/lib/umami.ts#L53-L59) · [YAML 编入 hash](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/packages/web/src/lib/share-url.ts#L77-L80)

**局限、成本、审查深度。** 有 Node/前端/本地服务成本，开发要求 Node `^20.19.0 || >=22.12.0`。有 schema、CLI、路由/存储、布局、分享等 Vitest 测试与 CI；本次只读测试和工作流，未安装或运行全套。README “约 100 token/步”是作者概算，未跨模型/中文复测，不能作为精确成本承诺。[Node 要求](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/package.json#L38-L49) · [CI](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/.github/workflows/ci.yml#L12-L44) · [schema 用例](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/packages/shared/__tests__/schema.test.ts#L72-L98) · [MIT 许可证](https://github.com/naorsabag/openhop/blob/927015aebbeeb2559e6296946b57b2594c9a1d37/LICENSE#L1-L13)

## 5. Ofori01/show-me：有来源校验的等距系统地图

**基本功能与输入输出。** 输入固定版本仓库及范围，agent 产出 `system-map/v1` JSON；脚本检查引用和统计文件，生成可点击地图、动画流程与 Markdown 文本版。节点带 `{file, line, evidence}` 引用；建筑规模来自认领文件的行数/文件数，并可分章节揭示。[仓库](https://github.com/Ofori01/show-me) · [在线自解释演示](https://ofori01.github.io/show-me/) · [处理分工](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/SKILL.md#L20-L60)

**如何帮助理解。** 同时回答“系统有哪些部分、关系在哪里、操作经过哪些地方”，且可回查来源。适合 AutoDigest 消化代码库时把“从哪得出”与“什么范围没覆盖”变成可检查数据。

**源码核实。** 不是 AST 分析器，也不自动理解所有语言；agent 负责读代码，脚本负责文本匹配、计量和几何。`validateMap` 检查文件、行号与默认前后 4 行窗口内的 evidence 原文，也查节点/边和流程接续。`scopeCoverage` 是 scope 文件集减去节点认领文件集，是文件覆盖而非语义覆盖。真实引文仍可能被错误解读。[引用门禁](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/scripts/validate.mjs#L44-L69) · [覆盖计算](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/scripts/validate.mjs#L402-L424) · [明确声明的证据边界](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/SKILL.md#L67-L88)

**测试实证。** 审阅脚本和导入依赖后，运行以下标准库测试及附带样例只读验证；未安装依赖或打开浏览器。

| 命令（仓库根目录） | 本次结果 |
|---|---|
| `node skills/show-me/scripts/self-test.mjs --repo skills/show-me` | 11 个门禁用例通过，含伪造证据、错行、失踪文件、错误节点和断开的流程 |
| `node skills/show-me/scripts/layout-test.mjs --repo skills/show-me` | 1 张样例通过：28 路径不穿越建筑、19 footprint 不重叠、路径点在 viewBox 内、6 区分组连续、重复布局确定 |
| `node skills/show-me/scripts/validate.mjs skills/show-me/examples/show-me.system-map.json --repo skills/show-me` | 19 节点、28 边、3 流引用通过；文件覆盖 19/19；1 条 32 词句长 lint，不阻断 |

通过只证明该样例与这些突变用例，不能推广为任意代码库分析正确。[门禁用例](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/scripts/self-test.mjs#L73-L172) · [布局断言](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/scripts/layout-test.mjs#L74-L143)

**局限和成本。** 主要成本为 agent 读源码、聚合和取证；Node ≥18，包无外部依赖。节点数有 6–40 的程序门禁，范围需要选择。生成页 CSS 仍请求 Google Fonts（有 fallback），“单文件”不等于默认完全离线。[执行要求](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/package.json#L26-L40) · [节点数量门禁](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/scripts/validate.mjs#L110-L119) · [外部字体例外](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/skills/show-me/scripts/render.mjs#L2-L10)。已读入口、校验器、计量/渲染关键实现及全部上述测试；未做新仓库的模型抽取、浏览器交互或视觉质量评测。[MIT 许可证](https://github.com/Ofori01/show-me/blob/62c8905665be8ff6f51df05eaccf6b38e1c183e1/LICENSE#L1-L13)

## 6. architecture-diagram-skill：有播放器模板的系统教学图

**基本功能与输入输出。** 输入系统描述、README/OpenAPI 或拟议流程，agent 改模板节点和 `flows`，交付 `architecture.html` 与 `architecture.md`。浏览器内选场景、播放步骤、读 payload、切 dev/prod 等模式、拖拽节点、换主题。[仓库](https://github.com/konraddzbik/architecture-diagram-skill) · [节点/流程/步骤/模式](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/skills/architecture-diagram/SKILL.md#L33-L45)

**如何帮助理解。** 同一拓扑展示“这一步谁在参与”“环境变化替换了什么”，适合 RAG、OAuth、CI/CD 和服务通信；它是教学模型，不接真实监控数据。

**源码核实。** 当前 skill 为 `1.4.0`，含真正单文件 CSS/JS/SVG 模板，player、连线路由、拖拽/本地保存、主题和 `archValidate()` 均有实现。`scripts/check.js` 检查版本/清单、JS 语法、flow 与节点 ID 以及样例引用；不验证架构是否吻合目标源码。样例 JSON 是规划材料，仍需转换为 HTML 和 JS，不能直接喂给一个现成 JSON 渲染器。[模板编辑与验证](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/skills/architecture-diagram/SKILL.md#L78-L108) · [样例真实用途](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/skills/architecture-diagram/SKILL.md#L122-L137) · [检查实现](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/scripts/check.js#L59-L122) · [浏览器完整性检查](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/skills/architecture-diagram/assets/template.html#L2212-L2244)

**局限和成本。** 线性流程是现成功能；并行/分支属于需要改代码的扩展，不能把“扩展难度表”当成已支持清单。复杂拓扑仍需布局取舍。展示只要浏览器，截图另需 Puppeteer/Chrome；字体默认外部加载。[内置和扩展边界](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/skills/architecture-diagram/SKILL.md#L284-L304) · [模板网络边界](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/skills/architecture-diagram/assets/template.html#L5-L14)

**审查深度。** 阅读 skill、模板关键 JS、完整检查脚本、截图脚本及 CI；未运行浏览器或生成新图。有 CI 不等于本次已验证最新运行通过。[MIT 许可证](https://github.com/konraddzbik/architecture-diagram-skill/blob/cd94e972682dfacd7c741f9096cacc90d5cc5c41/LICENSE#L1-L13)

## 7. NickyLam/Visualizer-Skill：带宿主降级路径的 SVG 设计规范

**基本功能与输入输出。** 输入机制、结构、流程或比较，输出 SVG、HTML widget，或 Markdown 宿主中的 Mermaid，亦可导出 `.svg/.html`。附配色表、Mermaid 参考和四个 SVG 示例。[仓库](https://github.com/NickyLam/Visualizer-Skill) · [输出路由](https://github.com/NickyLam/Visualizer-Skill/blob/409cc699c56bbdfc2b52a70509c24642585c0d5f/SKILL.md#L40-L62)

**如何帮助理解。** “结构/如何工作/训练步骤”等问题分别选结构图、具象示意、流程图；复杂主题拆成小图和连接文字。交互用于周期或参数变化，不把每个概念都压成同样的盒子。[路由和图解规则](https://github.com/NickyLam/Visualizer-Skill/blob/409cc699c56bbdfc2b52a70509c24642585c0d5f/SKILL.md#L133-L166)

**源码核实。** 是提示词、设计系统和素材包，未见运行器、校验脚本、package manifest 或测试。`read_me`、`show_widget` 是预期 WorkBuddy 提供的宿主工具，本仓库没有实现。普通 agent 安装它不代表有 WorkBuddy 内嵌面板；CLI/Markdown 明确降级为 Mermaid/文件。[宿主适配与 fallback](https://github.com/NickyLam/Visualizer-Skill/blob/409cc699c56bbdfc2b52a70509c24642585c0d5f/SKILL.md#L43-L59)

**局限、成本、审查深度。** 坐标布局由模型完成，680 宽视图、字号和颜色预算是提示约束而非程序检查；公式和代码不宜硬转 SVG。SVG 文件展示轻量，内嵌交互仍看宿主。已读完整 skill、README、资源清单及许可，未实际生成。[MIT 许可证](https://github.com/NickyLam/Visualizer-Skill/blob/409cc699c56bbdfc2b52a70509c24642585c0d5f/LICENSE#L1-L13)

## 8. justshowme：从交互解释到带画面检查的视频制作

**基本功能与输入输出。** 当前不是单一 skill，而是 `visualize`（HTML 幻灯片/长页）、`pixelviz`（手绘风动画、PNG/MP4）、`videoviz`（配音视频）三套。输入概念、PR、bug 或方案，输出可操作图解或可播放材料。[仓库](https://github.com/theolundqvist/justshowme) · [交互案例](https://theolundqvist.github.io/justshowme/examples/takeoff.html) · [事件循环案例](https://theolundqvist.github.io/justshowme/examples/event-loop.html) · [三模块定位](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/README.md#L14-L54)

**如何帮助理解。** 先定一句结论再拆少量画面，滑块展现权衡、开关开闭流程。值得借鉴的是“渲染成像后检查”的闭环，把源码可读却画面重叠的问题显性化。[从结论到画面](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/visualize/SKILL.md#L16-L39) · [截图回看闭环](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/visualize/SKILL.md#L52-L74)

**源码核实。** `shoot-slides.mjs` 用 Playwright 逐张截图；pixelviz capture 对帧调用 lint 并取图像 hash；videoviz check 在采样帧检测小字、文本重叠、越界及过空画面。这些是几何/画面检查，不能判定概念正确。多 agent 工作流依赖专用 `agent/parallel/pipeline/phase` 宿主，不是可直接运行的通用 Node 工具。[截图实现](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/visualize/scripts/shoot-slides.mjs#L18-L66) · [帧检查](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/pixelviz/scripts/capture.mjs#L43-L60) · [画面检查](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/videoviz/scripts/check.mjs#L26-L81) · [workflow 前提](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/visualize/workflows/design-slides.workflow.js#L1-L20)

**局限和成本。** visualize HTML 轻量，但 QA 要 Playwright；pixelviz 视频还要 ffmpeg。videoviz 有 Remotion/React、numpy/faster-whisper、Vertex AI Gemini TTS 与授权账号，成本明显更高。本地转写代码固定 `language='en'` 并按英文词序校对，不能未经测试承诺中文配音/逐字对齐。Remotion 许可须单独核对，不因本仓库 MIT 而自动没有商业限制。[视频依赖](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/videoviz/package.json#L1-L17) · [语言及校对实现](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/skills/videoviz/scripts/voice.py#L141-L167) · [上游许可说明](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/README.md#L98-L100)

**审查深度。** 已读三个模块目录、visualize 本体、截图、pixelviz capture、videoviz check/voice 关键实现及依赖；未跑多媒体链路、未上传 PR 附件、未验证中文。未见独立通用测试套件；capture/check 是验证实现，不应写成已全量测试。[仓库 MIT](https://github.com/theolundqvist/justshowme/blob/b7e20e8966d852f95c470179ee0b23f5abbab936/LICENSE#L1-L13)，pixelviz 保留 procedural-film 的 MIT 归属。

## 9. Matt Pocock teach：最接近持续消化并证明学会的流程

**基本功能与输入输出。** `/teach` 把独立目录作为长期学习工作区，输入学习目标和基础，逐次生成短 HTML 课程、复用练习组件、参考页、资源列表和学习记录，适合多轮学习。[仓库](https://github.com/mattpocock/skills) · [产物结构](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/SKILL.md#L8-L20)

**如何帮助理解。** 围绕具体任务讲一个小点，让用户练习并反馈，后续课依目标和记录继续。值得 AutoDigest 借鉴的是“讲过不等于学会”：学习记录应包含能用概念的证据、基础披露或纠正的误解，不能只记录材料已浏览。[引用和练习](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/SKILL.md#L91-L110) · [什么才算学到](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/LEARNING-RECORD-FORMAT.md#L29-L42)

**源码核实。** teach 目录是 skill、使命/资源/学习记录/词汇格式与 agent 元数据，没有现成课程程序、题库运行时或自动引用检查。要求先找可信来源再讲解；HTML、测验、模拟器和共享样式均由 agent 生成。教学理念是作者设计，不代表仓库已有学习效果实验。[教学理念](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/SKILL.md#L22-L45) · [由 agent 创建复用组件](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/SKILL.md#L63-L69)

**局限、成本、审查深度。** 需要多次模型调用、资料查找和用户练习；课件漂亮不能保证保持。会写长期目录，应在独立主题工作区使用。当前新版明确路径锚定调用目录，并要求变换正确答案的位置，搜索结果旧描述未必反映这些细节。读完整 teach、格式文件、教学 docs 及许可，未启动课程，也未将学习收益当实测。[路径锚定](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/SKILL.md#L10-L18) · [具体使命约束](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/skills/productivity/teach/MISSION-FORMAT.md#L25-L31) · [MIT 许可证](https://github.com/mattpocock/skills/blob/49dd158d1076134a641b33efb035946536778336/LICENSE#L1-L13)

## 对 AutoDigest 的可复用结论

以下是依据代码和接口的工程判断，不是学习效果排行榜。

1. **默认解释层可借 HumanLayer show-me。** 用最小图形回答当前问题，无需先引入服务或视频链路。
2. **可操作概念页可选 visual-explainer。** 只在变化参数或步骤机制本身有价值时加交互，保留来源和适用边界。
3. **学习闭环可借 teach。** 记录可观察的理解、误解修正和下一步练习，不只累积图文。
4. **代码库研究可借 Ofori01 的证据合同。** 将引用、源文本、版本、范围做成可检查数据，仍保留语义复核。
5. **系统流动画分两种工程取舍。** architecture-diagram 单文件模板接入轻、需要改 HTML；OpenHop 结构化 YAML 及长期本地运行时更丰富，但部署/分享边界更多。
6. **justshowme 优先借制作与检查闭环。** 截图回看比“默认全部变视频”更值得先引入；完整视频适合有复用/分享需求的主题。
7. **对话内嵌类先检查宿主。** visualise 和 Visualizer-Skill 的设计规范有用，不能把描述中的 iframe/工具函数当作已交付能力。

共同验收应是：看完能否回答原始问题，能否解释关键边/参数的含义，能否预测变化后的结果，能否从图回到证据。星数可筛选社区关注度，不能代替这四项验收。
