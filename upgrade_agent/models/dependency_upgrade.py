from dataclasses import dataclass


@dataclass
class DependencyUpgrade:

    dependency: str
    from_version: str
    to_version: str
    ecosystem: str