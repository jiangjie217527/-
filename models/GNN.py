import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import GCNConv


class EdgeWeightPredictor(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim=1):
        super().__init__()
        # 两层GCN
        self.conv1 = GCNConv(in_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        # 边预测MLP
        self.edge_mlp = nn.Sequential(
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, out_dim)
        )

    def forward(self, x, edge_index):
        # x: (N, in_dim)
        # edge_index: (2, E)
        h = F.relu(self.conv1(x, edge_index))
        h = F.relu(self.conv2(h, edge_index))  # (N, hidden_dim)

        # 获取每条边的两端嵌入
        row, col = edge_index
        edge_emb = torch.cat([h[row], h[col]], dim=1)  # (E, hidden_dim*2)
        edge_weight = self.edge_mlp(edge_emb).squeeze()  # (E,)
        return torch.nn.functional.softplus(edge_weight)