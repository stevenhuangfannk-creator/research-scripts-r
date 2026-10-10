import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
evidence = json.loads((BASE / 'input_evidence.json').read_text(encoding='utf-8'))
paths = [Path(record['path']) for record in evidence['h5ad']]

def fingerprint(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(block)
    stat = path.stat()
    return {'sha256': digest.hexdigest(), 'size_bytes': stat.st_size, 'mtime_ns': stat.st_mtime_ns}

before = {str(path): fingerprint(path) for path in paths}
subprocess.run([sys.executable, str(BASE / 'inspect_inputs.py')], check=True, capture_output=True)
after = {str(path): fingerprint(path) for path in paths}
report = {'before': before, 'after': after, 'unchanged': before == after,
          'comparison_scope': 'SHA256 and mtime before/after independent repeated h5py read-only inspection',
          'canonical_prior_record_sha256': 'c96701c4e0d079b8e9c08b8fbcd754910040367399f6884300852b8ea72e9f0a',
          'canonical_matches_prior_record': before[str(paths[0])]['sha256'] == 'c96701c4e0d079b8e9c08b8fbcd754910040367399f6884300852b8ea72e9f0a'}
(BASE / 'source_readonly_hashes.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
environment = os.environ.copy()
environment['PYTHONIOENCODING'] = 'utf-8'
environment['OMP_NUM_THREADS'] = '4'
command = [sys.executable, '-c', 'import regvelo as rgv; print("version", rgv.__version__); print("REGVELOVI", rgv.REGVELOVI.__name__); print("official_perturbation", callable(rgv.tl.in_silico_block_simulation))']
result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8', env=environment, timeout=60)
(BASE / 'api_import_stdout_stderr.log').write_text(result.stdout + result.stderr, encoding='utf-8')
(BASE / 'api_import_command.json').write_text(json.dumps({'command': command, 'exit_code': result.returncode}, indent=2), encoding='utf-8')
print('API import exit', result.returncode)
print(result.stdout + result.stderr)
