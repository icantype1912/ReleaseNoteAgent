import re


def normalize_version(version: str) -> str:
    return re.sub(r"^[\^~><= ]+", "", version)