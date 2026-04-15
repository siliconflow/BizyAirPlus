import json
import os
import subprocess
import sys
import urllib.request
from importlib.metadata import PackageNotFoundError, distributions, version

from packaging.requirements import Requirement
from packaging.version import Version, parse as parse_version


CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "bizyair-cloudberry"

# 设为 1/true/yes 可跳过自动升级
SKIP_UPDATE = str(os.environ.get("BIZYAIRPLUS_SKIP_UPDATE", "")).lower() in {
    "1",
    "true",
    "yes",
}

# 设为 1/true/yes 可只检查不升级
CHECK_ONLY = str(os.environ.get("BIZYAIRPLUS_CHECK_ONLY", "")).lower() in {
    "1",
    "true",
    "yes",
}


def log(message: str) -> None:
    print(f"\033[96m[BizyAirPlus]\033[0m {message}")


def warn(message: str) -> None:
    print(f"\033[93m[BizyAirPlus]\033[0m {message}")


def error(message: str) -> None:
    print(f"\033[91m[BizyAirPlus]\033[0m {message}")


def pip_install(requirement: str) -> None:
    cmd = [sys.executable, "-m", "pip", "install", "-U", requirement]
    log(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)


def get_installed_packages() -> dict[str, Version]:
    result: dict[str, Version] = {}
    for dist in distributions():
        if dist.version is None:
            continue
        name = dist.metadata.get("Name")
        if not name:
            continue
        result[name] = Version(dist.version)
    return result


def install_dependencies_from_requirements() -> None:
    requirements_path = os.path.join(CURRENT_DIR, "requirements.txt")
    if not os.path.exists(requirements_path):
        warn("requirements.txt not found, skip dependency installation.")
        return

    installed_packages = get_installed_packages()

    with open(requirements_path, "r", encoding="utf-8") as f:
        raw_lines = f.readlines()

    requirements = [
        line.strip()
        for line in raw_lines
        if line.strip() and not line.strip().startswith("#")
    ]

    for req_str in requirements:
        try:
            req = Requirement(req_str)
            installed_version = installed_packages.get(req.name)
            if not installed_version or not req.specifier.contains(installed_version):
                log(f"Dependency missing or out of range: {req_str}")
                pip_install(req_str)
            else:
                log(f"Dependency satisfied: {req.name}=={installed_version}")
        except Exception as e:
            error(f"Failed to process requirement '{req_str}': {e}")


def get_installed_version(package_name: str) -> Version | None:
    try:
        return Version(version(package_name))
    except PackageNotFoundError:
        return None
    except Exception as e:
        error(f"Failed to read installed version for {package_name}: {e}")
        return None


def get_latest_version_from_pypi(package_name: str, timeout: int = 5) -> Version | None:
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
        latest = data["info"]["version"]
        return parse_version(latest)
    except Exception as e:
        warn(f"Failed to query PyPI for {package_name}: {e}")
        return None


def ensure_cloudberry_installed_and_updated() -> None:
    installed = get_installed_version(PACKAGE_NAME)
    latest = get_latest_version_from_pypi(PACKAGE_NAME)

    if installed is None:
        warn(f"{PACKAGE_NAME} is not installed. Installing now...")
        try:
            pip_install(PACKAGE_NAME)
        except Exception as e:
            error(f"Failed to install {PACKAGE_NAME}: {e}")
        return

    log(f"Installed {PACKAGE_NAME}: {installed}")

    if latest is None:
        warn("Could not determine latest version from PyPI, skip update check.")
        return

    log(f"Latest {PACKAGE_NAME} on PyPI: {latest}")

    if latest > installed:
        warn(f"New version available: {installed} -> {latest}")
        if CHECK_ONLY:
            warn("BIZYAIRPLUS_CHECK_ONLY is enabled, skip auto upgrade.")
            return
        try:
            pip_install(PACKAGE_NAME)
            log(f"Upgrade finished. Please restart ComfyUI if needed.")
        except Exception as e:
            error(
                f"Failed to upgrade {PACKAGE_NAME}: {e}\n"
                f"Try manually: {sys.executable} -m pip install -U {PACKAGE_NAME}"
            )
    else:
        log(f"{PACKAGE_NAME} is up to date.")


def main() -> None:
    try:
        install_dependencies_from_requirements()
    except Exception as e:
        error(f"Dependency installation failed: {e}")

    if SKIP_UPDATE:
        warn("BIZYAIRPLUS_SKIP_UPDATE is set, skip package update check.")
        return

    try:
        ensure_cloudberry_installed_and_updated()
    except Exception as e:
        error(f"Update check failed: {e}")


if __name__ == "__main__":
    main()
else:
    main()