# 种植体周围炎 RegVelo 准入审计 / Admission feasibility audit

审计日期：2026-10-10（Asia/Shanghai）。实际执行方式为 h5py 只读读取，并逐块扫描所有储存矩阵值、重算输入 SHA-256；没有训练 RegVelo、运行 scVelo 或修改现有数据。本报告判断的是当前输入能否进入正式 RegVelo 建模。

**结论：当前没有 READY 数据集。主要本地对象有可追溯基因 counts，但全部缺失 spliced / unspliced / Ms / Mu，因此均为 NOT_READY。GSE266897 独立 GEO 数据只有元信息与访问探针，未生成本地分析对象，单列 BLOCKED。已有 CELLxGENE 中包含该研究的 Huang 6,587 细胞，已实际读取，不能与独立 GEO 数据相加。**

## 实际证据与范围 / Evidence and scope

限定检索根为 `C:/Users/13683/Desktop/scriptsR`、`C:/Users/13683/Documents/ChatGPT/Research_OS`、`C:/Users/13683/Documents/Codex`，以及元信息明确指向的 Virtual Perturbation Toolkit / JUND 历史目录。未做全盘扫描、未下载大规模 raw。二进制数据通常被 Git 忽略，因此已对明确数据目录使用 no-ignore 文件清单。

实际读取8个H5AD、Lin上游8个10x filtered H5、92,112行 curated-v2 overlay、CollecTRI边表及源元信息。H5AD输入为只读，全部counts有限、非负且为整数值，标准化 X 非整数，可明确区分。RDS只发现既有导出文件及源元信息，没有反序列化RDS；其内部层不能根据文件扩展名猜测，本报告的准入结论依赖已实际读取的H5AD。`h5ad_layer_evidence.json`保存层、轴、注释、供者交叉表、SHA及GRN交集，`audit.csv`含用户要求全部16列并增加证据字段。

| 实际对象 | cells × genes | counts位置 | 非零counts | 零比例 | 唯一symbol数 |
|---|---:|---|---:|---:|---:|
| `phase4a_preliminary_integrated.h5ad` | 92,112 × 21,934 | layers/counts | 147,063,492 | 92.72% | 21,934 |
| `GSE310110_annotated_v0.4.h5ad` | 13,977 × 36,601 | layers/counts | 36,429,424 | 92.88% | 36,591 |
| `GSE272774_annotated_v0.4.h5ad` | 41,902 × 58,336 | layers/counts | 86,805,932 | 96.45% | 56,813 |
| `GSE294615_annotated_v0.3.h5ad` | 7,754 × 20,633 | layers/counts | 12,233,061 | 92.35% | 20,633 |
| `GSE188217_annotated_v0.1.h5ad` | 18,574 × 27,998 | layers/counts | 25,339,541 | 95.13% | 27,933 |
| `GSE310110_Endothelial_cell_reuse_v0.4.h5ad` | 520 × 36,601 | layers/counts | 1,631,741 | 91.43% | 36,591 |
| `zenodo.19697597_Macrophage_reuse_v0.2.h5ad` | 1,410 × 21,934 | layers/counts | 2,677,473 | 91.34% | 21,934 |
| `periodontal_atlas.h5ad` | 105,918 × 35,369 | raw/X | 138,928,204 | 96.29% | 35,360 |

零比例按完整储存轴计算。GSE272774的union轴包含不同库未释放的gene，填零只为存储，不能解释为生物学零；速度建模必须重计数而非从这个union零分布推断动力学。GSE310110有36,601个gene ID但36,591个唯一symbol；GSE272774为58,336/56,813，小鼠为27,998/27,933，meta-atlas为35,369/35,360。TF–target接入必须显式处理gene ID/symbol多对一，不能默认为symbol唯一或静默按symbol合并。

GSE188217部分历史`subcluster_state`字符串含编码损坏；审计原样保留，不猜测恢复文字。counts/layers、gene轴、样本及独立fine标签的检查不依赖这些损坏字符串；该队列仍因缺剪接层与物种先验不匹配而NOT_READY。

