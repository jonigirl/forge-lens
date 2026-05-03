"""
dfq — DataForge Query library.

Load, query, and traverse Star Citizen DataForge XML records.
Users supply their own extracted DataForge files.

Modules:
    loader  — scan and load extracted XML directories
    query   — filter and select records by type / attribute
    graph   — UUID resolution and relationship traversal
    schema  — known record types and field mappings
    export  — serialise results to dict / JSON / CSV
"""

from dfq.graph import Graph
from dfq.loader import DataForgeLoader
from dfq.query import Query

__all__ = ["DataForgeLoader", "Query", "Graph"]
__version__ = "0.1.0"
