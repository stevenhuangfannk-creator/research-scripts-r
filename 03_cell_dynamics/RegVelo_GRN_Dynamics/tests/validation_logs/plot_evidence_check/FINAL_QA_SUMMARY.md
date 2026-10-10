# 图谱最终核验 / Final gallery QA

2026-10-10，正式 `official_zebrafish/hard_seed0`：**27/27 图件成功渲染，0 FAIL，0 NOT_RUN**。结果来自实际保存的输入、训练、速度、命运、GRN和配对虚拟扰动文件；未使用模拟或随机占位数据。

- 每个ID有300dpi PNG、可编辑文字SVG/PDF、绘图源CSV和JSON元数据。实际导出最小文字为7pt（PDF）/7px（SVG），27份PDF均通过5pt阈值审计。
- `plots_source_validation.json`：17 PASS、3 WARN、0 FAIL。WARN已说明：本任务要求300dpi PNG与矢量文件，未要求TIFF/600dpi；seed为单次运行元数据，未把多seed统计伪装成无误差条的均值。画布用于科研图谱，完整图集的投稿宽度尚未统一。
- 所有27图均经人工查看；修正后的C01/C02同名状态沿用A01原配色，未分配细胞为灰色。C03/E03采用2×2、7.2×6.4英寸画布；D01保留相同40条真实边，改用清楚的regulator→target双列布局；E04保留字面NULL对照；E06显式显示阻断后的真实零值。
- 独立只读核对A03/B03/B06/B07：保存层总量和检出、mean fit_t归一化、后验速度标准差均值、同细胞/同基因投影逐项匹配；受检原文件哈希前后不变。见 `evidence.json`、`FINDINGS.md`、`check.py`。
- C/D/E追加15项数值核对通过：C03概率及单纯形、C04归一化熵、D01/D02/D04真实权重、E01配对投影、E02效应、E03确为KO减配对基线、E04官方表及NULL=0.5、E06权重归零。见 `cd_e_evidence.json`。

**科学边界 / Scientific boundaries**：E04官方likelihood为ROC AUC，baseline=1、KO=0，参照0.5；>0.5表示模型内消耗，<0.5表示模型内富集。官方p值来自pooled-cell单侧ranksums，FDR为BH；不能当作donor/embryo独立重复证据。RegVelo/scVelo一致或不一致都不能自行确立真值。图件PASS不证明收敛、终末状态正确、实验因果或临床疗效。

**版面边界 / Layout limit**：字号核验针对导出原始物理尺寸。B04/B05及部分双面板图保留完整宽画布；把它们机械压缩到183mm可能使字号低于5pt，正式投稿时应分拆或重新排版。本次未宣称全部图已经统一到某一期刊最终版面。

源码修复与最后重绘仅影响布局、配色、NULL标签和导出，未修改数值输入、模型结果或workflow run state。执行用本工作区 `work/peri_audit/render_and_qa.py` 和 `check_cd_e_evidence.py`；本目录脚本副本保存当次执行证据。
