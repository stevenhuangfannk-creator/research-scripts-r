"""Read-only local HDF5 admission evidence; does not run velocity or modify inputs."""
from pathlib import Path
import csv
import gzip
import hashlib
import json
from collections import Counter
import h5py
import numpy as np

HERE = Path(__file__).resolve().parent
ATLAS = Path('C:/Users/13683/Documents/Codex/2026-10-07/files-pasted-by-the-user-project/outputs/oral_scrna_data')
LIN = Path('C:/Users/13683/Desktop/scriptsR/reproductions/lin_2026_peri_implantitis')
TF = Path('C:/Users/13683/Documents/Codex/2026-10-08/files-pasted-by-the-user-codex/outputs/tf-regulatory-network-atlas')
INPUTS = [LIN / 'results/phase4a/phase4a_preliminary_integrated.h5ad']
INPUTS += [ATLAS / d / 'objects' / n for d, n in [
    ('GSE310110', 'GSE310110_annotated_v0.4.h5ad'),
    ('GSE272774', 'GSE272774_annotated_v0.4.h5ad'),
    ('GSE294615', 'GSE294615_annotated_v0.3.h5ad'),
    ('GSE188217', 'GSE188217_annotated_v0.1.h5ad'),
    ('GSE310110', 'GSE310110_Endothelial_cell_reuse_v0.4.h5ad'),
    ('zenodo.19697597', 'zenodo.19697597_Macrophage_reuse_v0.2.h5ad'),
]]
INPUTS += [TF / 'data/raw/periodontal_atlas.h5ad']

def decode(a):
    return np.asarray([v.decode('utf-8') if isinstance(v, bytes) else str(v) for v in a])

def column(g, key):
    node = g[key]
    if isinstance(node, h5py.Dataset):
        a = node[()]
        return decode(a) if a.dtype.kind in 'OSU' else a
    if 'codes' in node and 'categories' in node:
        codes = node['codes'][()]
        categories = decode(node['categories'][()])
        return np.asarray([categories[i] if i >= 0 else '<NA>' for i in codes])
    if 'values' in node and 'mask' in node:
        a = node['values'][()]
        a = decode(a) if a.dtype.kind in 'OSU' else a
        if a.dtype.kind in 'OSU':
            a[node['mask'][()]] = '<NA>'
        return a
    return None

def matrix_stats(node):
    if isinstance(node, h5py.Group):
        shape = [int(x) for x in node.attrs['shape']]
        ds = node['data']
    else:
        shape = list(node.shape)
        ds = node
    out = {'shape': shape, 'storage': str(node.attrs.get('encoding-type', 'dense')),
           'dtype': str(ds.dtype), 'stored_values': int(ds.size)}
    total = 0.0
    nonzero = 0
    finite = True
    integer = True
    minimum, maximum = float('inf'), float('-inf')
    # CSR data stream or row blocks for dense matrices, never a full dense conversion.
    step = 1000000 if ds.ndim == 1 else 256
    chunks = (ds[i:i+step] for i in range(0, ds.shape[0], step))
    for a in chunks:
        finite &= bool(np.isfinite(a).all())
        integer &= bool((a == np.floor(a)).all())
        total += float(a.sum(dtype=np.float64))
        nonzero += int(np.count_nonzero(a))
        if a.size:
            minimum = min(minimum, float(a.min()))
            maximum = max(maximum, float(a.max()))
    out.update(nonzero=nonzero, finite=finite, integer_valued=integer, minimum_stored=minimum,
               maximum_stored=maximum, total=total,
               zero_fraction=1-nonzero/(shape[0]*shape[1]))
    return out

def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8*1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

