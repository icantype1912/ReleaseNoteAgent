from packaging import version


def filter_releases_between(releases, from_version, to_version):

    filtered = []

    for r in releases:

        v = r["version"]

        if version.parse(from_version) < version.parse(v) <= version.parse(
            to_version
        ):
            filtered.append(r)

    return filtered