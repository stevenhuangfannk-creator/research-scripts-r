"""Build the feasibility report from the actual read-only evidence and source metadata."""
from pathlib import Path
import csv
import json
import shutil

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ATLAS = Path('C:/Users/13683/Documents/Codex/2026-10-07/files-pasted-by-the-user-project/outputs/oral-scrna-atlas')
TF = Path('C:/Users/13683/Documents/Codex/2026-10-08/files-pasted-by-the-user-codex/outputs/tf-regulatory-network-atlas')
HIST = Path('C:/Users/13683/Desktop/本科科研汇总/Virtual_Cell_Feasibility_2026-10-08/PI_Inflammatory_Fibroblast_Virtual_Perturbation')
evidence = json.loads((HERE / 'h5ad_layer_evidence.json').read_text(encoding='utf-8'))
objects = evidence['objects']
prior = evidence['collectri']
by_id = {'zenodo.19697597':objects[0], 'GSE164241':objects[0], 'GSE310110':objects[1],
         'GSE272774':objects[2], 'GSE294615':objects[3], 'GSE188217':objects[4]}
rows = []
notes = {
 'zenodo.19697597': ('8 libraries / 7 donors (D6: IGT6+IGT8)', 38648,
   'Fibroblast 2996; Macrophage 1410; Endothelial 3037; provisional curated-v2',
   '优先取得可匹配8库的原始reads/BAM；源8个filtered H5只有gene总counts。恢复gene ID并选谱系内连续状态；健康来源与PI来源混杂，联合UMAP不可直接用于速度。'),
 'GSE164241': ('13 healthy libraries / 13 donors (local Lin view only)', 53464,
   'Fibroblast 12943; Endothelial 16522; Macrophage 7; Neutrophil 40',
   '只作13健康文库参考；不等于整个GSE164241。取得原始reads并独立计数、同谱系QC；不要与PI跨研究分组强制解释为疾病时间。'),
 'GSE310110': ('3 libraries / 3 title-derived biopsy IDs; clinical mapping not released', 13977,
   'Fibroblast 627 (589/32/6 by sample); Myeloid 280; Endothelial 520 (all one sample)',
   'SRA SRX31108634–SRX31108636可追溯；先核对run、10x chemistry及参考版本并估算大小，仅对一个库设计剪接重计数试验。解开symbol重复、样本/Cell Ranger版本耦合；内皮不支持跨供者亚型。'),
 'GSE272774': ('8 libraries / 8 patients reported; N=3, PI=5', 41902,
   'Fibroblast 4948 (N3626/PI1322); Myeloid 2475 (N1049/PI1426); Endothelial 8094',
   'SRA SRX25410355–SRX25410362可追溯；Singleron/GEXSCOPE需适配真实read布局。用Ensembl ID及共同释放22533基因，排查source范围与condition混杂；N不是从未感染健康。'),
 'GSE294615': ('3 libraries / 3 donors; one post-treatment condition', 7754,
   'Fibroblast 704; Myeloid 678; Endothelial 622',
   '查原始reads；单条件、3供者且Patient3贡献5860细胞；治疗后标签是共同临床取样背景，不是时间序列。先审查谱系连续状态、纯度与深度。'),
 'GSE188217': ('2 libraries; 1 library per condition; animal/donor mapping incomplete', 18574,
   'Fibroblast 5959; Myeloid 294; Neutrophil 1379; mouse oral reference',
   '不是人PI队列；原始reads与小鼠先验均需补齐，不能直接接人CollecTRI或按symbol大写转换。db/db与Control各1库不能作动物重复疾病检验。')}
