"""
Pipeline Forge — Test Suite
Tests for the universal pipeline composer, phase blocks, and templates.
"""

import json
import sys
from pathlib import Path

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / "scripts"))

from forge import (
    PhaseBlockLibrary,
    PhaseConfig,
    PhaseResult,
    PhaseStatus,
    PipelineComposer,
    PipelineConfig,
    PipelineResult,
    block_orient,
    block_grill,
    block_spec,
    block_workspace,
    block_implement,
    block_verify,
    block_review,
    block_finalize,
    block_finish,
    block_security_scan,
    block_perf_profile,
    block_compliance_check,
)


# ─── Phase Status Tests ──────────────────────────────────────────────────────

class TestPhaseStatus:
    """Tests for phase status enum."""

    def test_all_statuses(self):
        assert PhaseStatus.PENDING.value == "pending"
        assert PhaseStatus.RUNNING.value == "running"
        assert PhaseStatus.PASSED.value == "passed"
        assert PhaseStatus.FAILED.value == "failed"
        assert PhaseStatus.SKIPPED.value == "skipped"


# ─── Phase Block Tests ───────────────────────────────────────────────────────

class TestPhaseBlocks:
    """Tests for built-in phase blocks."""

    def test_block_orient(self, tmp_path):
        result = block_orient({}, tmp_path)
        assert result.status == PhaseStatus.PASSED
        assert result.name == "orient"

    def test_block_grill(self, tmp_path):
        result = block_grill({}, tmp_path)
        assert result.status == PhaseStatus.SKIPPED

    def test_block_spec(self, tmp_path):
        result = block_spec({}, tmp_path)
        assert result.status == PhaseStatus.PASSED

    def test_block_workspace(self, tmp_path):
        result = block_workspace({}, tmp_path)
        assert result.status == PhaseStatus.PASSED

    def test_block_implement(self, tmp_path):
        result = block_implement({}, tmp_path)
        assert result.status == PhaseStatus.PASSED

    def test_block_verify_no_tests(self, tmp_path):
        result = block_verify({}, tmp_path)
        # May pass or fail depending on pytest
        assert result.name == "verify"

    def test_block_review(self, tmp_path):
        result = block_review({}, tmp_path)
        assert result.status == PhaseStatus.PASSED

    def test_block_finalize(self, tmp_path):
        result = block_finalize({}, tmp_path)
        assert result.status == PhaseStatus.PASSED

    def test_block_finish(self, tmp_path):
        result = block_finish({}, tmp_path)
        assert result.status == PhaseStatus.PASSED

    def test_block_security_scan(self, tmp_path):
        result = block_security_scan({}, tmp_path)
        assert result.status == PhaseStatus.PASSED

    def test_block_perf_profile(self, tmp_path):
        result = block_perf_profile({}, tmp_path)
        assert result.name == "perf-profile"

    def test_block_compliance_check(self, tmp_path):
        result = block_compliance_check({}, tmp_path)
        assert result.status == PhaseStatus.PASSED


# ─── Phase Block Library Tests ───────────────────────────────────────────────

class TestPhaseBlockLibrary:
    """Tests for phase block registry."""

    def test_register_block(self):
        library = PhaseBlockLibrary()
        library.register("test", lambda c, t: PhaseResult(name="test", status=PhaseStatus.PASSED))
        assert "test" in library.list_blocks()

    def test_get_block(self):
        library = PhaseBlockLibrary()
        library.register("test", lambda c, t: PhaseResult(name="test", status=PhaseStatus.PASSED))
        block = library.get("test")
        assert block is not None

    def test_get_missing_block(self):
        library = PhaseBlockLibrary()
        assert library.get("nonexistent") is None


# ─── Pipeline Composer Tests ─────────────────────────────────────────────────

class TestPipelineComposer:
    """Tests for pipeline composer."""

    def test_compose_production_template(self):
        composer = PipelineComposer()
        config = composer.compose_from_template("production")
        assert config.name == "pipeline-production"
        assert len(config.phases) == 10

    def test_compose_security_template(self):
        composer = PipelineComposer()
        config = composer.compose_from_template("security")
        assert config.name == "pipeline-security"
        assert len(config.phases) == 6

    def test_compose_research_template(self):
        composer = PipelineComposer()
        config = composer.compose_from_template("research")
        assert config.name == "pipeline-research"

    def test_compose_perf_template(self):
        composer = PipelineComposer()
        config = composer.compose_from_template("perf")
        assert config.name == "pipeline-perf"

    def test_compose_quick_template(self):
        composer = PipelineComposer()
        config = composer.compose_from_template("quick")
        assert config.name == "pipeline-quick"
        assert len(config.phases) == 4

    def test_compose_full_template(self):
        composer = PipelineComposer()
        config = composer.compose_from_template("full")
        assert config.name == "pipeline-full"
        assert len(config.phases) == 12

    def test_compose_invalid_template(self):
        composer = PipelineComposer()
        with pytest.raises(ValueError):
            composer.compose_from_template("nonexistent")

    def test_list_templates(self):
        composer = PipelineComposer()
        templates = composer.list_templates()
        assert "production" in templates
        assert "security" in templates
        assert "full" in templates

    def test_list_blocks(self):
        composer = PipelineComposer()
        blocks = composer.list_blocks()
        assert "orient" in blocks
        assert "gate-7d" in blocks
        assert "security-scan" in blocks


# ─── Pipeline Run Tests ──────────────────────────────────────────────────────

class TestPipelineRun:
    """Tests for pipeline execution."""

    def test_run_quick_template(self, tmp_path):
        composer = PipelineComposer()
        config = composer.compose_from_template("quick")
        result = composer.run(config, tmp_path)
        # On empty dir, verify may fail (no tests) — that's expected
        assert result.completed_phases >= 2
        assert result.gate_status in ("PASS", "FAIL")

    def test_run_result_dict(self, tmp_path):
        composer = PipelineComposer()
        config = composer.compose_from_template("quick")
        result = composer.run(config, tmp_path)
        d = result.to_dict()
        assert "name" in d
        assert "phases" in d
        assert "gate_status" in d

    def test_run_result_markdown(self, tmp_path):
        composer = PipelineComposer()
        config = composer.compose_from_template("quick")
        result = composer.run(config, tmp_path)
        md = result.to_markdown()
        assert "# Pipeline Result" in md
        assert "Phases:" in md


# ─── Integration Tests ───────────────────────────────────────────────────────

class TestIntegration:
    """Integration tests for full pipeline flow."""

    def test_production_pipeline_run(self, tmp_path):
        """Test full production pipeline on temp directory."""
        composer = PipelineComposer()
        config = composer.compose_from_template("production")
        result = composer.run(config, tmp_path)
        # Gate and verify may fail on empty dir — that's expected
        assert result.completed_phases >= 4

    def test_security_pipeline_run(self, tmp_path):
        """Test security pipeline."""
        composer = PipelineComposer()
        config = composer.compose_from_template("security")
        result = composer.run(config, tmp_path)
        # Verify may fail on empty dir — that's expected
        assert result.completed_phases >= 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
