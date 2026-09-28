# Paper Reproductions

这里保存进入 L3（Reproduce）的论文复现项目。每个项目先保留论文工作流的完整上下文，再根据实际复现结果决定是否提取可复用资产。

## 新建复现项目

1. 从 [`_template/README.md`](_template/README.md) 和 [`_template/ASSET_EXTRACTION_REVIEW.md`](_template/ASSET_EXTRACTION_REVIEW.md) 开始。
2. 记录论文、数据、上游代码、许可证和 Research OS 笔记链接。
3. 先定义一个可验证的 target figure 或 analysis，不默认重跑整篇论文。
4. 原始数据、大型对象和生成结果留在 Git 外；README 记录 accession、校验信息和生成命令。
5. 达到有意义的复现阶段后再完成 Asset Extraction Review。

## 状态

`planned` → `environment_ready` → `data_ready` → `partial_reproduction` → `reproduced` → `validated` → `asset_reviewed` → `archived`

状态描述复现证据，不描述文件夹是否已经创建。环境或数据尚未准备好时，不使用 `reproduced`。

## 当前试点

- [`williams_2021_oral_atlas/`](williams_2021_oral_atlas/README.md)：Williams et al. 2021 人口腔黏膜单细胞图谱；Phase 2 最小试点。