for accession, obj in by_id.items():
    meta_path = ATLAS / 'datasets' / accession / 'metadata.yaml'
    meta = json.loads(meta_path.read_text(encoding='utf-8'))
    sample, cells, candidate, next_step = notes[accession]
    overlap = prior['overlap_by_input'][obj['path']]
    grn = ('human CollecTRI symbol overlap: '+str(overlap['edges'])+' edges; JUND='+str(overlap['JUND_edges'])+'; no RegVelo prior validation') if meta['species']=='Homo sapiens' else 'human prior species-mismatched; mouse Jund present, no validated mouse prior'
    if accession=='GSE272774': grn += '; shared-gene subset=31414 edges/JUND89'
    rows.append({'数据集':accession,'来源文献':meta['paper_title']+'; DOI '+meta['doi'],
      '物种':meta['species'],'组织':meta['tissue'],'分组':meta['condition'],'样本数':sample,
      '细胞数':cells,'已有本地路径':obj['path'],'Spliced':'ABSENT (actual HDF5 layer read)',
      'Unspliced':'ABSENT (actual HDF5 layer read)','原始测序文件':'No local BAM/FASTQ in audited data roots; processed counts ≠ raw reads',
      'GRN':grn,'候选细胞群':candidate,'速度 QC':'NOT_RUN; no splice layers, direction/terminal-state/depth/batch QC unavailable',
      '准入状态':'NOT_READY','下一步':next_step,'真实时间点':'NO longitudinal time; '+str(obj['metadata_counts'].get('timepoint','not reported')),
      '基因数':obj['n_genes'],'counts来源':'layers/counts; complete stored values finite nonnegative integers; X is normalized noninteger',
      'symbol唯一数':obj['unique_symbols'],'证据路径':str(meta_path)+'; '+str(HERE/'h5ad_layer_evidence.json'),
      '输入SHA256':obj['sha256'],'读取范围':'h5py read-only full stored-values scan; Lin annotation overlay exactly cell-ID aligned'})

meta_path = ATLAS/'datasets/GSE266897/metadata.yaml'
meta = json.loads(meta_path.read_text(encoding='utf-8'))
rows.append({'数据集':'GSE266897 direct GEO files','来源文献':meta['paper_title']+'; DOI '+meta['doi'],
  '物种':'Homo sapiens','组织':'Gingiva','分组':'induced gingivitis (not peri-implant mucositis)',
  '样本数':'4 libraries / 4 sample records; donor correspondence pending','细胞数':'Unknown for unprocessed direct files',
  '已有本地路径':str(meta_path),'Spliced':'UNKNOWN; no direct analysis object','Unspliced':'UNKNOWN; no direct analysis object',
  '原始测序文件':'SRA SRX24483678–SRX24483681 recorded; no local FASTQ/BAM',
  'GRN':'Human CollecTRI available; direct-object gene overlap not audited','候选细胞群':'Direct-file composition not measured; Huang member exists in separate meta-atlas',
  '速度 QC':'NOT_RUN; expression/velocity object unavailable','准入状态':'BLOCKED',
  '下一步':'复用已有CELLxGENE中Huang 6587细胞作GRN活动参考；若做velocity需追溯四库原始reads并做独立剪接计数/QC，1KB可访问探针不是完整下载。',
  '真实时间点':'No released longitudinal series established','基因数':'Unknown','counts来源':'No direct local count object',
  'symbol唯一数':'Unknown','证据路径':str(ATLAS/'datasets/GSE266897/access_audit.json')+'; '+str(meta_path),
  '输入SHA256':'Not applicable','读取范围':'GEO SOFT/sample metadata and prefix-probe record; no direct expression matrix read'})

obj=objects[-1]
rows.append({'数据集':'CELLxGENE periodontal meta-atlas (GSE266897 Huang member included)',
  '来源文献':'Easter et al. Nature Communications 2024; DOI 10.1038/s41467-024-49037-y; multiple source cohorts',
  '物种':'Homo sapiens','组织':'Gingiva / tooth-associated oral tissue','分组':'normal60811; periodontitis38520; gingivitis6587; no PI',
  '样本数':'34 library-like donor_id labels, not 34 proven independent donors','细胞数':obj['n_cells'],
  '已有本地路径':obj['path'],'Spliced':'ABSENT (layers empty)','Unspliced':'ABSENT (layers empty)',
  '原始测序文件':'No local FASTQ/BAM in this cache; source cohorts reused',
  'GRN':'Human CollecTRI408? Actual40903 symbol-matched edges/JUND108; curated prior, no velocity validation'.replace('408? Actual',''),
  '候选细胞群':'Author fibroblast17533; macrophage2129; blood/lymphatic endothelium; restrict a single cohort',
  '速度 QC':'NOT_RUN; no splicing layers','准入状态':'NOT_READY',
  '下一步':'用于已有GRN活动分析；RegVelo先分Study再追溯raw，不把来源/assay/疾病组作为时间。Huang6587不与直接GSE266897重复计数。',
  '真实时间点':'No longitudinal time key','基因数':obj['n_genes'],
  'counts来源':'raw/X actually read; finite nonnegative integer; normalized X is noninteger; layers empty',
  'symbol唯一数':obj['unique_symbols'],'证据路径':str(TF/'data/source_audit.json')+'; '+str(HERE/'h5ad_layer_evidence.json'),
  '输入SHA256':obj['sha256'],'读取范围':'Actual h5py read-only full stored-values scan; member cohort mapping corroborated from source audit'})

