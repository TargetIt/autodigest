#!/usr/bin/env python3
"""Bounded, dependency-free Archify CLI checks; run from any working directory.

Only writes this evidence directory. Existing result files are replaced on rerun.
Does not import upstream test suites, install dependencies, or launch browsers.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import time

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent.parent
REPO = RESEARCH / 'repos/tt-a1i/archify'
SHA = 'd0c8c7e9f4e06f303389f804208d387f27019ef5'
CLI = REPO / 'archify/bin/archify.mjs'
EXAMPLE = REPO / 'archify/examples/web-app.architecture.json'
NODE = shutil.which('node')
ARTIFACT = HERE / 'sample-web-app.html'
PROVENANCE = HERE / 'sample-web-app.delivery.json'
NETWORK_LOG = HERE / 'network-attempts.jsonl'
ENV = dict(os.environ)
ENV.update(ARCHIFY_UPDATE_CHECK_DISABLED='1',
           ARCHIFY_RESEARCH_NETWORK_LOG=str(NETWORK_LOG),
           NODE_OPTIONS='--require=' + str(HERE / 'no-network.cjs'))

def run_readonly_git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args], text=True).strip()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def portable(value):
    # Receipts are verbatim except this disclosed filesystem-root redaction.
    return value.replace(str(RESEARCH), 'Research')

def save_json(name, value):
    (HERE / name).write_text(portable(json.dumps(value, ensure_ascii=False, indent=2)) + '\n')

assert run_readonly_git('rev-parse', 'HEAD') == SHA
assert run_readonly_git('status', '--porcelain=v1') == ''
assert NODE is not None
NETWORK_LOG.write_text('')
fixture = json.loads(EXAMPLE.read_text())
assert not any(node.get('brand') or node.get('sources') for node in fixture['components'])
bad_node = copy.deepcopy(fixture)
bad_node['components'][0]['type'] = 'not-a-supported-component-type'
bad_reference = copy.deepcopy(fixture)
bad_reference['connections'][0]['to'] = 'missing-node-for-research-check'
save_json('invalid-component.architecture.json', bad_node)
save_json('invalid-reference.architecture.json', bad_reference)
results = []
commands = ['# Run from autodigest/; every Node child inherits the network guard and update-disable flag.',
            'export ARCHIFY_UPDATE_CHECK_DISABLED=1',
            'export ARCHIFY_RESEARCH_NETWORK_LOG="$PWD/Research/evidence/archify/network-attempts.jsonl"',
            'export NODE_OPTIONS="--require=$PWD/Research/evidence/archify/no-network.cjs"', '']

def case(name, args, expected_exit, expected_ok=None, expected_code=None):
    command = [NODE, str(CLI), *map(str, args)]
    before = digest(ARTIFACT) if ARTIFACT.exists() else None
    started = time.monotonic()
    proc = subprocess.run(command, cwd=HERE, env=ENV, text=True, capture_output=True, timeout=45)
    elapsed = round(time.monotonic() - started, 3)
    stdout = portable(proc.stdout)
    stderr = portable(proc.stderr)
    (HERE / f'{name}.stdout.txt').write_text(stdout)
    (HERE / f'{name}.stderr.txt').write_text(stderr)
    receipt = json.loads(proc.stdout) if proc.stdout.lstrip().startswith('{') else None
    codes = [d.get('code') for d in (receipt or {}).get('diagnostics', [])]
    after = digest(ARTIFACT) if ARTIFACT.exists() else None
    result = dict(name=name, exit_code=proc.returncode, expected_exit=expected_exit,
                  ok=(receipt or {}).get('ok'), stage=(receipt or {}).get('stage'),
                  diagnostic_codes=codes, elapsed_seconds=elapsed,
                  artifact_sha256_before=before, artifact_sha256_after=after)
    if receipt:
        result['update'] = receipt.get('update')
        result['validation'] = receipt.get('validation')
    results.append(result)
    commands.extend(['# ' + name + ': expected exit ' + str(expected_exit),
                     shlex.join(['node', portable(str(CLI)), *[portable(str(x)) for x in args]]), ''])
    save_json('results.json', {'repository': 'tt-a1i/archify', 'commit': SHA, 'cases': results})
    (HERE / 'commands.sh').write_text('\n'.join(commands))
    print(name, proc.returncode, result['stage'], codes, flush=True)
    assert proc.returncode == expected_exit, stdout[:2000] + stderr[:2000]
    if expected_ok is not None:
        assert receipt['ok'] == expected_ok
    if expected_code is not None:
        assert expected_code in codes, codes
    return receipt

case('01-validate-official', ['validate', 'architecture', EXAMPLE, '--json'], 0, True)
case('02-render-official', ['render', 'architecture', EXAMPLE, ARTIFACT], 0)
good = case('03-deliver-official', ['deliver', 'architecture', EXAMPLE, ARTIFACT, '--json'], 0, True)
assert good['update']['reason'] == 'disabled'
lastgood = digest(ARTIFACT)
save_json('provenance-before-failure.json', json.loads(PROVENANCE.read_text()))
case('04-reject-invalid-component', ['validate', 'architecture', HERE / 'invalid-component.architecture.json', '--json'], 1, False, 'schema/enum')
case('05-reject-invalid-reference', ['validate', 'architecture', HERE / 'invalid-reference.architecture.json', '--json'], 1, False, 'architecture/unknown-endpoint')
failed = case('06-deliver-invalid-reference', ['deliver', 'architecture', HERE / 'invalid-reference.architecture.json', ARTIFACT, '--json'], 1, False, 'architecture/unknown-endpoint')
assert digest(ARTIFACT) == lastgood
assert failed['update']['reason'] == 'disabled'
failed_provenance = json.loads(PROVENANCE.read_text())
assert failed_provenance['status'] == 'failed'
assert failed_provenance['artifact']['sha256'] == lastgood
save_json('provenance-after-failure.json', failed_provenance)
case('07-check-failed-provenance', ['check', ARTIFACT, '--json', '--require-provenance'], 1, False, 'delivery/provenance-failed')
case('08-recover-valid-delivery', ['deliver', 'architecture', EXAMPLE, ARTIFACT, '--json'], 0, True)
case('09-check-recovered-delivery', ['check', ARTIFACT, '--json', '--require-provenance'], 0, True)
assert json.loads(PROVENANCE.read_text())['status'] == 'current'
assert digest(ARTIFACT) == lastgood
assert NETWORK_LOG.read_text() == ''
status = run_readonly_git('status', '--porcelain=v1')
assert status == ''
save_json('provenance-recovered.json', json.loads(PROVENANCE.read_text()))
# The machine-bound live sidecar is our own test output. Archive a redacted
# snapshot after strict verification, so published evidence has portable paths.
PROVENANCE.unlink()
save_json('results.json', {
    'repository': 'tt-a1i/archify', 'commit': SHA,
    'runtime': subprocess.check_output([NODE, '--version'], text=True).strip(),
    'platform': platform.system() + ' ' + platform.machine(),
    'fixture': 'archify/examples/web-app.architecture.json',
    'fixture_sha256': digest(EXAMPLE),
    'network_update_check': 'disabled by ARCHIFY_UPDATE_CHECK_DISABLED=1',
    'network_guard_attempts': 0,
    'network_guard_limit': 'Node API guard, not OS-level network isolation or a general security audit',
    'artifact': {'path': 'Research/evidence/archify/sample-web-app.html',
                 'bytes': ARTIFACT.stat().st_size, 'sha256': lastgood},
    'lastgood_preserved_on_render_failure': True,
    'failed_provenance_rejected': True,
    'recovered_provenance': 'current',
    'upstream_worktree_status': status,
    'receipt_redaction': 'Absolute Research directory prefix replaced with Research in stored text receipts only',
    'cases': results,
    'not_tested': ['browser rendering or interaction', 'browser-check/finalize',
                   'visual review', 'network brand capture', 'other diagram families',
                   'concurrent delivery/races/crashes', 'model output or knowledge correctness'],
})
print('All 9 bounded checks completed; lastgood hash preserved; upstream unchanged.', flush=True)
