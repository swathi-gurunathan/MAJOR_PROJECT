import torch
import pandas as pd
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from sklearn.preprocessing import LabelEncoder, StandardScaler
import re

# Function to prepare PyG Data object
def prepare_data(nodes_file, edges_file, features_file, labels_file):
    # Load CSV files
    nodes_df = pd.read_csv(nodes_file)
    edges_df = pd.read_csv(edges_file)
    features_df = pd.read_csv(features_file)
    labels_df = pd.read_csv(labels_file)

    # Normalize the 'id' column in features_df to extract email addresses
    features_df['id'] = features_df['id'].apply(lambda x: re.search(r'<(.*?)>', x).group(1) if '<' in x else x)

    # Encode node IDs as integers
    le = LabelEncoder()
    nodes_df['node_idx'] = le.fit_transform(nodes_df['id'])
    id_map = dict(zip(nodes_df['id'], nodes_df['node_idx']))

    # Debugging: Print nodes DataFrame
    print("Nodes DataFrame:")
    print(nodes_df.head())

    # Prepare node features
    print("Features DataFrame before mapping:")
    print(features_df.head())
    features_df['id'] = features_df['id'].map(id_map)
    features_df = features_df.dropna(subset=['id'])  # Drop rows with NaN ID after mapping
    print("Features DataFrame after mapping:")
    print(features_df.head())

    # Check if features_df is empty
    if features_df.empty:
        raise ValueError("Features DataFrame is empty after mapping. Check the input files for mismatched IDs.")

    features_df = features_df.sort_values('id')
    x = torch.tensor(
        StandardScaler().fit_transform(features_df.drop(columns=['id']).values),
        dtype=torch.float
    )

    # Prepare labels (ensure they align with features)
    labels_df['id'] = labels_df['id'].map(id_map)
    labels_df = labels_df.dropna(subset=['id'])  # Drop unmapped
    labels_df = labels_df.sort_values('id')

    # Align labels to feature nodes only
    merged_df = pd.merge(features_df, labels_df, on='id', how='inner')
    x = torch.tensor(
        StandardScaler().fit_transform(merged_df.drop(columns=['id', 'label']).values),
        dtype=torch.float
    )
    y = torch.tensor(merged_df['label'].values, dtype=torch.long)

    # Filter edges to include only nodes present in features_df
    valid_node_ids = set(features_df['id'])
    edges_df = edges_df[edges_df['source'].isin(valid_node_ids) & edges_df['target'].isin(valid_node_ids)]

    # Map edge indices to the filtered node set
    edges_df['source'] = edges_df['source'].map(id_map)
    edges_df['target'] = edges_df['target'].map(id_map)
    edge_index = torch.tensor(edges_df[['source', 'target']].values.T, dtype=torch.long)

    return Data(x=x, edge_index=edge_index, y=y)

# Define a simple GNN
class GCN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index).relu()
        x = self.conv2(x, edge_index)
        return x

# Function to train the GNN
def train_gnn(data, input_dim, hidden_dim, output_dim, epochs=100, lr=0.01):
    model = GCN(input_dim=input_dim, hidden_dim=hidden_dim, output_dim=output_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = torch.nn.CrossEntropyLoss()

    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        out = model(data)
        loss = criterion(out, data.y)
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch+1}: Loss = {loss.item():.4f}")

if __name__ == "__main__":
    # File paths
    nodes_file = "nodes.csv"
    edges_file = "edges.csv"
    features_file = "features.csv"
    labels_file = "labels.csv"

    # Prepare data
    data = prepare_data(nodes_file, edges_file, features_file, labels_file)

    # Define model parameters
    input_dim = data.x.shape[1]  # Number of input features
    hidden_dim = 16              # Hidden layer size
    output_dim = len(data.y.unique())  # Number of classes

    # Train the GNN
    train_gnn(data, input_dim, hidden_dim, output_dim, epochs=100, lr=0.01)