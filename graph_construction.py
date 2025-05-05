import networkx as nx
import pandas as pd

# Function to create a graph from email data
def create_graph(email_data):
    G = nx.DiGraph()

    for email_entry in email_data:
        from_node = email_entry["from_email"]
        to_node = email_entry["to_email"]
        subject = email_entry["subject"]

        if from_node and to_node:
            # Add nodes and edge
            G.add_node(from_node)
            G.add_node(to_node)
            G.add_edge(from_node, to_node, subject=subject)

    return G

# Function to save graph nodes and edges to CSV
def save_graph_to_csv(G, nodes_file, edges_file):
    nodes = list(G.nodes)
    edges = list(G.edges(data=True))

    # Save nodes
    nodes_df = pd.DataFrame({"id": nodes})
    nodes_df.to_csv(nodes_file, index=False)

    # Save edges
    edges_df = pd.DataFrame([(u, v, d['subject']) for u, v, d in edges], columns=["source", "target", "subject"])
    edges_df.to_csv(edges_file, index=False)