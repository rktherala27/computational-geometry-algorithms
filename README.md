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

## Planned / Future Work

Possible future additions include:

- Graph-based topology extraction (e.g., BFS/DFS on meshes or surface samples).
- Curve and surface reconstruction algorithms from point clouds or discrete samples.
- Geometry processing utilities for simulation pipelines.

## Dependencies

- Python 3
- OpenCASCADE Technology Python bindings (pythonocc-core)
