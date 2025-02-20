from typing import Dict, Any
import networkx as nx
import matplotlib.pyplot as plt
import io
from pyvis.network import Network
import json

class VisaGraphVisualizer:
    def __init__(self, neo4j_connector):
        self.neo4j_connector = neo4j_connector
        with self.neo4j_connector as conn:
            self.driver = conn.driver
        
    def get_graph_data(self) -> Dict[str, Any]:
        """Extract graph data from Neo4j"""
        with self.driver.session() as session:
            # Query to get visa types and their relationships
            query = """
            MATCH (v:VisaType)
            RETURN v.name as name, 
                   v.minimum_salary as salary,
                   v.duration as duration,
                   v.processing_time as processing,
                   v.cost as cost
            """
            result = session.run(query)
            nodes = set()
            edges = []
            node_properties = {}
            
            for record in result:
                source = record['n']
                target = record['m']
                relationship = record['r']
                
                # Add nodes and their properties
                nodes.add(source.id)
                nodes.add(target.id)
                node_properties[source.id] = dict(source.items())
                node_properties[target.id] = dict(target.items())
                
                # Add edges
                edges.append({
                    'from': source.id,
                    'to': target.id,
                    'label': type(relationship).__name__
                })
                
            return {
                'nodes': [{'id': n, 'label': node_properties[n].get('name', str(n)), 
                          'properties': node_properties[n]} for n in nodes],
                'edges': edges
            }

    def generate_interactive_html(self, height="750px") -> str:
        """Generate interactive HTML visualization using pyvis"""
        graph_data = self.get_graph_data()
        net = Network(height=height, width="100%", bgcolor="#ffffff", 
                     font_color="black")
        
        # Add nodes and edges to the network
        for node in graph_data['nodes']:
            net.add_node(node['id'], label=node['label'], title=str(node['properties']))
            
        for edge in graph_data['edges']:
            net.add_edge(edge['from'], edge['to'], label=edge['label'])
            
        # Generate HTML file
        html_file = "temp_graph.html"
        net.save_graph(html_file)
        with open(html_file, 'r', encoding='utf-8') as f:
            html_string = f.read()
        return html_string

    def generate_static_plot(self) -> io.BytesIO:
        """Generate static matplotlib plot"""
        graph_data = self.get_graph_data()
        G = nx.Graph()
        
        # Add nodes and edges
        for node in graph_data['nodes']:
            G.add_node(node['id'], label=node['label'])
        for edge in graph_data['edges']:
            G.add_edge(edge['from'], edge['to'])
            
        # Create plot
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightblue', 
                node_size=1500, font_size=8)
        
        # Save to buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        return buf

    def export_graph_json(self) -> str:
        """Export graph data as JSON"""
        return json.dumps(self.get_graph_data(), indent=2)