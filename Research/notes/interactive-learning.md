# 交互解释、数学动画与可执行知识文档：12 个仓库源码调研

调研日期：2026-10-15（Asia/Shanghai）。本篇属于 AutoDigest 的 Research，关注“读者能不能通过操作、观察和复算建立理解”，包括数学动画、可操作解释、反馈回路、反应式笔记，以及支撑这些产物的数据可视化基础库。

**验证范围：**已下载固定提交的源码，静态阅读 README、核心实现、官方示例、部分测试、依赖声明和许可证；未安装这些仓库的依赖，未启动应用、渲染动画或运行上游测试。因此，“源码确认”表示实现路径存在且已读，“测试”表示审阅了测试内容，不表示本次测试通过。“帮助理解”的判断是基于功能机制的选型推断，未进行学习效果实验。

Stars、Forks、主分支提交日期和 Release 来自同一批 [GitHub API 快照](../evidence/github-metadata.json)，采集时间为 2026-10-15 03:11（UTC+8）。Stars 是**整个仓库**的关注度，不能证明学习效果或稳定性；主分支最后提交可能只是文档修改，也不能单独证明持续维护。源码链接固定到审阅时的完整 SHA，避免后续分支变化导致引文漂移。

## 先按理解任务选工具

| 你需要理解什么 | 优先看的工具 | 为什么值得看 |
| --- | --- | --- |
| 拖动一个变量，观察几何关系怎样变 | Mafs | 拖拽点、约束、函数图和 React 状态直接连接，接近一个可操作的小教具 |
| 改参数后重新算出中间结果，检查自己的判断 | marimo | Python 计算、控件、图和解释放在同一个依赖图中，便于复算 |
| 一串概念如何随时间演变，推导步骤怎样衔接 | Manim Community、Motion Canvas | 作者可以控制对象、公式、时间和讲述顺序，适合精心制作的讲解动画 |
| 正反馈、负反馈和循环关系 | LOOPY | 点击节点注入变化，观察变化沿关系传播；适合定性系统思考 |
| 把解释、多个联动控件和图汇成可分享网页 | Observable Framework | Markdown 与响应式 JavaScript 单元组合；可承载 Plot 或 D3 |
| 3D 数学结构、坐标变换、四元数的视觉直觉 | MathBox | 用 WebGL 场景表达数学关系，但维护和适配成本高于前几项 |
| 分布、离群值、相关性和分组差异 | Observable Plot、Vega-Lite | 从数据到图的路径短；需要作者另写问题、解释与验证环节 |
| 高度定制的图形、交互和解释过程 | D3 | 组成可视化的底层工具丰富，自由度高，工程投入也高 |
| 长期积累成带引用、代码和多种输出的知识书 | Quarto | 更擅长组织、执行和出版文档；互动需要另加 OJS 等能力 |

这些项目大多是**供人或 Agent 调用的库/应用/文档系统**，不是直接装入 Agent 就能替你讲清知识的 skill。把它们用于 ShowMe 一类工作流时，还需要提示规范、正确计算、讲述设计和最终产物检查。

## 关注度与维护快照

