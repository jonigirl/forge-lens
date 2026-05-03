# forge-lens — DataForge Query

[![PyPI](https://img.shields.io/pypi/v/forge-lens)](https://pypi.org/project/forge-lens/)
[![GitHub](https://img.shields.io/badge/github-jonigirl%2Fforge--lens-blue)](https://github.com/jonigirl/forge-lens)

Python library for loading, querying, and traversing Star Citizen DataForge XML records extracted by [unp4k/unforge](https://github.com/dolkensp/unp4k).

---

## Install

```
pip install forge-lens
```

---

## Quickstart

```python
from forge_lens import DataForgeLoader, Query, Graph

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

# Find all blueprints that craft a given entity UUID
blueprints = graph.blueprints_producing("entity-uuid-here")

# Find all reward pools that drop a given blueprint UUID
pools = graph.pools_containing("blueprint-uuid-here")

# Craft tree — nested dict of ingredients and what it produces
tree = graph.crafting_tree("blueprint-uuid-here")

# Reward pool — sorted list of item names in a pool
names = graph.reward_pool("pool-uuid-here")

# Fingerprint — detect when game data has changed after a patch
fp = loader.fingerprint()  # 12-char hex string; compare across sessions
```

---

## Legal Notice

Star Citizen and all associated game data are the property of Cloud Imperium Rights LLC. forge-lens only reads files from your own licensed installation and does not redistribute any RSI or CIG content. This is an unofficial fan tool, not affiliated with or endorsed by Cloud Imperium Games.

---

## Links

- [PyPI — forge-lens](https://pypi.org/project/forge-lens/)
- [GitHub — forge-lens](https://github.com/jonigirl/forge-lens)
- [Bug Tracker](https://github.com/jonigirl/forge-lens/issues)