rows.append({'数据集':'Historical JUND/STAT4 fibroblast subset (derived from Lin PI)',
  '来源文献':'Lin2026 PI input; DOI10.1038/s41368-026-00447-2; DoseDirKO historical model',
  '物种':'Homo sapiens','组织':'Peri-implant mucosa','分组':'PI-only operational Inflammatory_enriched subset',
  '样本数':'3 donors D3/D4/D6; 4 libraries (D6 repeated)','细胞数':120,
  '已有本地路径':str(HIST/'data/10x_target'),'Spliced':'ABSENT','Unspliced':'ABSENT',
  '原始测序文件':'10x target MTX export is processed gene counts, not raw reads',
  'GRN':'DoseDirKO WT networks460x460 expression-associated; not a validated directed RegVelo prior',
  '候选细胞群':'Exploratory operational fibroblast enrichment; no independently validated fine state',
  '速度 QC':'NOT_RUN; no splice counts','准入状态':'NOT_READY',
  '下一步':'保留既有DoseDirKO独立调用；RegVelo回到完整同谱系输入而非120细胞/460基因受限面板。JUND只是候选；pooled/供者冲突及稳定性FAIL必须保留。',
  '真实时间点':'None','基因数':'21934 count export; 460 DoseDirKO model panel',
  'counts来源':'Existing audit: canonical layers/counts exact export; no new model run in this audit',
  'symbol唯一数':'21934 input / 460 panel','证据路径':str(HIST/'data/input_manifest/input_manifest.json')+'; '+str(HIST/'results/virtual_ko/pooled_JUND_alpha0.5/run_manifest.json'),
  '输入SHA256':'See historical manifest; not recomputed for this derivative','读取范围':'Historical configuration, CSV/manifest and network metadata; canonical parent separately re-read'})

with (HERE/'audit.csv').open('w',encoding='utf-8-sig',newline='') as fh:
    writer=csv.DictWriter(fh,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)

qc_rows=[]
for obj in objects:
    counts=obj['layers'].get('counts') or obj['raw_X']
    qc_rows.append(f"| `{Path(obj['path']).name}` | {obj['n_cells']:,} × {obj['n_genes']:,} | {'raw/X' if obj['raw_X'] else 'layers/counts'} | {counts['nonzero']:,} | {counts['zero_fraction']*100:.2f}% | {obj['unique_symbols']:,} |")
