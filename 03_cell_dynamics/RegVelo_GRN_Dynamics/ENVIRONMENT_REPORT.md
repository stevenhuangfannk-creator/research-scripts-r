# 独立环境与版本核验 / Environment report

2026-10-10 实际创建并测试 Windows x86_64、CPython **3.10.22** 独立环境。未修改系统 Python、R、原有 Scanpy/Seurat 环境，未安装或重装 WSL。

| 项目 | 实测结果 |
|---|---|
| OS | Windows 11 Home，build 26200 |
| CPU | Intel i9-13900HX，24 cores / 32 logical processors；流程限制 OMP/MKL/Numba 为 4 threads |
| RAM | 总计约 15.7 GiB；开始时仅约 0.8 GiB free，Windows pagefile 可用；没有终止用户程序 |
| GPU | NVIDIA GeForce RTX 4070 Laptop GPU，8188 MiB |
| Driver / CUDA | 596.08；driver capability 13.2，实际 PyTorch runtime CUDA **12.4**，二者不是同一版本含义 |
| Disk | C: 开始时约 267 GiB free |
| WSL | `wsl --list --verbose` 表明尚未安装 distribution；不依赖 WSL |
| PyTorch | **2.5.1+cu124**；`cuda.is_available()` true，GPU train 已执行 |
| RegVelo | **0.4.2+ae68f699b154**，官方源码 SHA `ae68f699b154b0559598e8f09e9ae4f30206975d`；后缀为本地源码来源标记，不冒充官方 tag |
| scvi / Scanpy / scVelo / CellRank | 1.2.0 / 1.10.4 / 0.3.3 / 2.0.7 |
| AnnData / NumPy / SciPy / JAX | 0.11.4 / 1.26.4 / 1.13.1 / 0.4.35 |
| 依赖检查 | `uv pip check`：128 packages checked，PASS；官方 API import、CUDA probe：PASS |
| 收尾复核 | 独立环境补充 **pip 26.2.1** 后，`python -m pip check`：PASS；`python -m pip freeze --all` 记录129条包来源/版本 |

完整安装版本见 [DEPENDENCY_LOCK.txt](DEPENDENCY_LOCK.txt)，运行机器的 executable/version/CUDA 信息保存在独立 runtime 的 `environment.json`。源码 BSD-3-Clause；论文与数据许可仍按各来源要求使用。

收尾的真实命令与日志见 [finish_checks_summary.json](tests/validation_logs/finish_checks_summary.json)。`installed-freeze.txt` 保留实际本地安装来源；发布用锁将 RegVelo 的本地 file URI 替换为同一固定 SHA 的官方下载地址，其余版本来自实际 `pip freeze --all`。这次复核没有重建环境；clean-room bootstrap 状态仍如下所述。

## 环境位置 / Location

与本 repo 同级的 `regvelo_runtime/.venv/Scripts/python.exe` 是专用 Python。其 standalone base interpreter 也持久保存在 `regvelo_runtime/python`，不依赖临时 work 文件夹。运行脚本会优先查这个路径；其他机器通过 `-Python` 显式指定。

```powershell
# 在本模块根目录；首次在其他机器创建一个全新的隔离目录
powershell -ExecutionPolicy Bypass -File scripts/bootstrap_windows.ps1 -RuntimeRoot C:/Research/RegVelo/runtime
# 已有本次 runtime 时直接执行，不重复安装
powershell -ExecutionPolicy Bypass -File scripts/run_official.ps1 -Stage audit
```

bootstrap 脚本使用与本次相同的 uv→CPython→CUDA torch→固定依赖与源码步骤，但整份 bootstrap 的 clean-room 重建尚未另行执行；本次实际环境创建、依赖解析、import 和 GPU smoke 已执行。Windows锁不等价于Linux环境验证，Linux/WSL标 NOT_RUN。不要求管理员或全局 CUDA toolkit。

## 资源与偏离 / Resources and deviations

全量官方数据 697 cells；预处理按官方速度基因与 GRN 规则筛选至 1,007 genes，并保留所有细胞。正式配置 max_epochs=1500、early stopping patience=45（官方实现），batch_size=256 与官方默认 full batch 不同，以降低峰值内存；完整记录保存在 `fit_qc.json`。小样本 smoke 使用200cells/2epochs，不作为正式复现证据。

首次真实 smoke 发现 CLI 文件与包同名导致导入冲突，以及 scvi history 以 object dtype 存数值导致有限值检查失败；均已修复并重跑。原始错误日志保留，正式结果以最终 `run_state.json` 与 QC 为准。
