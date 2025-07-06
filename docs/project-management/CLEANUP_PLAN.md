# CROD Repository Cleanup Plan

## Overview
This document outlines the comprehensive cleanup and reorganization of the CROD Babylon Genesis repository.

## Current Issues

### 1. Duplicate Files
- 7 duplicate Dockerfiles in blockchain/elixir/
- 7 duplicate Dockerfiles in crod-docker/services/
- 3 copies of crod-neural-bridge implementation
- Multiple GUI implementations scattered across directories

### 2. Empty/Abandoned Directories
- `/districts/*` - All empty
- `/crod-gui/` - Empty (active GUI is in `/current/working/crod-gui/`)
- `/crod-data/`, `/crod-integration/`, `/build/`, `/bin/` - All empty
- Multiple empty directories in `/in-progress/`

### 3. Inconsistent Structure
- Blockchain code in 3+ different locations
- No clear separation between active and experimental code
- Mixed naming conventions (kebab-case vs underscore)
- 708 JSON files (many are training data)
- 98 Markdown files scattered throughout

## Proposed New Structure

```
/crod-babylon-genesis/
├── src/                      # All active source code
│   ├── blockchain/           # Consolidated blockchain implementations
│   │   ├── elixir/          # Elixir blockchain modules
│   │   ├── rust/            # Rust components
│   │   ├── python/          # Python ML/AI
│   │   └── shared/          # Shared interfaces
│   ├── frontend/            # All UI applications
│   │   └── crod-gui/        # React dashboard
│   ├── services/            # Microservices
│   │   ├── orchestration/   # Master orchestrator
│   │   ├── monitoring/      # Health monitoring
│   │   └── visualization/   # Visualization tools
│   └── integrations/        # External system integrations
├── infrastructure/          # DevOps and deployment
│   ├── docker/             # All Dockerfiles and compose
│   ├── kubernetes/         # K8s configurations
│   └── scripts/            # Deployment scripts
├── docs/                   # All documentation
│   ├── api/               # API documentation
│   ├── architecture/      # System design docs
│   └── guides/            # User guides
├── tests/                 # All test files
├── scripts/               # Utility scripts (Go programs)
└── archive/               # Old/experimental code

## Files to Remove
- /logs/ (add to .gitignore)
- All empty directories without purpose
- Duplicate Dockerfiles
- Old shell scripts (replaced by Go programs)

## Files to Consolidate
- All blockchain implementations → src/blockchain/
- All GUI projects → src/frontend/
- All Docker configurations → infrastructure/docker/
- All documentation → docs/

## Cleanup Steps

### Phase 1: Backup and Identify (Current)
1. Create backup of entire repository
2. Identify all active vs inactive components
3. Map dependencies between components

### Phase 2: Create New Structure
1. Create src/ directory hierarchy
2. Create infrastructure/ directory
3. Consolidate documentation

### Phase 3: Migration
1. Move active blockchain code to src/blockchain/
2. Move active GUI to src/frontend/
3. Consolidate all Docker files
4. Move services to proper locations

### Phase 4: Cleanup
1. Remove empty directories
2. Archive old/experimental code
3. Update all import paths
4. Fix naming conventions

### Phase 5: Documentation
1. Create README for each major directory
2. Update main README with new structure
3. Create migration guide

## Naming Convention
- Use kebab-case for all files and directories
- Exception: Go packages use underscore
- All CROD-specific modules prefixed with 'crod-'

## Priority Components to Preserve
1. `/current/working/crod-gui/` - Active React dashboard
2. `/blockchain/elixir/lib/` - Core blockchain implementation
3. `/cmd/` - New Go programs
4. `/visualization/` - Scientific visualization suite
5. `/docs/` - Existing documentation

## Next Steps
1. Review this plan
2. Create backup
3. Begin Phase 1 implementation