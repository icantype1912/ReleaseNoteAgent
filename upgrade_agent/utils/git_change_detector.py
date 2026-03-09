from git import Repo
import os


SUPPORTED_DEP_FILES = [
    "package.json"
]


def get_changed_dependency_files(repo_path="."):

    repo = Repo(repo_path)

    commit = repo.head.commit

    if not commit.parents:
        return []

    parent = commit.parents[0]

    diff = parent.diff(commit)

    changed_files = []

    for change in diff:

        file_path = change.b_path

        filename = os.path.basename(file_path)

        if filename in SUPPORTED_DEP_FILES:

            changed_files.append(file_path)

    return changed_files