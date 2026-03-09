def sample_releases(releases, max_releases=6):
    """
    Reduce release list size to avoid LLM token overflow.
    """

    if not releases:
        return []

    if len(releases) <= max_releases:
        return releases

    sampled = []

    # first release after upgrade
    sampled.append(releases[-1])

    # latest releases
    sampled.extend(releases[: max_releases - 1])

    return sampled