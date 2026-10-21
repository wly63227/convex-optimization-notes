"""Deterministic teaching models shared by figures and numeric checks."""
from math import sqrt
import numpy as np

A = np.array([[1., 0.], [0., 1.], [1., 1.]])
B = np.array([1., 2., 2.])

def ridge(lam):
    x = np.linalg.solve(A.T @ A + lam * np.eye(2), A.T @ B)
    fit = float(np.sum((A @ x - B)**2))
    size = float(x @ x)
    return x, fit, size, .5*(fit + lam*size)

def step_sequence(eta, count=8):
    x = 0.
    result = []
    for k in range(count+1):
        result.append({"k": k, "x": x, "error": abs(x-2), "value": (x-2)**2})
        x -= eta*2*(x-2)
    return result

def central_point(t):
    return (1+sqrt(1+2/t))/2

def huber(u, limit=1.):
    return np.where(np.abs(u)<=limit, u*u, 2*limit*np.abs(u)-limit*limit)

def exact_gradient_path(count=12):
    P = np.diag([1.,10.])
    x = np.array([10.,1.])
    path = [x.copy()]
    for _ in range(count):
        g = P@x
        if np.linalg.norm(g)<1e-14:break
        eta = (g@g)/(g@P@g)
        x = x-eta*g
        path.append(x.copy())
    return np.array(path)

def tv_step(lam):
    a=min(lam/2,1.)
    return np.array([a,a,2-a,2-a])
