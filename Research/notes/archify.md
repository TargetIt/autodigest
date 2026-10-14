# Archify：值得优先补录的架构与系统图解工具

本项是对首批调研的补充：**原来的 39 仓汇总没有收录 Archify，现已加入。** 我的判断是：如果目标是“让 Agent 帮我讲清一个系统，再把可探索的图发给别人”，它应进入优先试用名单。这个判断来自实现、样例和有限行为验证，不是以 Star 证明生成质量。

## 1. 项目身份、版本与关注度

| 项目 | 本次核实结果 |
| --- | --- |
| 官方仓库 | [tt-a1i/archify](https://github.com/tt-a1i/archify) |
| 官网与交互示例 | [archify.si](https://archify.si/) · [Proof Lab](https://archify.si/gallery.html) |
| 中文介绍 | [固定版本 README_ZH.md](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/README_ZH.md) |
| Star / Fork | **83,478 / 5,647**，GitHub REST API 精确快照 |
| 采集时间 | 2026-10-15 04:41:13，Asia/Shanghai（UTC 2026-10-14 20:41:13） |
| 最新正式 release | [v3.1.0](https://github.com/tt-a1i/archify/releases/tag/v3.1.0)，2026-10-13 17:23:05 UTC 发布（北京时间 10 月 14 日 01:23:05）；此处的“最新”限定在采集时点 |
| 本次审阅提交 | [`d0c8c7e9f4e06f303389f804208d387f27019ef5`](https://github.com/tt-a1i/archify/commit/d0c8c7e9f4e06f303389f804208d387f27019ef5)，默认分支提交时间 2026-10-14 |
| 本地源码 | [`Research/repos/tt-a1i/archify/`](../repos/tt-a1i/archify/)，固定版本 Git 子模块 |
| 主要运行条件 | 生成 CLI 为 Node.js ≥18；完整浏览器检查还需要 Chrome/Chromium |

元数据记录在 [github-metadata.json](../evidence/github-metadata.json)，与原先 39 仓的采集时间分开保留。Star 是仓库关注度，不是下载量、付费用户量或学习效果。

本次审阅与行为验证使用上述默认分支提交，时间晚于 v3.1.0 release；没有另外下载发行 ZIP 复测，不能把 HEAD 的所有细节直接当作该 ZIP 的行为。

官方明确将 `archify.si` 和本仓库与第三方在线服务区分开；检索到的 fork、近名网站不能直接当作官方服务。主代码与 skill 为 MIT，品牌标识和字体另有条款，不能把所有资产都概括为 MIT。[官方服务声明](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/README.md#L463-L473) · [LICENSE](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/LICENSE#L1-L22) · [第三方资产说明](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/THIRD_PARTY_NOTICES.md#L8-L39)

字体条款见[第三方字体说明](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/THIRD_PARTY_NOTICES.md#L51-L62)。官网 gallery 入口在本次 HTTP 检查中返回重定向及访问限制，未做线上交互验收；可直接查看下文的源码和本地生成样例。[入口检查记录](../evidence/external-link-check.json)

## 2. 基本功能：生成可以探索的解释页

它的核心流程是：**人描述系统或提出问题 → Agent 阅读材料并编写结构化 JSON → Archify 校验、渲染 → 读者在独立 HTML 中探索 → Agent 修改 JSON 继续迭代。** 它既有 skill 指令，也有 schema、Node 渲染器、浏览器 viewer 和校验代码。

| 能力 | 对理解知识的具体帮助 | 实际边界 |
| --- | --- | --- |
| 架构与边界 | 区分用户、服务、存储、消息队列、外部系统及其连接 | 组件抽象和关系由作者或 Agent 决定 |
| 节点说明、路径追踪与视图 | 先看全局，再聚焦某个组件或沿一条路径阅读，减少一次展示过多细节 | 交互只围绕图中已有的信息运行 |
| 源码引用 | 从图中节点回到固定提交的文件与行号，便于复核 | 是可选能力；没有引用的节点不会自动得到证据 |
| 主题与导出 | 暗色/浅色、独立 HTML、PNG/JPEG/WebP/SVG，以及有条件的 WebM | 各导出路径受浏览器支持影响；本次未逐一实测 |
| 校验与交付 | 检查结构、几何及生成文件，失败时给出明确诊断；安全交付流程保留上一份有效结果 | 自动检查与事实判断、视觉审阅分开 |

**当前代码支持 10 类图**：architecture、workflow、sequence、dataflow、lifecycle、erd、class、tree、timeline、waterfall，分别对应架构、流程、时序、数据流、生命周期、实体关系、类、树、时间线和执行瀑布。旧文章或页面残留的“五类图”口径已经不足以描述此版本。[类型路由及各 schema/例子入口](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/SKILL.md#L50-L63)

## 3. 源码核查后，哪些优点可以成立

**有真正的结构验证。** `validateSchema` 调用随仓分发的验证器，把错误转换为规则代码、具体字段、期望条件和修复建议。它不只是提示 Agent “请检查一下”。[验证实现](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/validator.mjs#L38-L81)

**架构图有路由与几何检查，但节点摆放仍需要编排。** 固定网格从 `row/col` 或显式 `pos` 得出坐标；它不负责仅凭拓扑重新安排全部节点。渲染器另有路由、标签和间距检查，所以也不能将其说成完全没有自动处理。实际效果取决于 Agent 选择的抽象层级、布局和文字密度。[位置计算](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/architecture/grid.mjs#L1-L30) · [渲染与路由检查入口](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/architecture/render-architecture.mjs#L13-L42)

**路径探索是实际实现的功能。** Viewer 从已经生成的节点和连接建立图，用 BFS 查找最短有向路径。适合回答“按这张图，A 到 B 经过什么”；它不会自行采集日志、执行代码或证明生产请求真的沿该路径发生。[路径模型](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/viewer/route-probe.js#L1-L5) · [BFS 实现](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/viewer/route-probe.js#L307-L333)

**源码引用确实经过 Git 核验。** 实现检查仓库身份、完整提交 SHA、固定版本中的文件对象和行号范围；支持网页链接，也支持 `local-only` 的本地引用模式。这比仅贴一个不固定版本的首页链接更可复查。[仓库与链接模式](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/repository-evidence.mjs#L154-L200) · [提交身份](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/repository-evidence.mjs#L231-L248) · [文件和行号](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/repository-evidence.mjs#L305-L355)

但核验器会跳过没有 `sources` 的节点，仓库引用模式只要求至少一条引用。**不能把“存在有效引用”扩大成“所有节点和连线都经过源码证明”。** 即使引用存在，也仍需人判断该代码是否支持图中的结论。[节点处理](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/repository-evidence.mjs#L271-L275) · [最低引用条件](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/repository-evidence.mjs#L373-L390)

**完整交付和视觉验收有明确区分。** `finalize` 编排 validate、deliver、check、browser-check；自动检查通过后仍可能标记 `visualReview: not-requested`，没有自动截图并由人看图。完整浏览器阶段缺少 Chrome/Chromium 时不能当作通过。[阶段定义](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/finalize.mjs#L20-L22) · [视觉审阅边界](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/SKILL.md#L79-L95) · [浏览器缺失处理](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/visual-check.mjs#L2461-L2480)

## 4. 相比已经收录的工具，什么时候选它

以下是依据工作方式作出的选型判断，没有做跨工具盲测或自动生成成功率排名。

| 对比对象 | 更适合选 Archify 的情况 | 另一工具仍有价值的情况 |
| --- | --- | --- |
| HumanLayer ShowMe | 已确定需要系统图，希望交付独立、可探索的页面 | 还在判断用树、伪代码、时序图还是文字最容易理解 |
| Mermaid | 需要节点说明、路径探索和更完整的解释页面 | 需要轻量文本语法，直接在 Markdown 中维护和嵌入图 |
| Excalidraw / draw.io | 希望 Agent 修改结构化 JSON，持续生成统一样式的图解 | 需要自由拖拽、手绘讨论或在通用编辑器中精细修改 |
| Ofori Show-me | 需要多种图类型和系统沟通页面，同时保留可选源码引用 | 更关注带引用的代码地图及其特定布局、走读方式 |

对 AutoDigest，我会将它优先用于**系统架构、请求链路、Agent 工具调用和数据处理流程**。学习概念时先用 ShowMe 判断表达方式；需要架构图时再用 Archify；要研究数值如何随参数变化，仍应使用可复算的 marimo/Mafs 等工具。图的动态效果并不等于数值实验。

## 5. 使用前值得知道的具体限制

- “支持 Mermaid 输入”是 skill 指导 Agent 读懂含义，再编写 Archify JSON；不能当作通用、无损的 Mermaid 解析器或换肤器。[映射说明](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/SKILL.md#L69-L77)
- CLI 声明 Node.js ≥18。完整交付的浏览器检查另需浏览器，不能从“CLI 零运行时 npm 依赖”推断所有阶段没有环境要求。[包声明](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/package.json#L1-L13)
- WebM 导出依赖 MediaRecorder、可用 MIME 和 `canvas.captureStream`，并有动画模式条件；本次不承诺所有浏览器均支持。[实际导出条件](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/viewer/export.js#L768-L797)
- 生成流程有可选更新提醒。实验中设置 `ARCHIFY_UPDATE_CHECK_DISABLED=1`，源码在启动更新子进程前检查该开关。[禁用逻辑](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/delivery-update.mjs#L48-L60)
- 官方 v3.1.0 发布说明仍列出长时序图的控件重叠、部分数据流图共享视觉通道、长泛型类型换行等限制。时间线和瀑布图只有接入真实日志或 trace 时才能标为实测时间；漂亮的示例时间不能当作性能数据。[发布说明及已知限制](https://github.com/tt-a1i/archify/releases/tag/v3.1.0)

外观上，本次实际查看了上游保存的 [架构示例图](https://raw.githubusercontent.com/tt-a1i/archify/d0c8c7e9f4e06f303389f804208d387f27019ef5/docs/assets/archify-architecture.png) 和 [Astron 中文系统图截图](https://raw.githubusercontent.com/tt-a1i/archify/d0c8c7e9f4e06f303389f804208d387f27019ef5/docs/cases/astron-agent-runtime.architecture.visual-check.1440x900.light.png)：颜色分类、边界框、箭头及图下说明的层次清楚，能解释它为何适合架构沟通；较密集的完整系统图仍存在缩放后小字号难读的问题。这是对两张官方样例的观察，**不是本次生成结果的浏览器验收，也不是任意输入都能画好的证据**。

## 6. 本次实际验证

本地验证记录、生成样例与原始回执保存在 [`evidence/archify/`](../evidence/archify/)。本次未安装 skill、未连接模型或云服务，也未运行全部上游测试；具体命令、预期拒绝的错误输入及检查结果见该目录的 README。

本次 9 次 CLI 调用符合预期：官方架构 JSON 的 validate、render、deliver 成功；非法组件类型和不存在的连接端点被拒绝；错误 deliver 保留上一份 HTML 的原始哈希，并将交付状态标为失败；恢复正确输入后，交付及严格状态检查重新通过。这里同时出现的“checker 9/9”是工具内部的九项静态产物检查，不能理解成九次浏览器测试。

可下载或本地打开 [本次生成的 HTML](../evidence/archify/sample-web-app.html)，查看[逐次退出码及哈希](../evidence/archify/results.json)。本次没有在浏览器打开该产物，也没有让模型根据陌生仓库生成新 JSON；因此这些检查支持渲染与错误处理行为，不支持“任意仓库都能自动画对”的结论。

适合下一步用真实材料评估的题目是：“画出 AutoDigest 的输入、核心解释、反馈、修复与输出流程，并给关键节点附上源码依据”。应检查图是否保留真实职责和异常分支，再评价是否清晰；不能仅按外观或导出成功判断知识是否理解正确。本次没有改动 AutoDigest 的现有工作流。
