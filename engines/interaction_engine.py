"""
interaction_engine.py (OGB-powered, real drug names)
------------------------------------------------------
Checks for pairwise drug-drug interactions using the OGB ogbl-ddi edge set.
Drug names are real names (e.g. "Lepirudin") — mapped via OGB CSVs.
"""

from .data_loader import (
    get_interaction_edge_set,
    get_node_degrees,
    get_severity,
    get_name_to_id,
    get_idx_to_db,
    get_ddi_descriptions,
)


def check_interactions(drugs: list) -> list:
    """
    Check all pairwise interactions among the provided list of real drug names.

    Args:
        drugs: List of real drug name strings, e.g. ['Lepirudin', 'Cetuximab']

    Returns:
        List of conflict dicts: {drug1, drug2, severity, description}
    """
    edge_set   = get_interaction_edge_set()
    degrees    = get_node_degrees()
    name_to_id = get_name_to_id()
    idx_to_db  = get_idx_to_db()
    ddi_desc   = get_ddi_descriptions()

    conflicts = []

    num_drugs = len(drugs)
    for i in range(num_drugs):
        for j in range(i + 1, num_drugs):
            name_a = drugs[i]
            name_b = drugs[j]

            id_a = name_to_id.get(name_a, -1)
            id_b = name_to_id.get(name_b, -1)

            if id_a == -1 or id_b == -1:
                continue

            pair = (min(id_a, id_b), max(id_a, id_b))

            if pair in edge_set:
                severity = get_severity(id_a, id_b, degrees)

                # Try to get the real description from OGB data
                db_a = idx_to_db.get(id_a, "")
                db_b = idx_to_db.get(id_b, "")
                db_key = (min(db_a, db_b), max(db_a, db_b))
                description = ddi_desc.get(
                    db_key,
                    f"A known drug interaction exists between {name_a} and {name_b} "
                    f"according to the OGB ogbl-ddi FDA interaction graph."
                )

                conflicts.append({
                    "drug1":       name_a,
                    "drug2":       name_b,
                    "severity":    severity,
                    "description": description,
                })

    return conflicts
