"""
forge_lens — DataForge Query library.

Load, query, and traverse Star Citizen DataForge XML records.
Users supply their own extracted DataForge files.

Modules:
    loader  — scan and load extracted XML directories
    query   — filter and select records by type / attribute
    graph   — UUID resolution and relationship traversal
    schema  — known record types and field mappings
    export  — serialise results to dict / JSON / CSV
"""

from forge_lens.graph import Graph
from forge_lens.loader import DataForgeLoader
from forge_lens.query import Query

__all__ = ["DataForgeLoader", "Query", "Graph"]
__version__ = "0.2.0"
