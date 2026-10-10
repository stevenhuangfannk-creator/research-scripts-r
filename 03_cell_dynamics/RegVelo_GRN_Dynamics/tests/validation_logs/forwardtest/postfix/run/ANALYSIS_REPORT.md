# RegVelo 真实运行报告 / Executed analysis

执行成功仅证明对应计算完成；科学可靠性需结合模型 QC、方向性、基线与对照。

| 阶段 | 状态 | 秒 | 证据或错误 |
|---|---|---:|---|
| audit | FAIL | 2.969 | ValueError: Missing required RNA layers: spliced, unspliced. Expression cannot reconstruct splicing counts.. Evidence: C:\Users\13683\Documents\Codex\2026-10-10\files-pasted-by-the-user-codex\work\official_sources\forwardtest_postfix\run\INPUT_AUDIT.json |
| prepare | NOT_RUN |  |  |
| fit | NOT_RUN |  |  |
| velocity | NOT_RUN |  |  |
| fate | NOT_RUN |  |  |
| grn | NOT_RUN |  |  |
| perturb | NOT_RUN |  |  |
| visualize | NOT_RUN |  |  |
| report | PASS | 0.625 | C:\Users\13683\Documents\Codex\2026-10-10\files-pasted-by-the-user-codex\work\official_sources\forwardtest_postfix\run\ANALYSIS_REPORT.md |

## 参数 / Parameters

```json
{
  "input": "C:\\Users\\13683\\Documents\\Codex\\2026-10-10\\files-pasted-by-the-user-codex\\work\\forwardtest\\canonical_fibroblasts_32_audit_only.h5ad",
  "grn": "C:\\Users\\13683\\Documents\\Codex\\2026-10-08\\files-pasted-by-the-user-codex\\outputs\\tf-regulatory-network-atlas\\data\\cache\\collectri.csv",
  "output": "C:\\Users\\13683\\Documents\\Codex\\2026-10-10\\files-pasted-by-the-user-codex\\work\\official_sources\\forwardtest_postfix\\run",
  "grn_orientation": "regulator_by_target",
  "group_key": "major_cell_type",
  "time_key": null,
  "species": "Homo sapiens",
  "gene_id_type": "gene_symbol",
  "input_provenance": "C:\\Users\\13683\\Desktop\\scriptsR\\reproductions\\lin_2026_peri_implantitis\\results\\phase4a\\phase4a_preliminary_integrated.h5ad",
  "seed": 0,
  "mode": "hard",
  "perturb": {
    "tfs": [
      "JUND"
    ],
    "cutoff": 0.001,
    "effects": 0
  },
  "grn_format": "edge_list",
  "grn_columns": {
    "regulator": "source",
    "target": "target",
    "weight": "weight"
  }
}
```

## 解释边界 / Interpretation

这是 regulon-level in silico knockout；不是 CRISPR 实验。横断面疾病组不等价于真实时间。所有缺失图件均为 NOT_RUN 或 NOT_APPLICABLE，不能以教程图替代。