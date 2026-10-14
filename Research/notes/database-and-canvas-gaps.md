# 数据库结构图与知识画布补充

这四项补上“数据库结构理解”和“把知识放进可编辑画布”的缺口。它们与 Archify 的系统讲解互补：数据库图从 schema/元数据得到表和字段，知识画布组织材料，Archify 负责围绕一个问题讲清系统关系。本次仅做固定版本静态源码审阅，没有连接数据库、运行上游构建或调用模型。

Star / Fork 是 2026-10-15 北京时间 04:54–04:55 的 GitHub API 快照；默认分支代码与 release 分开记录。元数据见 [数据库候选证据](../evidence/database-diagram-candidates.json) 和 [相邻能力候选证据](../evidence/adjacent-visualization-candidates.json)。

| 工具 | Star | Fork | 定位 | 本次审阅版本 |
| --- | ---: | ---: | --- | --- |
| [drawDB](https://github.com/drawdb-io/drawdb) | 40,016 | 3,311 | 可视编辑 ERD、SQL 导入导出 | [f7c92920faaf](https://github.com/drawdb-io/drawdb/commit/f7c92920faaf7aa699111a8c58eff1457ab7f6e0) |
| [ChartDB](https://github.com/chartdb/chartdb) | 22,996 | 1,501 | 数据库元数据导入与结构编辑 | [c24936a402bb](https://github.com/chartdb/chartdb/commit/c24936a402bb3e24b4858f05282d69a04fcfe25b) |
| [Liam ERD](https://github.com/liam-hq/liam) | 5,138 | 241 | schema 转可发布交互 ERD | [0c5e362c2cbd](https://github.com/liam-hq/liam/commit/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814) |
| [AFFiNE](https://github.com/toeverything/AFFiNE) | 73,505 | 5,358 | 文档与无限画布组成知识工作区 | [0b69a6da21e8](https://github.com/toeverything/AFFiNE/commit/0b69a6da21e8fd35beb85667bb8496d9b3852238) |

## drawDB：直接编辑数据库模型

适合设计或学习表、字段、键、关系，导入现有 SQL 后继续修改，也能导出 SQL、DBML、Mermaid 等格式。核心代码按 MySQL、PostgreSQL、SQLite、MariaDB、SQL Server、Oracle 分派解析结果转换与 SQL 生成；本地用 Dexie/IndexedDB 保存图。[导入分派](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/utils/importSQL/index.js) · [导出分派](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/utils/exportSQL/index.js) · [本地存储](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/data/db.js) · [Mermaid 导出](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/utils/exportAs/mermaid.js)

当前版本还有 schema 差异转迁移 SQL 的代码；这说明不只是画矩形。生成迁移脚本不等于脚本已在目标数据库执行验证，尤其要检查类型、约束和数据库方言。[迁移 SQL 实现](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/utils/migrations/diffToSQL.js)

**AI 导入是条件性扩展入口。** `importSqlWithAi` 从 extensions context 注入，界面只有拿到该函数才显示入口；默认 context 是空对象。`normalizeAiDiagram` 会修正类型、过滤找不到字段的关系并报告警告。这些实现不能证明默认开源构建自带可用的模型服务，也不能证明模型猜的关系正确。[扩展上下文](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/context/ExtensionsContext.jsx) · [AI 入口及显示条件](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/components/EditorHeader/Modal/Modal.jsx) · [生成结果归一化与校验](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/src/utils/importAiDiagram.js)

许可为 [AGPL-3.0](https://github.com/drawdb-io/drawdb/blob/f7c92920faaf7aa699111a8c58eff1457ab7f6e0/LICENSE)。本次 API 无 latest release，但已核对默认分支 SHA；不能用 `package.json` 的 `0.0.0` 评价维护状态。用于 AutoDigest 时优先保留 SQL/DBML 与原生图，以表之间的真实键关系解释数据模型；再由 Archify 解释这些表所在的业务链路。

## ChartDB：把数据库已有结构变成图

主要入口是执行工具提供的元数据查询，把结果导入编辑器。以 PostgreSQL 为例，查询抽取表、列、外键、索引等信息；导入代码建立表、关系、视图依赖并安排初始位置。它处理的是结构元数据，并非自动读取业务记录来理解业务。[PostgreSQL 元数据查询](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/src/lib/data/import-metadata/scripts/postgres-script.ts) · [元数据转图](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/src/lib/data/import-metadata/import/index.ts) · [外键关系转换](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/src/lib/data/import-metadata/import/relationships.ts)

有浏览器 IndexedDB 存储。**同方言和部分跨方言导出都可本地完成**：界面默认不选 AI，同方言、generic 目标，以及已支持的 PostgreSQL → MySQL/MariaDB/SQL Server 路径调用确定性导出；没有确定性转换路径，或在跨方言时主动选择 AI，才进入 `exportSQL` 的模型分支。该分支在没有缓存时校验配置，用 AI SDK 请求配置的 OpenAI 兼容端点。不能把整个工具说成必须依赖 AI，也不能说启用跨方言 AI 转换后结构内容永远不离开浏览器。转换出的 SQL 仍需数据库验证。[界面选择与实际分派](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/src/dialogs/export-sql-dialog/export-sql-dialog.tsx#L146-L160) · [本地跨方言支持清单](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/src/lib/data/sql-export/cross-dialect/index.ts#L32-L42)[本地存储](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/src/context/storage-context/storage-provider.tsx) · [SQL 导出与外部模型分支](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/src/lib/data/sql-export/export-sql-script.ts)

许可为 [AGPL-3.0](https://github.com/chartdb/chartdb/blob/c24936a402bb3e24b4858f05282d69a04fcfe25b/LICENSE)；API latest release 为 v1.20.1（2026-04-07），审阅 HEAD 日期 2026-04-11。对“现有库到底有哪些表、哪些是外键、哪些是视图依赖”的理解很有用。没有外键约束的业务关系不会因为自动导入就完整出现。

## Liam ERD：从 schema 构建可交互文档

主要价值是将数据库 schema 放进可缩放、筛选和查看细节的 ERD，适合随代码一起维护的数据库文档。所审 parser 按 `schemarb`、`postgres`、`prisma`、`drizzle`、`tbls`、`liam` 分派；PostgreSQL 路径使用 WASM 解析器。不能把文档列出的所有数据库都理解成“任意方言 SQL 直接输入都支持”：例如 MySQL 官方说明走 tbls 中间格式。[格式分派](https://github.com/liam-hq/liam/blob/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814/frontend/packages/schema/src/parser/index.ts) · [PostgreSQL 解析实现](https://github.com/liam-hq/liam/blob/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814/frontend/packages/schema/src/parser/sql/postgresql/parser.ts) · [MySQL 支持方式](https://github.com/liam-hq/liam/blob/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814/frontend/apps/docs/content/docs/parser/supported-formats/mysql.mdx)

CLI 的构建流程先解析并写入 `schema.json`，遇到解析错误会返回错误，再复制前端资源生成目录；并明确要求通过 HTTP 服务访问，不能把它描述为 Archify 那种双击单文件 HTML 的同类交付。布局使用 ELK 的 layered 算法，通过 React Flow 节点与边转换调用。[预处理](https://github.com/liam-hq/liam/blob/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814/frontend/packages/cli/src/cli/erdCommand/runPreprocess.ts) · [静态站点构建](https://github.com/liam-hq/liam/blob/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814/frontend/packages/cli/src/cli/erdCommand/buildCommand/index.ts) · [ELK 布局](https://github.com/liam-hq/liam/blob/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814/frontend/packages/erd-core/src/features/erd/utils/computeAutoLayout/getElkLayout.ts)

许可为 [Apache-2.0](https://github.com/liam-hq/liam/blob/0c5e362c2cbda0e17b3ac8d9707d2a421d64f814/LICENSE)；API latest release 指向 `@liam-hq/cli@0.7.24`（2025-11-25），是这个多包仓库的 CLI release，不能代表所有组件的发布版本。适合把结构解释持续放在项目文档里；schema 本身未声明的业务含义需要另写解释。

## AFFiNE：把文字与图留在同一个知识工作区

适合在消化知识时，将笔记、图形、思维导图、引用材料放在可编辑画布中，再切回文档组织表达。代码确实有 `page` / `edgeless` 模式服务，以及应用层连接编辑器和文档持久状态的实现；画布根组件同时渲染文档块和 surface，思维导图有计算子树尺寸与左右布局的实现。[模式接口与默认服务](https://github.com/toeverything/AFFiNE/blob/0b69a6da21e8fd35beb85667bb8496d9b3852238/blocksuite/affine/shared/src/services/doc-mode-service.ts) · [实际编辑器模式接入](https://github.com/toeverything/AFFiNE/blob/0b69a6da21e8fd35beb85667bb8496d9b3852238/packages/frontend/core/src/blocksuite/view-extensions/editor-view/doc-mode-service.ts) · [画布渲染](https://github.com/toeverything/AFFiNE/blob/0b69a6da21e8fd35beb85667bb8496d9b3852238/blocksuite/affine/blocks/root/src/edgeless/edgeless-root-block.ts) · [思维导图布局](https://github.com/toeverything/AFFiNE/blob/0b69a6da21e8fd35beb85667bb8496d9b3852238/blocksuite/affine/gfx/mindmap/src/view/layout.ts)

**这是完整工作区，日常手工整理价值高；本次没有据此认定它能够自动反推代码架构。** README 宣传 AI 与同步协作能力，本轮没有运行其服务端或测量 AI 成图质量，故不把这些演示承诺作为源码审阅已证明的效果。相较 Archify，部署、账户、同步和完整应用维护的范围更大；如果只需要一篇架构解释，优先使用更聚焦的交付路径。

不能把全仓许可简写为 MIT。根许可将 backend 与 common/native 指向 backend/server/LICENSE，其余按 MIT；该服务端文件区分 EE 条款和 CE/客户端部分的 MPL-2.0。这里如实记录文件划分，具体发行物须继续核对对应版本。[根许可范围](https://github.com/toeverything/AFFiNE/blob/0b69a6da21e8fd35beb85667bb8496d9b3852238/LICENSE) · [服务端 EE / CE 说明](https://github.com/toeverything/AFFiNE/blob/0b69a6da21e8fd35beb85667bb8496d9b3852238/packages/backend/server/LICENSE)。API latest release v0.27.4（2026-08-18）。

## 选型关系

- 想亲自修改数据库模型：drawDB。
- 已有数据库，想导出元数据立即看结构：ChartDB。
- schema 在仓库中，想持续发布 ERD 文档：Liam ERD。
- 想把笔记和思维导图一起长期整理：AFFiNE。
- 想解释这些结构怎样组成一个系统、一次请求怎样流动：仍优先 Archify，关键关系回到上述来源核对。

这些是根据实现作出的适用性判断，不是同题实测排名。四份源码都位于 [`Research/repos/`](../repos/README.md)，由父仓子模块固定版本。
