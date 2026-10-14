# 调研下载源码

此目录保存本次调研下载的 **41 份源码**：报告中的 40 个主仓库，以及核对 D3 数据绑定实现时使用的 `d3/d3-selection`。每份源码位于 `<owner>/<repo>/`，作为 Git 子模块固定到报告审阅的 commit，不跟随上游默认分支自动更新。

AutoDigest 的目录分工为：

```text
autodigest/
├── .gitmodules             # Git 子模块地址与路径配置
├── tool/                   # 原有 AutoDigest 全部内容
└── Research/
    ├── README.md           # 调研汇总
    ├── notes/              # 分组源码分析
    ├── evidence/           # 元数据、引用与迁移核验记录
    ├── scripts/            # 元数据采集与源码核验
    └── repos/              # 本次下载的源码
        ├── humanlayer/skills/
        ├── Ofori01/show-me/
        └── ...
```

## 取得源码

父仓提交的是每个上游仓库的固定 Git 引用，源码文件来自对应上游仓库。GitHub 网页可点击子模块跳到固定版本；普通 clone 或 GitHub 的 ZIP 下载不会包含这些子模块的源码文件。

已有 AutoDigest 克隆时，在仓库根目录执行：

```bash
git submodule update --init --depth 1 --jobs 4
```

只想看 ShowMe，可先获取一个仓库：

```bash
git submodule update --init --depth 1 -- Research/repos/humanlayer/skills
```

首次克隆并取得全部 41 个直接子模块：

```bash
git clone https://github.com/TargetIt/autodigest.git
cd autodigest
git submodule update --init --depth 1 --jobs 4
```

这里不加 `--remote`，以免把调研版本换成上游最新版本；也不要求递归获取上游项目自身的子模块或安装运行依赖。需要运行某个项目时，再按该版本自身说明准备环境。

## 当前检出范围与核验

原先的 40 份下载由 Git 检出和源码归档组成，已移入本目录；新增的 Archify 直接下载到本目录。部分大型 Git 仓库沿用调研时的**稀疏检出**，本地只展开选定源码和文档；每份仓库仍固定到完整上游提交。归档转为 Git 仓库时，保留已有文件内容，补齐缺失路径并恢复原始执行位。逐仓状态见 [`source-checkouts.json`](../evidence/source-checkouts.json)。

子模块版本能够从上游重新获取；本次本地使用的稀疏配置属于检出设置，不会随父仓提交传播。新初始化的子模块默认展开完整受控文件。若要展开当前已有的稀疏检出，例如 D2：

```bash
git -C Research/repos/d2lang/d2 sparse-checkout disable
```

从 AutoDigest 仓库根目录执行以下命令，可核对 41 个子模块的版本、地址、干净状态，以及源码索引中全部引用的文件哈希和行号；此脚本不运行上游代码：

```bash
python3 Research/scripts/verify_source_checkouts.py
```

## 源码入口

下表的本地链接适用于已经初始化子模块的工作区；固定版本链接可直接在 GitHub 阅读。工具功能、Star 和选型结论见[调研汇总](../README.md)。

