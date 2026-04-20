import pymatching
import sinter
from typing import List
import os
import numpy as np
import stim
import itertools
import matplotlib.pyplot as plt
import beliefmatching
from numpy import dtype
from numpy.matlib import rand
from stimbposd import SinterDecoder_BPOSD, sinter_decoders
import math
import random
import time
import multiprocessing

print(stim.__version__,os.cpu_count())


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


def get_Am(A,m,q,M,check_matrix):
    for i in range(q):
        m[i] = random.randint(1, 2 ** M-1)
        cur = m[i]
        for j in range(M):
            if (cur & 1 == 1):
                A[i] ^= check_matrix[j]
            cur >>= 1
    return (A,m)

def get_Am_full(A,m,M,check_matrix):
    for i in range(1,2**M):
        m[i - 1] = i
        cur = i
        for j in range(M):
            if cur & 1 == 1:
                A[i - 1] ^= check_matrix[j]
            cur >>= 1
    return (A,m)


def get_lambda(y,m,q,S,sample_int):
    for i in range(q):
        tmp = 0
        for k in range(S):
            tmp += (-1) ** ((m[i] & sample_int[k]).bit_count() )
        y[i] = -math.log(tmp / S)
    return y

if __name__ == '__main__':
    circuit_error_p = [1.0, .9, .8]
    p = .001
    S = int((1/p) * 100)

    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=1,
        distance=3,
        after_clifford_depolarization=p * circuit_error_p[0],
        after_reset_flip_probability=p * circuit_error_p[1],
        before_measure_flip_probability=p * circuit_error_p[2]
    )
    dem = circuit.detector_error_model(flatten_loops=True)
    K = dem.num_errors
    M = dem.num_detectors

    q_star = []
    q_c = []
    for i in range(K):
        q_star.append(dem[i].args_copy()[0])

    H = beliefmatching.detector_error_model_to_check_matrices(dem, allow_undecomposed_hyperedges=True)
    check_matrix = H.check_matrix.toarray()
    delta = 0.1
    q = int(delta ** (-2) * K * max(math.log(K / delta) ** 2 * math.log(1 / delta) ** 2 * math.log(K),
                                    math.log(1 / .01)) / 40)
    q = 2 ** M - 1
    print(S,q,K,M)
    A = np.zeros((q,K),dtype=np.uint8)
    y = np.zeros(q)
    m = np.zeros(q,dtype=np.uint8)

    sampler = circuit.compile_detector_sampler()
    sample = sampler.sample(shots=S, bit_packed=False)
    sample_int = np.zeros(S, dtype=np.uint8)
    for k in range(S):
        for i, b in enumerate(sample[k]):
            sample_int[k] |= np.uint8(b << i)
        # for b in sample[k]:
        #     sample_int[k] = (sample_int[k]<<1) | b
    start_time = time.time()
    A,m = get_Am_full(A,m,M,check_matrix)
    y = get_lambda(y,m, q, S, sample_int)
    end_time = time.time()
    print("time= ",end_time - start_time)
    x = np.linalg.lstsq(A,y,rcond=None)

    for i in range(K):
        q_c.append(0.5*(1-math.exp(-x[0][i])) )
    diff = 0
    for i in range(K):
        diff = max(diff,math.fabs(q_c[i]-q_star[i])/q_star[i])
    print(diff)

    print("---")
    diff = 0
    loc = 0
    for i in range(q):
        tmp = .0
        for j in range(K):
            tmp += A[i][j]*(-math.log(1-2*q_star[j]))
        ans = math.fabs(tmp-y[i])
        if(ans > diff):
            diff = ans
            loc = i
    print(diff/y[i],diff)

    dem_pred = stim.DetectorErrorModel()
    error_idx = 0
    for instruction in dem.flattened():
        if instruction.type == 'error':
            targets = instruction.targets_copy()
            dem_pred.append('error', q_c[error_idx], targets)
            error_idx += 1
        else:
            dem_pred.append(instruction)
    H_pred =beliefmatching.detector_error_model_to_check_matrices(dem_pred, allow_undecomposed_hyperedges=True)
    print(calculate(dem_pred,H_pred,4))

