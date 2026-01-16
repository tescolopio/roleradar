"""Graph database models for relationship tracking."""

import networkx as nx
import pickle
import os


class GraphDatabase:
    """Simple graph database using NetworkX for relationship tracking."""
    
    def __init__(self, filepath="roleradar_graph.pkl"):
        """Initialize graph database."""
        self.filepath = filepath
        self.graph = nx.DiGraph()
        self.load()
    
    def load(self):
        """Load graph from file if exists."""
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'rb') as f:
                    self.graph = pickle.load(f)
            except Exception as e:
                print(f"Error loading graph: {e}")
                self.graph = nx.DiGraph()
    
    def save(self):
        """Save graph to file."""
        try:
            with open(self.filepath, 'wb') as f:
                pickle.dump(self.graph, f)
        except Exception as e:
            print(f"Error saving graph: {e}")
    
    def add_company(self, company_id, **attributes):
        """Add a company node."""
        self.graph.add_node(f"company:{company_id}", type="company", **attributes)
        self.save()
    
    def add_opportunity(self, opportunity_id, company_id, **attributes):
        """Add an opportunity node and link to company."""
        self.graph.add_node(f"opportunity:{opportunity_id}", type="opportunity", **attributes)
        self.graph.add_edge(f"company:{company_id}", f"opportunity:{opportunity_id}", relation="has_opening")
        self.save()
    
    def add_signal(self, signal_id, company_id, signal_type, **attributes):
        """Add a hiring signal and link to company."""
        self.graph.add_node(f"signal:{signal_id}", type="signal", signal_type=signal_type, **attributes)
        self.graph.add_edge(f"company:{company_id}", f"signal:{signal_id}", relation="shows_signal")
        self.save()
    
    def get_company_connections(self, company_id):
        """Get all connections for a company."""
        node_id = f"company:{company_id}"
        if node_id not in self.graph:
            return []
        
        connections = {
            "opportunities": [],
            "signals": []
        }
        
        for neighbor in self.graph.neighbors(node_id):
            node_data = self.graph.nodes[neighbor]
            if node_data.get("type") == "opportunity":
                connections["opportunities"].append(node_data)
            elif node_data.get("type") == "signal":
                connections["signals"].append(node_data)
        
        return connections
    
    def find_companies_with_multiple_signals(self, min_signals=2):
        """Find companies with multiple hiring signals."""
        companies = []
        for node in self.graph.nodes():
            if not node.startswith("company:"):
                continue
            
            signal_count = sum(
                1 for neighbor in self.graph.neighbors(node)
                if self.graph.nodes[neighbor].get("type") == "signal"
            )
            
            if signal_count >= min_signals:
                companies.append({
                    "id": node.replace("company:", ""),
                    "signal_count": signal_count
                })
        
        return companies
