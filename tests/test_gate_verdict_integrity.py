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


def test_verify_executes_tests_not_collection(monkeypatch, tmp_path):
    import subprocess
    commands = []

    def fake_run(command, **kwargs):
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, "1 passed", "")

    monkeypatch.setattr(forge.subprocess if hasattr(forge, "subprocess") else subprocess, "run", fake_run)
    monkeypatch.delitem(sys.modules, "pytest", raising=False)
    result = forge.block_verify({}, tmp_path)
    assert result.status == forge.PhaseStatus.PASSED
    assert "--co" not in commands[0]
    assert "pytest" in commands[0]


def test_verify_rejects_no_tests(monkeypatch, tmp_path):
    import subprocess

    monkeypatch.delitem(sys.modules, "pytest", raising=False)
    monkeypatch.setattr(subprocess, "run", lambda command, **kwargs: subprocess.CompletedProcess(command, 5, "no tests ran", ""))
    result = forge.block_verify({}, tmp_path)
    assert result.status == forge.PhaseStatus.FAILED


def test_verify_rejects_recursive_execution(monkeypatch, tmp_path):
    monkeypatch.setitem(sys.modules, "pytest", object())
    result = forge.block_verify({}, tmp_path)
    assert result.status == forge.PhaseStatus.FAILED


def test_verify_does_not_mask_failed_pytest_with_fallback(monkeypatch, tmp_path):
    import subprocess
    (tmp_path / "verify_all.py").write_text("print('fallback')")
    calls = []
    def fake_run(command, **kwargs):
        calls.append(command)
        return subprocess.CompletedProcess(command, 1, "1 failed", "")
    monkeypatch.delitem(sys.modules, "pytest", raising=False)
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = forge.block_verify({}, tmp_path)
    assert result.status == forge.PhaseStatus.FAILED
    assert len(calls) == 1


def test_verify_allows_fallback_only_when_pytest_missing(monkeypatch, tmp_path):
    import subprocess
    (tmp_path / "verify_all.py").write_text("print('fallback')")
    calls = []
    def fake_run(command, **kwargs):
        calls.append(command)
        if len(calls) == 1:
            return subprocess.CompletedProcess(command, 1, "", "No module named pytest")
        return subprocess.CompletedProcess(command, 0, "fallback succeeded", "")
    monkeypatch.delitem(sys.modules, "pytest", raising=False)
    monkeypatch.setattr(subprocess, "run", fake_run)
    result = forge.block_verify({}, tmp_path)
    assert result.status == forge.PhaseStatus.PASSED
    assert len(calls) == 2
