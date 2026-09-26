import numpy as np
from OCP.gp import gp_Pnt, gp_Vec

def to_np_pnt(p: gp_Pnt) -> np.ndarray:
    return np.array([p.X(), p.Y(), p.Z()])
 
def to_np_vec(v: gp_Vec) -> np.ndarray:
    return np.array([v.X(), v.Y(), v.Z()])
 
def normalize(v: np.ndarray) -> np.ndarray:
    m = np.linalg.norm(v)
    return v / m if m > 1e-14 else v

