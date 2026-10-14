# 结构图、白板、思维导图与信息图：源码审阅记录

调研日期：2026-10-15。范围：11 个 GitHub 主仓的 README、许可证和关键实现；另核实 Graphviz 官方来源。本文件记录静态审阅证据，**没有安装依赖、运行第三方仓库代码或验证真实渲染效果**，因此不能把代码中存在的功能当作已经通过端到端测试的能力。各条目中的使用建议属于基于代码机制的判断；GitHub Stars 及活跃度由同次调研的主报告统一记录，避免使用网页四舍五入数字。

最重要的区分是：Mermaid、D2、PlantUML 负责把关系描述变成图；Excalidraw、draw.io 负责可编辑的视觉工作区；Markmap 负责把已有层级展开为导图；AntV Infographic 负责选择信息结构并套用视觉组件；React Flow 和 tldraw 更接近开发可视化产品的基础设施。它们都不自动保证输入知识正确，也不自动构成完整的教学流程。

## 1. Mermaid：最适合进入知识笔记的文本图

- **入口**：[GitHub](https://github.com/mermaid-js/mermaid) · [文档](https://mermaid.js.org/) · [在线编辑器](https://mermaid.live/)；标识 `mermaid-js/mermaid`。
- **基本功能与知识价值**：用文本描述流程、时序、状态、类/实体关系、甘特和思维导图等。适合把“先后发生什么”“谁依赖谁”“有哪些状态”显式画出来；语法可保留在 Markdown 和 Git 中，便于解释修订。
- **输入 → 输出**：Mermaid DSL → SVG 和可绑定的交互函数；嵌入网页或支持 Mermaid 的 Markdown 环境。PNG/PDF 导出通常由编辑器或另配 CLI 处理，不应混同为本次阅读的核心 API 返回格式。
- **源码验证**：[`Diagram.fromText`](https://github.com/mermaid-js/mermaid/blob/e28fbd9ded0a07ba9569e51be4764c1ad4daa8f6/packages/mermaid/src/Diagram.ts#L19-L96) 先检测图类型、按需加载实现，再将对应 parser、database、renderer 组合；源码位置相关的注释和 frontmatter 偏移也有明确处理。[流程图渲染器](https://github.com/mermaid-js/mermaid/blob/e28fbd9ded0a07ba9569e51be4764c1ad4daa8f6/packages/mermaid/src/diagrams/flowchart/flowRenderer-v3-unified.ts#L20-L44) 将解析结果转换为布局数据，调用所选布局算法；[`mermaidAPI`](https://github.com/mermaid-js/mermaid/blob/e28fbd9ded0a07ba9569e51be4764c1ad4daa8f6/packages/mermaid/src/mermaidAPI.ts#L626-L681) 序列化 SVG，并按安全配置使用 DOMPurify 或 iframe，最后返回 `svg` 和 `bindFunctions`。
- **条件与局限**：核心渲染路径使用浏览器 DOM；适合结构化关系，不是任意手绘排版或教学模拟器。图过密、说明过长时仍需拆图；可解析只证明语法成立，不证明关系真实。许可证：[MIT](https://github.com/mermaid-js/mermaid/blob/e28fbd9ded0a07ba9569e51be4764c1ad4daa8f6/LICENSE#L1-L21)。
- **对 AutoDigest 的建议**：作为默认“机制/关系图”输出，和文字中的节点命名保持一致；每条重要边说明它是顺序、因果、依赖还是包含。

## 2. Excalidraw：适合边讨论边修改的解释白板

- **入口**：[GitHub](https://github.com/excalidraw/excalidraw) · [直接使用](https://excalidraw.com/) · [组件文档](https://docs.excalidraw.com/)；标识 `excalidraw/excalidraw`。
- **基本功能与知识价值**：手绘风格无限画布，包含形状、箭头、文字和图片，可将类比、注释、边界和局部细节放到同一张白板上。很适合“你指出不懂的一块，我就在那块继续解释”。
- **输入 → 输出**：拖拽操作或程序生成的元素/场景 JSON → 可继续编辑的 `.excalidraw` 文件、SVG 和 Canvas/图片输出。
- **源码验证**：[`serializeAsJSON`](https://github.com/excalidraw/excalidraw/blob/4c37956ba5f04ec342a9d9d5891a38f22c5b7b4e/packages/excalidraw/data/json.ts#L52-L74) 持久化 `elements`、清理后的 `appState`、所需 `files`；[Canvas 导出](https://github.com/excalidraw/excalidraw/blob/4c37956ba5f04ec342a9d9d5891a38f22c5b7b4e/packages/excalidraw/scene/export.ts#L232-L267) 实际调用 `rough.canvas` 和静态场景 renderer；[SVG 导出](https://github.com/excalidraw/excalidraw/blob/4c37956ba5f04ec342a9d9d5891a38f22c5b7b4e/packages/excalidraw/scene/export.ts#L363-L387) 可把原始场景 JSON 嵌入 metadata，使图片保留再编辑资料，随后由 [Rough SVG 渲染](https://github.com/excalidraw/excalidraw/blob/4c37956ba5f04ec342a9d9d5891a38f22c5b7b4e/packages/excalidraw/scene/export.ts#L471-L490) 生成元素。
- **条件与局限**：网页直接用，产品集成需 React 与浏览器环境；本次核实的是场景与导出，不把官网协作服务等同于安装 npm 组件即自动获得完整协作后端。它擅长空间表达，不自动进行逻辑验证；AI 直接输出场景 JSON 时，文字换行、箭头绑定、重叠仍需实际渲染检查。许可证：[MIT](https://github.com/excalidraw/excalidraw/blob/4c37956ba5f04ec342a9d9d5891a38f22c5b7b4e/LICENSE#L1-L21)。
- **对 AutoDigest 的建议**：用于核心解释的手绘类比图，并同时保存场景源文件和预览，方便用户反馈后局部修改。

## 3. draw.io / diagrams.net：复杂、规范、可长期维护的图

- **入口**：[GitHub](https://github.com/jgraph/drawio) · [在线编辑器](https://app.diagrams.net/) · [桌面版入口](https://get.diagrams.net/)；标识 `jgraph/drawio`。
- **基本功能与知识价值**：通用流程图、架构图、网络图、组织图与白板编辑器。适合需要细调尺寸、连接线、分组、多页和规范图标的正式说明，尤其是从概念草图继续加工成长期文档。
- **输入 → 输出**：交互编辑或 `.drawio`/XML 图模型 → 可编辑图文件、SVG/PNG/PDF 等导出；其中 SVG 可以嵌入图模型。
- **源码验证**：[模型编码/压缩](https://github.com/jgraph/drawio/blob/9034053fba80a435e27d68d374bc564b83917ae9/src/main/webapp/js/grapheditor/Graph.js#L3325-L3359) 使用 URL 编码、deflate 和 Base64；[`createFileData`](https://github.com/jgraph/drawio/blob/9034053fba80a435e27d68d374bc564b83917ae9/src/main/webapp/js/diagramly/EditorUi.js#L2489-L2511) 根据模式输出 XML 或含 XML 的 HTML/SVG；[可编辑 SVG 导出](https://github.com/jgraph/drawio/blob/9034053fba80a435e27d68d374bc564b83917ae9/src/main/webapp/js/diagramly/EditorUi.js#L8795-L8809) 在 SVG `content` 属性中写入原始模型。这解释了它为何能保存“看得见的图”和“可继续编辑的结构”。
- **条件与局限**：可用网页、桌面或自托管方式；模型 XML 比 Mermaid DSL 冗长，Agent 生成后必须检查几何位置。当前仓库 [README](https://github.com/jgraph/drawio/blob/9034053fba80a435e27d68d374bc564b83917ae9/README.md#L25-L39) 明确说明本版本不支持实时协同编辑，SVG 导出用于展示而非跨软件保真编辑。
- **许可必须分开写**：代码 [Apache-2.0](https://github.com/jgraph/drawio/blob/9034053fba80a435e27d68d374bc564b83917ae9/LICENSE#L1-L9)；[README 中的图标、stencil 和模板条款](https://github.com/jgraph/drawio/blob/9034053fba80a435e27d68d374bc564b83917ae9/README.md#L7-L19) 另有限制，尤其不得把相关资产用于 Atlassian 产品或其市场生态，最终用户导出图不在该限制内。因此不能把整个仓库的一切资产概括成无附加条件的 Apache-2.0。
- **对 AutoDigest 的建议**：作为“整理成正式图”的出口；若核心诉求只是快速解释，先用 Mermaid 或 Excalidraw 通常更轻。

## 4. D2：偏架构表达的图描述语言

- **入口**：[GitHub，当前正式位置](https://github.com/d2lang/d2) · [文档](https://d2lang.com/) · [Playground](https://play.d2lang.com/)；标识 `d2lang/d2`。旧地址 `terrastruct/d2` 已重定向，不应把两者算成两个项目。
- **基本功能与知识价值**：用文本表达节点、连线、嵌套容器、标签、样式和分层图，适合复杂系统的组成关系、边界、架构演进及多步说明。
- **输入 → 输出**：D2 DSL → 图结构与布局结果 → SVG；CLI 还提供其他导出路径，但本次主要核实编译/布局链路。
- **源码验证**：[`d2lib`](https://github.com/d2lang/d2/blob/6a7b4837838a3907604a1d9eec57ee98b6f3cd01/d2lib/d2.go#L72-L124) 将输入交给 parser/compiler，并合并配置；[布局阶段](https://github.com/d2lang/d2/blob/6a7b4837838a3907604a1d9eec57ee98b6f3cd01/d2lib/d2.go#L184-L229) 测量尺寸后调用布局和边路由，能够复用特定场景的几何结果。默认布局名称在 [applyDefaults](https://github.com/d2lang/d2/blob/6a7b4837838a3907604a1d9eec57ee98b6f3cd01/d2lib/d2.go#L326-L329) 为 `dagre`。
- **需要更新旧认知**：本次 HEAD 的 [README](https://github.com/d2lang/d2/blob/6a7b4837838a3907604a1d9eec57ee98b6f3cd01/README.md#L185-L204) 已将 TALA 列为 bundled、opt-in；[TALA 目录说明](https://github.com/d2lang/d2/blob/6a7b4837838a3907604a1d9eec57ee98b6f3cd01/d2layouts/d2talalayout/README.md#L15-L27) 说明其本地布局、边路由与确定性多 seed 尝试；[L67–L69](https://github.com/d2lang/d2/blob/6a7b4837838a3907604a1d9eec57ee98b6f3cd01/d2layouts/d2talalayout/README.md#L67-L69) 明确适用仓库主许可，第三方来源保留各自 notices。不能照抄旧文章说 TALA 永远闭源收费。
- **条件与局限**：可使用本地 CLI 或嵌入 Go/JS 相关实现；相比 Mermaid，要额外维护渲染工具链和语言知识。自动布局并不保证所有复杂图一次美观，本次未做布局质量测试。根许可：[MPL-2.0](https://github.com/d2lang/d2/blob/6a7b4837838a3907604a1d9eec57ee98b6f3cd01/LICENSE.txt#L1-L6)。
- **对 AutoDigest 的建议**：当 Mermaid 的容器/架构布局不足时再选 D2，保留 `.d2` 源文件，不只提交图片。

## 5. PlantUML：形式化关系图，以及官方 Agent 接入

- **入口**：[GitHub](https://github.com/plantuml/plantuml) · [官网](https://plantuml.com/) · [官方 Node MCP 子项目](https://github.com/plantuml/plantuml/tree/8678962c537bfb854073fc15394ac0b5ed5ea83e/plantuml-mcp-js)；标识 `plantuml/plantuml`。
- **基本功能与知识价值**：文本驱动的时序、类、状态、活动等 UML 及其他图。它适合把“参与者、消息、条件、状态迁移”讲得精确，尤其适合协议、程序行为和系统交互。
- **输入 → 输出**：PlantUML 源文本 → Java 主实现的图像/文档格式；同仓 Node MCP 则返回语法检查、解析解释或 SVG 的结构化结果。不同运行形态的输出能力要分别看。
- **源码验证**：[`SourceStringReader`](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/src/main/java/net/sourceforge/plantuml/SourceStringReader.java#L101-L106) 将源文本分解为 UML blocks，随后 [调用每个 Diagram 的 exportDiagram](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/src/main/java/net/sourceforge/plantuml/SourceStringReader.java#L174-L198)；[`PSystemBuilder`](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/src/main/java/net/sourceforge/plantuml/PSystemBuilder.java#L242-L276) 按图类型寻找 factory，聚合错误而非把所有文本统一视作普通节点图。
- **与 ShowMe/Agent 场景特别相关**：官方 `@plantuml/mcp-js` 的 [`server.js`](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/plantuml-mcp-js/server.js#L100-L178) 确实注册 `check_syntax`、`render_diagram`，另有 [`explain_diagram`](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/plantuml-mcp-js/server.js#L182-L215) 返回带原始行号的解析解释。它调用 TeaVM 编译的引擎，使用 Viz.js/WASM 处理 Graphviz 布局；[package.json](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/plantuml-mcp-js/package.json#L1-L39) 可核对包身份、MIT 许可与依赖。这里的“explain”是解释图语法如何被解析，不是自动教学文章。
- **条件与局限**：传统 Java 路径需要对应 Java/布局依赖；Node MCP 运行无需 Java，但 [其 README](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/plantuml-mcp-js/README.md#L20-L72) 明确只输出 SVG，不支持 PNG/PDF；该 server 当前未给引擎提供标准库/本地文件加载器，`!include` 会报错，主题会有忽略警告。不能把完整 Java 版本的全部特性承诺给 Node MCP。
- **许可证**：[LICENSES.md](https://github.com/plantuml/plantuml/blob/8678962c537bfb854073fc15394ac0b5ed5ea83e/LICENSES.md#L1-L37) 明确默认 GPL-3.0-or-later，并提供 GPLv2、LGPL、Apache、BSD、EPL、MIT 等变体；官方 npm `@plantuml/core` 与 `@plantuml/mcp-js` 标为 MIT。应按实际选用的发行物记录，生成图片不自动被 GPL 覆盖。
- **对 AutoDigest 的建议**：用于技术机制解释；如果要给 Agent 接入语法检查和真正渲染，官方 MCP 比只有“写 PlantUML 提示词”的 skill 更完整，但仍需要视觉 QA 与事实核查。

## 6. Markmap：把 Markdown 大纲变成可折叠的知识导航

- **入口**：[GitHub](https://github.com/markmap/markmap) · [官网与在线试用](https://markmap.js.org/)；标识 `markmap/markmap`。不要把早期 `dundalek/markmap` 与目前活跃实现混为一谈。
- **基本功能与知识价值**：从 Markdown 标题和列表生成交互思维导图。适合先建立概念目录、展示章节归属、逐层展开学习路径，并保持笔记正文作为唯一源。
- **输入 → 输出**：Markdown → 层级树 → SVG/HTML 交互视图，支持折叠、缩放、平移。
- **源码验证**：[`Transformer.transform`](https://github.com/markmap/markmap/blob/122bf0500ee7aca4f023c2465f7e26bf023eec52/packages/markmap-lib/src/transform.ts#L62-L84) 实际通过 markdown-it 渲染 HTML，再 `buildTree` / `cleanNode` 转树；[视图布局](https://github.com/markmap/markmap/blob/122bf0500ee7aca4f023c2465f7e26bf023eec52/packages/markmap-view/src/view.ts#L221-L247) 测量节点宽高，使用 `d3-flextree` 布局；[折叠操作](https://github.com/markmap/markmap/blob/122bf0500ee7aca4f023c2465f7e26bf023eec52/packages/markmap-view/src/view.ts#L142-L159) 修改 `payload.fold` 后重新渲染。[CLI](https://github.com/markmap/markmap/blob/122bf0500ee7aca4f023c2465f7e26bf023eec52/packages/markmap-cli/src/index.ts#L68-L105) 支持离线模式下内联资源并写 HTML。
- **条件与局限**：网页可直接使用，批处理可用 Node CLI。它忠实转换已有结构，不会替用户判断“该知识应如何分类”；树无法充分表达跨分支依赖、反馈环或多对多关系，不应把树当成因果网络。默认资源可能走 CDN，离线交付应明确启用资源内联。许可证：[MIT](https://github.com/markmap/markmap/blob/122bf0500ee7aca4f023c2465f7e26bf023eec52/LICENSE#L1-L21)。
- **对 AutoDigest 的建议**：最适合把知识锚定/摘要整理成导览页，点击展开配合核心解释，不能代替机制图。

## 7. Diagrams（mingrammer）：用 Python 写云系统架构图

- **入口**：[GitHub](https://github.com/mingrammer/diagrams) · [文档](https://diagrams.mingrammer.com/)；标识 `mingrammer/diagrams`。
- **基本功能与知识价值**：提供云服务、开源组件等节点图标，通过 Python 连接、分组、标记关系，适合解释基础设施、数据流、服务边界和部署方式。
- **输入 → 输出**：Python 中的 `Diagram`、`Cluster`、`Node`、`Edge` → Graphviz DOT → PNG/JPG/SVG/PDF/DOT（代码列出的格式）。
- **源码验证**：[`Diagram`](https://github.com/mingrammer/diagrams/blob/9df75e65c03bf9f3da8c0ddbacc33d4ecf5e31e8/diagrams/__init__.py#L183-L218) 维护 `graphviz.Digraph` 和图/节点/边属性；[上下文退出及 render](https://github.com/mingrammer/diagrams/blob/9df75e65c03bf9f3da8c0ddbacc33d4ecf5e31e8/diagrams/__init__.py#L226-L265) 调用 Graphviz 生成文件；[`Node.__rshift__`](https://github.com/mingrammer/diagrams/blob/9df75e65c03bf9f3da8c0ddbacc33d4ecf5e31e8/diagrams/__init__.py#L435-L458) 将 `>>`/`<<` 运算符转换为有向连接。这是代码对图模型的封装，不是运行 Python 业务系统再自动发现其架构。
- **条件与局限**：[pyproject](https://github.com/mingrammer/diagrams/blob/9df75e65c03bf9f3da8c0ddbacc33d4ecf5e31e8/pyproject.toml#L5-L17) 标记 Python `~=3.9` 与 Python graphviz 包依赖，实际图像渲染还需要 Graphviz 系统引擎。更适合熟悉 Python 的技术读者；不适合通用教学插图或任意交互实验。根许可：[MIT](https://github.com/mingrammer/diagrams/blob/9df75e65c03bf9f3da8c0ddbacc33d4ecf5e31e8/LICENSE#L1-L21)，云厂商图标的品牌/资产条款不能仅由代码 MIT 推断。
- **对 AutoDigest 的建议**：作为云系统解释的专用工具，不放进每次普通知识消化的默认流程。

## 8. React Flow / Svelte Flow（xyflow）：可点击、可操作的知识图应用底座

- **入口**：[GitHub](https://github.com/xyflow/xyflow) · [React Flow](https://reactflow.dev/) · [Svelte Flow](https://svelteflow.dev/)；标识 `xyflow/xyflow`。
- **基本功能与知识价值**：构建节点式交互界面的前端库，提供自定义节点/边、连接、拖拽、选择、缩放等。可以把知识点做成带例子、证据、展开面板和进度的节点，也可以做过程编辑器。
- **输入 → 输出**：由应用提供 `nodes`、`edges`、节点组件与事件逻辑 → 浏览器中的可操作图界面；持久化、数据来源、知识抽取和导出流程需要应用自行组织。
- **源码验证**：[`NodeRenderer`](https://github.com/xyflow/xyflow/blob/3d35b57317576b0916c0bfeaaedd573aaacc2839/packages/react/src/container/NodeRenderer/index.tsx#L38-L94) 只订阅可见节点 ID、共享 ResizeObserver，再渲染 NodeWrapper；[`EdgeRenderer`](https://github.com/xyflow/xyflow/blob/3d35b57317576b0916c0bfeaaedd573aaacc2839/packages/react/src/container/EdgeRenderer/index.tsx#L58-L89) 对可见边绑定交互回调。官方 [自动布局示例](https://github.com/xyflow/xyflow/blob/3d35b57317576b0916c0bfeaaedd573aaacc2839/examples/react/src/examples/Layouting/index.tsx#L24-L72) 显式调用外部 Dagre 再更新节点 position，说明自动布局应单独配置，不能把所有布局能力都归给 React Flow 本体。
- **条件与局限**：需要 React/Svelte 应用开发。它是 SDK，不是拿到论文即自动生成知识图的完整软件；与自带完整编辑器的 Excalidraw/draw.io 的接入工作量不同。核心许可：[MIT](https://github.com/xyflow/xyflow/blob/3d35b57317576b0916c0bfeaaedd573aaacc2839/LICENSE#L1-L21)，商业示例/支持等另看对应产品条款。
- **对 AutoDigest 的建议**：当需要“点击概念查看解释、来源、练习”和持续状态时再选；仅交付一篇文章无需专门搭应用。

## 9. Kroki：把多种画图引擎统一为一个渲染 API

- **入口**：[GitHub](https://github.com/yuzutech/kroki) · [官网](https://kroki.io/) · [文档](https://docs.kroki.io/)；标识 `yuzutech/kroki`，不是 `kroki/kroki`。
- **基本功能与知识价值**：给 Mermaid、PlantUML、Graphviz、D2、Excalidraw、Vega 等提供统一 HTTP 接口。价值在于让知识生产流程按问题选择图种，同时用一致的方式生成产物；它本身不理解文章、不负责教学设计。
- **输入 → 输出**：POST 图源文本或包含 `diagram_type`、`diagram_source`、`output_format` 的 JSON；也支持 GET 中编码的图源 → 对应引擎支持的图像格式。
- **源码验证**：[`Server`](https://github.com/yuzutech/kroki/blob/d161fd8e5735131f986da59f8f359c72f3fa770c/server/src/main/java/io/kroki/server/Server.java#L99-L125) 将图种注册到不同 service；[`DiagramHandler`](https://github.com/yuzutech/kroki/blob/d161fd8e5735131f986da59f8f359c72f3fa770c/server/src/main/java/io/kroki/server/service/DiagramHandler.java#L49-L101) 处理 URL 解码与 POST 输入。部分引擎由 [`Commander`](https://github.com/yuzutech/kroki/blob/d161fd8e5735131f986da59f8f359c72f3fa770c/server/src/main/java/io/kroki/server/action/Commander.java#L27-L76) 启动子进程、输入图源并约束超时；另一些由 [`Delegator`](https://github.com/yuzutech/kroki/blob/d161fd8e5735131f986da59f8f359c72f3fa770c/server/src/main/java/io/kroki/server/action/Delegator.java#L65-L82) HTTP 转发给配套服务。
- **条件与局限**：使用远端服务时图源需要发送出去；自托管需部署服务器、所选引擎以及相关 companion 服务。统一 API 不等于所有图种支持相同格式，也不保证各引擎版本兼容。根许可：[MIT](https://github.com/yuzutech/kroki/blob/d161fd8e5735131f986da59f8f359c72f3fa770c/LICENSE#L1-L21)，组合镜像中各引擎保留各自许可证，仓库也有独立 [licenses 目录](https://github.com/yuzutech/kroki/tree/d161fd8e5735131f986da59f8f359c72f3fa770c/licenses)。
- **对 AutoDigest 的建议**：在确定确实要并行使用多种图 DSL 后，再作为基础渲染服务引入。

## 10. AntV Infographic：离“把知识变成说明图”较近的框架与官方 Skill

- **入口**：[GitHub](https://github.com/antvis/Infographic) · [官网](https://infographic.antv.vision/) · [模板画廊](https://infographic.antv.vision/gallery) · [官方 skills 目录](https://github.com/antvis/Infographic/tree/2ea1894255e4002c7735586778be86d13ec30346/skills)；标识 `antvis/Infographic`。
- **基本功能与知识价值**：用结构化 DSL/配置把列表、步骤、对比、层级、关系与数值组织成信息图，带模板、主题、图标和编辑能力。比纯流程图更适合“把一页知识的主要结构讲清楚”。
- **输入 → 输出**：Infographic 缩进语法或配置对象 → SVG 信息图；浏览器 API 可导出 SVG/PNG data URL，SSR 入口可输出 SVG 字符串。
- **源码验证**：[`parseSyntaxToAst`](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/src/syntax/parser.ts#L169-L201) 按缩进栈构造 AST，并保留行号用于错误反馈；[`Infographic`](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/src/runtime/Infographic.tsx#L99-L118) 先 compose 模板，再用 Renderer 渲染，按 `editable` 创建编辑器。[compose](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/src/runtime/Infographic.tsx#L135-L164) 把结构、标题、条目组件与 data/theme 合成 SVG；[导出方法](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/src/runtime/Infographic.tsx#L184-L196) 区分 SVG 和 PNG；[SSR](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/src/ssr/renderer.ts#L8-L49) 建立 DOM shim，等待资源加载并导出 SVG，包含 10 秒超时。
- **官方 Skill 到底做什么**：[`infographic-creator`](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/skills/infographic-creator/SKILL.md#L20-L94) 规定模板、数据结构与语法；[`infographic-syntax-creator`](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/skills/infographic-syntax-creator/SKILL.md#L8-L31) 负责从用户内容选模板并生成 DSL。这里是对外部 skill 的研究，没有安装或执行它们。Skill 本身不是事实核查器；它要求模型提取结构，真实渲染仍依赖框架或接入层。
- **条件与局限**：浏览器集成需 JS/TS，批量 SVG 可考虑 SSR；字体/图标等资源在离线交付时要验证。适合已被整理的内容，不应为套漂亮模板硬把复杂因果压成列表；框架处于 `0.x` 版本系列，应固定依赖版本后验证产物。许可证：[MIT](https://github.com/antvis/Infographic/blob/2ea1894255e4002c7735586778be86d13ec30346/LICENSE#L1-L21)。
- **对 AutoDigest 的建议**：值得优先试验，作为“概念对比/流程/层级摘要”的结构化视觉输出，但先保留文字解释与事实来源，再选择模板。

## 11. tldraw：能力完整的无限画布 SDK，许可必须单列

- **入口**：[GitHub](https://github.com/tldraw/tldraw) · [SDK 文档](https://tldraw.dev/) · [在线白板](https://www.tldraw.com/)；标识 `tldraw/tldraw`。
- **基本功能与知识价值**：React 无限画布、形状、箭头、嵌入内容、可扩展节点和编辑操作，适合开发“材料、概念、解释、练习放在一个画布里”的知识工作台。
- **输入 → 输出**：用户操作或 Editor API 生成的形状记录 → 可交互画布与图像输出。需要应用开发来连接资料库和学习流程。
- **源码验证**：[`ShapeUtil`](https://github.com/tldraw/tldraw/blob/694791e0acebc0f9df4a16a5880b72d128f8a621/packages/editor/src/lib/editor/shapes/ShapeUtil.ts#L189-L232) 将默认属性、几何、组件和指示形状抽象为扩展契约；[SVG 导出](https://github.com/tldraw/tldraw/blob/694791e0acebc0f9df4a16a5880b72d128f8a621/packages/editor/src/lib/exports/exportToSvg.tsx#L15-L74) 在真实 DOM 中渲染 JSX、等待资源并内联 foreignObject 样式，说明任意 HTML 节点的导出并非简单截图。
- **当前许可不是 MIT**：[根 LICENSE](https://github.com/tldraw/tldraw/blob/694791e0acebc0f9df4a16a5880b72d128f8a621/LICENSE.md#L15-L50) 允许开发环境使用等行为，但默认禁止生产使用，另有试用/商业安排，并禁止绕过 License Key 执行。[LicenseManager](https://github.com/tldraw/tldraw/blob/694791e0acebc0f9df4a16a5880b72d128f8a621/packages/editor/src/lib/license/LicenseManager.ts#L344-L370) 实际校验 ECDSA 签名；[生产状态判断](https://github.com/tldraw/tldraw/blob/694791e0acebc0f9df4a16a5880b72d128f8a621/packages/editor/src/lib/license/LicenseManager.ts#L688-L719) 将缺失、无效或域名不匹配的许可标为 `unlicensed-production`。应归为“源码可见、商业许可条件的 SDK”，不能与无附加生产限制的 MIT 工具混为一类。官方 [许可说明](https://tldraw.dev/community/license) 也说明生产需有效密钥。
- **对 AutoDigest 的建议**：可用于较完整的学习画布产品评估；若当前目标只是交付解释图，先用 Excalidraw；若以后嵌入生产应用，应按当时具体许可方案评估。

## 12. 补充：Graphviz 的官方主仓在 GitLab

[Graphviz 官网源码页](https://graphviz.org/download/source/) 明确指向 [gitlab.com/graphviz/graphviz](https://gitlab.com/graphviz/graphviz)。不应拿一个 GitHub 镜像的 Stars 当作 Graphviz 官方 GitHub Stars。本次只核实官方文档与来源，没有对 Graphviz C/C++ 主仓做源码深审。

它用 DOT 描述图并通过 `dot`、`neato` 等布局引擎产生 SVG、PNG、PDF 等图形；对于依赖图、网络和程序结构很有价值，也是 Diagrams 等工具的重要底层依赖。当前官方 [许可页](https://graphviz.org/license/) 标明 EPL-2.0。面向一般学习者可以先选上层封装；需要程序化批量生成或直接控制图布局时再直接研究 DOT。

## 针对知识消化的选型结论

| 想解决的理解问题 | 优先工具 | 选择理由 | 不应期待它自动做到什么 |
| --- | --- | --- | --- |
| 过程怎么走、对象怎么交互 | Mermaid；精确 UML 可选 PlantUML | 关系与顺序显式，图源可审阅 | 证明事件或因果正确 |
| 知识有哪些层级，先看哪部分 | Markmap | Markdown 直接生成可折叠导航 | 从错误大纲自动重建正确分类 |
| 用类比、箭头和局部注释讲清一个机制 | Excalidraw | 可修改白板，适合用户反馈后迭代 | 自动消除重叠和误导性类比 |
| 用比较、步骤、层级做一页说明 | AntV Infographic | 官方 skill + DSL + 真正 renderer | 自动核查原文和选择唯一正确结构 |
| 系统很复杂、嵌套边界多 | D2 / draw.io | 更丰富的架构排布和编辑方式 | 自动证明架构与真实系统一致 |
| 云组件与部署拓扑 | Diagrams | Python + 服务图标 + Graphviz | 自动从业务代码发现真实部署 |
| 点击节点看证据、做练习并保存状态 | React Flow / tldraw | 可定制交互应用底座 | 无开发即可成为知识产品 |
| 一个流水线需要多种画图引擎 | Kroki | 统一渲染接口 | 替代教学设计、资料检索和事实核查 |

对 AutoDigest 最值得借鉴的不是增加图片数量，而是增加一条可回看的链路：**问题 → 经核对的解释结构 → 对应图源 → 渲染图 → 用户指出不懂之处 → 修订解释和图源**。建议先把 Mermaid、Markmap、Excalidraw、AntV Infographic 作为四种互补出口；复杂 UML、架构图和应用 SDK 按需求启用。

## 复查用的固定源码版本

| 项目 | 实际审阅的 commit SHA |
| --- | --- |
| Mermaid | `e28fbd9ded0a07ba9569e51be4764c1ad4daa8f6` |
| Excalidraw | `4c37956ba5f04ec342a9d9d5891a38f22c5b7b4e` |
| draw.io | `9034053fba80a435e27d68d374bc564b83917ae9` |
| D2 | `6a7b4837838a3907604a1d9eec57ee98b6f3cd01` |
| PlantUML（含 Node MCP） | `8678962c537bfb854073fc15394ac0b5ed5ea83e` |
| Markmap | `122bf0500ee7aca4f023c2465f7e26bf023eec52` |
| Diagrams | `9df75e65c03bf9f3da8c0ddbacc33d4ecf5e31e8` |
| xyflow | `3d35b57317576b0916c0bfeaaedd573aaacc2839` |
| Kroki | `d161fd8e5735131f986da59f8f359c72f3fa770c` |
| AntV Infographic | `2ea1894255e4002c7735586778be86d13ec30346` |
| tldraw | `694791e0acebc0f9df4a16a5880b72d128f8a621` |

审阅下载使用浅克隆和稀疏检出，只读取所需文件；上述链接指向固定 commit，避免默认分支更新后行号失去对应。源码入口与行为解释均为人工静态审阅结论，未执行上游构建、测试或服务。