report=f'''# 种植体周围炎 RegVelo 准入审计 / Admission feasibility audit

审计日期：2026-10-10（Asia/Shanghai）。实际执行方式为 h5py 只读读取，并逐块扫描所有储存矩阵值、重算输入 SHA-256；没有训练 RegVelo、运行 scVelo 或修改现有数据。本报告判断的是当前输入能否进入正式 RegVelo 建模。

**结论：当前没有 READY 数据集。主要本地对象有可追溯基因 counts，但全部缺失 spliced / unspliced / Ms / Mu，因此均为 NOT_READY。GSE266897 独立 GEO 数据只有元信息与访问探针，未生成本地分析对象，单列 BLOCKED。已有 CELLxGENE 中包含该研究的 Huang 6,587 细胞，已实际读取，不能与独立 GEO 数据相加。**

## 实际证据与范围 / Evidence and scope

限定检索根为 `C:/Users/13683/Desktop/scriptsR`、`C:/Users/13683/Documents/ChatGPT/Research_OS`、`C:/Users/13683/Documents/Codex`，以及元信息明确指向的 Virtual Perturbation Toolkit / JUND 历史目录。未做全盘扫描、未下载大规模 raw。二进制数据通常被 Git 忽略，因此已对明确数据目录使用 no-ignore 文件清单。

实际读取8个H5AD、Lin上游8个10x filtered H5、92,112行 curated-v2 overlay、CollecTRI边表及源元信息。H5AD输入为只读，全部counts有限、非负且为整数值，标准化 X 非整数，可明确区分。RDS只发现既有导出文件及源元信息，没有反序列化RDS；其内部层不能根据文件扩展名猜测，本报告的准入结论依赖已实际读取的H5AD。`h5ad_layer_evidence.json`保存层、轴、注释、供者交叉表、SHA及GRN交集，`audit.csv`含用户要求全部16列并增加证据字段。

| 实际对象 | cells × genes | counts位置 | 非零counts | 零比例 | 唯一symbol数 |
|---|---:|---|---:|---:|---:|
{chr(10).join(qc_rows)}

零比例按完整储存轴计算。GSE272774的union轴包含不同库未释放的gene，填零只为存储，不能解释为生物学零；速度建模必须重计数而非从这个union零分布推断动力学。GSE310110有36,601个gene ID但36,591个唯一symbol；GSE272774为58,336/56,813，小鼠为27,998/27,933，meta-atlas为35,369/35,360。TF–target接入必须显式处理gene ID/symbol多对一，不能默认为symbol唯一或静默按symbol合并。

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

可复用先验是实际本地 `collectri.csv`：43,175边、1,186个source（包含复合TF约定）、6,693 targets，完整SHA `{prior['sha256']}`。它整合知识资源与文献有符号边，属于人类curated TF–target先验，不是这批口腔细胞重新推断的直接因果网络；当前未找到匹配同细胞ATAC/motif或实验结合网络。

| 输入gene轴 | regulator交集 | target交集 | prior边交集 | JUND边 |
|---|---:|---:|---:|---:|
| Lin21,934交集gene |1175|6417|40877|105|
| GSE310110 gene symbols |1180|6506|41280|107|
| GSE272774完整union |1178|6499|41167|106|
| GSE272774共同分析22,533gene |955|5352|31414|89|
| GSE294615 |1180|6543|41449|108|
| CELLxGENE meta-atlas |1180|6447|40903|108|

以上只是当前gene symbol的静态交集；不等于经过velocity gene过滤、表达/剪接信号检查、GRN方向/维度验证后的模型regulon。JUND出现在人类基因轴和先验中，只能说明候选可查，不能说明调控活跃或疾病驱动。小鼠Jund存在，但当前人CollecTRI直接symbol匹配为0；需要可信小鼠网络/orthology及版本记录，不能简单大写symbol。

历史DoseDirKO网络位于 `{HIST}/results/virtual_ko/pooled_JUND_alpha0.5/WT_network_run0.npy`；元信息确认460基因表达关联网络，不能当作已经方向验证的RegVelo先验。历史结论仍PARTIAL，INPUT_OK限探索性输入，RUN_OK通过，PREDICTION_STABLE失败，BIO_VALIDATED未评估；CXCL8/IL6 pooled与供者方向冲突，无匹配真实KO/KD。网络distance/signed propagation不是RNA velocity或实验log2FC。

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
'''
(HERE/'PERI_IMPLANTITIS_REGVELO_FEASIBILITY.md').write_text(report,encoding='utf-8')
dest=ROOT/'outputs/research-scripts-r/03_cell_dynamics/RegVelo_GRN_Dynamics/examples/peri_implantitis_audit'
dest.mkdir(parents=True,exist_ok=True)
for name in ['PERI_IMPLANTITIS_REGVELO_FEASIBILITY.md','audit.csv','h5ad_layer_evidence.json','audit_inputs.py','write_report.py','read_only_audit.log']:
    shutil.copy2(HERE/name,dest/name)
print(f'Wrote {len(rows)} dataset audit rows; copied to {dest}')
