# Archify：有限本地行为验证

2026-10-15，固定审阅提交 [`d0c8c7e9f4e06f303389f804208d387f27019ef5`](https://github.com/tt-a1i/archify/tree/d0c8c7e9f4e06f303389f804208d387f27019ef5)，macOS arm64、已有 Node **v22.23.2**。这次确实运行了 CLI；没有安装依赖、skill、模型或浏览器，也没有运行上游完整测试套件。

HTML 示例包含上游生成器附带的 Viewer 代码；本目录保留该提交根目录 `LICENSE` 的逐字副本 [UPSTREAM_LICENSE.txt](UPSTREAM_LICENSE.txt)，用于来源和许可归档。生成 HTML 内也保留了 JetBrains Mono 的 OFL 通知。

HTML 保留生成器原始字节（含行尾空白），没有做格式化或清理，以保持与实测 SHA256 一致；文档和脚本的空白检查不适用于这一原始产物。

实测支持的结论：**这个官方 architecture 示例能够经 schema/布局检查生成 HTML；两种明确的错误输入会被拒绝；一次端点引用错误导致的 deliver 失败不会覆盖上一次成功 HTML，并且会把交付状态标为失败。** 这些结论限于本页列出的输入和路径。

| 检查 | 实际退出码 | 观察到的行为 |
| --- | ---: | --- |
| `validate architecture` 官方示例 | 0 | `ok: true`；包含渲染和静态 artifact checker |
| `render architecture` 官方示例 | 0 | 生成 [sample-web-app.html](sample-web-app.html)，823,705 字节 |
| `deliver architecture` 官方示例 | 0 | 静态检查 **9/9**，`compositionProfile: showcase`、`compositionStatus: pass`，0 errors、0 warnings |
| `validate` 非法组件类型 | 1 | `/components/0/type` 返回 `schema/enum` |
| `validate` 不存在的连接目标 | 1 | 返回 `architecture/unknown-endpoint` 及 `layout/constraint` |
| 将不存在目标的输入 `deliver` 到已有 HTML | 1 | `stage: render`；HTML SHA256 保持不变；provenance 变为 `failed` |
| 对保留的 HTML 执行 `check --require-provenance` | 1 | `delivery/provenance-failed`，不会把旧图冒充本次成功交付 |
| 重新 `deliver` 正确示例 | 0 | provenance 恢复 `current`，HTML SHA256 仍相同 |
| 对恢复后的 HTML 执行 `check --require-provenance` | 0 | 静态检查和 provenance 检查通过 |

这里的 “9/9” 是 Archify 自身 checker 的九项几何/产物检查，不是 9 个浏览器测试：single_svg、finite_svg、orthogonal_arrows、label_route_clearance、relationship_crossings、relationship_corridors、container_border_runs、route_rhythm、legend_clearance。

lastgood HTML SHA256：`48b8012b0bfeeaf4fbffac8072cebf820f239010657bcf1cd53621d5298b03dc`。失败前后的哈希及全部退出码见 [results.json](results.json)，失败状态见 [provenance-after-failure.json](provenance-after-failure.json)，恢复状态见 [provenance-recovered.json](provenance-recovered.json)。错误输入只改了官方 JSON 的一个组件 `type` 或一个连接 `to`，保存在本目录以便复核。

## 执行边界与复现

先审查了 CLI 的选定分支、renderer/checker 的本地导入、可选更新检查和品牌图片联网路径；记录见 [static-audit.json](static-audit.json)。选定入口的静态 import 扫描列出 33 个本地模块，没有发现外部包导入。扫描只是辅助，不能视为完整 JavaScript 分析或安全审计。

所有实际执行显式设置 `ARCHIFY_UPDATE_CHECK_DISABLED=1`；成功/失败 deliver 回执均返回 `update.reason: disabled`。官方样例没有 `brand` 或 repository source evidence，未进入品牌抓取或仓库证据读取分支。额外的 [no-network.cjs](no-network.cjs) 通过 `NODE_OPTIONS` 预载到 CLI 及其 Node 子进程，拒绝常见 HTTP/HTTPS/TCP/DNS/fetch API；[network-attempts.jsonl](network-attempts.jsonl) 为空。这个 guard 不是操作系统级网络隔离。

复现命令，从 `autodigest/` 运行：

```sh
python3 Research/evidence/archify/run-verification.py
```

[run-verification.py](run-verification.py) 只使用 Python 标准库和现有 Node；会重写本目录中的测试结果。[commands.sh](commands.sh) 列出各次 CLI 调用。`*.stdout.txt` / `*.stderr.txt` 保存输出；其中绝对 Research 路径前缀统一替换为 `Research`，其余内容保留。运行产生的、绑定机器路径的 `.delivery.json` 在全部检查结束后归档为脱敏 snapshot；因此提交的 provenance JSON 是研究证据，不应直接作为另一台机器的有效交付凭证。复现时脚本会重新生成有效 sidecar 并验证。

上游仓库运行前后 `git status --porcelain=v1` 均为空。上游测试 `test/cli.test.mjs` 的失败保留案例仅供静态参考；其 helper 导入 `parse5` / `saxes`，本次没有导入这些测试或为它们安装包。

## 源码如何支持观察

- [官方输入](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/examples/web-app.architecture.json#L1-L41) 描述 10 个组件、边、边界和说明卡片；没有从文字自动推导架构的步骤。
- [`validate` 路径](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/archify.mjs#L6919-L6953) 冻结输入，在临时目录渲染，再运行 `check-render-output.mjs`。这解释了 validate 不只是 JSON 语法检查。
- [Schema diagnostics](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/validator.mjs#L38-L78) 将校验错误转成 `schema/*`；[architecture 端点检查](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/architecture/render-architecture.mjs#L795-L825) 根据已声明组件检查 `from` / `to`，返回未知端点与候选修复。
- [deliver 的 render 失败分支](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/archify.mjs#L4814-L4830) 记录失败并返回；[checker 失败分支](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/archify.mjs#L4845-L4885) 也在提交前停止。**这次实际触发了前者，未故障注入后者。**
- [strict check 的 provenance 闸门](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/archify.mjs#L5470-L5500) 在检查 artifact 前拒绝失效交付状态；这对应第 7 步实测。
- [禁用更新检查](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/bin/delivery-update.mjs#L48-L60) 在启动 update child 之前返回；[品牌分支](https://github.com/tt-a1i/archify/blob/d0c8c7e9f4e06f303389f804208d387f27019ef5/archify/renderers/shared/brand-marks.mjs#L597-L625) 对没有 `brand` 的节点直接返回。

全部引用和对应本地源码 SHA256 见 [source-index.json](source-index.json)。

**没有验证的部分：**浏览器实际显示、交互/导出行为、`browser-check`、`finalize`、视觉审阅、联网品牌抓取、其他九种图类型、并发/崩溃/竞态，以及 LLM 的知识正确性。生成的 HTML 没有在浏览器中打开；几何检查通过不能等同于视觉体验好，也不能证明所表达架构符合真实系统。
