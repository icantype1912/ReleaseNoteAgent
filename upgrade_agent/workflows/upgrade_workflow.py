from typing import TypedDict, List

from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

from upgrade_agent.resolvers.repository_resolver import resolve_repository
from upgrade_agent.api_clients.github_client import fetch_github_releases
from upgrade_agent.api_clients.changelog_client import fetch_changelog

from upgrade_agent.utils.release_filter import filter_releases_between
from upgrade_agent.utils.release_sampler import sample_releases
from upgrade_agent.parsers.changelog_parser import extract_version_sections


# -----------------------------
# Graph State
# -----------------------------

class UpgradeState(TypedDict):

    dependency: str
    from_version: str
    to_version: str

    repo_url: str

    releases: List[dict]

    summary: str


# -----------------------------
# LLM Initialization
# -----------------------------

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# -----------------------------
# Node 1 — Resolve Repository
# -----------------------------

def resolve_repo(state: UpgradeState):

    dependency = state["dependency"]

    repo = resolve_repository(dependency)

    if not repo:
        print(f"Repository not found for {dependency}")

    return {"repo_url": repo}


# -----------------------------
# Node 2 — Fetch Releases
# -----------------------------

def fetch_releases(state: UpgradeState):

    repo = state["repo_url"]

    if not repo:
        return {"releases": []}

    print(f"Fetching releases for {repo}")

    releases = fetch_github_releases(repo)

    filtered = filter_releases_between(
        releases,
        state["from_version"],
        state["to_version"],
    )

    if filtered:
        print(f"GitHub releases found: {len(filtered)}")

        filtered = sample_releases(filtered)

        return {"releases": filtered}

    print("No GitHub releases found. Trying CHANGELOG...")

    changelog = fetch_changelog(repo)

    if not changelog:
        print("No CHANGELOG found.")

        return {"releases": []}

    sections = extract_version_sections(
        changelog,
        state["from_version"],
        state["to_version"],
    )

    sections = sample_releases(sections)

    print(f"Changelog sections found: {len(sections)}")

    return {"releases": sections}


# -----------------------------
# Node 3 — Summarize Releases
# -----------------------------

def summarize_releases(state: UpgradeState):

    releases = state.get("releases", [])

    if not releases:

        return {
            "summary": "No release notes or changelog entries were found for this upgrade."
        }

    notes = ""

    for r in releases:

        note = r.get("notes") or ""

        # prevent extremely large prompts
        note = note[:1200]

        notes += f"\nVersion {r.get('version')}:\n{note}\n"

    prompt = f"""
You are a software release analysis assistant.

Summarize the key changes in the following release notes.

Focus on:
- security fixes
- breaking changes
- major features
- bug fixes that could impact behavior

Release notes:
{notes}
"""

    response = llm.invoke([HumanMessage(content=prompt)])

    return {"summary": response.content}


# -----------------------------
# Build LangGraph Workflow
# -----------------------------

def build_upgrade_graph():

    graph = StateGraph(UpgradeState)

    graph.add_node("resolve_repo", resolve_repo)
    graph.add_node("fetch_releases", fetch_releases)
    graph.add_node("summarize_releases", summarize_releases)

    graph.set_entry_point("resolve_repo")

    graph.add_edge("resolve_repo", "fetch_releases")
    graph.add_edge("fetch_releases", "summarize_releases")

    return graph.compile()