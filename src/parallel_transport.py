import numpy as np
from src.utils import to_np_vec, normalize

def sample_curve(curve, tmin, tmax, num_samples=100):
    s_samples = np.linspace(tmin, tmax, num_samples, endpoint=True)
    positions = []
    tangents = []
    
    for t in s_samples:
        p = curve.Value(t)
        positions.append(np.array([p.X(), p.Y(), p.Z()]))
        
        dpds = curve.DN(t, 1)
        T = np.array([dpds.X(), dpds.Y(), dpds.Z()])
        tangents.append(normalize(T))
        
    return np.array(positions), np.array(tangents), s_samples

def compute_transported_frames(curve, tmin, tangents):
    # Initial frame
    t_arr = tangents[0]
    normal_approx = to_np_vec(curve.DN(tmin, 2))
    n_arr = normalize(normal_approx - np.dot(normal_approx, t_arr) * t_arr)
    
    # Omegas
    omegas = []
    for i in range(len(tangents) - 1):
        T0, T1 = tangents[i], tangents[i + 1]
        omega = np.cross(T0, T1)
        omegas.append(normalize(omega))
    
    # Transport
    T_curr, N_curr = t_arr.copy(), n_arr.copy()
    frames = [(T_curr.copy(), N_curr.copy())]
    
    for i in range(len(tangents) - 1):
        T_next = tangents[i + 1]
        cos_theta = np.clip(np.dot(T_curr, T_next), -1.0, 1.0)
        sin_theta = np.linalg.norm(np.cross(T_curr, T_next))
        theta = np.arctan2(sin_theta, cos_theta)
        
        if theta < 1e-10:
            N_next = N_curr.copy()
        else:
            omega_hat = omegas[i]
            N_par = np.dot(N_curr, omega_hat) * omega_hat
            N_perp = N_curr - N_par
            N_next = N_par + N_perp * cos_theta + np.cross(omega_hat, N_perp) * sin_theta
            
        N_next = normalize(N_next - np.dot(N_next, T_next) * T_next)
        frames.append((T_next.copy(), N_next.copy()))
        T_curr, N_curr = T_next, N_next
        
    return frames, t_arr, n_arr

def apply_holonomy_correction(frames):
    T_first, N_first = frames[0]
    T_last, N_last = frames[-1]
    
    sin_phi = np.dot(np.cross(N_first, N_last), T_first)
    cos_phi = np.dot(N_first, N_last)
    phi = np.arctan2(sin_phi, cos_phi)
    
    N_total = len(frames)
    corrected = []
    
    for i, (T, N) in enumerate(frames):
        theta_correction = phi * i / (N_total - 1)
        cos_c, sin_c = np.cos(theta_correction), np.sin(theta_correction)
        B = np.cross(T, N)
        
        N_corrected = normalize(cos_c * N - sin_c * B)
        corrected.append((T.copy(), N_corrected.copy()))
        
    return corrected