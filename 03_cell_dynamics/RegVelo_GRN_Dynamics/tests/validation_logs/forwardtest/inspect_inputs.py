import json
import sys
from pathlib import Path
from importlib import metadata

import h5py
import pandas as pd

BASE = Path(__file__).resolve().parent
PROJECT = Path('C:/Users/13683/Desktop/scriptsR/reproductions/lin_2026_peri_implantitis')
INPUTS = [
    PROJECT / 'results/phase4a/phase4a_preliminary_integrated.h5ad',
    PROJECT / 'results/phase4b/cell2location_input/curated_v2/scrna_reference_counts.h5ad',
]
PRIOR = Path('C:/Users/13683/Documents/Codex/2026-10-08/files-pasted-by-the-user-codex/outputs/tf-regulatory-network-atlas/data/cache/collectri.csv')

def strings(node):
    if isinstance(node, h5py.Group) and 'values' in node:
        return strings(node['values'])
    if isinstance(node, h5py.Group) and 'categories' in node:
        categories = strings(node['categories'])
        return [categories[int(code)] if code >= 0 else '' for code in node['codes'][:]]
    values = node[:]
    return [v.decode('utf-8') if isinstance(v, bytes) else str(v) for v in values]

def shape(node):
    dims = node.attrs['shape'] if isinstance(node, h5py.Group) and 'shape' in node.attrs else node.shape
    return [int(value) for value in dims]

records = []
for path in INPUTS:
    with h5py.File(path, 'r') as handle:
        var_key = handle['var'].attrs.get('_index', '_index')
        obs_key = handle['obs'].attrs.get('_index', '_index')
        genes = strings(handle['var'][var_key])
        cells = strings(handle['obs'][obs_key])
        annotations = {}
        for key, node in handle['obs'].items():
            if isinstance(node, h5py.Group) and 'categories' in node:
                categories = strings(node['categories'])
                codes = node['codes'][:]
                annotations[key] = {value: int((codes == idx).sum()) for idx, value in enumerate(categories)}
        records.append({
            'path': str(path), 'size_bytes': path.stat().st_size,
            'n_cells': len(cells), 'n_genes': len(genes),
            'unique_cells': len(set(cells)) == len(cells), 'unique_genes': len(set(genes)) == len(genes),
            'JUND_in_var_names': 'JUND' in genes, 'var_columns': list(handle['var']),
            'layers': {key: shape(node) for key, node in handle.get('layers', {}).items()},
            'X_shape': shape(handle['X']), 'obs_columns': list(handle['obs']),
            'categorical_counts': annotations,
        })
frame = pd.read_csv(PRIOR)
jund = frame.loc[frame['source'] == 'JUND']
prior = {'path': str(PRIOR), 'format': 'edge_list', 'columns': list(frame.columns),
         'n_edges': len(frame), 'n_exact_JUND_edges': len(jund),
         'n_exact_JUND_targets': jund['target'].nunique(),
         'JUND_weight_values': sorted(jund['weight'].unique().tolist())}
versions = {'python': sys.version, 'executable': sys.executable}
for package in ['regvelo', 'torch', 'scvi-tools', 'scanpy', 'scvelo', 'cellrank', 'anndata', 'h5py', 'pandas']:
    try:
        versions[package] = metadata.version(package)
    except metadata.PackageNotFoundError:
        versions[package] = 'NOT_INSTALLED'
report = {'h5ad': records, 'prior': prior, 'environment': versions}
(BASE / 'input_evidence.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
for record in records:
    print(json.dumps({key: record[key] for key in ['path', 'n_cells', 'n_genes', 'layers', 'JUND_in_var_names', 'obs_columns']}, ensure_ascii=False))
print(json.dumps(prior, ensure_ascii=False))
print(json.dumps(versions, ensure_ascii=False))
