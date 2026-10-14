# Run from autodigest/; every Node child inherits the network guard and update-disable flag.
export ARCHIFY_UPDATE_CHECK_DISABLED=1
export ARCHIFY_RESEARCH_NETWORK_LOG="$PWD/Research/evidence/archify/network-attempts.jsonl"
export NODE_OPTIONS="--require=$PWD/Research/evidence/archify/no-network.cjs"

# 01-validate-official: expected exit 0
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs validate architecture Research/repos/tt-a1i/archify/archify/examples/web-app.architecture.json --json

# 02-render-official: expected exit 0
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs render architecture Research/repos/tt-a1i/archify/archify/examples/web-app.architecture.json Research/evidence/archify/sample-web-app.html

# 03-deliver-official: expected exit 0
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs deliver architecture Research/repos/tt-a1i/archify/archify/examples/web-app.architecture.json Research/evidence/archify/sample-web-app.html --json

# 04-reject-invalid-component: expected exit 1
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs validate architecture Research/evidence/archify/invalid-component.architecture.json --json

# 05-reject-invalid-reference: expected exit 1
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs validate architecture Research/evidence/archify/invalid-reference.architecture.json --json

# 06-deliver-invalid-reference: expected exit 1
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs deliver architecture Research/evidence/archify/invalid-reference.architecture.json Research/evidence/archify/sample-web-app.html --json

# 07-check-failed-provenance: expected exit 1
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs check Research/evidence/archify/sample-web-app.html --json --require-provenance

# 08-recover-valid-delivery: expected exit 0
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs deliver architecture Research/repos/tt-a1i/archify/archify/examples/web-app.architecture.json Research/evidence/archify/sample-web-app.html --json

# 09-check-recovered-delivery: expected exit 0
node Research/repos/tt-a1i/archify/archify/bin/archify.mjs check Research/evidence/archify/sample-web-app.html --json --require-provenance
