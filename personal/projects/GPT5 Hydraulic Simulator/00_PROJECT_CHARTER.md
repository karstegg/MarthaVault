---
Status:: Draft
Priority:: Med
Assignee:: Greg
DueDate:: 
Tags:: #year/2025 #personal
---

# Project Charter — Hydraulic Simulator
Goal: browser-based, physically accurate *lumped-parameter* hydraulic circuit simulator with interactive controls and tests.

Scope
- SI units only.
- Fluids: density ρ, dynamic viscosity μ(T), bulk modulus β(T).
- Lines: R (viscous), L (inertance), C (compliance via β).
- Valves (variable orifice): q = Cd·A(ξ)·sgn(Δp)·√(2|Δp|/ρ).
- Cylinder: two-chamber continuity + mechanics; friction = Coulomb + viscous (Stribeck optional later).
- Pump: displacement source with efficiencies + relief; reservoir.
- Solver: Backward Euler for pressure states; semi-implicit for mechanics; deterministic step(dt).
- Initial circuit: reservoir → pump → 4/2 valve → cylinder. Return backpressure = **2 bar**.
- Interactivity: pump ON/OFF, flow-control opening 0–100%, spool ±1.

Deliverables
- PR-style diffs, numerical derivations first, code second, **unit tests** with tolerances, and ledger updates.
- No invented constants—ask when data are missing.

Non-goals (phase 1)
- CFD, full thermal coupling, cavitation modeling beyond a simple p ≥ p_vapor clamp.
