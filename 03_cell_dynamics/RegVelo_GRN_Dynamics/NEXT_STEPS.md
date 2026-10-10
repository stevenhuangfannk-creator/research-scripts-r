# 下一步 / Next steps

1. 现有官方案例可直接查看27图和完整模型；用run_official.ps1 -Stage all -Resume验证恢复，不必重训。修改TF只执行perturb，避免整体config hash改变重跑训练。
2. 如需论文数值级比较，再完成同输入完整训练seed1/2、正式soft/soft_regularized及统一ModelComparison；目前小样本测试与后验seed稳定性不能替代。
3. 分别审查mNC_arch2含8个arch1的终末边界，以及与scVelo约20.23%投影方向分歧；运行邻域/terminal敏感性后再扩大生物学论断。
4. 匹配官方Perturb-seq真实观测、核实原始Smart-seq3 accession及批次条件；现有AUC/p只解释为模型内预测。
5. PI先从Lin完整2996成纤维细胞（D3/D4/D6等供者）做GRN活动与状态连续性审查，第二候选为1410巨噬；JUND/RELA/STAT3/CEBPB均为待审候选，不预设driver。
6. 先取得单文库raw run清单、chemistry、文件大小与参考注释，限定一次剪接重计数试验；真实S/U、ID对齐、供者/深度/方向QC通过后才由NOT_READY转CONDITIONAL/READY。现有横断面组别与归一化counts不构造时间或剪接层。
7. 后续单独执行clean-room Windows bootstrap、Linux/WSL环境复核；Workbench adapter仍Planned，按其既有审核流程决定是否确认知识节点。