| 仓库 | 本地源码 | 固定版本 |
| --- | --- | --- |
| [3b1b/manim](https://github.com/3b1b/manim) | [打开目录](3b1b/manim/) | [fafa083a4fb2](https://github.com/3b1b/manim/tree/fafa083a4fb274bba9cabde0b6e2f50ba6da0622) |
| [antvis/Infographic](https://github.com/antvis/Infographic) | [打开目录](antvis/Infographic/) | [2ea1894255e4](https://github.com/antvis/Infographic/tree/2ea1894255e4002c7735586778be86d13ec30346) |
| [apache/echarts](https://github.com/apache/echarts) | [打开目录](apache/echarts/) | [34f4d927eafe](https://github.com/apache/echarts/tree/34f4d927eafe251f26f63afd3aeefa30f2feba30) |
| [bentossell/visualise](https://github.com/bentossell/visualise) | [打开目录](bentossell/visualise/) | [35cd185b58af](https://github.com/bentossell/visualise/tree/35cd185b58af5db2f9d0fe13d9872b544a467483) |
| [coleam00/excalidraw-diagram-skill](https://github.com/coleam00/excalidraw-diagram-skill) | [打开目录](coleam00/excalidraw-diagram-skill/) | [8646fcc9f74f](https://github.com/coleam00/excalidraw-diagram-skill/tree/8646fcc9f74f38539c6cdb4c969723336a96ddcd) |
| [d2lang/d2](https://github.com/d2lang/d2) | [打开目录](d2lang/d2/) | [6a7b4837838a](https://github.com/d2lang/d2/tree/6a7b4837838a3907604a1d9eec57ee98b6f3cd01) |
| [d3/d3](https://github.com/d3/d3) | [打开目录](d3/d3/) | [ca958d45217b](https://github.com/d3/d3/tree/ca958d45217b4c15332d971b935451a6d4c978f4) |
| [d3/d3-selection（D3 支撑依赖）](https://github.com/d3/d3-selection) | [打开目录](d3/d3-selection/) | [d8ea8005f87c](https://github.com/d3/d3-selection/tree/d8ea8005f87ca72496d748a91ab6e0ccbe1a2011) |
| [DayuanJiang/next-ai-draw-io](https://github.com/DayuanJiang/next-ai-draw-io) | [打开目录](DayuanJiang/next-ai-draw-io/) | [623eb91e5794](https://github.com/DayuanJiang/next-ai-draw-io/tree/623eb91e579465dabe2794da5aac2dfaceba0f71) |
| [ericblue/visual-explainer-skill](https://github.com/ericblue/visual-explainer-skill) | [打开目录](ericblue/visual-explainer-skill/) | [811b823653f0](https://github.com/ericblue/visual-explainer-skill/tree/811b823653f0d1d9b1d2bc6f7c13df952f0216e7) |
| [excalidraw/cli](https://github.com/excalidraw/cli) | [打开目录](excalidraw/cli/) | [55fe7f494837](https://github.com/excalidraw/cli/tree/55fe7f494837078781a062c4d3faf29c159ebec5) |
| [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw) | [打开目录](excalidraw/excalidraw/) | [4c37956ba5f0](https://github.com/excalidraw/excalidraw/tree/4c37956ba5f04ec342a9d9d5891a38f22c5b7b4e) |
| [excalidraw/excalidraw-mcp](https://github.com/excalidraw/excalidraw-mcp) | [打开目录](excalidraw/excalidraw-mcp/) | [157aa23ceb19](https://github.com/excalidraw/excalidraw-mcp/tree/157aa23ceb1976008aadc89eb05e3444060f09d6) |
| [humanlayer/skills](https://github.com/humanlayer/skills) | [打开目录](humanlayer/skills/) | [653b6411c1f7](https://github.com/humanlayer/skills/tree/653b6411c1f70c275a18e37673b042ff99f67ceb) |
| [jgraph/drawio](https://github.com/jgraph/drawio) | [打开目录](jgraph/drawio/) | [9034053fba80](https://github.com/jgraph/drawio/tree/9034053fba80a435e27d68d374bc564b83917ae9) |
| [jgraph/drawio-mcp](https://github.com/jgraph/drawio-mcp) | [打开目录](jgraph/drawio-mcp/) | [3398377f740d](https://github.com/jgraph/drawio-mcp/tree/3398377f740d47faa0245b107b886e856fa3930f) |
| [konraddzbik/architecture-diagram-skill](https://github.com/konraddzbik/architecture-diagram-skill) | [打开目录](konraddzbik/architecture-diagram-skill/) | [cd94e972682d](https://github.com/konraddzbik/architecture-diagram-skill/tree/cd94e972682dfacd7c741f9096cacc90d5cc5c41) |
| [ManimCommunity/manim](https://github.com/ManimCommunity/manim) | [打开目录](ManimCommunity/manim/) | [622520d34190](https://github.com/ManimCommunity/manim/tree/622520d34190062f32d68af066c80f1c937fc8bf) |
| [marimo-team/marimo](https://github.com/marimo-team/marimo) | [打开目录](marimo-team/marimo/) | [58be5a93f384](https://github.com/marimo-team/marimo/tree/58be5a93f384dc0fa6e130f98c8688999df74305) |
| [markmap/markmap](https://github.com/markmap/markmap) | [打开目录](markmap/markmap/) | [122bf0500ee7](https://github.com/markmap/markmap/tree/122bf0500ee7aca4f023c2465f7e26bf023eec52) |
| [mattpocock/skills](https://github.com/mattpocock/skills) | [打开目录](mattpocock/skills/) | [49dd158d1076](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336) |
| [mermaid-js/mermaid](https://github.com/mermaid-js/mermaid) | [打开目录](mermaid-js/mermaid/) | [e28fbd9ded0a](https://github.com/mermaid-js/mermaid/tree/e28fbd9ded0a07ba9569e51be4764c1ad4daa8f6) |
| [mingrammer/diagrams](https://github.com/mingrammer/diagrams) | [打开目录](mingrammer/diagrams/) | [9df75e65c03b](https://github.com/mingrammer/diagrams/tree/9df75e65c03bf9f3da8c0ddbacc33d4ecf5e31e8) |
| [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | [打开目录](motion-canvas/motion-canvas/) | [7b91435c301d](https://github.com/motion-canvas/motion-canvas/tree/7b91435c301d530351dcf5ebb91dd139c002e405) |
| [naorsabag/openhop](https://github.com/naorsabag/openhop) | [打开目录](naorsabag/openhop/) | [927015aebbee](https://github.com/naorsabag/openhop/tree/927015aebbeeb2559e6296946b57b2594c9a1d37) |
| [ncase/loopy](https://github.com/ncase/loopy) | [打开目录](ncase/loopy/) | [2d8e13f0a006](https://github.com/ncase/loopy/tree/2d8e13f0a006f4024f27ad1712d7f9c2c1ad7cd9) |
| [NickyLam/Visualizer-Skill](https://github.com/NickyLam/Visualizer-Skill) | [打开目录](NickyLam/Visualizer-Skill/) | [409cc699c56b](https://github.com/NickyLam/Visualizer-Skill/tree/409cc699c56bbdfc2b52a70509c24642585c0d5f) |
| [nicobailon/visual-explainer](https://github.com/nicobailon/visual-explainer) | [打开目录](nicobailon/visual-explainer/) | [33a6b4d43958](https://github.com/nicobailon/visual-explainer/tree/33a6b4d43958d2d152c9cb13762af802062fade5) |
| [observablehq/framework](https://github.com/observablehq/framework) | [打开目录](observablehq/framework/) | [85e843e6acfa](https://github.com/observablehq/framework/tree/85e843e6acfa3dbe93129c125156352c9c50b697) |
| [observablehq/plot](https://github.com/observablehq/plot) | [打开目录](observablehq/plot/) | [535723d5e433](https://github.com/observablehq/plot/tree/535723d5e433727720d9b673c31622821bb03210) |
| [Ofori01/show-me](https://github.com/Ofori01/show-me) | [打开目录](Ofori01/show-me/) | [62c8905665be](https://github.com/Ofori01/show-me/tree/62c8905665be8ff6f51df05eaccf6b38e1c183e1) |
| [plantuml/plantuml](https://github.com/plantuml/plantuml) | [打开目录](plantuml/plantuml/) | [8678962c537b](https://github.com/plantuml/plantuml/tree/8678962c537bfb854073fc15394ac0b5ed5ea83e) |
| [quarto-dev/quarto-cli](https://github.com/quarto-dev/quarto-cli) | [打开目录](quarto-dev/quarto-cli/) | [b86f98d38294](https://github.com/quarto-dev/quarto-cli/tree/b86f98d382940bef6c65f37ea0bdfba844f19b6d) |
| [stevenpetryk/mafs](https://github.com/stevenpetryk/mafs) | [打开目录](stevenpetryk/mafs/) | [e74a3ef465f4](https://github.com/stevenpetryk/mafs/tree/e74a3ef465f4ddc98704814d2ae18b73a6cd9dae) |
| [theolundqvist/justshowme](https://github.com/theolundqvist/justshowme) | [打开目录](theolundqvist/justshowme/) | [b7e20e8966d8](https://github.com/theolundqvist/justshowme/tree/b7e20e8966d852f95c470179ee0b23f5abbab936) |
| [tldraw/tldraw](https://github.com/tldraw/tldraw) | [打开目录](tldraw/tldraw/) | [694791e0aceb](https://github.com/tldraw/tldraw/tree/694791e0acebc0f9df4a16a5880b72d128f8a621) |
| [unconed/mathbox](https://github.com/unconed/mathbox) | [打开目录](unconed/mathbox/) | [f80933e114ed](https://github.com/unconed/mathbox/tree/f80933e114ed8051c8182fe09b83837696b4f0e9) |
| [vega/vega-lite](https://github.com/vega/vega-lite) | [打开目录](vega/vega-lite/) | [85fab8d12c87](https://github.com/vega/vega-lite/tree/85fab8d12c873b3b224ef9a33c807642953325ba) |
| [xyflow/xyflow](https://github.com/xyflow/xyflow) | [打开目录](xyflow/xyflow/) | [3d35b5731757](https://github.com/xyflow/xyflow/tree/3d35b57317576b0916c0bfeaaedd573aaacc2839) |
| [yuzutech/kroki](https://github.com/yuzutech/kroki) | [打开目录](yuzutech/kroki/) | [d161fd8e5735](https://github.com/yuzutech/kroki/tree/d161fd8e5735131f986da59f8f359c72f3fa770c) |
| [tt-a1i/archify](https://github.com/tt-a1i/archify) | [打开目录](tt-a1i/archify/) | [d0c8c7e9f4e0](https://github.com/tt-a1i/archify/tree/d0c8c7e9f4e06f303389f804208d387f27019ef5) |
