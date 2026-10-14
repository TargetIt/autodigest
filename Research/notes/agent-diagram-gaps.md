# 架构绘图查漏：Agent、MCP、渲染器与可编辑画布

本组是对原有 40 个主仓的系统补充。先筛查 9 个候选，再结合跨组热门仓库检索和 fork 身份核对扩展到 **13 个候选，选取 6 个深入静态审阅**；其余保留筛选理由。新收项目都不是 Archify 的同名镜像，原报告已有的官方 draw.io / Excalidraw MCP、Next AI Draw.io、Mermaid 等没有重复计数。

**按用户明确偏好，今后绘制架构图默认优先使用 Archify。** 下列工具在需要原生可编辑文件、长期维护图模型、AWS 特定结构、终端输出或自由白板时作为补充。可拖拽、播放或高亮关系，只表示图的交互方式，不能自动称为真实系统仿真或教学效果验证。

本页 Star/Fork 来自 GitHub REST API，采集区间为 **2026-10-15 04:53:52—04:55:24（北京时间）**；各项精确 UTC 时间、默认分支 SHA、release、许可证 API 值和候选状态保存在 [候选与元数据](../evidence/agent-diagram-candidates.json)。这些数值是仓库关注度；`awslabs/mcp` 的 Star 是整个合集，不能冒充旧 Diagram MCP 单模块的 Star。

所有深入项均已直接浅克隆到 `Research/repos/<owner>/<repo>/`，没有在临时目录留下新的源码副本。**本轮未安装依赖、skill 或 MCP，未启动应用或浏览器，未执行上游脚本或测试。** 下文的功能判断来自固定版本实现与测试代码静态阅读，不能理解为实测通过；默认分支能力也不自动代表最近发行包已有该行为。

## 1. 六项补充如何选择

