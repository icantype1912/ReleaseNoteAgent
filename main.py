from upgrade_agent.parsers.npm_parser import (
    parse_package_json,
    parse_package_json_content,
)

from dotenv import load_dotenv
load_dotenv()

from upgrade_agent.diff_engine.detect_upgrades import detect_upgrades

from upgrade_agent.utils.git_utils import get_previous_file_version
from upgrade_agent.utils.git_change_detector import get_changed_dependency_files

from upgrade_agent.workflows.upgrade_workflow import build_upgrade_graph


def main():

    repo_path = "."

    print("\nScanning repository for dependency changes...\n")

    changed_files = get_changed_dependency_files(repo_path)

    if not changed_files:

        print("No dependency file changes detected.")
        return

    print("Detected dependency files:\n")

    for f in changed_files:
        print(f" - {f}")

    all_upgrades = []

    for dependency_file in changed_files:

        print(f"\nProcessing {dependency_file}\n")

        new_deps = parse_package_json(dependency_file)

        old_content = get_previous_file_version(repo_path, dependency_file)

        if not old_content:

            print("Could not load previous version of file")
            continue

        old_deps = parse_package_json_content(old_content)

        upgrades = detect_upgrades(old_deps, new_deps, "npm")

        all_upgrades.extend(upgrades)

    if not all_upgrades:

        print("\nNo dependency upgrades detected.\n")
        return

    print("\nDetected Dependency Upgrades\n")

    workflow = build_upgrade_graph()

    for upgrade in all_upgrades:

        print(
            f"\nAnalyzing {upgrade.dependency} "
            f"{upgrade.from_version} → {upgrade.to_version}"
        )

        result = workflow.invoke(
            {
                "dependency": upgrade.dependency,
                "from_version": upgrade.from_version,
                "to_version": upgrade.to_version,
            }
        )

        print("\nRepository:", result.get("repo_url"))

        print("\nReleases included in upgrade:\n")

        releases = result.get("releases", [])

        for r in releases:
            print(f" - {r['version']}")

        print("\nAI Summary:\n")

        print(result.get("summary"))

        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()