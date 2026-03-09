from git import Repo


def get_previous_file_version(repo_path: str, file_path: str):

    repo = Repo(repo_path)

    # get last commit
    commit = repo.head.commit

    # get previous commit
    parent = commit.parents[0]

    try:
        blob = parent.tree / file_path
        return blob.data_stream.read().decode("utf-8")

    except Exception:
        return None
    
def normalize_github_url(url):

    if not url:
        return None

    url = url.replace("git+", "")
    url = url.replace(".git", "")

    return url