| 项目 | Star / Fork | 主要补足的能力 | 与 Archify 的分工 |
| --- | ---: | --- | --- |
| [Agents365-ai/drawio-skill](https://github.com/Agents365-ai/drawio-skill) | 10,141 / 723 | 原生 draw.io 模型、源码导入、增量同步、规则检查 | 需要长期维护 `.drawio` 和人工布局时补充 |
| [yctimlin/mcp_excalidraw](https://github.com/yctimlin/mcp_excalidraw) | 2,538 / 285 | CLI/MCP 驱动实时画布、元素级修改、原生文件与离线渲染 | 需要人和 Agent 共同编辑 Excalidraw 时补充 |
| [awslabs/diagram-as-code](https://github.com/awslabs/diagram-as-code) | 1,587 / 106 | AWS YAML 建模、PNG 生成、Go CLI 与 MCP | AWS 图进入 Git/CI 或接 CloudFormation 时补充 |
| [aws-samples/sample-architecture-diagram-mcp-server](https://github.com/aws-samples/sample-architecture-diagram-mcp-server) | 7 / 1 | AWS 交互 HTML、引导讲解、ELK 布局、draw.io 输出 | AWS 专题讲解与可编辑交付的低关注度候选 |
| [lukilabs/beautiful-mermaid](https://github.com/lukilabs/beautiful-mermaid) | 11,194 / 410 | 独立 Mermaid 子集解析、SVG 与终端 ASCII/Unicode | 把轻量结构图嵌入终端/聊天界面时补充 |
| [plait-board/drawnix](https://github.com/plait-board/drawnix) | 14,941 / 1,298 | Mermaid/Markdown 转可编辑白板，浏览器本地保存 | 面向手动整理、思维导图和讨论的相邻工具 |

## 2. Draw.io Architecture Studio：不只是提示词

仓库：[**Agents365-ai/drawio-skill**](https://github.com/Agents365-ai/drawio-skill)；**10,141 Star / 723 Fork**。审阅 SHA：`57270820d3cd71cbdf4fb6b2f7091d4fb37bb019`；HEAD 提交日期：2026-10-11（UTC）；API latest release：[v3.4.2](https://github.com/Agents365-ai/drawio-skill/releases/tag/v3.4.2)。本地：[源码目录](../repos/Agents365-ai/drawio-skill/)。

**功能与输入输出。** Agent 可把自然语言整理成 Diagram IR，或调用源码/IaC/接口描述导入器，生成可在 draw.io 继续编辑的 `.drawio`。统一 CLI 还有同步、多视图、依赖查询、规则检查和 HTML 讲解页。比如 Python 包的导入关系可变成带文件来源的模块图，再由人调整布局并持续更新；“导入关系”不等于完整的运行调用链。

**源码核实。** Python 导入器使用 `ast.parse` / `ast.walk` 识别 import；统一入口按格式分派导入器。IR 写出过程尝试 Graphviz 布局，失败时退回网格，再生成 mxGraph XML。`reconcile` 只处理首个未压缩页面，依赖稳定模型 ID 匹配旧元素、保留既有几何和样式，并记录手动标签与新来源的冲突。因此不能承诺任意多页/压缩文件都无损同步。MCP 入口是独立的标准库 JSON-RPC 服务，通过子进程调用同一 CLI；它并非把请求转发给 jgraph 官方 MCP。

- [Python AST 导入器](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/pyimports.py#L74-L100)；[格式导入与来源元数据](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/diagramctl.py#L168-L204)。
- [IR 到原生 draw.io 与布局回退](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/diagram_ir.py#L502-L540)；[同步范围与冲突处理](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/diagram_ir.py#L1137-L1217)。
- [MCP 调用真实 CLI](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/diagramctl_mcp.py#L260-L271)。
- [what-if 的真实计算](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/diagram_ir.py#L1064-L1097)：沿图中出边遍历，并跳过标注 `isolates_failure` 的边。这是基于作者模型的影响范围分析，不模拟负载、重试、时间或真实故障。

**校验边界与成本。** `validate.py` 有 XML/元素/几何规则，但边穿节点与交叉检查只适用于已保存显式 waypoints 的边；自动路由在 draw.io 渲染时才产生，校验器不会猜测。看图修复仍由 Agent 按工作流完成。核心 IR/查询/同步路径使用 Python 标准库；更好的自动布局需 Graphviz，原生图片/PDF 导出需 draw.io 桌面 CLI；部分品牌图标默认使用 CDN，离线需要内嵌。[几何检查适用范围](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/scripts/validate.py#L92-L96) · [结构检查与视觉审阅的区别](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/SKILL.md#L79-L98)。

**许可和审阅范围。** 主代码 MIT；本地形状索引来自 jgraph/drawio-mcp，附 Apache-2.0 来源说明，不能把该索引也说成作者独立设计。已读入口、上述算法及 `tests/test_diagramctl.py`、`tests/test_mcp_server.py` 中选定用例；未运行测试，也未验证所有导入器。README 的比较表仍有“Pure SKILL.md”旧口径，应以当前脚本为准。[主许可](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/LICENSE#L1-L21) · [形状索引归属](https://github.com/Agents365-ai/drawio-skill/blob/57270820d3cd71cbdf4fb6b2f7091d4fb37bb019/skills/drawio-skill/data/SHAPE-INDEX-NOTICE.md#L1-L12)。

**与已有 jgraph 官方 MCP / Archify 的差异。** 官方 jgraph 项目本身已有形状查询、插件和导出路径，不能笼统说它“不会导出”。此项目的增量价值在于图模型、来源导入、同步和规则工具。Archify 保持默认架构讲解工具；明确要求维护原生 `.drawio` 时，这个补充更对口。

## 3. mcp_excalidraw：人和 Agent 共用的图形工作台

仓库：[**yctimlin/mcp_excalidraw**](https://github.com/yctimlin/mcp_excalidraw)；**2,538 Star / 285 Fork**。审阅 SHA：`8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f`；HEAD 提交日期：2026-10-09（UTC）；API latest release：[v2.1.2](https://github.com/yctimlin/mcp_excalidraw/releases/tag/v2.1.2)。本地：[源码目录](../repos/yctimlin/mcp_excalidraw/)。

**功能与输入输出。** 用 CLI、MCP 或 REST 创建/查询/修改元素，浏览器通过 WebSocket 同步同一画布；可导出 `.excalidraw`，也能生成 PNG/SVG。输入既可以是 Agent 发出的元素操作，也可以是已有场景文件。适合一边讲系统、一边挪节点、改箭头，再保存源图。它不从这些操作中自动判断系统架构是否正确。

**独立实现证据。** 服务端的元素创建 API 经 schema 检查后调用 `commitCanvasMutation`，再向浏览器广播；这是持续的共享状态，和仅在聊天中创建一次图的入口不同。原生场景导出明确写入 Excalidraw 版本、元素与图片文件；渲染器在 Node 中准备场景并调用 Excalidraw 自身的 SVG exporter，随后可用 resvg 栅格化。

- [元素修改与实时广播](https://github.com/yctimlin/mcp_excalidraw/blob/8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f/src/server.ts#L350-L378)。
- [原生场景构造](https://github.com/yctimlin/mcp_excalidraw/blob/8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f/src/core/scene-io.ts#L24-L47)。
- [Node 端 SVG/PNG 渲染与限制](https://github.com/yctimlin/mcp_excalidraw/blob/8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f/src/core/render/index.ts#L135-L197)。
- [跨重启持久化开关](https://github.com/yctimlin/mcp_excalidraw/blob/8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f/src/core/canvas-persistence.ts#L122-L138)：只有配置 `EXCALIDRAW_DATA_DIR` 才启用磁盘状态保存，不能把“有实时画布”说成“默认已永久保存”。

**依赖、边界与许可。** 当前包要求 Node ≥20，服务端依赖 Express、ws、MCP SDK、jsdom、resvg；编辑画布需要本地服务，单独 `render` 路径则可以直接读场景文件。Mermaid 转画布仍有浏览器路径，不能把整个工具说成都无需浏览器。中文等非拉丁文字可能使用系统字体，渲染源码明确提示跨机器输出可能不同，不能扩大“字节稳定”的承诺。主代码为 MIT。[运行依赖](https://github.com/yctimlin/mcp_excalidraw/blob/8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f/package.json#L35-L46) · [Node 下限](https://github.com/yctimlin/mcp_excalidraw/blob/8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f/package.json#L101-L103) · [许可](https://github.com/yctimlin/mcp_excalidraw/blob/8084a1c8b410d625fcfd59d5cffb32f3a86a2a6f/LICENSE#L1-L21)。

**审阅范围与 Archify 分工。** 已读 MCP/CLI 共用模块、画布服务、导出/持久化/渲染实现，并静态看过 `scripts/check-render.mjs` 与 `scripts/check-durable-state.mjs` 的代表性断言；没有启动服务或验证并发行为。它值得独立收录，但该仓 README 对官方 Excalidraw MCP 的对比只代表作者表述，不能当官方项目最新能力的证据。需要长时间人机共编辑原生画布时选它；需要结构清楚、带讲解的架构成品，默认仍用 Archify。

## 4. AWS diagram-as-code：YAML 与 CI 中的架构图

仓库：[**awslabs/diagram-as-code**](https://github.com/awslabs/diagram-as-code)；**1,587 Star / 106 Fork**。审阅 SHA：`4ec965cf8bdb309d714bc6202e7954fc43338bbe`；HEAD 提交日期：2026-09-16（UTC）；API latest release：[v0.24](https://github.com/awslabs/diagram-as-code/releases/tag/v0.24)。本地：[源码目录](../repos/awslabs/diagram-as-code/)。

**功能与输入输出。** 使用 AWS-oriented YAML 定义资源、层级、连接和布局，Go CLI 生成 PNG；另有 MCP 入口和标为 Beta 的 CloudFormation 转换。适合把 AWS 部署结构与文档放入同一 Git 工作流。自然语言到 YAML 由宿主 Agent 完成；不能说 MCP 本身内置了一个自动理解需求的模型。

**源码核实。** MCP handler 将 `yamlContent` 写入临时文件，调用真实绘图函数，再返回 base64 PNG。绘图过程缩放容器、解析连接锚点、绘制图片并 `png.Encode`；不是浏览器截图。名为 `getDiagramAsCodeFormat` 的工具返回内嵌的格式/提示文本，并未调用 LLM。定义文件支持 URL、本地和 Embed；URL 路径会读取缓存/联网获取，因此“无需浏览器”不等于“任何配置都离线”。

- [MCP 的 YAML→PNG 路径](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/cmd/awsdac-mcp-server/main.go#L268-L335)。
- [布局、绘制与 PNG 编码](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/internal/ctl/create.go#L199-L265)。
- [格式工具实际返回提示模板](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/cmd/awsdac-mcp-server/main.go#L411-L429)。
- [定义文件的联网与本地分支](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/internal/ctl/create.go#L316-L347)。

**运行成本与准确版本。** 编译当前审阅 HEAD 应以 `go.mod` 的 **Go 1.25.0** 为准，README 安装段仍写“1.21 or higher”，两者有差异。可以使用合适平台的预编译程序，但本轮没下载发行包验证。MCP 此路径只声明 PNG 输出；保留 YAML 才能维护结构，PNG 不是自由编辑源格式。源码主许可为 Apache-2.0，AWS 图标另遵循其资产条款。[实际工具链与依赖](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/go.mod#L1-L16) · [README 较旧的 Go 要求](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/README.md#L29-L36) · [MCP 输出格式限制](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/cmd/awsdac-mcp-server/main.go#L220-L229) · [主许可](https://github.com/awslabs/diagram-as-code/blob/4ec965cf8bdb309d714bc6202e7954fc43338bbe/LICENSE#L1-L6)。

**审阅与分工。** 已读 MCP handler、绘图及定义加载，并看过 `cmd/awsdac-mcp-server/main_test.go` 对参数、返回 MIME 和异常的用例；未运行 Go 测试、未验证 CloudFormation 全格式兼容。它补的是 AWS/YAML/CI 路线，不提供 Archify 那样的独立交互讲解页，也不是已经弃用的 `awslabs.aws-diagram-mcp-server` 原模块。

## 5. AWS Architecture Diagram MCP Sample：与 Archify 最接近的一项低关注度候选

仓库：[**aws-samples/sample-architecture-diagram-mcp-server**](https://github.com/aws-samples/sample-architecture-diagram-mcp-server)；**7 Star / 1 Fork**。审阅 SHA：`c7af5d75322ed10add9921dd3ca5786b512fdd3c`；HEAD 提交日期：2026-09-28（UTC）；API latest release：API 无 latest release。本地：[源码目录](../repos/aws-samples/sample-architecture-diagram-mcp-server/)。

**功能与输入输出。** Agent 提供服务、连接、容器和讲解步骤，生成自包含交互 HTML；另有自动布局的 `.drawio` 和用于下游工具的数据 JSON。读者可拖节点、开详情、折叠组、跟随步骤阅读。仓库还有时序/流程等入口，本次重点只审架构路径。它属于 **aws-samples 示例仓库**，不应称为正式托管 AWS 服务；7 Star 也不应被写成已经广泛验证。

**源码核实。** HTML 生成器把结构 JSON 与本地图标数据嵌入已构建模板。`.drawio` 路径通过共享 `@aws-live-diagram/core` 的 ELK compound layout 布局节点和嵌套容器，再输出 mxGraph XML；这比 Archify 架构网格依赖作者指定 row/col 更偏自动放置。生成 HTML 前的验证会检查图内引用，并默认修复；对于不存在的连接端点，会**删除这条连接并记录回执**，不是自动推断正确连接。

- [自动布局后输出原生 draw.io](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/mcp-server.js#L118-L133)；[真实 ELK 层级布局调用](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/lib/layout.js#L18-L57)。
- [图数据与图标收集](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/lib/html-generator.js#L280-L301)；[嵌入单文件 HTML](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/lib/html-generator.js#L341-L348)。
- [HTML 路径默认先校验并修复](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/mcp-server.js#L204-L222)。
- [无效端点的删除策略](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/lib/validate.js#L111-L143)：用户要复核修复回执；“产物能打开”不证明原模型被完整保留。

**条件、许可与限制。** Node ≥18，MCP/Zod/ELK 与本仓 workspace 包组成生成环境；阅读已生成 HTML 不要求安装这些包。官方 AWS 图标不随项目打包，要按官方资产包说明准备，缺图标时会回退为首字母。draw.io 的 PNG/SVG/PDF 导出需可选桌面 CLI；HTML 栅格化/动画导出另有 Chromium/ffmpeg 条件。源码 MIT-0（MIT No Attribution），不是普通 MIT；第三方包和图标有各自条款。该工具不自动访问部署环境验证连线、不自行报价或部署。[运行条件](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/package.json#L37-L54) · [图标准备](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/README.md#L87-L103) · [MIT-0 许可](https://github.com/aws-samples/sample-architecture-diagram-mcp-server/blob/c7af5d75322ed10add9921dd3ca5786b512fdd3c/LICENSE#L1-L16)。

**审阅与分工。** 读过 schema、HTML/XML 生成、共享布局和验证器，并静态看了 `test/validate.test.ts` 对坏连接、重复 ID、组循环的用例；没有运行 MCP、布局或浏览器测试。与 Archify 的比较是源码机制对照，未做视觉效果排名。AWS 主题需要可拖拽输出、引导步骤及 `.drawio` 时可以试验；通用架构图继续优先 Archify。

## 6. beautiful-mermaid：给终端和聊天界面补轻量渲染

仓库：[**lukilabs/beautiful-mermaid**](https://github.com/lukilabs/beautiful-mermaid)；**11,194 Star / 410 Fork**。审阅 SHA：`2ac8bbbb060ca0a65a6a21f3200bd99b1587b488`；HEAD 提交日期：2026-05-06（UTC）；API latest release：[v1.1.2](https://github.com/lukilabs/beautiful-mermaid/releases/tag/v1.1.2)。本地：[源码目录](../repos/lukilabs/beautiful-mermaid/)。

**作者与功能。** 包中作者为 **Craft Docs**，仓库属于 `lukilabs`，不是 `mermaid-js` 官方。输入 Mermaid 文本，输出 SVG 字符串或 ASCII/Unicode 图；适合让 Agent 的结构解释直接出现在终端、聊天界面或应用 UI。它是可嵌入库，不是完整的架构讲解系统，也不能因为名称有 Mermaid 就承诺支持官方全部语法。

**源码核实。** 导出层路由到自有的 parse→layout→render 管线，当前覆盖流程/状态、时序、类、ER、XY 图。部分布局使用 ELK：同步封装通过 FakeWorker 内部 dispatcher 绕过异步队列；`renderMermaidSVGAsync` 直接调用同步函数，并不是后台线程。ASCII 有单独导出管线。既没有要求浏览器 DOM，也并非“零依赖”，package 明列 elkjs 和 entities。

- [导出与类型路由](https://github.com/lukilabs/beautiful-mermaid/blob/2ac8bbbb060ca0a65a6a21f3200bd99b1587b488/src/index.ts#L22-L63)。
- [真实渲染管线及 async 包装](https://github.com/lukilabs/beautiful-mermaid/blob/2ac8bbbb060ca0a65a6a21f3200bd99b1587b488/src/index.ts#L111-L166)。
- [同步 ELK 调度](https://github.com/lukilabs/beautiful-mermaid/blob/2ac8bbbb060ca0a65a6a21f3200bd99b1587b488/src/elk-instance.ts#L85-L112)。
- [作者、依赖和测试脚本](https://github.com/lukilabs/beautiful-mermaid/blob/2ac8bbbb060ca0a65a6a21f3200bd99b1587b488/package.json#L38-L60)。

**边界、许可和审阅。** SVG 可供进一步排版，但这不等于自带图形拖拽编辑器或源码引用核验。不要用 README 的性能数字作本轮性能实测；没有压测大图、兼容全部 Mermaid 语法或复核所有中文布局。当前 HEAD 的 package version 是 1.1.3，而 GitHub latest release 是 v1.1.2，二者不相同。主许可 MIT；ASCII 路线承认移植自 Alexander Grooff 的 mermaid-ascii。已读入口、ELK 封装、包信息，并静态看了 SVG integration 和 ASCII fixtures 测试；没有执行 Bun/npm。[许可](https://github.com/lukilabs/beautiful-mermaid/blob/2ac8bbbb060ca0a65a6a21f3200bd99b1587b488/LICENSE#L1-L21)。

**与 Archify 分工。** 需要单张结构图直接嵌入终端或自建工具时，它的 SVG/文本输出很实用；需要节点说明、可探索系统页面和交付校验流程时，优先 Archify。

## 7. Drawnix：可编辑知识白板，不能误写成内置 AI 架构生成器

仓库：[**plait-board/drawnix**](https://github.com/plait-board/drawnix)；**14,941 Star / 1,298 Fork**。审阅 SHA：`b138ff867943ddff6c4c79560e10ab6ee3b5600e`；HEAD 提交日期：2026-09-07（UTC）；API latest release：[v0.4.0](https://github.com/plait-board/drawnix/releases/tag/v0.4.0)。本地：[源码目录](../repos/plait-board/drawnix/)。

**功能与输入输出。** 主体是基于 Plait/React 的白板，支持思维导图、流程图、自由画、图片、主题和撤销重做。Mermaid 可以转换成画布元素，Markdown 可以转换成思维导图；随后可手动修改，保存 `.drawnix` JSON 或导出 PNG。典型用法是把 Agent 已写出的结构文本导入后，由人做归类、连线与布局调整。

**源码核实。** Mermaid 对话框动态加载 `@plait-board/mermaid-to-drawnix`，解析结果是 Plait 元素，通过 `board.insertFragment` 插入真正可编辑的画布；Markdown 对话框使用另一个转换包创建 MindElement。应用用 localforage 写入 IndexedDB/LocalStorage；源格式序列化保存元素、viewport、theme。它没有在这些入口中调用 LLM，因此不能把文本导入功能描述为“应用自己从问题理解架构”。

- [Mermaid 转元素并插入画布](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/packages/drawnix/src/components/ttd-dialog/mermaid-to-drawnix.tsx#L69-L116)。
- [Markdown 转思维导图](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/packages/drawnix/src/components/ttd-dialog/markdown-to-drawnix.tsx#L66-L108)。
- [浏览器存储驱动](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/apps/web/src/app/app.tsx#L20-L28)；[变更自动保存](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/apps/web/src/app/app.tsx#L96-L105)。
- [原生文件保存](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/packages/drawnix/src/data/json.ts#L18-L38)；[保存的数据结构](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/packages/drawnix/src/data/json.ts#L62-L72)。

**成本、许可和审阅。** 浏览器运行；自行构建涉及 Node/npm、Nx、Vite、React、Plait 和两个转换依赖，主许可 MIT。已经读到的是转换包的调用边界，没有进一步下载这两个包核对全部语法支持，因此不承诺 Mermaid 全类型或无损双向往返。浏览器缓存不是云同步、团队协作或永久备份的保证，需保留导出的源文件。[运行库依赖](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/package.json#L17-L41) · [许可](https://github.com/plait-board/drawnix/blob/b138ff867943ddff6c4c79560e10ab6ee3b5600e/LICENSE#L1-L21)。

已静态读转换/存储路径及部分测试文件；`drawnix.spec.tsx` 的基础渲染测试体中断言被注释，不能单凭有测试文件就宣称覆盖充分。没有运行前端或转换测试。此项属于相邻的编辑/理解工具：人需要自由整理知识结构时有用；要 Agent 生成架构讲解成品，继续优先 Archify。

## 8. 候选筛除、历史血缘和官方服务边界

候选均留有精确元数据及筛选依据，详见 [agent-diagram-candidates.json](../evidence/agent-diagram-candidates.json)。没有把暂不收录解释成项目无用。

| 候选 | Star / Fork | 本轮决定与具体依据 |
| --- | ---: | --- |
| [awslabs/mcp](https://github.com/awslabs/mcp) 内旧 AWS Diagram 模块 | 9,780 / 1,806（全合集） | 不收旧模块作为当前可安装推荐。官方博客明确该包于 2026-06 弃用且 PyPI 版本撤下；固定 HEAD 中原 `src/aws-diagram-mcp-server` 路径不在。整个合集仍存在，不能说 AWS MCP 全部停用。 |
| [hustcc/mcp-mermaid](https://github.com/hustcc/mcp-mermaid) | 642 / 60 | 保留为社区 Mermaid MCP 候选。读取 `src/utils/render.ts` 确认用 mermaid-isomorphic 做渲染封装；没有发现足以优先于本轮六项的独立架构建模/解释层，未克隆和实测，也不标为 Mermaid 官方。 |
| [Mermaid-Chart/vscode-mermaid-chart](https://github.com/Mermaid-Chart/vscode-mermaid-chart) | 154 / 33 | 官方 VS Code 插件，应与官方托管 MCP 服务分开。README 描述代码生成、Copilot 指令、修复及账号集成；本轮没有审完插件实现，不把插件仓 Star 或源码可见性归给远端 MCP 服务。 |
| [Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator) | 7,434 / 569 | 作为 Archify 血缘记录，不重复主推荐。当前是 v1.1 风格的 skill 与 HTML/SVG 模板；Archify 明确记录由其 v1.0 fork/rewrite。原项目仍可单独使用，并不是仓库自动迁移到 Archify。 |
| [hasibweb/OpenDraw](https://github.com/hasibweb/OpenDraw) | 2 / 0 | GitHub `fork=true`，parent/source 均指向 Itz-Agasta/OpenDiagram，剔除重复入口。不能把它当独立原创引擎。 |
| [Itz-Agasta/OpenDiagram](https://github.com/Itz-Agasta/OpenDiagram) | 52 / 10 | 保留观察。README 与源码树有 typed DiagramSpec、布局/renderer、Excalidraw 和完整应用栈；需额外深入 harness/API/数据库流程。不能因 Star 低否认机制，但本轮优先完成已有六项；未克隆/运行，不将宣传的自动纠错写成证实结果。 |
| [lgboim/AI-Diagram](https://github.com/lgboim/AI-Diagram) | 2 / 0 | 不作为优先候选。实际入口 `gras.py` 提示模型返回 Python，却写成 `.dot` 交给 Graphviz；README 还指向不存在的 `app.py`。属于代码与使用说明已有明显不一致的小样例，未运行，也没有尝试修复。 |

AWS 官方说明给出的迁移方向是 Claude Code 的 `deploy-on-aws` 插件内架构图 skill，以及 Kiro 场景的 `diagrams-mcp`。本轮只核实官方指向与 skill 路径，没有为这两个替代项声称实测或赋予旧合集 Star；上文 `awslabs/diagram-as-code` 是另一条独立 AWS 绘图路线。来源：[AWS 更新说明](https://aws.amazon.com/blogs/machine-learning/build-aws-architecture-diagrams-using-amazon-q-cli-and-mcp/) · [deploy-on-aws 架构图 skill](https://github.com/awslabs/agent-plugins/tree/main/plugins/deploy-on-aws/skills/aws-architecture-diagram)。

Mermaid 的官方远端 MCP 确实存在，官方文档列出校验/渲染与账号项目管理工具；**每次工具调用需要 Mermaid 账号认证**。本轮没有找到并审阅其对应的公开服务端实现，故只列服务边界，未虚构一个“官方开源 MCP 仓库”，也没有把社区 wrapper 当官方仓。来源：[Mermaid 官方 MCP 文档](https://mermaid.ai/docs/ai/mcp-server)。

Archify 血缘的一手证据见 [固定版本 CHANGELOG](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/CHANGELOG.md#L441-L455)。这解释了为什么 Cocoon 值得保留出处，但不会作为“又一个独立的新 Archify”重复增加推荐数量。
