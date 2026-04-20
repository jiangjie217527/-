import pymatching
import beliefmatching
from typing import List
import sinter
import numpy as np
import math
import stim
import os
import threading
import queue
import datetime
import time
import random

q = queue.Queue()

def gen(idx):
    circuit_error_p = [1.0, .9, .8]
    p = idx/200.0
    S = int((1/p) * 300)
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

    q_star = []
    for i in range(K):
        q_star.append(dem[i].args_copy()[0])

    sampler = circuit.compile_detector_sampler()
    sample = sampler.sample(shots=S, bit_packed=False)
    y = np.zeros(M)
    for i in range(M):
        tmp = 0
        for k in range(S):
            tmp += (-1) ** sample[k][i]
        y[i] = -math.log(tmp / S)
    q.put((p,y,q_star))

def multi_rand_gen(x):
    for i in range(x):
        r = random.random()
        if r <= 0.0001:
            continue
        r = r * 15
        gen(r)


if __name__ == '__main__':
    np.set_printoptions(linewidth=100000)
    t = []
    start_time = time.time()
    for i in range(6):
        t.append(threading.Thread(target=multi_rand_gen,args=(1,)))
        t[i].start()
    for i in range(6):
        t[i].join()
    end_time = time.time()
    print("time= ", end_time - start_time)
    msg = "-x10"
    f = open("./data/"+str(datetime.date.today())+msg+".txt","w")
    while not q.empty():
        result = q.get()
        print(result[0],result[1],result[2],file=f)
    f.close()
