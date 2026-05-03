"""Minimal usage demo — requires an extracted DataForge directory.

Usage:
    uv run main.py <path-to-DataForge-records-dir>
"""

import sys
from pathlib import Path

from forge_lens import DataForgeLoader, Graph, Query


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: uv run main.py <path-to-DataForge-records-dir>")
        sys.exit(1)

    root = Path(sys.argv[1])
    loader = DataForgeLoader(root).load()
    print(f"Loaded {len(loader)} records across {len(loader.record_types)} types")

    results = Query(loader).of_type("EntityClassDefinition").all()
    print(f"EntityClassDefinition records: {len(results)}")

    graph = Graph(loader)
    graph.build()
    print(repr(graph))


if __name__ == "__main__":
    main()