## 逐队列结论 / Cohort decisions

| 数据集 | 本地范围 | 准入 | 主要缺口 |
|---|---|---|---|
| Lin / zenodo.19697597 PI | 38,648 cells；8库/7供者 | NOT_READY | 无剪接层、无本地raw；注释provisional，无独立fine state |
| GSE164241 Lin健康视图 | 53,464 cells；13库/13供者 | NOT_READY | 无剪接层；只是健康局部视图，非GEO全部队列 |
| GSE310110 | 13,977 cells；3份PI活检 | NOT_READY | 无剪接层；3库processing版本冲突，内皮520全部来自一库 |
| GSE272774 | 41,902 cells；N3/PI5 | NOT_READY | 无剪接层；source gene范围、技术及疾病耦合；N是既往感染消退参照 |
| GSE294615 | 7,754 cells；3名治疗后供者 | NOT_READY | 无剪接层；单条件/单次取样，第三供者主导 |
| GSE188217 | 18,574 mouse cells；2库 | NOT_READY | 无剪接层、人先验不匹配；每条件1库无重复疾病检验 |
| GSE266897 direct GEO | 4个诱导性牙龈炎文库；元信息 | BLOCKED | 独立表达/QC/细胞数尚不可审计；不是种植体周围黏膜炎 |
| CELLxGENE meta-atlas | 105,918 cells；34库标签 | NOT_READY | raw/X总counts可用但无剪接；没有PI，跨研究不能作连续疾病轨迹 |
| 历史JUND/STAT4 subset | 120 cells/3供者；460基因模型 | NOT_READY | 受限操作性输入及表达关联网络，非RegVelo先验/时间过程 |

不存在健康–种植体周围黏膜炎–PI完整三组准入队列；牙龈炎也不能替换种植体周围黏膜炎。`Upon diagnosis`、`After step 1/2 treatment`、`baseline`是取样背景，不是纵向多时间点。健康/炎症/疾病横断面分组、不同论文或UMAP空间位置均不自动提供真实方向。

Lin canonical仍有最初major_cell_type标签；实际导入atlas时应用curated-v2 overlay。本审计明确逐cell ID核对overlay全量唯一对应，再得到PI成纤维2,996、巨噬1,410、内皮3,037；健康巨噬只有7、中性粒40。不得以原canonical未更新标签或健康稀少细胞宣称跨疾病谱系命运。joint scVI来自doublet过滤前参考，singlet投影并未重训练；来源与疾病组耦合。

## GRN与JUND / GRN evidence

可复用先验是实际本地 `collectri.csv`：43,175边、1,186个source（包含复合TF约定）、6,693 targets，完整SHA `4473c9189dd53dacc80297709ad1452dda1086a1cc2185f9a56146c261668701`。它整合知识资源与文献有符号边，属于人类curated TF–target先验，不是这批口腔细胞重新推断的直接因果网络；当前未找到匹配同细胞ATAC/motif或实验结合网络。

| 输入gene轴 | regulator交集 | target交集 | prior边交集 | JUND边 |
|---|---:|---:|---:|---:|
| Lin21,934交集gene |1175|6417|40877|105|
| GSE310110 gene symbols |1180|6506|41280|107|
| GSE272774完整union |1178|6499|41167|106|
| GSE272774共同分析22,533gene |955|5352|31414|89|
| GSE294615 |1180|6543|41449|108|
| CELLxGENE meta-atlas |1180|6447|40903|108|

以上只是当前gene symbol的静态交集；不等于经过velocity gene过滤、表达/剪接信号检查、GRN方向/维度验证后的模型regulon。JUND出现在人类基因轴和先验中，只能说明候选可查，不能说明调控活跃或疾病驱动。小鼠Jund存在，但当前人CollecTRI直接symbol匹配为0；需要可信小鼠网络/orthology及版本记录，不能简单大写symbol。

