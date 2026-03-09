from upgrade_agent.models.dependency_upgrade import DependencyUpgrade


def detect_upgrades(old_deps, new_deps, ecosystem):

    upgrades = []

    for dep, new_version in new_deps.items():

        if dep in old_deps:

            old_version = old_deps[dep]

            if old_version != new_version:

                upgrades.append(
                    DependencyUpgrade(
                        dependency=dep,
                        from_version=old_version,
                        to_version=new_version,
                        ecosystem=ecosystem,
                    )
                )

    return upgrades