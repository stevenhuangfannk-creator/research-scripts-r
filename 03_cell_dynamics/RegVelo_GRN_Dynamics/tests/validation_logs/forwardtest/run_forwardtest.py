import json
import os
import subprocess
import sys
from pathlib import Path

import anndata as ad
import h5py
import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix

BASE = Path(__file__).resolve().parent
WORKSPACE = BASE.parent.parent
MODULE = WORKSPACE / 'outputs/research-scripts-r/03_cell_dynamics/RegVelo_GRN_Dynamics'
SCRIPT = MODULE / 'scripts/regvelo.py'
SOURCE = Path('C:/Users/13683/Desktop/scriptsR/reproductions/lin_2026_peri_implantitis/results/phase4a/phase4a_preliminary_integrated.h5ad')
PRIOR = Path('C:/Users/13683/Documents/Codex/2026-10-08/files-pasted-by-the-user-codex/outputs/tf-regulatory-network-atlas/data/cache/collectri.csv')

def read_rows(node, rows, n_columns):
    pointers = node['indptr'][:]
    values, indices, result_ptr = [], [], [0]
    for row in rows:
        start, stop = int(pointers[row]), int(pointers[row + 1])
        values.append(node['data'][start:stop])
        indices.append(node['indices'][start:stop])
        result_ptr.append(result_ptr[-1] + stop - start)
    return csr_matrix((np.concatenate(values), np.concatenate(indices), np.asarray(result_ptr)), shape=(len(rows), n_columns))

with h5py.File(SOURCE, 'r') as handle:
    obs = ad.io.read_elem(handle['obs'])
    var = ad.io.read_elem(handle['var'])
    rows = np.flatnonzero(obs['major_cell_type'].astype(str).to_numpy() == 'Fibroblasts')[:32]
    data = ad.AnnData(X=read_rows(handle['X'], rows, len(var)), obs=obs.iloc[rows].copy(), var=var.copy())
    for layer, node in handle['layers'].items():
        data.layers[layer] = read_rows(node, rows, len(var))
    data.uns['forwardtest_provenance'] = {
        'source_path': str(SOURCE), 'selection': 'first 32 existing major_cell_type=Fibroblasts, deterministic audit-only subset',
        'source_n_cells': len(obs), 'source_layers': list(handle['layers']),
        'matrix_values': 'source row values copied exactly; no synthetic RNA layers, normalization or gene filtering',
        'scope': 'low-cost interface audit; not training, dynamics or prediction',
    }
data.obs_names = pd.Index(data.obs_names.astype(str))
data.var_names = pd.Index(data.var_names.astype(str))
probe = BASE / 'canonical_fibroblasts_32_audit_only.h5ad'
data.write_h5ad(probe, compression='gzip')
config = {
    'input': str(probe), 'grn': str(PRIOR), 'output': 'run',
    'grn_orientation': 'regulator_by_target', 'group_key': 'major_cell_type', 'time_key': None,
    'species': 'Homo sapiens', 'gene_id_type': 'gene_symbol',
    'input_provenance': str(SOURCE), 'seed': 0, 'mode': 'hard',
    'perturb': {'tfs': ['JUND'], 'cutoff': 0.001, 'effects': 0},
}
config_path = BASE / 'job.json'
config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding='utf-8')

environment = os.environ.copy()
environment['PYTHONIOENCODING'] = 'utf-8'
environment['OMP_NUM_THREADS'] = '4'
records = []
commands = [
    ('help', [sys.executable, str(SCRIPT), '--help']),
    ('audit', [sys.executable, str(SCRIPT), 'audit', '--config', str(config_path)]),
    ('report', [sys.executable, str(SCRIPT), 'report', '--config', str(config_path)]),
    ('pip_check', [sys.executable, '-m', 'pip', 'check']),
]
for name, command in commands:
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', env=environment, timeout=60)
    log = BASE / f'{name}_stdout_stderr.log'
    log.write_text(result.stdout + result.stderr, encoding='utf-8')
    records.append({'test': name, 'command': command, 'exit_code': result.returncode, 'log': str(log)})
    print(f'{name}: exit={result.returncode}; log={log}')
    if name == 'audit':
        print((result.stdout + result.stderr).strip())

sys.path.insert(0, str(MODULE / 'src'))
from regvelo_workflow.core import validate_grn
try:
    validate_grn(pd.read_csv(PRIOR, index_col=0), data.var_names, 'regulator_by_target')
    prior_result = {'status': 'PASS'}
except Exception as error:
    prior_result = {'status': 'FAIL', 'error': f'{type(error).__name__}: {error}'}
(BASE / 'prior_direct_validator.json').write_text(json.dumps(prior_result, indent=2), encoding='utf-8')
(BASE / 'commands.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'prior validator: {prior_result}')