records = []
genesets = {}
common_genesets = {}
for path in INPUTS:
    if not path.is_file():
        records.append({'path': str(path), 'exists': False})
        continue
    rec = {'path': str(path), 'exists': True, 'bytes': path.stat().st_size}
    with h5py.File(path, 'r') as f:
        rec['root_keys'] = list(f.keys())
        rec['layers'] = {k: matrix_stats(f['layers'][k]) for k in f.get('layers', {})}
        rec['X'] = matrix_stats(f['X'])
        rec['raw_X'] = matrix_stats(f['raw/X']) if 'raw/X' in f else None
        rec['obs_keys'] = list(f['obs'].keys())
        rec['var_keys'] = list(f['var'].keys())
        rec['obsm'] = list(f.get('obsm', {}).keys())
        rec['obsp'] = list(f.get('obsp', {}).keys())
        rec['uns_keys'] = list(f.get('uns', {}).keys())
        rec['n_cells'], rec['n_genes'] = rec['X']['shape']
        rec['metadata_counts'] = {}
        rec['qc_metrics'] = {}
        for k in ['n_genes_by_counts', 'total_counts', 'pct_counts_mt']:
            if k in f['obs']:
                a = column(f['obs'], k)
                rec['qc_metrics'][k] = {str(q):float(np.quantile(a, q)) for q in [0, 0.25, 0.5, 0.75, 1]}
        cols = {}
        for k in rec['obs_keys']:
            if any(w in k.lower() for w in ['sample', 'donor', 'condition', 'disease', 'celltype', 'cell_type', 'label', 'state', 'study', 'assay', 'time', 'batch']):
                a = column(f['obs'], k)
                if a is not None and len(a) == rec['n_cells']:
                    cols[k] = a
                    c = Counter(str(x) for x in a)
                    rec['metadata_counts'][k] = dict(c) if len(c) <= 100 else {'unique_count': len(c)}
        symbol_key = next((k for k in ['gene_symbol', 'gene_symbols', 'feature_name', 'symbol', 'gene_name', '_index'] if k in f['var']), None)
        if symbol_key:
            symbols = decode(column(f['var'], symbol_key))
            genesets[str(path)] = set(symbols.tolist())
            rec['symbol_key'] = symbol_key
            rec['symbols_head'] = symbols[:8].tolist()
            rec['unique_symbols'] = int(len(set(symbols.tolist())))
            rec['JUND_in_symbol_axis'] = bool('JUND' in symbols)
            rec['mouse_Jund_in_symbol_axis'] = bool('Jund' in symbols)
            if 'shared_gene_for_analysis' in f['var']:
                common_genesets[str(path)] = set(symbols[np.asarray(column(f['var'], 'shared_gene_for_analysis'), dtype=bool)].tolist())
        rec['source_gene_flags'] = {}
        for k in f['var']:
            if k.startswith('source_present_') or k in ['shared_gene_for_analysis', 'source_symbol_conflict']:
                a = column(f['var'], k)
                rec['source_gene_flags'][k] = int(np.asarray(a, dtype=bool).sum())
        # Preserve donor representation of each provisional broad cell class.
        ct = next((k for k in ['major_cell_type', 'celltype_major', 'celltype_broad', 'celltype', 'cell_type', 'major_celltype', 'cell_type_coarse', 'celltype_final', 'celltype_curated_v2'] if k in cols), None)
        sample = next((k for k in ['sample_id', 'sample', 'sample_name', 'donor_id', 'donor'] if k in cols), None)
        if ct and sample:
            rec['celltype_sample_cross_tab'] = {
                name: dict(Counter(str(x) for x in cols[sample][cols[ct] == name]))
                for name in np.unique(cols[ct])
            }
    rec['sha256'] = sha256(path)
    records.append(rec)
    print(json.dumps({k:rec[k] for k in ['path', 'n_cells', 'n_genes', 'layers', 'symbol_key', 'JUND_in_symbol_axis', 'metadata_counts'] if k in rec}, ensure_ascii=False), flush=True)

raw10x = []
for path in sorted((LIN / 'data/raw/pi_scrna').rglob('*.h5')):
    if '__MACOSX' in str(path):
        continue
    with h5py.File(path, 'r') as f:
        raw10x.append({'path':str(path), 'root_keys':list(f.keys()), 'matrix_keys':list(f['matrix'].keys()),
                      'shape_genes_cells':f['matrix/shape'][()].tolist(),
                      'feature_keys':list(f['matrix/features'].keys()), 'layers_spliced_unspliced_present':False})

