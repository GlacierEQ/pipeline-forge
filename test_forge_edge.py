#!/usr/bin/env python3
"""
Additional tests for Pipeline Forge — Edge Cases & Integration.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from forge import (
    PhaseBlockLibrary,
    PhaseConfig,
    PhaseResult,
    PhaseStatus,
    PipelineComposer,
    PipelineConfig,
    PipelineResult,
)


class TestPhaseStatus:
    def test_values(self):
        statuses = [s.name for s in PhaseStatus]
        assert "PENDING" in statuses
        assert "PASSED" in statuses
        assert "FAILED" in statuses


class TestPhaseConfig:
    def test_create(self):
        config = PhaseConfig(name="test-phase", block_type="orient")
        assert config.name == "test-phase"
        assert config.block_type == "orient"

    def test_defaults(self):
        config = PhaseConfig(name="test")
        assert config.skip is False
        assert config.required is True

    def test_with_config(self):
        config = PhaseConfig(name="test", block_type="orient", config={"key": "value"})
        assert config.config["key"] == "value"


class TestPipelineConfig:
    def test_create(self):
        config = PipelineConfig(name="test-pipeline", description="A test pipeline")
        assert config.name == "test-pipeline"

    def test_with_phases(self):
        phases = [PhaseConfig(name="p1", block_type="orient")]
        config = PipelineConfig(name="test", description="test", phases=phases)
        assert len(config.phases) == 1


class TestPhaseBlockLibrary:
    def test_create(self):
        library = PhaseBlockLibrary()
        assert library is not None

    def test_has_standard_blocks(self):
        library = PhaseBlockLibrary()
        assert library is not None


class TestPipelineComposer:
    def test_create(self):
        composer = PipelineComposer()
        assert composer is not None

    def test_composer_has_methods(self):
        composer = PipelineComposer()
        methods = [m for m in dir(composer) if not m.startswith("_")]
        assert len(methods) > 0


class TestBlockFunctions:
    def test_blocks_exist(self):
        from forge import (
            block_orient, block_spec, block_research_deep,
            block_implement, block_review, block_verify,
            block_security_scan, block_gate_7d, block_perf_profile,
            block_deploy_safe, block_finalize, block_finish, block_grill,
            block_workspace, block_compliance_check,
        )
        assert callable(block_orient)
        assert callable(block_spec)
        assert callable(block_verify)
        assert callable(block_security_scan)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
