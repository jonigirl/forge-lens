# dfq — DataForge Query

[![PyPI](https://img.shields.io/pypi/v/dfq)](https://pypi.org/project/dfq/)
[![GitHub](https://img.shields.io/badge/github-jonigirl%2Fforge--lens-blue)](https://github.com/jonigirl/forge-lens)

Python library for loading, querying, and traversing Star Citizen DataForge XML records extracted by [unp4k/unforge](https://github.com/dolkensp/unp4k).

---

## Install

```
pip install dfq
```

---

## Quickstart

```python
from dfq import DataForgeLoader, Query, Graph

# Load all extracted DataForge XML files
loader = DataForgeLoader(r"C:\SCData\Data\Libs\Foundry\Records")
loader.load()

# Query records by type and attribute
results = (
    Query(loader)
    .of_type("SItemCooler")
    .where("__name", "COOLER_S01_INDUSTRIAL_FLEXI")
    .all()
)

for elem in results:
    print(elem.attrib)

# Build UUID graph for relationship traversal
graph = Graph(loader)
graph.build()

# Resolve a UUID to a display name
name = graph.resolve_name("some-uuid-here")
```

---

## Legal Notice

Star Citizen and all associated game data are the property of Cloud Imperium Rights LLC. dfq only reads files from your own licensed installation and does not redistribute any RSI or CIG content. This is an unofficial fan tool, not affiliated with or endorsed by Cloud Imperium Games.

---

## Links

- [PyPI — dfq](https://pypi.org/project/dfq/)
- [GitHub — forge-lens](https://github.com/jonigirl/forge-lens)
- [Bug Tracker](https://github.com/jonigirl/forge-lens/issues)
