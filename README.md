# Geometric Sweep and Physics-Based Modeling

A collection of computational geometry and physics modeling tools in Python, focused on parametric 3D curves and field-based simulations.

## Contents

- **Frame transport** — rotation-minimizing frames along closed 3D B-spline curves, with holonomy correction for consistent closure.
- **Swept solids** — cross-section sweeping along curves using OCCT/CadQuery, with manufacturability (plate stackability) checks.
- **Field computation** — Biot-Savart magnetic field evaluation from discretized current loops.
- **Particle tracing** — charged particle trajectory integration under Lorentz force using `scipy.integrate.solve_ivp`.
- **3D geometry primitives** — nearest point on segment/polyline/triangle, point-plane projection, segment-to-segment distance, line-plane intersection.

## Requirements

numpy

scipy

matplotlib

cadquery for CAD operations (Check cadquery installation manual)

## Usage

Each module is self-contained — see individual scripts for example usage and test cases.