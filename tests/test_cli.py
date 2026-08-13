"""CLI 单元测试"""
import subprocess
import sys


def test_cli_help():
    result = subprocess.run([sys.executable, "-m", "gstack_agent", "--help"],
                            capture_output=True, text=True)
    assert result.returncode == 0
    assert "gstack-agent" in result.stdout
    assert "analyze" in result.stdout
    assert "office-hours" in result.stdout
    assert "ceo-review" in result.stdout
    assert "investigate" in result.stdout
    print("✓ CLI help")


def test_no_command_exits_1():
    result = subprocess.run([sys.executable, "-m", "gstack_agent"],
                            capture_output=True, text=True)
    assert result.returncode == 1
    print("✓ No command exits 1")


def test_office_hours_auto():
    result = subprocess.run(
        [sys.executable, "-m", "gstack_agent", "office-hours", "--auto", "test idea"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "gstack Office-Hours" in result.stdout
    print("✓ office-hours --auto")


def test_ceo_review():
    result = subprocess.run(
        [sys.executable, "-m", "gstack_agent", "ceo-review", "test plan"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "CEO Review" in result.stdout
    print("✓ ceo-review")


def test_investigate():
    result = subprocess.run(
        [sys.executable, "-m", "gstack_agent", "investigate", "test symptom"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Investigate" in result.stdout
    print("✓ investigate")


def test_analyze():
    result = subprocess.run(
        [sys.executable, "-m", "gstack_agent", "analyze", "test task"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Office-Hours" in result.stdout
    assert "CEO Review" in result.stdout
    assert "Investigate" in result.stdout
    print("✓ analyze (all three)")


if __name__ == "__main__":
    test_cli_help()
    test_no_command_exits_1()
    test_office_hours_auto()
    test_ceo_review()
    test_investigate()
    test_analyze()
    print("\nAll tests passed! ✓")