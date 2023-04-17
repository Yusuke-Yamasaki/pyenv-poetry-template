import os
import platform
import sys
from typing import Literal

ENV_MARKERS = Literal["os_name", "sys_platform", "platform_machine", "platform_system"]


def collect_env_markers() -> dict[ENV_MARKERS, str]:
    """Pythonの環境マーカーを取得する

    Returns:
        dict[str, str]: 環境マーカとその値
    """
    env_markers: dict[ENV_MARKERS, str] = {}
    env_markers["os_name"] = os.name
    env_markers["sys_platform"] = sys.platform
    env_markers["platform_machine"] = platform.machine()
    env_markers["platform_system"] = platform.system()
    return env_markers
