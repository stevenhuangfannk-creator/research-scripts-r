# 运行环境与依赖

本库以 R 为主，按方法准备依赖。包版本证据见 [package_status.tsv](validation/package_status.tsv) 和 [sessionInfo.txt](validation/sessionInfo.txt)；它们记录 V1 构建时的环境，不保证在新电脑上直接可用。入门步骤见[中文使用指南](USAGE_ZH_CN.md)。

## R 环境

V1 使用 R 4.3.1，并通过 `R_LIBS` 加载额外的独立包库，补充 Matrix 1.6-5 与缺少的 CRAN Windows 二进制包，没有覆盖原有包库。包二进制文件和缓存位于仓库之外，本机路径只作为构建证据，不能作为流程依赖。

在兼容的 R 环境中准备所选方法的依赖，先检查 namespace，再运行对应小示例。完整成功环境确认后，可以按已验证流程建立 `renv` 锁定；当前未提供完整锁定文件。

```r
# 在 R / RStudio 控制台检查所需包；此代码不会安装包。
packages <- c("yaml", "jsonlite", "Seurat", "SeuratObject", "Matrix")
for (pkg in packages) {
  tryCatch({
    loadNamespace(pkg)
    cat(pkg, as.character(packageVersion(pkg)), "OK\n")
  }, error = function(e) cat(pkg, conditionMessage(e), "\n"))
}
```

“已经安装”与“能成功加载”是不同状态。例如 Matrix／Seurat 的版本不兼容时，包可能存在，但 namespace 仍加载失败。

## 尚未完成的环境

V1 的 CellChat 目标为 tag `v2.1.2`，Monocle3 目标为 `v1.4.27`。既有官方接口审查还记录了 CellChat 开发文档版本 `2.2.0.9001`；这些是已记录的目标与审查版本，不是自动追踪的最新版本。

本机验证时缺少 Rtools，CellChat／Monocle3 所需源代码编译与附加依赖尚未齐备。后续需先准备兼容的 R／Bioconductor 环境及官方小示例，再完成运行验证；接口审查通过不能代替执行证据。

Python 方法仍是候选或实验性规划。复现时应分别建立独立环境并记录经过测试的版本，目前没有共享的大型 Python 环境或未经验证的 requirements 锁定。
