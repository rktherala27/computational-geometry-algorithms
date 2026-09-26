import os
from src.curve_builder import build_periodic_curve, create_wire_from_curve
from src.parallel_transport import sample_curve, compute_transported_frames, apply_holonomy_correction
from src.plate_modelling import export_stacked_plates

# Control points from original notebook
CTRL_PTS = [
    ( 1.00,  0.50,  0.00), ( 1.20,  0.42, -0.80), ( 1.60,  0.28, -1.50),
    ( 2.10,  0.08, -1.20), ( 2.50,  0.00,  0.00), ( 2.30, -0.22,  1.00),
    ( 1.80, -0.45,  1.50), ( 1.30, -0.50,  1.30), ( 1.00, -0.35,  0.80),
    ( 0.95, -0.10,  0.50), ( 1.00,  0.15,  0.20), ( 1.00,  0.50,  0.00),
]

def main():
    os.makedirs("output", exist_ok=True)
    
    print("Building base curve...")
    curve, tmin, tmax = build_periodic_curve(CTRL_PTS)
    base_wire = create_wire_from_curve(curve, tmin, tmax)
    
    print("Computing kinematics and parallel transport...")
    positions, tangents, _ = sample_curve(curve, tmin, tmax)
    frames, _, _ = compute_transported_frames(curve, tmin, tangents)
    
    print("Applying holonomy correction...")
    corrected_frames = apply_holonomy_correction(frames)
    
    print("Generating sweeps and stackable plates...")
    export_stacked_plates(corrected_frames, positions, base_wire, out_dir="output")
    
    print("Pipeline complete.")

if __name__ == "__main__":
    main()