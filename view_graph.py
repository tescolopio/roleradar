#!/usr/bin/env python3
"""Visualize the relationship graph structure."""

from src.roleradar.models.graph import GraphDatabase

def main():
    graph_db = GraphDatabase()

    print("=" * 80)
    print("RoleRadar Graph Database Structure")
    print("=" * 80)

    # Count node types
    companies = sum(1 for n in graph_db.graph.nodes() if n.startswith("company:"))
    opportunities = sum(1 for n in graph_db.graph.nodes() if n.startswith("opportunity:"))
    signals = sum(1 for n in graph_db.graph.nodes() if n.startswith("signal:"))

    print(f"\nNodes:")
    print(f"  Companies: {companies}")
    print(f"  Opportunities: {opportunities}")
    print(f"  Signals: {signals}")
    print(f"  Total Nodes: {graph_db.graph.number_of_nodes()}")
    print(f"  Total Edges: {graph_db.graph.number_of_edges()}")

    # Show some example relationships
    print(f"\nExample Relationships:")
    print("-" * 80)

    edge_count = 0
    for source, target, data in graph_db.graph.edges(data=True):
        if edge_count >= 10:
            break

        source_type = source.split(":")[0]
        target_type = target.split(":")[0]
        relation = data.get("relation", "connected to")

        source_data = graph_db.graph.nodes[source]
        target_data = graph_db.graph.nodes[target]

        if source_type == "company":
            company_name = source_data.get("name", "Unknown")
            if target_type == "opportunity":
                job_title = target_data.get("title", "Unknown Role")
                print(f"  {company_name} → {relation} → {job_title}")
            elif target_type == "signal":
                signal_type = target_data.get("signal_type", "unknown")
                print(f"  {company_name} → {relation} → {signal_type} signal")

        edge_count += 1

    # Find companies with multiple signals
    print(f"\nCompanies with Multiple Signals:")
    print("-" * 80)
    multi_signal_companies = graph_db.find_companies_with_multiple_signals(min_signals=2)
    for comp in multi_signal_companies[:5]:
        company_id = f"company:{comp['id']}"
        company_data = graph_db.graph.nodes.get(company_id, {})
        company_name = company_data.get("name", "Unknown")
        print(f"  {company_name}: {comp['signal_count']} signals")

    print("=" * 80)

if __name__ == "__main__":
    main()
