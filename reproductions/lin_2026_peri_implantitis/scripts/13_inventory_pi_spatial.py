"""Inventory PI Space Ranger output without interpreting biology."""
from __future__ import annotations
import json
from pathlib import Path
import scanpy as sc

ROOT=Path(__file__).resolve().parents[1]

def main():
 d=ROOT/'data'/'raw'/'pi_spatial'/'space ranger output'; spatial=d/'spatial'
 out=ROOT/'results'/'phase4b'/'pi_spatial_inventory.json'; out.parent.mkdir(parents=True,exist_ok=True)
 result={'root':str(d),'files':{},'matrices':{},'spatial':{}}
 for p in d.rglob('*'):
  if p.is_file() and '__MACOSX' not in str(p): result['files'][str(p.relative_to(d))]={'bytes':p.stat().st_size}
 for name in ('filtered_feature_bc_matrix.h5','raw_feature_bc_matrix.h5'):
  a=sc.read_10x_h5(d/name)
  result['matrices'][name]={'cells_or_barcodes':int(a.n_obs),'features':int(a.n_vars)}
 positions=spatial/'tissue_positions_list.csv'
 with positions.open(encoding='utf-8') as f: rows=sum(1 for _ in f)
 result['spatial']['tissue_position_rows']=rows
 with positions.open(encoding='utf-8') as f:
  first=f.readline().strip().split(',')
 result['spatial']['tissue_position_columns']=len(first)
 result['spatial']['position_format']='headerless_6_column' if len(first)==6 else 'unknown'
 for name in ('scalefactors_json.json',): result['spatial'][name]=json.loads((spatial/name).read_text(encoding='utf-8'))
 result['spatial']['required_files']=['tissue_hires_image.png','tissue_lowres_image.png','detected_tissue_image.jpg','tissue_positions_list.csv','scalefactors_json.json','aligned_fiducials.jpg','LWM.tif']
 result['spatial']['missing_required']=[name for name in result['spatial']['required_files'] if not (spatial/name).exists()]
 out.write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps({'filtered':result['matrices']['filtered_feature_bc_matrix.h5'],'raw':result['matrices']['raw_feature_bc_matrix.h5'],'positions':rows,'missing_required':result['spatial']['missing_required'],'output':str(out)},indent=2))
if __name__=='__main__': main()
