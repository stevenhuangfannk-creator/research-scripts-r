# 扰动稳定性脚本独立审查 / Independent source review

审查范围为 [validate_perturbation.py](../../scripts/validate_perturbation.py) 的数学定义、运行次序与保存逻辑，以及已有正式输入的 cell/gene 索引、终末细胞 JSON 和已保存 blocked-edge 表。**没有运行模型、重新训练或重算稳定性，没有修改运行中的脚本或正式结果。** 本文件的 PASS 仅表示当前配置下源码逻辑符合所声明比较，不是实际稳定性计算的 PASS。

完整只读证据见 [stability_script_readonly_review.json](stability_script_readonly_review.json)。审查时脚本 SHA256 为 `9bd3ad144556fe21e57a464aaa12410f34c165d4bce46715035f5361c3dcffe6`，正式输入为697 cells × 1,007 genes。

## 数学与次序 / Mathematics and order

| 检查 | 源码行为与结论 |
|---|---|
| seed0参考 | grid首先运行seed0、配置cutoff0=0.001、fraction=1；每个TF的reference都在seed1/2、其他cutoff和half比较前建立。 |
| 配对后验 | 每次simulation在官方load及sampling之前执行`_seed`；baseline与KO都通过`TF=[]`及完整`customized_GRN`进入同一官方路径。同seed的baseline用于该seed的KO，避免把原始fate对象当成配对baseline。 |
| 冻结终末细胞 | 相同categorical labels以终末JSON键顺序作为categories；每个模型使用同一批终末cell IDs，随后断言lineage列顺序。实际四组各30个细胞，非空、无重叠，全部在正式cell轴上。 |
| cutoff与强权重half | 使用`fc1[target,regulator]`的对应TF列，按`abs(weight)>cutoff`筛选；稳定降序排列，并选择`ceil(n×0.5)`条最强边。保存目标基因清单。cutoff0下elf1为100条、half50条；nr2f5为106条、half53条。 |
| 数值定义 | 每细胞effect=`||v_KO−v_baseline||₂`；fate delta=`p_KO−p_baseline`。effect的Spearman在同一cell顺序计算；方向判断使用全体细胞的mean fate delta。 |
| 判定范围 | `posterior_seed`比较要求每细胞effect Spearman≥0.8；仅当参考和比较的mean fate delta绝对值都>1e-4时要求同号。fate-delta相关、cutoff及half敏感性是描述性结果，不进入这个PASS判定。 |
| 保存顺序 | 每次已完成的simulation先保存新velocity/fate、transition、概率校验与targets；delta/effect CSV随后保存。整体summary和QC在完整grid结束后保存，中断不等于完整比较完成。 |

`_save_fate`对有限值、概率上下界和行和进行检查；正式fate/model/terminal JSON还由脚本记录并核对hash。若保护文件变化，最终会写PARTIAL并报错。

## 解释限制 / Interpretation limits

1. 如果没有“两侧mean fate delta都大于1e-4”的行，方向筛选为空；`all()`逻辑为true，而`nontrivial_mean_direction_agreement`为null。这表示没有达到阈值的方向证据，不能写成所有生物命运方向都稳定。
2. `both_mean_effects_above_1e4`字段实际阈值是 **1e-4**，其名称有歧义；应以代码和criterion字符串的明确数值解释。
3. 当前simulation复制原始fate对象。源码刷新velocity、fit_t、latent_time_regvelo、fate及transition，但没有刷新继承的`velocity_umap`、`velocity_graph/velocity_graph_neg`、`velocity_std/velocity_uncertainty`及`obs.latent_time`等派生字段。**这些继承字段不能作为本次敏感性的箭头、不确定性或归一化latent-time结果。** 此问题不改变脚本基于新velocity/fate计算的effect/delta CSV；后续清理应在独立stability派生结果中留痕，不覆写正式输入。
4. seed0/1/2只改变一个已训练seed0模型的后验采样。**多训练seed稳定性为NOT_RUN，生物学验证为NOT_RUN。** cutoff和最强half结果描述模型依赖，不证明实验稳健性。

实际计算是否达到criterion应读取运行完成后的`STABILITY_QC.json`及数值表；本审查没有提前赋予那些结果PASS。
