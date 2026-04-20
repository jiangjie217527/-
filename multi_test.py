import multiprocessing
import numpy as np

from multiprocessing import Process

def fun(x):
    return x**2

def ite(x,i):
    x[i]*=i

if __name__ == '__main__':
    number =Array( np.array([1,2,3]))

    pool = multiprocessing.Pool()
    result = pool.map(fun,number)
    pool.close()
    pool.join()
    print(number)

    pool = multiprocessing.Pool()
    result = pool.map(fun,number)
    pool.close()
    pool.join()
    print(number)

    p = []
    for i in range(3):
        p.append(Process(target=ite,args=(number,i)))
        p[i].start()
    for i in range(3):
        p[i].join()
    print(number)


