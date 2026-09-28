# Research Scripts R

一个按研究项目和分析职责整理的 R 科研代码库。当前保留 3 个既有项目，并以 Williams 2021 oral atlas 作为首个论文复现试点。

代码库采用两层结构：第一层保留独立研究项目，第二层按分析模块组织脚本。这样可以看清每个项目的完整流程，同时避免把不同数据集的脚本误当成可直接互换的通用函数。

## 项目

| 目录 | 研究内容 | 当前状态 |
|---|---|---|
| `projects/01_zilongjin_network_pharmacology/` | 紫龙金片与结直肠癌肝转移的网络药理学 | 单一综合 Quarto 流程；缺少输入数据 |
| `projects/02_gse255834_scrna_pipeline/` | GSE255834 APAP 肝损伤 scRNA-seq 预处理与注释 | 主链清楚；存在硬编码路径和中间对象命名缺口 |
| `projects/03_apap_mouse_liver_atlas/` | Ben-Moshe 2022 × GSE280652 小鼠肝脏图谱、注释与通讯 | 主流程与历史分支并存；缺少最终对象的可执行合并步骤 |

## 模块体系

| 模块 | 负责内容 | 典型操作 |
|---|---|---|
| `01_data_ingestion` | 数据读取与对象构建 | H5/矩阵读取、样本元数据解析、Seurat 对象创建 |
| `02_quality_control` | 数据清洗与质量控制 | barcode calling、双细胞识别、线粒体/UMI/基因数过滤、QC 诊断 |
| `02_integration_clustering` | 数据整合与聚类 | 合并、标准化、HVG、PCA、Harmony、邻接图、聚类、UMAP |
| `03_decontamination` | 环境 RNA 去污染 | DecontX、校正计数重建 |
| `03_annotation` / `04_annotation` | 细胞类型与亚群注释 | marker score、一级/二级/三级注释、标签回写 |
| `04_cell_communication` | 细胞通讯 | CellChat、LIANA/CellPhoneDB、配体-受体和通路比较 |
| `05_reports` | 结果汇总与专题报告 | 读取预计算对象，生成统计表和可视化报告 |
| `06_functional_analysis` | 常规功能分析 | PPI、CytoHubba、GO、KEGG、GSEA、药材-成分-靶点网络 |
| `99_legacy` | 无法纳入当前主链但需要保留的历史代码 | 提取代码块、旧实验分支 |

模块编号表达大致顺序，不代表所有项目都必须具备全部模块。当前代码高度依赖具体数据集，因此没有为了“通用化”而抽象尚未复用的函数。

## 推荐使用方式

1. 进入具体项目，先读项目 `README.md`。
2. 根据 README 准备数据。原始数据和大型对象不要提交 Git。
3. 按模块编号和项目 README 的顺序运行。
4. 在运行前检查脚本中的绝对路径、线程数和 R 包版本。
5. 新分析优先放入现有模块；只有出现新的、长期稳定的职责时才新增模块。

完整的逐脚本职责、输入输出和状态见 [`docs/script-catalog.md`](docs/script-catalog.md)。
Phase 2 对既有代码的保留/候选判断见 [`docs/phase2-code-disposition.md`](docs/phase2-code-disposition.md)。

## 论文复现与可复用资产

- [`reproductions/`](reproductions/README.md)：进入 L3 的完整论文复现；当前只实施一个 Williams 2021 试点。
- [`reproductions/_template/`](reproductions/_template/README.md)：轻量 README 与 Asset Extraction Review 模板。
- [`library/`](library/README.md)：经过真实复现和重复验证后才进入的共享资产入口；当前没有已晋升资产。

论文复现先保留完整上下文。共享 workflow、function 或 visualization 只有经过 Asset Extraction Review 后才提取。

## 数据和版本管理

- Git 只管理代码、README、轻量配置和方法说明。
- `.gitignore` 排除 RDS/H5/矩阵、原始数据、结果、图、渲染物、缓存、压缩包和 `.env`。
- 当前仓库没有原始数据、PDF、PPT、图片或生成结果。
- 已扫描密码、Token、API Key 和私钥，未发现真实凭据。
- GSE255834 脚本仍含 `C:/Users/zhaozize/Desktop/APAP` 绝对路径，属于待修复的可移植性问题。

## 可运行性

整理时没有执行既有分析；原始数据和中间对象仍然缺失。Phase 2 找到本机 R 4.3.1，但当前 Seurat/Matrix 版本不兼容，Quarto 仍不可用。所有 28 个既有代码文件保持未修改；每个项目的已知阻塞项记录在自己的 README 和 `Notes/` 中。