历史DoseDirKO网络位于 `C:\Users\13683\Desktop\本科科研汇总\Virtual_Cell_Feasibility_2026-10-08\PI_Inflammatory_Fibroblast_Virtual_Perturbation/results/virtual_ko/pooled_JUND_alpha0.5/WT_network_run0.npy`；元信息确认460基因表达关联网络，不能当作已经方向验证的RegVelo先验。历史结论仍PARTIAL，INPUT_OK限探索性输入，RUN_OK通过，PREDICTION_STABLE失败，BIO_VALIDATED未评估；CXCL8/IL6 pooled与供者方向冲突，无匹配真实KO/KD。网络distance/signed propagation不是RNA velocity或实验log2FC。

## 重计数和动力学准入 / Recount and QC route

限定已有数据根没有FASTQ/BAM/loom。Lin8个filtered H5结构只有matrix/data/indices/indptr/shape/barcodes/features；名称中的raw文件夹或filtered H5不代表包含未剪接reads。现有MTX只有gene总counts，不能通过普通归一化拆成spliced/unspliced。

GSE310110源SOFT有BioProject PRJNA1365154和SRX31108634–36，GSE272774有PRJNA1138705和SRX25410355–62，GSE266897有PRJNA1108695和SRX24483678–81。它们提供原始reads追溯路线，未在本次下载；实验accession也不是已核实的FASTQ大小、读长/条码布局或可正确计数证明。当前原始转移字节数=0，预期下载及计数磁盘需求未取得runinfo，因此未知，不能给出虚构GB估计。下一步先保存run清单、文件大小、参考build/annotation、chemistry/read布局和固定工具版本，再限定单文库重计数验证，保留barcode/gene对应。Singleron/GEXSCOPE不得套用未经核实的10x布局。

剪接计数可得后才能评为CONDITIONAL，再完成：原始S/U计数的barcode/Ensembl对齐；同谱系细胞与供者身份审查；有效速度gene/TF覆盖；scVelo基线与phase portrait；按样本、深度、细胞周期和批次检验方向；邻域连接与真实生物学先后证据；终末状态可信度。没有速度QC时不构建CellRank疾病命运、不为满足图谱强行命名终末状态。

建议优先从完整Lin PI成纤维2,996细胞考察修复/基质/炎症表达的谱系内连续性。D3/D4/D6分别653/888/821，具有多供者检查机会；操作性富集551及模型120不用于定义唯一正式亚型。第二选择为Lin巨噬1,410细胞（D3/D4/D5/D6/D7=554/463/165/145/71），先核查单核/巨噬边界与来源，再讨论连续状态。GSE310110髓系280可作小型状态审查，成纤维589/32/6及单供者内皮不宜先做稳定跨供者扰动。候选TF由可用regulon、表达/剪接信号和稳定性重新筛查，可保留JUND/RELA/STAT3/CEBPB作待审候选，不预设有效。

缺剪接层期间可复用现有CollecTRI-ULM/VIPER调控活性、供者pseudobulk表达、固定程序评分及限定DoseDirKO探索，分别记录观察/先验推断/模型预测。它们无需冒称velocity，也不替代真实CRISPR/siRNA验证。

## 可复现与自检 / Reproduction and checks

只读审计命令：
```powershell
& 'C:/Users/13683/Documents/Codex/2026-10-07/files-pasted-by-the-user-project/work/atlas-env/Scripts/python.exe' './audit_inputs.py'
python './write_report.py'
```
首条在本审计目录运行；实际Python3.12.14、h5py3.16.0。固定本地路径需要迁移时修改，脚本只向本报告目录写证据，不覆盖数据。完整日志为 `read_only_audit.log`。自检：8个H5AD真实层读取PASS；counts/X区分PASS；input SHA重新计算PASS；92,112-cell overlay精确对齐PASS；数据集/真实分组不混淆PASS；正式velocity/RegVelo/CellRank/真实扰动均NOT_RUN。准入状态反映输入缺口，不是已计算速度的科学失败。
