import json
from upgrade_agent.utils.semver_utils import normalize_version


def parse_package_json(file_path: str):
    """
    Parse dependencies from a package.json file on disk.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as f:

            content = f.read().strip()

            # Handle empty files
            if not content:
                print(f"Warning: {file_path} is empty.")
                return {}

            data = json.loads(content)

    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {}

    dependencies = {}

    for section in ["dependencies", "devDependencies"]:

        if section in data:

            for name, version in data[section].items():

                dependencies[name] = normalize_version(version)

    return dependencies


def parse_package_json_content(content: str):
    """
    Parse dependencies from raw package.json content
    (used when reading previous file versions from git).
    """

    try:
        if not content or not content.strip():
            return {}

        data = json.loads(content)

    except Exception as e:
        print(f"Error parsing package.json content from git: {e}")
        return {}

    dependencies = {}

    for section in ["dependencies", "devDependencies"]:

        if section in data:

            for name, version in data[section].items():

                dependencies[name] = normalize_version(version)

    return dependencies