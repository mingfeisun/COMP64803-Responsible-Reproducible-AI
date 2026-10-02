import torch.optim as optim
import matplotlib.pyplot as plt
import torch
from graph_elements.graph import Graph
import numpy as np
import random 

random.seed(42)
torch.manual_seed(42)
np.random.seed(42)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class GraphSolver:
    def __init__(self, graph: Graph, T=24, epochs=1000, lambda_n=100000000, econ_coef=1000):
        self.graph: Graph = graph
        self.epochs = epochs
        self.econ_coef = econ_coef
        self.sources = graph.get_sources()
        self.sinks = graph.get_sinks()
        # 2) Prepare shapes
        self.S = len(self.sources)
        self.D = len(self.sinks)
        self.T = T
        self.matrix_distance = torch.zeros((self.S, self.D))

        for source_idx, source in enumerate(self.sources):
            for sink_idx, sink in enumerate(self.sinks): 
                for connection in source.connections:
                    if connection.node_b.node_id == sink.node_id:
                        self.matrix_distance[source_idx][sink_idx] = connection.weight

        # 3) Instead of masked_select, create a full matrix_power_allocation as a leaf Parameter
        #    The entire (S, D, T) becomes trainable
        self.matrix_power_allocation = torch.nn.Parameter(
            torch.rand((self.S, self.D, self.T), dtype=torch.float)
        )

        # 4) Build connectivity mask
        self.connectivity_mask = (self.matrix_distance != 0).float()  # shape (S, D)
        # Expand to (S, D, T)
        self.connectivity_mask_3d = self.connectivity_mask.unsqueeze(-1).expand(self.S, self.D, self.T)

        # 5) Read node data from the graph (example)
        self._build_node_tensors()

        # 6) Define optimizer *directly on matrix_power_allocation*
        self.optimizer = optim.Adam([self.matrix_power_allocation], lr=15)
        self.losses = []

        # 7) define hyperparameters
        self.lambda_n = lambda_n

    def _build_node_tensors(self):
        # for demonstration, collect S sources and D sinks
        self.list_total_power = []
        self.list_lcoe = []
        self.list_econ_coefficient = []
        self.list_demand_profile = []
        
        for source in self.sources:
            self.list_total_power.append(source.get_power_output_series())
            self.list_lcoe.append(source.get_lcoe_output_series())

        for sink in self.sinks:
            self.list_econ_coefficient.append(self.econ_coef)
            self.list_demand_profile.append(sink.demand_profile)

        self.list_total_power = torch.tensor(self.list_total_power, dtype=torch.float)
        self.list_lcoe       = torch.tensor(self.list_lcoe,       dtype=torch.float)
        self.list_econ_coefficient = torch.tensor(self.list_econ_coefficient, dtype=torch.float)
        self.list_demand_profile   = torch.tensor(self.list_demand_profile,   dtype=torch.float)
        
    def solve(self):    
        for epoch in range(self.epochs):
            self.optimizer.zero_grad()
            power_allocation_valid = torch.nn.ReLU()(self.matrix_power_allocation) * self.connectivity_mask_3d

            dist_3d = self.matrix_distance.unsqueeze(-1).expand(self.S, self.D, self.T)
            received_power = (power_allocation_valid * dist_3d).sum(dim=0) 

            U = self.list_demand_profile - received_power 
            cost_term = (self.list_lcoe * torch.relu(power_allocation_valid.sum(dim=1))).sum()
            
            econ_term = self.list_econ_coefficient[:, None] * torch.nn.ReLU()(U)
            J = torch.sum(econ_term) + torch.sum(cost_term)

            supply_violations = self.lambda_n * (power_allocation_valid.sum(dim=1) - self.list_total_power)
        
            L_supply = torch.relu(supply_violations)
            
            L_total = J + torch.sum(L_supply)
            L_total.backward()

            self.optimizer.step()
            self.losses.append(L_total.item())

            if epoch % 200 == 0:
                print(f"Epoch {epoch}, Loss: {L_total.item():.4f}")
                print(f"Unmet {torch.relu(U)}")

        return torch.nn.ReLU()(self.matrix_power_allocation).detach(), self.losses