| 仓库 | Stars | Forks | 主分支 HEAD 日期（UTC） | 最新正式 Release | 核对的许可证 |
| --- | ---: | ---: | --- | --- | --- |
| [ManimCommunity/manim](https://github.com/ManimCommunity/manim) | 41,533 | 3,191 | [2026-10-12](https://github.com/ManimCommunity/manim/commit/622520d34190062f32d68af066c80f1c937fc8bf) | [v0.22.0](https://github.com/ManimCommunity/manim/releases/tag/v0.22.0)（2026-10-08） | MIT（两份版权声明） |
| [3b1b/manim](https://github.com/3b1b/manim) | 95,073 | 7,795 | [2026-09-09](https://github.com/3b1b/manim/commit/fafa083a4fb274bba9cabde0b6e2f50ba6da0622) | [v1.7.2](https://github.com/3b1b/manim/releases/tag/v1.7.2)（2024-12-13） | MIT |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | 19,327 | 840 | [2026-07-02](https://github.com/motion-canvas/motion-canvas/commit/7b91435c301d530351dcf5ebb91dd139c002e405) | [v3.17.2](https://github.com/motion-canvas/motion-canvas/releases/tag/v3.17.2)（2024-12-14） | MIT |
| [stevenpetryk/mafs](https://github.com/stevenpetryk/mafs) | 3,444 | 100 | [2025-03-30](https://github.com/stevenpetryk/mafs/commit/e74a3ef465f4ddc98704814d2ae18b73a6cd9dae) | [v0.21.0](https://github.com/stevenpetryk/mafs/releases/tag/v0.21.0)（2024-10-20） | MIT |
| [unconed/mathbox](https://github.com/unconed/mathbox) | 1,505 | 126 | [2023-01-25](https://github.com/unconed/mathbox/commit/f80933e114ed8051c8182fe09b83837696b4f0e9) | [v2.3.1](https://github.com/unconed/mathbox/releases/tag/v2.3.1)（2023-01-21） | MIT |
| [observablehq/plot](https://github.com/observablehq/plot) | 5,404 | 250 | [2026-09-01](https://github.com/observablehq/plot/commit/535723d5e433727720d9b673c31622821bb03210) | [v0.6.17](https://github.com/observablehq/plot/releases/tag/v0.6.17)（2025-02-14） | ISC |
| [observablehq/framework](https://github.com/observablehq/framework) | 3,663 | 209 | [2026-05-15](https://github.com/observablehq/framework/commit/85e843e6acfa3dbe93129c125156352c9c50b697) | [v1.13.4](https://github.com/observablehq/framework/releases/tag/v1.13.4)（2026-03-02） | ISC |
| [marimo-team/marimo](https://github.com/marimo-team/marimo) | 23,173 | 1,334 | [2026-10-14](https://github.com/marimo-team/marimo/commit/58be5a93f384dc0fa6e130f98c8688999df74305) | [0.25.1](https://github.com/marimo-team/marimo/releases/tag/0.25.1)（2026-10-01） | Apache-2.0 |
| [ncase/loopy](https://github.com/ncase/loopy) | 1,749 | 249 | [2019-04-17](https://github.com/ncase/loopy/commit/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9) | 无 API latest release | CC0-1.0 |
| [quarto-dev/quarto-cli](https://github.com/quarto-dev/quarto-cli) | 6,086 | 469 | [2026-10-14](https://github.com/quarto-dev/quarto-cli/commit/b86f98d382940bef6c65f37ea0bdfba844f19b6d) | [v1.10.19](https://github.com/quarto-dev/quarto-cli/releases/tag/v1.10.19)（2026-10-06） | CLI 自身 MIT |
| [d3/d3](https://github.com/d3/d3) | 113,752 | 22,632 | [2026-05-28](https://github.com/d3/d3/commit/ca958d45217b4c15332d971b935451a6d4c978f4) | [v7.9.0](https://github.com/d3/d3/releases/tag/v7.9.0)（2024-03-12） | ISC |
| [vega/vega-lite](https://github.com/vega/vega-lite) | 5,517 | 726 | [2026-10-08](https://github.com/vega/vega-lite/commit/85fab8d12c873b3b224ef9a33c807642953325ba) | [v6.5.0](https://github.com/vega/vega-lite/releases/tag/v6.5.0)（2026-10-08） | BSD-3-Clause |

以上 12 个仓库采集时均未归档。**MathBox、LOOPY、Mafs 要特别留意较久的主分支间隔**；“仍能访问”不等于“已验证兼容当前浏览器和依赖”。Quarto 的 GitHub 自动许可证识别返回 `NOASSERTION`，但仓库 [COPYING.md][quarto-license] 明确是 MIT，不能据此写成“无许可证”；其集成的第三方组件另有各自许可证。

## 1. Manim Community：把数学变化按步骤讲清楚

入口：[GitHub](https://github.com/ManimCommunity/manim) · [文档](https://docs.manim.community/) · [示例画廊](https://docs.manim.community/en/stable/examples.html)。

**功能与输入输出。**用 Python 描述 `Scene`、图形、公式、坐标系和动画，渲染成视频或图片。典型输入是“一个矩阵、原始向量、变换顺序和讲述节奏”；输出是向量、坐标网格和公式同步变化的动画。它能把“结果是什么”扩展成“每一步怎样变到结果”，适合线性代数、微积分、几何和算法解释。[项目定位与版本说明][ce-about]

**源码确认。**`Scene.play_internal` 按时间推进，每一步更新状态并交给 renderer；`Transform` 对齐起止图形的数据后按 `alpha` 插值。这意味着运动是程序规定的可复现过程。`ValueTracker` 可作为参数，由 updater 驱动指针和标签一起变化，适合把“变量 → 几何结果”显式连接。[播放循环][ce-scene]、[形态插值][ce-transform]、[参数联动示例][ce-tracker]

**适用、限制与成本。**适合需要反复播放的教学片段。默认视频产物里的学习者主要观看；“动画能播放”并不自动等于“学习者能随意调参”。脚本、公式和教学顺序要作者设计，渲染和排版也有成本。快照依赖为 Python ≥3.11，包含 PyAV、ManimPango、Cairo、ModernGL 等；使用 TeX 的场景还要按安装文档准备相应工具。[依赖声明][ce-deps]

**验证与许可证。**审阅了 `ValueTracker` 的插值测试，明确检查 `1.0 → 2.5` 在 `alpha=0.7` 时得到 `2.05`，本次未运行。[测试][ce-test]；MIT，保留项目两份版权声明。[许可证说明][ce-license]

## 2. 3b1b/manim（ManimGL）：理解 3Blue1Brown 的原始动画工作方式

入口：[GitHub](https://github.com/3b1b/manim) · [文档](https://3b1b.github.io/manim/) · [官方 example_scenes.py][gl-example]。

**功能与价值。**这是 Grant Sanderson 的原始 Manim 路线，当前包名是 `manimgl`，代码常用 `from manimlib import *`；社区版包名是 `manim`。两者来源相关，但安装、API 和示例不应混用。它适合研究 3Blue1Brown 风格的对象变换、公式匹配、持续更新和 OpenGL 预览。[官方区分与环境要求][gl-about]

**源码确认与输入输出。**Python 场景输入 → 预览窗口或渲染文件。`draw_frame` 让 camera 捕获场景对象，`update_mobjects` 将时间增量和帧率传到对象；示例中正方形宽度变化时，括号位置和数字通过 updater 跟着变化。这比只读“支持动态数学”更具体：几何量和文本确实能由同一个状态驱动。[渲染与更新][gl-core]、[联动示例][gl-example]

**适用、限制与成本。**优先用于研究作者工作流或复现兼容版本的场景；新建通用 AutoDigest 动画模版，社区版通常更方便建立统一规范。这是选型判断，不是两个版本的性能比较。系统涉及 Python、FFmpeg、OpenGL，TeX 需求按场景决定；旧视频代码可能依赖旧 API。仓库本次 HEAD 与最新正式 Release 的日期差距较大，应固定目标版本。[环境说明][gl-about]

**验证与许可证。**读了坐标系与曲线上取点的单元测试，未运行。[测试][gl-test]；引擎为 MIT。[许可证][gl-license] 这不代表外部视频、课程或所有场景素材也自动获得相同授权。

## 3. Motion Canvas：适合算法流程与旁白同步的动画

入口：[GitHub](https://github.com/motion-canvas/motion-canvas) · [官网/文档](https://motion-canvas.io/) · [入门示例源码][mc-example]。

**功能与输入输出。**TypeScript generator 动画库，加一个实时预览编辑器。输入 TS/TSX 场景、图形属性、时间安排及可选音频；输出可播放/导出的说明动画。对“指针怎么移动、数据怎么经过几个阶段、哪一步该高亮”这类算法知识特别合适。官方将旁白同步作为主要目标之一。[项目说明][mc-about]

**源码确认。**`all()` 把多个 generator 任务交给调度器并等待全部结束；`SignalContext.tweener()` 根据起止属性、时间函数和插值函数持续更新属性。入门场景同时修改圆的位置和填充色，能直接看出代码的时间编排方式。[并行任务][mc-all]、[插值更新][mc-signal]、[示例][mc-example]

**适用、限制与成本。**如果 AutoDigest 要生成“算法讲解短片”，比自行实现 Canvas 时间轴更合适。编辑器中的交互主要服务动画作者，不能把它等同于学习者调参实验。需要 TypeScript/前端工具链，以及对节奏、布局、旁白的设计；普通概念图无需承担这样的成本。

**验证与许可证。**审阅的测试用 24 FPS 和 60 FPS 验证相同等待时长，针对时间语义而不是只检查函数存在，本次未运行。[测试][mc-test]；MIT。[许可证][mc-license]

## 4. Mafs：最接近“拖一下就看懂”的二维数学教具

入口：[GitHub](https://github.com/stevenpetryk/mafs) · [文档和交互示例](https://mafs.dev/) · [可移动点指南](https://mafs.dev/guides/interaction/movable-points)。

**功能与输入输出。**提供 React 数学组件：坐标系、函数曲线、向量、几何图形、变换和可移动点。输入 React 组件、数学函数与约束；输出网页中的可操作图形。拖动半径点，圆同步变化；拖动向量端点，投影关系同步变化——这是它帮助理解的主要机制。

**源码确认。**`useMovablePoint` 把点存进 React state，将水平/垂直/自定义约束变成函数，再通过 `onMove={setPoint}` 接回状态。官方 `MovableCircle` 用点的模长作为圆半径，确实形成“操作 → 参数变化 → 几何重绘”的闭环。[核心实现][mafs-core]、[圆半径示例][mafs-example]

**适用、限制与成本。**优先用于 AutoDigest 中二维几何、函数、线性代数的互动解释。需要 React ≥18 和前端打包环境，依赖手势库和 KaTeX；不是完整课程平台，也不是任意方程自动求解器。主分支快照停在 2025-03，应对当前 React/构建环境做实际验证后再选作长期基础。[依赖声明][mafs-deps]

**验证与许可证。**审阅了曲线采样的单元测试；项目另声明对文档示例做浏览器截图回归，本次没有运行这些检查。[采样测试][mafs-test]；MIT。[许可证][mafs-license]

## 5. MathBox：3D 数学结构的浏览器演示层

入口：[GitHub](https://github.com/unconed/mathbox) · [演示站](https://mathbox.org/) · [四元数示例](https://mathbox.org/math/quat.html)。

**功能与输入输出。**在 Three.js、ShaderGraph 和 WebGL 之上构建数学图形场景，支持坐标空间、数据采样、线、面、向量与动画。输入数学表达式回调、采样域和场景声明；输出可旋转/播放的浏览器数学图。空间结构、参数曲面、坐标映射等是它的强项。[说明与官方示例入口][mathbox-about]

**源码确认。**`Interval` 把样本索引映射到坐标区间，再将坐标和可选时间参数交给用户回调。四元数示例真实执行 `Quaternion.multiply` 并 `emit` 四个分量，而非仅播放预录视频。[采样机制][mathbox-core]、[四元数示例源码][mathbox-example]

**适用、限制与成本。**适合已经知道数学关系、希望构建精细 3D 直觉演示的作者。它负责可视化与数据流，不会替你验证方程或推导。主分支最后提交为 2023-01；`three` 声明了宽松 peer dependency，而开发依赖基线较旧，不能据此认定已兼容任何新版本 Three.js。接入前需要浏览器/GPU 和依赖兼容性试验，因此不是 AutoDigest 首个默认渲染器。[依赖基线][mathbox-deps]

**验证与许可证。**读了数组宽度变化触发 buffer 重建的测试，未运行。[测试][mathbox-test]；MIT。[许可证][mathbox-license]

## 6. Observable Plot：让数据里的规律更容易被发现

入口：[GitHub](https://github.com/observablehq/plot) · [文档](https://observablehq.com/plot/) · [画廊](https://observablehq.com/@observablehq/plot-gallery)。

**功能与输入输出。**对表格数据使用 marks、scales、分组和分箱等语法，生成 SVG/带图例的图形，并提供指针提示等交互。输入是数据及字段映射，不是自然语言知识；输出是分布、趋势、散点关系、分面等统计视图。适合让读者检查“这个判断在数据里有什么证据”。

**源码确认。**`plot()` 初始化 mark 和 channel，推导 scale 与尺寸，创建 SVG 后逐个调用 mark 的 render。分箱示例把连续体重转成各区间计数；pointer 实现计算最近数据点，并分派所选值，可供其他视图联动。[数据到 SVG][plot-core]、[mark 渲染][plot-render]、[分箱示例][plot-example]、[交互实现][plot-pointer]

**适用、限制与成本。**做一张解释性统计图通常比直接写 D3 更省代码。对于“梯度下降为什么更新”“反馈环如何形成”这类过程机制，还需要自行计算模型并设计控件、解释和实验。相关图形能揭示关联，不自动建立因果关系。网页端需要 JavaScript；静态图输出与完整互动网页应区分。

**验证与许可证。**读了分箱输出选项测试，未运行。[测试][plot-test]；ISC。[许可证][plot-license]

## 7. Observable Framework：把可操作解释组织成一整篇文章

入口：[GitHub](https://github.com/observablehq/framework) · [文档](https://observablehq.com/framework/) · [官方项目示例](https://github.com/observablehq/framework/tree/main/examples)。

**功能与输入输出。**静态站点生成器，将 Markdown、JavaScript、控件与可视化组合成数据应用/报告。输入 Markdown 页、JS 单元及可选 data loader；输出可托管的交互网站。它适合 AutoDigest 的“正文解释 + 一个参数 + 几张联动图 + 小实验”整篇呈现。

**源码确认。**编译器从单元的引用/声明提取 `inputs`、`outputs`，生成 `define(...)`；客户端注册到 Observable Runtime，`view` 将控件值接成 generator，依赖这些值的单元因而可以重算。这是跨代码块的真实数据流，不仅是把脚本塞进 Markdown。[编译器][framework-compile]、[运行时接线][framework-runtime]、[反应式示例][framework-example]

**适用、限制与成本。**适合已有 JavaScript 能力、希望把交互解释长期发布为网站的人。需要区分：**前端 JS 可以在浏览器交互时重算；Python/R 等 data loader 主要在构建时产出静态数据快照**，不会因为读者拖动滑条自动在服务器重新执行。若想要实时 Python 计算，要另建服务或采用 marimo 一类运行方式。[data loader 机制][framework-loaders]

**验证与许可证。**审阅转译器 snapshot 测试和变量依赖输出断言，未运行。[测试][framework-test]；ISC。[许可证][framework-license] 开源 Framework 与 Observable 的商业托管服务不是同一个收费对象。

## 8. marimo：用可重复计算的小实验消化知识

入口：[GitHub](https://github.com/marimo-team/marimo) · [文档](https://docs.marimo.io/) · [示例](https://docs.marimo.io/examples/) · [画廊](https://marimo.io/gallery/)。

**功能与输入输出。**反应式 Python notebook；代码以 `.py` 保存，可作为脚本执行或提供应用界面。输入 Python 计算、Markdown 解释、slider 等 UI；输出中间值、图和可重新运行的学习实验。特别适合把“我觉得这个参数应该这样影响结果”变成可以亲手验证的预测。

**源码确认。**注册 cell 时根据定义和引用连接父子依赖并检测环；执行顺序使用拓扑排序。官方 slider 示例在一个 cell 创建控件，在下游 cell 读取 `slider.value`。这为“参数变了，相关计算和显示跟着变”提供了明确实现基础。[依赖图][marimo-graph]、[拓扑排序][marimo-order]、[slider 示例][marimo-example]

**适用、限制与成本。**在 AutoDigest 中适合 Attention、概率、优化、数值方法等有可执行公式的主题。需要 Python 与相应数值库；自动重算会放大昂贵计算成本，应规划缓存或 lazy 模式。WebAssembly 模式可免后端，但官方明确不是所有 notebook/包都兼容，重计算任务仍适合本机/服务器。反应式执行帮助保持依赖关系一致，不能保证公式、数据和随机过程本身正确。[运行依赖][marimo-deps]、[WASM 范围][marimo-wasm]

**验证与许可证。**读了菱形依赖图的拓扑顺序测试，即便输入单元顺序倒置也期望相同依赖顺序，未运行。[测试][marimo-test]；Apache-2.0。[许可证][marimo-license]

## 9. LOOPY：把反馈关系变成可以“推一下”的模型

入口：[GitHub](https://github.com/ncase/loopy) · [直接使用](https://ncase.me/loopy/) · [用户示例](https://ncase.me/loopy/v1.1/pages/examples/)。规范仓库是 `ncase/loopy`，默认分支是 `gh-pages`，本次主要审阅 `v1.1`。

**功能与输入输出。**浏览器里画节点和箭头，设置正向/反向关系，然后点击节点注入增减信号。输入是你对系统的定性结构假设；输出是可运行、可分享、可嵌入的循环关系模型。适合讨论“越焦虑越拖延”“强化回路与平衡回路”等关系怎样相互影响。

**源码确认。**节点收到信号后直接 `value += signal.delta`，再向出边传播；边把信号沿路径移动，到端点时乘上边的 strength，再传给下一节点。模型能序列化为节点、边和标签数组，分享链接把这些数据带在 URL 中。[节点更新][loopy-node]、[传播规则][loopy-edge]、[序列化][loopy-serialize]、[链接分享][loopy-share]

**适用、限制与成本。**适合初步系统思考，浏览器界面门槛低。它不是经过校准的定量系统动力学求解器：传播按图形路径运行，并且有信号总数/单边信号上限；节点数字不应直接解释成真实时间、真实单位或预测结果。“画了因果箭头”仍只是作者假设。主分支代码时间为 2019-04；可作为小型思想实验工具，长期集成前要做运行验证。

**验证与许可证。**本次目录检查未发现专门自动化测试套件；依据实现、示例和说明交叉核对，没有宣称已运行。项目为 CC0-1.0，README 另列使用的第三方代码，重分发时应分别检查。[许可证][loopy-license]、[第三方与版本说明][loopy-deps]

## 10. Quarto：把理解过程沉淀为带代码、图和引用的知识文档

入口：[GitHub](https://github.com/quarto-dev/quarto-cli) · [官网/文档](https://quarto.org/) · [Observable JS 交互文档](https://quarto.org/docs/interactive/ojs/)。

**功能与输入输出。**以 Pandoc 为基础，组织 Markdown、交叉引用、图表和可执行代码，连接 Jupyter、Knitr、Observable 等。输入 `.qmd`、notebook、代码和素材；输出 HTML 网站/书籍，以及依目标配置生成 PDF、Word 等文档。它帮助“保存并复查自己怎么得出结论”，尤其适合多篇主题长期累积。[项目能力说明][quarto-about]

**源码确认。**渲染流程先调用执行引擎，得到计算结果；OJS 编译器再检查目标格式是否支持 JavaScript，处理交互单元。测试样本用 `viewof name` 输入框驱动下游 Markdown 问候语，证明交互来自 OJS 的依赖关系。[执行步骤][quarto-execute]、[OJS 格式门槛][quarto-ojs]、[交互样本][quarto-example]

**适用、限制与成本。**适合作为 AutoDigest 输出与出版层，而不是首个画图引擎。HTML 可以容纳交互，不能假设同一交互在 PDF/Word 输出中原样运行。Python/R 计算通常在渲染时执行；需要随浏览器操作重算的内容应明确采用 OJS 或另外的服务。CLI、语言内核和不同输出格式的工具链会增加环境管理成本。

**验证与许可证。**审阅 Playwright 对 OJS 执行和跨文档定义导入的检查，未运行。[测试][quarto-test]；CLI 自身 MIT，实际许可证文件是 `COPYING.md`。[许可证][quarto-license]

## 11. D3：高度定制知识可视化的基础层

入口：[GitHub](https://github.com/d3/d3) · [文档](https://d3js.org/) · [画廊](https://observablehq.com/@d3/gallery)。

**功能与输入输出。**围绕 Web 标准提供数据绑定、比例尺、形状、布局、拖拽、刷选、缩放和动画等模块。输入数据、DOM/SVG/Canvas 绘制逻辑与交互代码；输出定制图形或互动解释。常见教学用法是让数据与图形保持对应，例如排序过程中移动条形，或在树结构里逐步展开搜索。

**源码确认。**`d3/d3` 本身主要是 30 个模块的聚合出口，不能把读了这个入口称为读完底层算法。因此本次额外审阅了依赖仓库 `d3/d3-selection`：`data.js` 按 key 把数据与节点匹配到 enter/update/exit；`join.js` 创建新节点、更新已有节点、删除退出节点，并恢复数据顺序。[聚合入口][d3-exports]、[按 key 绑定][d3-data]、[join 实现][d3-join]

**适用、限制与成本。**适合 Plot/Vega-Lite 无法表达的独特交互；自由度来自你自行设计数据、状态、布局和叙事，因此工程成本较高。只想完成常规统计图时，先看 Plot 或 Vega-Lite。库不负责解释知识是否正确，图中的动态变化也需要对应真实的算法状态。官方入门示例明确展示了自行建比例尺、SVG 与坐标轴的工作量。[示例][d3-example]

**验证与许可证。**额外审阅了 `join` 的添加、删除、按 key 更新与重排测试，未运行。[测试][d3-test]；D3 为 ISC。[许可证][d3-license] 附加子仓库固定 SHA 在对应源码链接中，未将其另算一款推荐工具。

## 12. Vega-Lite：用结构化规格生成交互统计图

入口：[GitHub](https://github.com/vega/vega-lite) · [文档](https://vega.github.io/vega-lite/docs/) · [示例](https://vega.github.io/vega-lite/examples/) · [在线编辑器](https://vega.github.io/editor/#/examples/vega-lite/bar)。

**功能与输入输出。**用 JSON 描述 data、mark、encoding、transform 和交互参数，再编译成 Vega 规格。输入结构化图表规范和数据；输出可交互的统计视图，由 Vega 运行时渲染。很适合 Agent 生成可审阅的图形规格，也适合通过刷选、过滤和分面帮助读者探索数据。

**源码确认。**编译器经过配置合并、规范化、模型树构建、组件解析、数据流优化，最后组装 Vega spec。interval selection 的编译器生成交互信号；官方散点例子用 `params: brush` 和颜色条件突出矩形框选范围内的点。[主编译管线][vl-core]、[刷选信号][vl-select]、[完整 JSON 示例][vl-example]

**适用、限制与成本。**比从 D3 的 DOM 操作开始更适合常规数据分析，也利于版本控制。它的语法主要针对统计图，不负责任意数学场景、故事节奏或高精度物理仿真；复杂交互可能需要 Vega 或自行写代码。此快照 peer dependency 是 Vega `^6.4.0`，工具链声明 Node ≥22，必须把 Vega-Lite 和 Vega 的版本配对。[依赖声明][vl-deps]

**验证与许可证。**审阅 interval selection 对坐标编码、事件流、初始区间与 scale 绑定的测试定义，未运行。[测试][vl-test]；BSD-3-Clause。[许可证][vl-license]

## 给 AutoDigest 的落地建议

优先准备三种能力，而不是把十二个工具全部安装：

1. **可操纵解释：Mafs 或 marimo。**前者适合二维几何/函数，后者适合 Python 数值计算。一个主题先做一个可控变量，并显示中间量，要求读者先预测再操作。
2. **按步骤讲述：Manim Community 或 Motion Canvas。**根据团队的 Python/TypeScript 能力二选一。动画中持续保留对象身份、公式含义和当前步骤；讲解完成后补一个可修改参数的小实验。
3. **组织与发布：Observable Framework 或 Quarto。**前者偏互动网页与响应式 JS；后者偏带引用和代码的长文、书籍及多格式输出。Plot/Vega-Lite 作为其中的数据图层，D3 留给确有需要的定制场景。

以 `Transformer Attention` 为例，建议的最小产物是：用 marimo 或浏览器计算实现小规模 `QKᵀ → scale → softmax → weighted sum`；允许修改一个 query 分量或 temperature，同时展示 logits、权重和最终向量；再用 Manim/Motion Canvas 说明运算顺序。这里的 temperature 应明确区分于标准缩放因子 `√dₖ`。这是基于工具能力提出的后续实现方案，本次未开发或验证该演示。

LOOPY 可辅助讲反馈回路，但不应代替 Attention 的数值计算。MathBox 值得作为 3D 数学案例与设计灵感库；考虑维护间隔，先做小样再决定是否纳入长期依赖。

## 复查方式

本篇所有实现和测试引文都固定到下载时的 commit，下载快照与集中元数据 SHA 已逐项核对一致。若要重新评估工具，应先阅读各项目当前安装说明，再在隔离环境中执行选定示例与有意义的行为检查。优先验证“修改输入是否改变正确的中间量与输出”，而不仅是截图是否好看。本次没有把第三方仓库的 Agent/skill 指令当成本地执行授权。

[ce-about]: https://github.com/ManimCommunity/manim/blob/622520d34190062f32d68af066c80f1c937fc8bf/README.md#L20-L38
[ce-scene]: https://github.com/ManimCommunity/manim/blob/622520d34190062f32d68af066c80f1c937fc8bf/manim/scene/scene.py#L1384-L1417
[ce-tracker]: https://github.com/ManimCommunity/manim/blob/622520d34190062f32d68af066c80f1c937fc8bf/manim/mobject/value_tracker.py#L21-L63
[ce-transform]: https://github.com/ManimCommunity/manim/blob/622520d34190062f32d68af066c80f1c937fc8bf/manim/animation/transform.py#L200-L250
[ce-test]: https://github.com/ManimCommunity/manim/blob/622520d34190062f32d68af066c80f1c937fc8bf/tests/module/mobject/test_value_tracker.py#L19-L24
[ce-deps]: https://github.com/ManimCommunity/manim/blob/622520d34190062f32d68af066c80f1c937fc8bf/pyproject.toml#L23-L51
[ce-license]: https://github.com/ManimCommunity/manim/blob/622520d34190062f32d68af066c80f1c937fc8bf/README.md#L138-L140
[gl-about]: https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/README.md#L13-L27
[gl-core]: https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/manimlib/scene/scene.py#L241-L272
[gl-example]: https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/example_scenes.py#L281-L338
[gl-test]: https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/tests/test_coordinate_systems.py#L28-L48
[gl-license]: https://github.com/3b1b/manim/blob/fafa083a4fb274bba9cabde0b6e2f50ba6da0622/LICENSE.md#L1-L21
[mc-about]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/README.md#L18-L29
[mc-all]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/src/flow/all.ts#L5-L25
[mc-signal]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/src/signals/SignalContext.ts#L263-L279
[mc-example]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/examples/src/scenes/quickstart.tsx#L1-L22
[mc-test]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/packages/core/src/flow/scheduling.test.ts#L16-L43
[mc-license]: https://github.com/motion-canvas/motion-canvas/blob/7b91435c301d530351dcf5ebb91dd139c002e405/LICENSE#L1-L21
[mafs-core]: https://github.com/stevenpetryk/mafs/blob/e74a3ef465f4ddc98704814d2ae18b73a6cd9dae/src/interaction/useMovablePoint.tsx#L6-L58
[mafs-example]: https://github.com/stevenpetryk/mafs/blob/e74a3ef465f4ddc98704814d2ae18b73a6cd9dae/docs/components/guide-examples/MovableCircle.tsx#L11-L25
[mafs-test]: https://github.com/stevenpetryk/mafs/blob/e74a3ef465f4ddc98704814d2ae18b73a6cd9dae/src/display/Plot/PlotUtils.test.ts#L1-L24
[mafs-deps]: https://github.com/stevenpetryk/mafs/blob/e74a3ef465f4ddc98704814d2ae18b73a6cd9dae/package.json#L80-L89
[mafs-license]: https://github.com/stevenpetryk/mafs/blob/e74a3ef465f4ddc98704814d2ae18b73a6cd9dae/LICENSE#L1-L7
[mathbox-about]: https://github.com/unconed/mathbox/blob/f80933e114ed8051c8182fe09b83837696b4f0e9/README.md#L11-L34
[mathbox-core]: https://github.com/unconed/mathbox/blob/f80933e114ed8051c8182fe09b83837696b4f0e9/src/primitives/types/data/interval.js#L29-L72
[mathbox-example]: https://github.com/unconed/mathbox/blob/f80933e114ed8051c8182fe09b83837696b4f0e9/examples/math/quat.html#L105-L140
[mathbox-test]: https://github.com/unconed/mathbox/blob/f80933e114ed8051c8182fe09b83837696b4f0e9/test/primitives/types/data/array.spec.ts#L1-L26
[mathbox-deps]: https://github.com/unconed/mathbox/blob/f80933e114ed8051c8182fe09b83837696b4f0e9/package.json#L42-L49
[mathbox-license]: https://github.com/unconed/mathbox/blob/f80933e114ed8051c8182fe09b83837696b4f0e9/LICENSE.md#L1-L18
[plot-core]: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/src/plot.js#L126-L161
[plot-render]: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/src/plot.js#L282-L294
[plot-pointer]: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/src/interactions/pointer.js#L125-L183
[plot-example]: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/docs/transforms/bin.md#L17-L39
[plot-test]: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/test/transforms/bin-test.js#L1-L36
[plot-license]: https://github.com/observablehq/plot/blob/535723d5e433727720d9b673c31622821bb03210/LICENSE#L1-L13
[framework-compile]: https://github.com/observablehq/framework/blob/85e843e6acfa3dbe93129c125156352c9c50b697/src/javascript/transpile.ts#L31-L54
[framework-runtime]: https://github.com/observablehq/framework/blob/85e843e6acfa3dbe93129c125156352c9c50b697/src/client/main.js#L25-L65
[framework-loaders]: https://github.com/observablehq/framework/blob/85e843e6acfa3dbe93129c125156352c9c50b697/docs/data-loaders.md#L5-L25
[framework-example]: https://github.com/observablehq/framework/blob/85e843e6acfa3dbe93129c125156352c9c50b697/docs/reactivity.md#L5-L45
[framework-test]: https://github.com/observablehq/framework/blob/85e843e6acfa3dbe93129c125156352c9c50b697/test/javascript/transpile-test.ts#L30-L95
[framework-license]: https://github.com/observablehq/framework/blob/85e843e6acfa3dbe93129c125156352c9c50b697/LICENSE#L1-L13
[marimo-graph]: https://github.com/marimo-team/marimo/blob/58be5a93f384dc0fa6e130f98c8688999df74305/marimo/_runtime/dataflow/graph.py#L92-L128
[marimo-order]: https://github.com/marimo-team/marimo/blob/58be5a93f384dc0fa6e130f98c8688999df74305/marimo/_runtime/dataflow/__init__.py#L132-L167
[marimo-example]: https://github.com/marimo-team/marimo/blob/58be5a93f384dc0fa6e130f98c8688999df74305/examples/ui/slider.py#L1-L28
[marimo-test]: https://github.com/marimo-team/marimo/blob/58be5a93f384dc0fa6e130f98c8688999df74305/tests/_runtime/test_dataflow.py#L456-L478
[marimo-wasm]: https://github.com/marimo-team/marimo/blob/58be5a93f384dc0fa6e130f98c8688999df74305/docs/guides/wasm.md#L5-L35
[marimo-deps]: https://github.com/marimo-team/marimo/blob/58be5a93f384dc0fa6e130f98c8688999df74305/pyproject.toml#L12-L63
[marimo-license]: https://github.com/marimo-team/marimo/blob/58be5a93f384dc0fa6e130f98c8688999df74305/LICENSE#L1-L4
[loopy-node]: https://github.com/ncase/loopy/blob/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9/v1.1/js/Node.js#L106-L129
[loopy-edge]: https://github.com/ncase/loopy/blob/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9/v1.1/js/Edge.js#L36-L119
[loopy-share]: https://github.com/ncase/loopy/blob/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9/v1.1/js/Loopy.js#L175-L200
[loopy-serialize]: https://github.com/ncase/loopy/blob/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9/v1.1/js/Model.js#L249-L322
[loopy-license]: https://github.com/ncase/loopy/blob/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9/LICENSE.txt#L1-L17
[loopy-deps]: https://github.com/ncase/loopy/blob/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9/README.md#L11-L24
[quarto-about]: https://github.com/quarto-dev/quarto-cli/blob/b86f98d382940bef6c65f37ea0bdfba844f19b6d/README.md#L10-L24
[quarto-execute]: https://github.com/quarto-dev/quarto-cli/blob/b86f98d382940bef6c65f37ea0bdfba844f19b6d/src/command/render/render-files.ts#L220-L239
[quarto-ojs]: https://github.com/quarto-dev/quarto-cli/blob/b86f98d382940bef6c65f37ea0bdfba844f19b6d/src/execute/ojs/compile.ts#L123-L154
[quarto-example]: https://github.com/quarto-dev/quarto-cli/blob/b86f98d382940bef6c65f37ea0bdfba844f19b6d/tests/docs/ojs/test-ojs.qmd#L1-L21
[quarto-test]: https://github.com/quarto-dev/quarto-cli/blob/b86f98d382940bef6c65f37ea0bdfba844f19b6d/tests/integration/playwright/tests/ojs-define.spec.ts#L1-L23
[quarto-license]: https://github.com/quarto-dev/quarto-cli/blob/b86f98d382940bef6c65f37ea0bdfba844f19b6d/COPYING.md#L1-L21
[d3-exports]: https://github.com/d3/d3/blob/ca958d45217b4c15332d971b935451a6d4c978f4/src/index.js#L1-L30
[d3-join]: https://github.com/d3/d3-selection/blob/d8ea8005f87ca72496d748a91ab6e0ccbe1a2011/src/selection/join.js#L1-L15
[d3-data]: https://github.com/d3/d3-selection/blob/d8ea8005f87ca72496d748a91ab6e0ccbe1a2011/src/selection/data.js#L31-L72
[d3-test]: https://github.com/d3/d3-selection/blob/d8ea8005f87ca72496d748a91ab6e0ccbe1a2011/test/selection/join-test.js#L5-L35
[d3-example]: https://github.com/d3/d3/blob/ca958d45217b4c15332d971b935451a6d4c978f4/docs/getting-started.md#L30-L65
[d3-license]: https://github.com/d3/d3/blob/ca958d45217b4c15332d971b935451a6d4c978f4/LICENSE#L1-L13
[vl-core]: https://github.com/vega/vega-lite/blob/85fab8d12c873b3b224ef9a33c807642953325ba/src/compile/compile.ts#L72-L132
[vl-select]: https://github.com/vega/vega-lite/blob/85fab8d12c873b3b224ef9a33c807642953325ba/src/compile/selection/interval.ts#L26-L98
[vl-example]: https://github.com/vega/vega-lite/blob/85fab8d12c873b3b224ef9a33c807642953325ba/examples/specs/interactive_brush.vl.json#L1-L19
[vl-test]: https://github.com/vega/vega-lite/blob/85fab8d12c873b3b224ef9a33c807642953325ba/test/compile/selection/interval.test.ts#L7-L52
[vl-deps]: https://github.com/vega/vega-lite/blob/85fab8d12c873b3b224ef9a33c807642953325ba/package.json#L135-L149
[vl-license]: https://github.com/vega/vega-lite/blob/85fab8d12c873b3b224ef9a33c807642953325ba/LICENSE#L1-L27
