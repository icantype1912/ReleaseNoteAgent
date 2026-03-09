import re


def extract_version_sections(changelog_text, from_version, to_version):
    """
    Extract changelog entries between two versions.
    """

    pattern = r"##?\s*v?(\d+\.\d+\.\d+)"

    matches = list(re.finditer(pattern, changelog_text))

    sections = []

    for i, match in enumerate(matches):

        version = match.group(1)

        start = match.start()

        end = matches[i + 1].start() if i + 1 < len(matches) else len(changelog_text)

        section_text = changelog_text[start:end]

        sections.append(
            {
                "version": version,
                "notes": section_text,
            }
        )

    return sections