"""Regression checks for gate verdict integrity (run with pytest)."""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("forge", Path(__file__).resolve().parents[1] / "scripts" / "forge.py")
forge = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = forge
spec.loader.exec_module(forge)


def test_required_skip_is_not_pass():
    cfg = forge.PipelineConfig(name="skip", phases=[forge.PhaseConfig(name="grill", required=True, skip=True)])
    result = forge.PipelineComposer().run(cfg, Path("."))
    assert not result.success
    assert result.gate_status == "FAIL"


def test_optional_skip_is_allowed():
    cfg = forge.PipelineConfig(name="skip", phases=[forge.PhaseConfig(name="grill", required=False, skip=True)])
    result = forge.PipelineComposer().run(cfg, Path("."))
    assert result.success
    assert result.gate_status == "PASS"


def test_incomplete_results_are_not_pass():
    cfg = forge.PipelineConfig(name="incomplete", phases=[forge.PhaseConfig(name="a"), forge.PhaseConfig(name="b")])
    result = forge.PipelineResult(name="incomplete", config=cfg, start_time="now", phases=[forge.PhaseResult(name="a", status=forge.PhaseStatus.PASSED)])
    assert not result.all_passed


def test_retry_recalculates_gate():
    cfg = forge.PipelineConfig(name="retry", phases=[forge.PhaseConfig(name="flaky")])
    composer = forge.PipelineComposer()
    attempts = iter([forge.PhaseStatus.FAILED, forge.PhaseStatus.PASSED])
    composer.library.register("flaky", lambda metadata, target: forge.PhaseResult(name="flaky", status=next(attempts)))
    result = composer.run_with_retry(cfg, Path("."), max_retries=1)
    assert result.success
    assert result.gate_status == "PASS"
