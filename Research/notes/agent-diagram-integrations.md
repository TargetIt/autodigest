# Agent 绘图集成与数据图表的源码笔记

采集日期：2026-10-15（Asia/Shanghai）。各项目的实时 Star、Fork、默认分支提交和 release 见 [GitHub 快照](../evidence/github-metadata.json)。这里记录固定版本的实现依据；浏览器渲染、远端 MCP、模型 API 和商业服务没有做端到端测试。

## coleam00 的 Excalidraw Diagram Skill

[仓库](https://github.com/coleam00/excalidraw-diagram-skill) · 审阅版本 `8646fcc9f74f38539c6cdb4c969723336a96ddcd`。

它把自然语言解释组织成可继续编辑的 `.excalidraw` 文件，并用 Python、Playwright 和 Chromium 生成 PNG。对知识消化的价值是把一对多、汇聚、时间顺序等关系映射成不同空间形状，也要求技术图放入具体代码或数据作为说明材料。[设计与证据要求](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/SKILL.md#L34-L82)

实现不是一个独立的自然语言解析器：Agent 根据 skill 写 JSON，渲染器读取 JSON、计算包围盒，在浏览器调用 Excalidraw 的 `exportToSvg`，最后截取 SVG 元素生成 PNG。模板从 `esm.sh` 加载未锁定版本的 Excalidraw bundle，因此本版本默认渲染路径有外部网络依赖。[Python 渲染流程](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/references/render_excalidraw.py#L87-L166) · [HTML 导入与导出](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/references/render_template.html#L15-L41)

必须区分两类验证：代码中的 `validate_excalidraw` 只检查顶层 type 和非空 elements 数组；文字重叠、箭头错位由 skill 要求 Agent 渲染后看图修复。它没有自动证明知识内容正确。本次对已读函数做了六个无浏览器检查，其中一个刻意无效的元素类型仍通过顶层校验，证实其检查范围有限。[结构检查](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/references/render_excalidraw.py#L21-L35) · [看图修复要求](https://github.com/coleam00/excalidraw-diagram-skill/blob/8646fcc9f74f38539c6cdb4c969723336a96ddcd/SKILL.md#L447-L505)

使用条件是支持文件读写和运行渲染器的 Agent、Python ≥3.11、Playwright、Chromium。当前所审树未见 LICENSE 文件，GitHub 的 license 检测也为空；不能仅凭仓库公开就写成“MIT”。适合借鉴设计和渲染复查方法，复用源码前需核实授权。

## Excalidraw 官方 MCP App

[仓库](https://github.com/excalidraw/excalidraw-mcp) · 审阅版本 `157aa23ceb1976008aadc89eb05e3444060f09d6`。

它让 Agent 通过 MCP 生成手绘图，在支持 MCP Apps 的宿主里流式展示，并允许进入全屏编辑。适合在解释过程中逐步展开结构，而不只是回复一个最终截图。`read_me` 返回元素格式；`create_view` 接收元素 JSON；前端分别处理部分输入、完整输入和工具结果，存在 checkpoint 的读取、恢复与保存机制。[服务端工具](https://github.com/excalidraw/excalidraw-mcp/blob/157aa23ceb1976008aadc89eb05e3444060f09d6/src/server.ts#L401-L475) · [流式输入处理](https://github.com/excalidraw/excalidraw-mcp/blob/157aa23ceb1976008aadc89eb05e3444060f09d6/src/mcp-app.tsx#L804-L830)

checkpoint 可用本地文件、内存或 Redis 实现，并非所有部署都只在浏览器保存。`export_to_excalidraw` 会压缩并加密内容，再上传至 Excalidraw 的 JSON 服务生成分享链接；这个分享动作与本地文件导出不同。[存储实现](https://github.com/excalidraw/excalidraw-mcp/blob/157aa23ceb1976008aadc89eb05e3444060f09d6/src/checkpoint-store.ts#L24-L132) · [分享上传代码](https://github.com/excalidraw/excalidraw-mcp/blob/157aa23ceb1976008aadc89eb05e3444060f09d6/src/server.ts#L550-L592)

本次未连接公共 MCP 服务，不能把 README 列出的宿主都当作已验证兼容。README/package 声明 MIT，但该版本根目录未见单独 LICENSE 文件，GitHub 自动检测为空；报告保留这种差异。相比通用 Excalidraw 编辑器，它是 Agent 集成层，星数单独统计。

## draw.io 官方 MCP 与 Assistant Plugins

[仓库](https://github.com/jgraph/drawio-mcp) · 审阅版本 `3398377f740d47faa0245b107b886e856fa3930f`。

同仓包含内嵌交互图的 MCP App、打开浏览器的 MCP Tool Server、供编码助手使用的 drawio skill/plugin，以及不启用 MCP 的项目指令。对于 AutoDigest，可先让 Agent 产生流程图或精确位置的架构图，再在 draw.io 中人工调整，保存原生 XML 以便追溯和修改。[官方入口说明](https://github.com/jgraph/drawio-mcp/blob/3398377f740d47faa0245b107b886e856fa3930f/README.md)

`create_diagram` 对 XML 与 Mermaid 输入做区分；方向或层级关系图可以选择 ELK 重新布局节点。节点位置本身有含义的泳道、分区或架构图，宜保留位置并按需用 libavoid 绕开障碍物布线。`search_shapes` 使用本地图形索引，弱匹配还可以查询图标服务。它不是一条“把文字变图片”的黑箱调用。[输入和布局参数](https://github.com/jgraph/drawio-mcp/blob/3398377f740d47faa0245b107b886e856fa3930f/mcp-app-server/src/shared.js#L6811-L6877) · [ELK 服务端布局桥接](https://github.com/jgraph/drawio-mcp/blob/3398377f740d47faa0245b107b886e856fa3930f/mcp-tool-server/src/elk-pass.js#L1-L20) · [本地索引查询](https://github.com/jgraph/drawio-mcp/blob/3398377f740d47faa0245b107b886e856fa3930f/shared/shape-search.js#L1-L100) · [远程图标补充](https://github.com/jgraph/drawio-mcp/blob/3398377f740d47faa0245b107b886e856fa3930f/shared/icon-search.js#L1-L25)

一个当前版本的细节值得保留：README 的布局能力表把 Tool Server 的 ELK 标为未支持，但 `mcp-tool-server/src/elk-pass.js` 已存在对应实现。因此报告按固定源码说明实现存在，不把表格当成完整能力边界，也不推定已发布 npm 包与 HEAD 完全一致。

本次运行 `node --test mcp-tool-server/test/shape-search.test.js`，三个现有测试全部通过：相对图像路径转换、绝对/data URI 保留、强匹配标记。这个结果只验证查询辅助函数，没有验证整个图形 UI。主代码 LICENSE 为 Apache-2.0；draw.io 图标、模板资产的独立条件另见编辑器项目。内嵌效果取决于宿主是否支持 MCP Apps，桌面格式导出取决于安装的 draw.io Desktop。

## Excalidraw 官方 CLI

[仓库](https://github.com/excalidraw/cli) · 审阅版本 `55fe7f494837078781a062c4d3faf29c159ebec5`。

它既能管理 Excalidraw+ 工作区，也能把本地 `.excalidraw` 文件渲染成 PNG。后者无需账号或 API key，可作为知识图的可重复导出步骤；前者通过公共 API 操作云端资源，二者的账号要求不能混写。[本地渲染命令](https://github.com/excalidraw/cli/blob/55fe7f494837078781a062c4d3faf29c159ebec5/src/commands/render.ts#L78-L90)

实现使用 Playwright Core 驱动已安装浏览器，先校验场景和内嵌图片，再使用随构建打包的渲染器。图像数据、空场景、找不到 frame 等都有拒绝路径及相应测试。中文手绘字体首次使用可能需要下载，下载有 SHA-256 校验和缓存；提供 `--fonts-url none` 禁止下载时会回退字体。因此“本地渲染”不应被解释成默认完全无网络依赖。[渲染入口](https://github.com/excalidraw/cli/blob/55fe7f494837078781a062c4d3faf29c159ebec5/src/render.ts#L112-L178) · [字体加载](https://github.com/excalidraw/cli/blob/55fe7f494837078781a062c4d3faf29c159ebec5/src/fonts.ts#L22-L89) · [拒绝无效输入测试](https://github.com/excalidraw/cli/blob/55fe7f494837078781a062c4d3faf29c159ebec5/test/render-validation.test.ts#L15-L65)

代码 MIT，Node ≥22。此次静态审阅，没有构建或启动浏览器。它本身不负责理解主题、自动画关系、检验论断，适合作为已有 Excalidraw 生成流程的输出工具。

## Next AI Draw.io

[仓库](https://github.com/DayuanJiang/next-ai-draw-io) · 审阅版本 `623eb91e579465dabe2794da5aac2dfaceba0f71`。

这是较完整的 AI 绘图应用，具有聊天界面、draw.io 编辑画布、多个模型 provider 和桌面打包路径。输入文字或材料后生成可编辑图，用户可以继续要求增删某个节点。适合需要持续修改图、希望直接使用产品界面的场景，搭建成本高于单个 Markdown skill。

源码的 `display_diagram`、`edit_diagram`、`append_diagram` 各有明确 schema。`edit_diagram` 以 cell ID 进行增删改；`append_diagram` 用来续写被截断的 XML。浏览器 handler 将 XML 结构错误返回模型重试，还包含可选视觉验证及次数控制，而不是只把一次模型输出当最终结果。[工具 schema](https://github.com/DayuanJiang/next-ai-draw-io/blob/623eb91e579465dabe2794da5aac2dfaceba0f71/lib/chat-tools.ts#L13-L110) · [校验、修复与重试](https://github.com/DayuanJiang/next-ai-draw-io/blob/623eb91e579465dabe2794da5aac2dfaceba0f71/hooks/use-diagram-tool-handlers.ts#L227-L337)

仓库有 XML validation、edit、history、多页以及浏览器交互测试，但本次只读了相关实现与测试目录，没有跑模型调用或整套应用。视觉模型复查仍可能遗漏事实错误；XML 合法也不等于图中因果关系成立。主代码 Apache-2.0；需要模型服务配置与相应调用成本。自部署可控制部署位置，但数据实际发送范围仍取决于选择的模型 provider。

## Eric Blue 的 Visual Explainer Skill

[仓库](https://github.com/ericblue/visual-explainer-skill) · 审阅版本 `811b823653f0d1d9b1d2bc6f7c13df952f0216e7`。

这是基于图像生成 API 的解释图 skill，支持白板、信息图、幻灯片、思维导图、界面草图等风格。它先组织详细视觉提示，再请求图片；多帧模式是生成几张递进的图，并非同一个可操作的交互模型。[入口与风格](https://github.com/ericblue/visual-explainer-skill/blob/811b823653f0d1d9b1d2bc6f7c13df952f0216e7/skill/visual-explainer.md#L1-L44) · [多帧与图片请求](https://github.com/ericblue/visual-explainer-skill/blob/811b823653f0d1d9b1d2bc6f7c13df952f0216e7/skill/visual-explainer.md#L527-L590)

与 `nicobailon/visual-explainer` 是两个项目。本仓实际主要是 Markdown 指令、元数据和 Makefile，图片 API 调用以 shell 示例写在 skill 中；不是具有确定性布局的独立渲染引擎。输出主要是 PNG，修改通常要重新生成，不能像原生 Excalidraw/XML 那样逐节点精确编辑。

还发现具体版本一致性问题：文案将 Gemini 后端称为 Nano Banana 2，实际请求示例却写 `gemini-2.0-flash-preview-image-generation`。这只能证明该版本文案与请求标识不一致；本次没有验证这些外部 API 的当前可用性，不据此给出可直接复制的调用方案。代码 MIT，需要图像服务凭据和调用费用。适合做讲解插图，精确公式、代码、中文标签和箭头关系要人工复查。

## Apache ECharts

[仓库](https://github.com/apache/echarts) · 审阅版本 `34f4d927eafe251f26f63afd3aeefa30f2feba30`。

ECharts 是浏览器交互图表库。输入数据和 option，输出曲线、柱图、散点等数据表达；在知识学习中适合比较变量变化、展示实验结果和多组数据联动。它不负责自动读材料、判断哪些知识正确，也不是默认的因果模拟器。

`setOption` 将输入交给模型并调度更新；数据 transform 层支持登记和组合转换，让原始数据与呈现规则分离。仓库的视觉测试页和单元测试设施可用于检查绘制行为，不能替代数据来源检查。[更新入口](https://github.com/apache/echarts/blob/34f4d927eafe251f26f63afd3aeefa30f2feba30/src/core/echarts.ts#L724-L791) · [数据转换注册与执行](https://github.com/apache/echarts/blob/34f4d927eafe251f26f63afd3aeefa30f2feba30/src/data/helper/transform.ts#L333-L427)

代码 Apache-2.0。可在 HTML/JavaScript 解释页中使用，但需要自己定义数据、编码、单位和交互。本次只做静态审查，没有建立完整图表应用或运行其完整测试集。
