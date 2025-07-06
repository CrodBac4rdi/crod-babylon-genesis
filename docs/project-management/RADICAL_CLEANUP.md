# RADICAL CLEANUP PLAN - FINAL

## Current Chaos
- 35+ directories in root
- Multiple duplicates (crod-gui vs src/frontend/crod-gui)
- Old stuff mixed with new
- No clear structure

## NEW SIMPLE STRUCTURE

```
crod-babylon-genesis/
├── src/                    # ALL active code
├── docs/                   # ALL documentation
├── visualization/          # Visualization tools (already good)
├── .github/               # GitHub config
├── archive/               # Old experiments
└── README.md              # Main readme
```

## TO DELETE
- /bin, /build (empty)
- /crod-gui (duplicate of src/frontend)
- /current (old working directory)
- /demos (can go to docs/demos)
- /in-progress (old experiments)
- /internal, /k8s, /laufende-projekte (unclear purpose)
- /logs (should not be in git)
- /monitoring, /orchestration (move to src/services)
- /output (generated files)
- /quantum, /reality (experimental)
- /scripts (old shell scripts)
- /security (move to docs)
- /tests (empty)
- /visuals (duplicate of visualization)

## TO MOVE
- /blockchain → /src/blockchain
- /cmd → /src/cmd
- /crod-core → /src/core
- /integrations → /src/integrations
- /crod-docker → /infrastructure/docker

## KEEP AS IS
- /.github (GitHub config)
- /visualization (already organized)
- /docs (documentation)
- /assets (images/logos)