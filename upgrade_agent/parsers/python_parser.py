def parse_requirements(file_path: str):

    dependencies = {}

    with open(file_path, "r") as f:

        for line in f:

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "==" in line:

                name, version = line.split("==")

                dependencies[name] = version

    return dependencies