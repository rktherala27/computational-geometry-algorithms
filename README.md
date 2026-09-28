

Profile avatar



README_poisson_solver
Document
The README is ready. Four things to settle before pushing, since I wrote the file names from your repo description:

File names: I used serial.cpp, openmp.cpp, mpi_matrix.cpp, mpi_domain.cpp as placeholders. Replace them with your actual filenames, and consider renaming the two MPI files to something meaningful like that if they are currently version1/version2, because the names now carry the design distinction

Leftover debug print in the serial code: the CG function prints every entry of Ap before the iteration loop. With N = 100 that floods the console, and it looks like leftover debugging. Delete that block before pushing

Inconsistent defaults: the serial version runs N = 4 with tolerance 1e-8 and max 10000 iterations, while the parallel versions run N = 100 with 1e-6 and 1000. Anyone comparing runtimes across the four programs would measure different problems. Either unify the constants, or state the defaults per file in the README. Unifying is the better fix, it is five lines

OpenMP timing: the stray second omp_get_wtime() assignment in main() still muddles what is being measured. Also worth fixing while you are in the file

The README deliberately frames the two MPI versions as two designs of the same algorithm with different communication structure, because that framing is what makes the repo interesting to someone like Moses. It also leaves the convergence study and CUDA extension mentioned under Status, so if either is not actually done yet, either finish it or cut the line before pushing.

That is three of the four repos with proper READMEs now, rotation, particle transport, and Poisson. The remaining one from the email was the sweep geometry project, if you want to keep going.

Basically this repo is currently getting restructured with modern c++ concepts integration into the legacy code. These 4 files are present in legacy folder and the other folders are being created to extend this solver for new simulation scenarios like convection diffusion equation in 2D



README_poisson_solver
Document
Updated. The README now tells the full arc of the repo: solver built from scratch and verified in four standalone forms, then restructured with modern C++ and extended to convection-diffusion. That narrative, legacy reference plus active modernization, is more interesting to a reviewer than a finished static solver, because it shows both the numerical foundation and the software engineering direction.

A few things to check when you apply it:

I assumed legacy/ as the folder name and the same four file placeholders as before. Fix the names to match what actually exists, including the build commands if the new layout puts a CMakeLists at the root

The modern C++ section is deliberately written in prose rather than a file table, because that layer is still taking shape. Once the structure settles, add the actual layout and build instructions there, one short code block is enough

The earlier code fixes still apply to the legacy files: the debug print of Ap in the serial CG, the OpenMP timing block, the swapped halo comments in mpi_domain, and the inconsistent defaults between the serial and parallel versions. Since the legacy folder is now explicitly a reference, having it clean matters more, because that is the version people will read against the new structure

One consideration on the convection-diffusion extension: the CG solver only applies while the system stays symmetric positive definite. With a dominant convection term the discretized operator generally loses symmetry, so the natural next solver is BiCGSTAB or GMRES. Worth deciding early, since it affects whether the restructured solver interface needs to support more than CG

That covers all four repos that were going into the Tensiq reply: rotation, particle transport, Poisson, and the DLR evidence story for the email. When the restructured Poisson code is ready, the modern C++ section of that README can grow into its own short document if it gets too dense.

import os
from src.curve_builder import build_periodic_curve, create_wire_from_curve
from src.parallel_transport import sample_curve, compute_transported_frames, apply_holonomy_correction
from src.plate_modelling import export_stacked_plates

Control points from original notebook
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
    frames, ,  = compute_transported_frames(curve, tmin, tangents)
    

    print("Applying holonomy correction...")
    corrected_frames = apply_holonomy_correction(frames)
    

    print("Generating sweeps and stackable plates...")
    export_stacked_plates(corrected_frames, positions, base_wire, out_dir="output")
    

    print("Pipeline complete.")

if _name_ == "_main_":
    main()

This is another project I did for proxima fusion interview. I want to update the readme file for this. Do you remember how we structured the folders for this? See in other chats


