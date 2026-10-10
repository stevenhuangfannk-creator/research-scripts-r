param([Parameter(Mandatory=$true)][string]$RuntimeRoot, [string]$BootstrapPython = 'python')
$ErrorActionPreference = 'Stop'
$moduleRoot = Split-Path $PSScriptRoot -Parent
New-Item -ItemType Directory -Force -Path $RuntimeRoot | Out-Null
$RuntimeRoot = (Resolve-Path -LiteralPath $RuntimeRoot).Path
if (Test-Path -LiteralPath (Join-Path $RuntimeRoot '.venv')) { throw 'Existing environment preserved. Choose a new RuntimeRoot.' }
$toolsRoot = Join-Path $RuntimeRoot 'bootstrap_tools'
& $BootstrapPython -m pip install --target $toolsRoot 'uv==0.13.0'
if ($LASTEXITCODE) { throw 'uv installation failed' }
$uvExe = Join-Path $toolsRoot 'bin/uv.exe'
$env:UV_PYTHON_INSTALL_DIR = Join-Path $RuntimeRoot 'python-managed'
$env:UV_CACHE_DIR = Join-Path $RuntimeRoot 'cache'
& $uvExe python install 3.10.22 --no-bin
if ($LASTEXITCODE) { throw 'Python download failed' }
$basePython = Join-Path $env:UV_PYTHON_INSTALL_DIR 'cpython-3.10.22-windows-x86_64-none/python.exe'
$envPython = Join-Path $RuntimeRoot '.venv/Scripts/python.exe'
& $uvExe venv (Join-Path $RuntimeRoot '.venv') --python $basePython
if ($LASTEXITCODE) { throw 'Environment creation failed' }
& $uvExe pip install --python $envPython 'torch==2.5.1+cu124' --index-url 'https://download.pytorch.org/whl/cu124'
if ($LASTEXITCODE) { throw 'CUDA PyTorch installation failed' }
$env:SETUPTOOLS_SCM_PRETEND_VERSION_FOR_REGVELO = '0.4.2+ae68f699b154'
& $uvExe pip install --python $envPython --extra-index-url 'https://download.pytorch.org/whl/cu124' --index-strategy unsafe-best-match -r (Join-Path $moduleRoot 'DEPENDENCY_LOCK.txt')
if ($LASTEXITCODE) { throw 'Locked dependencies installation failed' }
& $uvExe pip check --python $envPython
if ($LASTEXITCODE) { throw 'Dependency compatibility check failed' }
& $envPython -c 'import torch,regvelo,cellrank,scvelo; print(torch.__version__, torch.cuda.is_available())'
if ($LASTEXITCODE) { throw 'API import check failed' }
Write-Output "Environment ready: $envPython"
