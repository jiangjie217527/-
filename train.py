from models import EdgeWeightPredictor

import stim
import beliefmatching
import pymatching
import numpy as np
import itertools

import torch
import torch.nn as nn
from torch_geometric.data import Data
from torch_geometric.loader import DataLoader

def load_data(name,T,M,K):
    y = np.zeros((T,M))
    q_star = np.zeros((T,K))
    p = np.zeros(T)
    f = open("./data/"+name+".txt",'r')
    for i in range(T):
        x = f.readline().split()
        p[i] = float(x[0])
        for j in range(1,M+1):
            y[i][j-1] = float(x[j])
        for j in range(M+1,1+M+K):
            q_star[i][j - (M+1)] = float(x[j])
    return y,q_star,p

def calculate(dem,H,max_order):
    matching = pymatching.Matching.from_detector_error_model(dem)
    K = dem.num_errors
    q =[]
    for i in range(K):
        q.append(dem[i].args_copy()[0])
    q = np.array(q)
    check_matrix = H.check_matrix
    obs_matrix = H.observables_matrix
    prob=.0

    element=np.array([i for i in range(K)])
    for r in range(max_order):
        for comb in itertools.combinations(element,r):
            e = np.array([0] * K,dtype=np.uint8)
            for location in comb:
                e[location] = 1
            syndrome = (check_matrix @ e) %2
            actual_obs = (obs_matrix @ e) %2
            predicted_obs = matching.decode(syndrome, return_observables=True)
            if (not np.equal(actual_obs,predicted_obs)):
                prob += np.prod([q[i] if e[i] else (1-q[i]) for i in range(K)])
    return prob

if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = EdgeWeightPredictor(in_dim=1, hidden_dim=64).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()


    # create edges
    circuit_error_p = [1.0, .9, .8]
    p = 0.01
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=1,
        distance=3,
        after_clifford_depolarization=p * circuit_error_p[0],
        after_reset_flip_probability=p * circuit_error_p[1],
        before_measure_flip_probability=p * circuit_error_p[2]
    )
    dem = circuit.detector_error_model(flatten_loops=True)
    M = dem.num_detectors
    K = dem.num_errors
    H = beliefmatching.detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)
    check_matrix = H.check_matrix.toarray()
    print(M,K,device)
    edge_index = np.zeros((2,K))
    for i in range(K):
        flg = 0
        for j in range(M):
            if check_matrix[j][i] == 1:
                edge_index[flg][i] = j
                flg += 1
        if flg == 1: # 自环
            edge_index[flg][i] = edge_index[0][i]

    edge_index = torch.tensor(edge_index, dtype=torch.long, device=device)
    # end of edges

    train_data_list = []
    test_data_list = []
    T = 9999
    test_size = 99
    batch_size = 256
    name = "2026-04-20-a10000"
    y,q_star,p = load_data(name,T,M,K)
    for i in range(T-test_size):
        data = Data(x=torch.tensor(y[i], dtype=torch.float, device=device).unsqueeze(1),
                    edge_index=edge_index,
                    y_edge=torch.tensor(q_star[i], dtype=torch.float, device=device))
        train_data_list.append(data)

    for i in range(T-test_size,T):
        data = Data(x=torch.tensor(y[i], dtype=torch.float, device=device).unsqueeze(1),
                    edge_index=edge_index,
                    y_edge=torch.tensor(q_star[i], dtype=torch.float, device=device))
        test_data_list.append(data)

    train_loader = DataLoader(train_data_list, batch_size, shuffle=True)
    test_loader = DataLoader(test_data_list,batch_size,shuffle=False)

    # y = torch.tensor(y,dtype=torch.float,device = device)
    # print(model(y,edge_index))


    # train
    epochs = 200

    # for batch in y_loader:
    #     batch = batch.to(torch.float).to(device)
    #     print(model(batch,edge_index))
    #     exit()
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            batch=batch.to(device)
            optimizer.zero_grad()
            pred = model(batch.x,batch.edge_index)
            loss = criterion(pred,batch.y_edge)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * batch.num_graphs
        if epoch % 100 == 0:
            print("loss =",total_loss/len(train_loader.dataset))

    # eval
    model.eval()
    with torch.no_grad():
        cur = T - test_size
        for batch in test_loader:
            batch = batch.to(device)
            pred = model(batch.x, batch.edge_index).cpu().numpy()
            # for j in range(batch.num_graphs):
            #     diff = 0.0
            #     for i in range(K):
            #         y_edge = batch.y_edge[j * K + i].cpu().item()
            #         diff = max(diff,abs(pred[j * K + i] - y_edge)/y_edge)
            #     print(diff)
            for j in range(batch.num_graphs):
                cur_p = p[cur]
                cur +=1
                circuit = stim.Circuit.generated(
                    "surface_code:rotated_memory_z",
                    rounds=1,
                    distance=3,
                    after_clifford_depolarization=cur_p * circuit_error_p[0],
                    after_reset_flip_probability=cur_p * circuit_error_p[1],
                    before_measure_flip_probability=cur_p * circuit_error_p[2]
                )
                dem = circuit.detector_error_model(flatten_loops=True)
                H = beliefmatching.detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)

                dem_pred = stim.DetectorErrorModel()
                error_idx = 0
                for instruction in dem.flattened():
                    if instruction.type == 'error':
                        targets = instruction.targets_copy()
                        dem_pred.append('error', pred[j*K + error_idx], targets)
                        error_idx += 1
                    else:
                        dem_pred.append(instruction)
                H_pred = beliefmatching.detector_error_model_to_check_matrices(dem_pred,
                                                                               allow_undecomposed_hyperedges=True)
                print(calculate(dem_pred, H_pred, 4),calculate(dem,H,4))
