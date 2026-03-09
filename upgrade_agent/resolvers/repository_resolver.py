import requests
import yaml
import os
from upgrade_agent.utils.git_utils import normalize_github_url

CONFIG_PATH = "upgrade_agent/config/dependency_sources.yaml"


def load_local_registry():

    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH) as f:
        data = yaml.safe_load(f)

    return data or {}


def resolve_from_registry(package_name):

    url = f"https://registry.npmjs.org/{package_name}"

    try:

        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return None

        data = response.json()

        repo = data.get("repository", {})

        if isinstance(repo, dict):

            return normalize_github_url(repo.get("url"))

    except Exception:
        pass

    return None


def resolve_repository(package_name):

    # 1. check local overrides
    registry = load_local_registry()

    if package_name in registry:

        return registry[package_name]["repo"]

    # 2. npm registry lookup
    repo_url = resolve_from_registry(package_name)

    if repo_url:
        return repo_url

    return None