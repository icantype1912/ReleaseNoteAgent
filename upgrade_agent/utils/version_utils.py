def normalize_tag(tag):

    if tag.startswith("v"):
        return tag[1:]

    return tag