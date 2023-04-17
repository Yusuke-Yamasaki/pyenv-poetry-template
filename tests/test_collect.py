import pytest
from src.app import collect_env_markers


@pytest.mark.parametrize(
    "os_name",
    [
        ["posix", "java", "nt"],
    ],
)
def test_os_name(os_name: list[str]) -> None:
    env_markers = collect_env_markers()
    assert env_markers["os_name"] in os_name


@pytest.mark.parametrize(
    "platform_machine",
    [
        ["x86_64", "arm64", "aarch64"],
    ],
)
def test_platform_machine(platform_machine: list[str]) -> None:
    env_markers = collect_env_markers()
    assert env_markers["platform_machine"] in platform_machine


@pytest.mark.parametrize(
    "platform_system",
    [
        ["Linux", "Darwin", "Windows", "Java"],
    ],
)
def test_platform_system(platform_system: list[str]) -> None:
    env_markers = collect_env_markers()
    assert env_markers["platform_system"] in platform_system


@pytest.mark.parametrize(
    "sys_platform",
    [
        ["linux", "darwin", "win32"],
    ],
)
def test_sys_platform(sys_platform: list[str]) -> None:
    env_markers = collect_env_markers()
    assert env_markers["sys_platform"] in sys_platform
