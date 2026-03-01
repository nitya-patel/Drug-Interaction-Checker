"""
data_loader.py
--------------
Downloads and caches the OGB ogbl-ddi dataset.
Provides:
  - get_drug_names()             -> list of real drug name strings (e.g. "Lepirudin")
  - get_name_to_id()             -> dict {drug_name: node_idx}
  - get_interaction_edge_set()   -> set of (int, int) tuples for O(1) pair lookup
  - get_ddi_descriptions()       -> dict {(db_id_a, db_id_b): description_str}
  - get_num_drugs()              -> int total number of drug nodes
"""

# ── PyTorch 2.6+ compatibility fix ──────────────────────────────────────────── #
import torch as _torch
_original_torch_load = _torch.load
def _patched_torch_load(f, *args, **kwargs):
    kwargs.setdefault("weights_only", False)
    return _original_torch_load(f, *args, **kwargs)
_torch.load = _patched_torch_load
# ────────────────────────────────────────────────────────────────────────────── #

from ogb.linkproppred import LinkPropPredDataset
import pandas as pd
import os

# ── Module-level caches ──────────────────────────────────────────────────────── #
_dataset     = None
_edge_set    = None
_drug_names  = None          # list[str] in node-index order
_name_to_id  = None          # dict {name: node_idx}
_idx_to_db   = None          # dict {node_idx: DrugBank-ID (e.g. "DB00001")}
_ddi_desc    = None          # dict {(db_id_a, db_id_b): description}
_HIGH_DEGREE_THRESHOLD = 500


def _load_dataset():
    global _dataset
    if _dataset is None:
        _dataset = LinkPropPredDataset(name="ogbl-ddi")
    return _dataset


def _get_mapping_dir() -> str:
    # __file__ is engines/data_loader.py; go up to medigraph/ first
    engines_dir = os.path.dirname(os.path.abspath(__file__))
    medigraph_dir = os.path.dirname(engines_dir)
    return os.path.join(medigraph_dir, "dataset", "ogbl_ddi", "mapping")


def _build_name_maps():
    """Build idx→real-name and name→idx maps using OGB mapping CSVs."""
    global _drug_names, _name_to_id, _idx_to_db
    if _drug_names is not None:
        return

    mapping_dir = _get_mapping_dir()

    # 1. node_idx → DrugBank ID
    node2drug = pd.read_csv(os.path.join(mapping_dir, "nodeidx2drugid.csv.gz"))
    node2drug.columns = ["node_idx", "drug_id"]

    # 2. DrugBank ID → real name (from description file)
    desc = pd.read_csv(os.path.join(mapping_dir, "ddi_description.csv.gz"),
                        usecols=["first drug id", "first drug name",
                                  "second drug id", "second drug name"])
    id2name: dict[str, str] = {}
    for _, row in desc[["first drug id", "first drug name"]].drop_duplicates().iterrows():
        id2name[row["first drug id"]] = row["first drug name"]
    for _, row in desc[["second drug id", "second drug name"]].drop_duplicates().iterrows():
        id2name[row["second drug id"]] = row["second drug name"]

    # 3. Build idx → real name list (fallback to DB-ID if somehow missing)
    names = []
    idx_to_db = {}
    for _, row in node2drug.sort_values("node_idx").iterrows():
        idx  = int(row["node_idx"])
        dbid = row["drug_id"]
        real = id2name.get(dbid, dbid)        # fallback to DrugBank ID
        names.append(real)
        idx_to_db[idx] = dbid

    # Deduplicate names (some drugs may share a common name, append DrugBank ID)
    seen: dict[str, int] = {}
    unique_names = []
    for name in names:
        if name in seen:
            seen[name] += 1
            unique_names.append(f"{name} ({idx_to_db[len(unique_names)]})")
        else:
            seen[name] = 1
            unique_names.append(name)

    _drug_names = unique_names
    _name_to_id = {name: idx for idx, name in enumerate(unique_names)}
    _idx_to_db  = idx_to_db


def _build_ddi_descriptions():
    """Build (db_id_a, db_id_b) → description dict from the OGB description CSV."""
    global _ddi_desc
    if _ddi_desc is not None:
        return

    mapping_dir = _get_mapping_dir()
    desc = pd.read_csv(os.path.join(mapping_dir, "ddi_description.csv.gz"))
    _ddi_desc = {}
    for _, row in desc.iterrows():
        a, b, d = row["first drug id"], row["second drug id"], row["description"]
        key = (min(a, b), max(a, b))
        _ddi_desc[key] = str(d)


# ── Public API ───────────────────────────────────────────────────────────────── #

def get_num_drugs() -> int:
    ds = _load_dataset()
    return ds[0]["num_nodes"]


def get_drug_names() -> list:
    _build_name_maps()
    return _drug_names


def get_name_to_id() -> dict:
    _build_name_maps()
    return _name_to_id


def get_idx_to_db() -> dict:
    _build_name_maps()
    return _idx_to_db


def get_interaction_edge_set() -> set:
    global _edge_set
    if _edge_set is None:
        ds = _load_dataset()
        graph = ds[0]
        edge_index = graph["edge_index"]
        sources = edge_index[0].tolist()
        targets = edge_index[1].tolist()
        _edge_set = set()
        for s, t in zip(sources, targets):
            _edge_set.add((min(s, t), max(s, t)))
    return _edge_set


def get_ddi_descriptions() -> dict:
    _build_ddi_descriptions()
    return _ddi_desc


def get_node_degrees() -> dict:
    ds = _load_dataset()
    graph = ds[0]
    edge_index = graph["edge_index"]
    degrees: dict = {}
    for node_id in edge_index[0].tolist() + edge_index[1].tolist():
        degrees[node_id] = degrees.get(node_id, 0) + 1
    return degrees


def get_severity(node_id_a: int, node_id_b: int, degrees: dict) -> str:
    deg_a = degrees.get(node_id_a, 0)
    deg_b = degrees.get(node_id_b, 0)
    if deg_a > _HIGH_DEGREE_THRESHOLD or deg_b > _HIGH_DEGREE_THRESHOLD:
        return "Severe"
    return "Moderate"
