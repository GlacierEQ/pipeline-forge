---
name: pipeline-forge
description: >
  Universal pipeline builder — compose any workflow from reusable phase blocks.
  Use when creating new pipelines, customizing workflows, or building domain-specific
  automation. The meta-system behind all mega-pipelines.
  Triggers: "build pipeline", "new workflow", "pipeline template", "forge", "compose workflow".
---

# Pipeline Forge

## Purpose

Build any pipeline by composing reusable phase blocks. One template, infinite pipelines.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PIPELINE FORGE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │
│  │ PHASE    │ │ PHASE    │ │ PHASE    │ │ PHASE    │  ...     │
│  │ LIBRARY  │ │ LIBRARY  │ │ LIBRARY  │ │ LIBRARY  │          │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘          │
│       │            │            │            │                  │
│       └────────────┼────────────┼────────────┘                  │
│                    ▼            ▼                               │
│            ┌───────────────────────────┐                       │
│            │   PIPELINE COMPOSER       │                       │
│            │   (config-driven)         │                       │
│            └───────────────────────────┘                       │
│                    │                                           │
│                    ▼                                           │
│            ┌───────────────────────────┐                       │
│            │   PIPELINE RUNNER         │                       │
│            │   (evidence collection)   │                       │
│            └───────────────────────────┘                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Phase Blocks

### Primitives (always available)
| Block | Purpose |
|-------|---------|
| `orient` | Inspect environment, decide shape |
| `grill` | Resolve decisions interactively |
| `spec` | Create specification document |
| `implement` | Write code |
| `verify` | Run tests |
| `review` | Code review |
| `finalize` | Update docs, mark done |
| `finish` | Report |

### Power-ups (domain-specific)
| Block | Purpose |
|-------|---------|
| `gate-7d` | Production readiness (7 dimensions) |
| `security-scan` | Threat model + CVE scan |
| `perf-profile` | Benchmark + optimize |
| `research-deep` | Multi-source research |
| `forensic-audit` | Evidence chain verification |
| `compliance-check` | Regulatory compliance |
| `deploy-safe` | Staged deployment |

## Config Format

```yaml
# pipeline.yaml
name: my-pipeline
description: Custom workflow

phases:
  - name: orient
    type: primitive
    skip: false

  - name: security
    type: power-up
    config:
      severity: high
      auto_fix: false

  - name: implement
    type: primitive

  - name: gate
    type: power-up
    config:
      dimensions: all
      fail_fast: true

  - name: verify
    type: primitive

  - name: finish
    type: primitive
```

## Built-in Templates

| Template | Phases | Use Case |
|----------|--------|----------|
| `production` | orient → grill → spec → workspace → implement → gate-7d → verify → review → finalize → finish | Full-cycle engineering |
| `security` | orient → threat-model → scan → fix → verify → report | Security audit |
| `research` | orient → scope → collect → synthesize → cite → report | Deep research |
| `perf` | orient → profile → hotspot → optimize → benchmark → report | Performance engineering |
| `quick` | orient → implement → verify → finish | Fast iteration |

## Usage

### Run existing template
```bash
python3 forge.py --template production --target <dir>
```

### Run custom config
```bash
python3 forge.py --config pipeline.yaml --target <dir>
```

### Create new pipeline from template
```bash
forge.py --create my-pipeline --base production --add security-scan:3
```

## Output

Every pipeline produces:
- `PIPELINE_RESULT.md` — human-readable report
- `pipeline-result.json` — machine-readable evidence
- Phase-specific artifacts (specs, reports, etc.)

## Integration

Works with:
- `mega-pipeline-production` (production readiness)
- `mega-pipeline-security` (security audit)
- `mega-pipeline-research` (deep research)
- `mega-pipeline-perf` (performance)
- Any custom pipeline you build

**The forge is infinite.**
