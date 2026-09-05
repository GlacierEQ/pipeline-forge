# Pipeline Forge

Universal pipeline builder — compose any workflow from reusable phase blocks.

## Quick Start

```bash
# Run a built-in template
python3 scripts/forge.py run --template production --target <dir>
python3 scripts/forge.py run --template security --target <dir>
python3 scripts/forge.py run --template research --target <dir>
python3 scripts/forge.py run --template perf --target <dir>
python3 scripts/forge.py run --template quick --target <dir>
python3 scripts/forge.py run --template full --target <dir>

# List available templates
python3 scripts/forge.py list templates

# List available phase blocks
python3 scripts/forge.py list blocks
```

## Templates

| Template | Phases | Use Case |
|----------|--------|----------|
| `production` | orient → grill → spec → workspace → implement → gate-7d → verify → review → finalize → finish | Full-cycle engineering |
| `security` | orient → security-scan → implement → verify → finalize → finish | Security audit |
| `research` | orient → grill → research-deep → spec → implement → verify → finalize → finish | Deep research |
| `perf` | orient → perf-profile → grill → implement → verify → gate-7d → finalize → finish | Performance engineering |
| `quick` | orient → implement → verify → finish | Fast iteration |
| `full` | orient → grill → spec → workspace → implement → gate-7d → security-scan → perf-profile → verify → review → finalize → finish | Everything |

## Phase Blocks

### Primitives
- `orient` — Inspect environment, decide shape
- `grill` — Resolve decisions interactively
- `spec` — Create specification document
- `workspace` — Prepare environment
- `implement` — Write code
- `verify` — Run tests
- `review` — Code review
- `finalize` — Update docs
- `finish` — Report

### Power-ups
- `gate-7d` — 7-dimension production audit
- `security-scan` — Threat model + CVE scan
- `perf-profile` — Benchmark + optimize
- `research-deep` — Multi-source research
- `compliance-check` — Regulatory compliance
- `deploy-safe` — Staged deployment

## Create Custom Pipeline

```bash
# From YAML config
python3 scripts/forge.py run --config my-pipeline.yaml --target <dir>

# From existing template
python3 scripts/forge.py run --template production --target <dir>
```

### YAML Config Format

```yaml
name: my-pipeline
description: Custom workflow

phases:
  - name: orient
    type: primitive

  - name: security-scan
    type: power-up
    config:
      severity: high

  - name: implement
    type: primitive

  - name: gate-7d
    type: power-up
    config:
      dimensions: all
      fail_fast: true

  - name: verify
    type: primitive

  - name: finish
    type: primitive
```

## Structure

```
pipeline-forge/
├── SKILL.md                  # Forge spec
├── README.md                 # This file
├── scripts/
│   └── forge.py              # Universal composer + runner
├── templates/
│   ├── security.yaml         # Security audit pipeline
│   ├── research.yaml         # Deep research pipeline
│   └── perf.yaml             # Performance engineering pipeline
├── references/               # Documentation
└── examples/                 # Example configs
```

## Integration

Works with:
- `mega-pipeline-production` — Production readiness
- `mega-pipeline-security` — Security audit
- `mega-pipeline-research` — Deep research
- `mega-pipeline-perf` — Performance

## License

APEX Estate — GlacierEQ
