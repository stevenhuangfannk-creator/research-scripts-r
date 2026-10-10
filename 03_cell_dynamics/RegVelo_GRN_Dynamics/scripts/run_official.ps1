param([ValidateSet('audit','prepare','fit','velocity','fate','grn','perturb','visualize','report','all')][string]$Stage = 'all',
      [string]$Python = '', [string]$Config = '', [string[]]$TF = @(), [switch]$Resume)
$ErrorActionPreference = 'Stop'
$moduleRoot = Split-Path $PSScriptRoot -Parent
$outputsRoot = (Resolve-Path (Join-Path $moduleRoot '../../..')).Path
if (-not $Python) { $Python = Join-Path $outputsRoot 'regvelo_runtime/.venv/Scripts/python.exe' }
if (-not $Config) { $Config = Join-Path $moduleRoot 'config/official_zebrafish.json' }
if (-not (Test-Path -LiteralPath $Python)) { throw "RegVelo Python not found: $Python. Supply -Python or use bootstrap_windows.ps1." }
$env:OMP_NUM_THREADS = '4'
$env:MKL_NUM_THREADS = '4'
$env:NUMBA_NUM_THREADS = '4'
$arguments = @('-u', (Join-Path $PSScriptRoot 'regvelo.py'), $Stage, '--config', $Config)
if ($TF.Count -gt 0) { $arguments += '--tf'; $arguments += $TF }
if ($Resume) { $arguments += '--resume' }
& $Python @arguments
exit $LASTEXITCODE
