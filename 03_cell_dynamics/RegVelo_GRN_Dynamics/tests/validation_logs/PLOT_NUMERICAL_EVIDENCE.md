# 核心图件数值核对 / Core plot evidence check

状态：PASS。仅只读核对；检查期间所有受检文件SHA-256保持不变。

- A03：697个细胞顺序与官方输入一致，真实spliced/unspliced层总量及检出基因数逐细胞匹配；单位是预处理层数值，图件没有改称原始UMI。
- B03：导出的latent_time与velocity.h5ad保存obs值一致，严格等于mean fit_t的min-max缩放；数值有限，范围[0,1]。
- B06：真实保存的velocity_std层为697×1007，有限且非负；导出的697个值匹配逐细胞跨基因平均标准差。
- B07：RegVelo与scVelo的697个细胞、1007个基因及UMAP顺序完全一致；两组箭头分量分别来自各自保存velocity_umap；细胞类型标签与原始输入一致。
- 元数据将速度、潜在时间、不确定性和比较标为Model-predicted，明确限制真实时钟、运动和真值结论。本次受检图表数据未见随机或合成替代值。

注意：velocity_qc.json的latent_time_range字段记录未缩放mean fit_t（4.462–8.328），而保存obs latent_time及B03为[0,1]；建议字段命名明确该区别。

边界：数值一致性不证明动力学方向、收敛或生物学可靠性；未重新生成后验抽样。完整逐项误差与SHA-256见evidence.json。
