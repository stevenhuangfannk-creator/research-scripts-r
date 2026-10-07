# 单细胞质量控制（scrna_qc）

计算线粒体/核糖体比例，结合 feature 和 UMI 数检查细胞质量，并记录保留情况。

方法状态：VALIDATED；执行验证：PASS。[方法卡](METHOD_CARD.md) · [输出说明](OUTPUT_CATALOG.md) · [示例与验证](examples/README.md) · [图例入口](gallery/README.md) · [配置](config/default.yml)

## 准备什么输入

含 RNA counts 的 Seurat 对象（RDS）。基因名应能够匹配所选物种的 mt_pattern/ribo_pattern；元数据须含 nFeature_RNA 和 nCount_RNA。

## 包在这里如何使用

Seurat::PercentageFeatureSet() 计算 percent.mt/percent.ribo；按给定阈值生成 qc_pass，必要时用 subset() 过滤。qc.tsv 始终记录过滤前的全部细胞。

## 配置哪些参数

mt_pattern、ribo_pattern 为正则表达式；thresholds 必须是包含 min_features、max_features、min_counts、max_counts、max_mt 的数值列表。filter: false 仅标记 qc_pass，true 才过滤细胞。核糖体比例会计算，但当前不用于 qc_pass。

## 运行方式

先在仓库根目录打开 R/终端，核对本地依赖（Seurat，以及统一入口使用的 yaml）。脚本不会自动安装包。将配置中的 input 指向真实输入 RDS，output_dir 设为本次运行目录；所有相对路径按仓库根目录解析。每次运行使用独立 output_dir，避免覆盖前次结果。

默认配置是起点，请先复制为自己的配置或修改必要字段。核对输入要求与参数后，在仓库根目录运行：

```powershell
Rscript scripts/run_method.R scrna_qc 01_scrna_core/quality_control/config/default.yml
```

工作流：[workflow.R](scripts/workflow.R)；统一入口：[run_method.R](../../scripts/run_method.R)。现有 PASS 仅覆盖方法卡所列范围，首次用于真实数据仍应核查结果。

默认配置里的基因模式和 thresholds 是说明性占位，不能原样运行。下面仅展示“人类基因符号 + 不筛除细胞的审计”配置格式，不是生物学推荐阈值；物种、模式和阈值需按数据修改：

```yaml
input: data/input.rds
output_dir: results/scrna_qc
mt_pattern: "^MT-"
ribo_pattern: "^RP[SL]"
thresholds:
  min_features: 0
  max_features: .inf
  min_counts: 0
  max_counts: .inf
  max_mt: 100
filter: false
```

小鼠符号通常需改为 ^mt-、^Rp[sl]；若出现“无匹配基因”警告，先核查 feature ID。

## 结果与边界

输出写入配置的 output_dir，具体文件见[输出说明](OUTPUT_CATALOG.md)。统一入口还会保存 sessionInfo.txt 和 run_metadata.yml。

没有通用的线粒体比例阈值。统一阈值可能去除真实损伤状态，应按组织与 capture 检查分布。QC 不能替代 doublet/ambient RNA 检测；使用 Ensembl ID 时不能直接假定 ^MT- 能匹配。

PASS：pbmc_small 本身缺少线粒体/核糖体基因，现有验证覆盖审计/过滤及额外三基因测试中的精确比例计算；没有验证真实组织的最佳 QC 阈值。