I checked our chat history for this project. I found the context around it, the OCCT and B-rep work and the Proxima interview prep, but not the exact folder structure we settled on. What I can reconstruct reliably is from your main.py imports: a src/ package with three modules, curve_builder, parallel_transport, and plate_modelling, plus an output/ directory the pipeline writes to. If we structured it differently back then, correct me and I will adjust.

Here is the README based on that structure and what the pipeline does.


README_sweep_geometry
Document
The README is ready. Three things to confirm before it goes in, since I reconstructed them rather than remembering them:

Structure: I wrote it as main.py plus src/ with the three module names your imports show. If the repo has anything more, like a tests/ folder or differently named entry script, tell me and I will match it

Dependency: I listed pythonocc-core as the OCCT binding, which is the standard choice for this kind of work. If you use a different binding or a specific OCCT version, fix that line, since a wrong dependency line is worse than none

Output format: I kept the export description generic, one file per plate in output/. If the plates are exported as STEP or STL, say so in the plate_modelling line, the format is part of what makes it manufacturing-relevant

One writing choice worth mentioning: I framed the README around the actual geometric problem, torsion-free sweeping on closed curves, rather than the interview it came from. The Proxima Fusion context belongs in your conversation with Moses or in the repo's commit history, not the README, where the work should stand on its own.

That is now all four repos covered, rotation, particle transport, Poisson, and sweep geometry, each with a README that states the problem, the method, and honest limitations. Combined with the DLR evidence plan and the reply draft, the Tensiq material is essentially complete except for the fixes we flagged in each repo and the convergence plots. Anything else you want prepared before you fly out?

# 3D Sweep Geometry: Rotation-Minimizing Frames and Stackable Plates

Sweeps cross-sections along arbitrary closed 3D curves without unwanted
torsion, using parallel-transported frames, and exports the swept geometry as
stackable plates. Built on OpenCASCADE Technology (OCCT) through its Python
bindings.

The driving problem: when a cross-section is swept along a 3D curve using a
naive fixed reference frame, the profile picks up artificial twisting. This
pipeline replaces that with rotation-minimizing frames computed by parallel
transport, corrects the holonomy so the frames close consistently on the
periodic curve, and exports the result as plates that can be stacked
manufacturing-style.

## Pipeline

The `main.py` script runs four stages in order:

1. **Base curve construction** (`curve_builder`): a periodic, closed spline
   curve is built from control points and converted into a topological wire.
   The curve is smooth and differentiable, which the frame computation needs.
2. **Sampling and parallel transport** (`parallel_transport`): the curve is
   sampled into positions and tangents, and an initial frame is transported
   along the curve by successive minimal rotations that keep each frame
   perpendicular to the tangent. No external reference frame is used, so no
   twist accumulates from the parametrization.
3. **Holonomy correction** (`parallel_transport`): on a closed curve,
   parallel-transported frames generally do not return to their starting
   orientation. The mismatch (holonomy) is measured at the closure point and
   distributed as a smooth correction along the curve, so the swept surface
   closes seamlessly.
4. **Sweep and plate export** (`plate_modelling`): cross-sections are placed
   on the corrected frames and swept, and the result is exported as
   stackable plates, one file per plate, into `output/`.

## Repository Structure

```
main.py                     pipeline entry point
src/
  curve_builder.py          curve construction from control points
  parallel_transport.py     sampling, frame transport, holonomy correction
  plate_modelling.py        sweep construction and plate export
output/                     generated geometry files
```

## Usage

```bash
python main.py
```

Control points for the base curve are defined in `main.py`. The pipeline
prints each stage and writes the exported geometry to `output/`.

## Notes

- Parallel transport frames are one way to construct a rotation-minimizing
  frame; the alternative Frenet frame is undefined at inflection points and
  flips where curvature direction reverses, which is why it is not used here.
- The holonomy correction is what makes the closed-curve case consistent.
  Without it, the swept profile would show a visible mismatch at the seam.
- The same pipeline works for open curves; the correction step simply becomes
  a no-op.

## Dependencies

- Python 3
- OpenCASCADE Technology Python bindings (pythonocc-core)