netpath = TF / 'data/cache/collectri.csv'
network = {'path':str(netpath), 'exists':netpath.is_file()}
if netpath.is_file():
    with netpath.open(encoding='utf-8-sig', newline='') as f:
        edges = list(csv.DictReader(f))
    network['columns'] = list(edges[0])
    network['row_count'] = len(edges)
    source = next(k for k in ['source', 'tf', 'TF'] if k in edges[0])
    target = next(k for k in ['target', 'gene', 'Target'] if k in edges[0])
    sources = set(e[source] for e in edges)
    targets = set(e[target] for e in edges)
    network['regulator_count'] = len(sources)
    network['target_count'] = len(targets)
    network['JUND_targets'] = sorted(set(e[target] for e in edges if e[source] == 'JUND'))
    network['JUND_target_count'] = len(network['JUND_targets'])
    network['overlap_by_input'] = {}
    for path, genes in genesets.items():
        aligned = [e for e in edges if e[source] in genes and e[target] in genes]
        network['overlap_by_input'][path] = {'regulators':len(set(e[source] for e in aligned)),
            'targets':len(set(e[target] for e in aligned)), 'edges':len(aligned),
            'JUND_edges':sum(e[source] == 'JUND' for e in aligned),
            'gene_symbol_intersection_only':True, 'species_remap_or_regvelo_validation_performed':False}
        if path in common_genesets:
            shared = common_genesets[path]
            common_edges = [e for e in edges if e[source] in shared and e[target] in shared]
            network['overlap_by_input'][path]['shared_gene_for_analysis_overlap'] = {
                'genes':len(shared), 'regulators':len(set(e[source] for e in common_edges)),
                'targets':len(set(e[target] for e in common_edges)), 'edges':len(common_edges),
                'JUND_edges':sum(e[source] == 'JUND' for e in common_edges)}
    network['sha256'] = sha256(netpath)
    print(json.dumps({'network':network}, ensure_ascii=False), flush=True)

overlay_path = LIN / 'results/phase4a/myeloid_plasma_audit/curated_v2_annotations.tsv.gz'
with gzip.open(overlay_path, 'rt', encoding='utf-8-sig', newline='') as fh:
    overlay_rows = list(csv.DictReader(fh, delimiter='\t'))
overlay = {'path':str(overlay_path), 'sha256':sha256(overlay_path), 'rows':len(overlay_rows),
           'columns':list(overlay_rows[0])}
with h5py.File(INPUTS[0], 'r') as f:
    cell_ids = column(f['obs'], '_index')
    conditions = column(f['obs'], 'condition')
    donors = column(f['obs'], 'donor_id')
    samples = column(f['obs'], 'sample_id')
    overlay_map = {r['cell_id']:r for r in overlay_rows}
    assert len(overlay_map) == len(overlay_rows)
    assert set(cell_ids) == set(overlay_map)
    overlay['exact_cell_id_alignment'] = True
    overlay['condition_summary'] = {}
    for cond in np.unique(conditions):
        idx = np.flatnonzero(conditions == cond)
        labels = [overlay_map[cell_ids[i]]['major_cell_type'] for i in idx]
        overlay['condition_summary'][str(cond)] = {
            'cells':len(idx), 'donors':len(set(donors[idx])), 'libraries':len(set(samples[idx])),
            'celltype_counts':dict(Counter(labels)),
            'celltype_donor_counts':{ct:dict(Counter(str(donors[i]) for i in idx if overlay_map[cell_ids[i]]['major_cell_type']==ct)) for ct in set(labels)}}

HERE.mkdir(parents=True, exist_ok=True)
(HERE / 'h5ad_layer_evidence.json').write_text(json.dumps({'audit_date':'2026-10-10',
    'mode':'h5py read-only; complete stored matrix values scanned; input SHA256 recomputed',
    'objects':records, 'lin_raw_10x_h5':raw10x, 'collectri':network, 'lin_curated_overlay':overlay}, ensure_ascii=False, indent=2), encoding='utf-8')
