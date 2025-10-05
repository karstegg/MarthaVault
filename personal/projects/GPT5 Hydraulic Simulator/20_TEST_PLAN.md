---
Status:: Draft
Priority:: Med
Assignee:: Greg
DueDate:: 
Tags:: #year/2025 #personal
---

# Acceptance Tests (high level)
- Finite signals: pP, pA, pB, x, v remain finite over 1000 steps.
- Pump OFF ⇒ supply tends to 2 bar backpressure (±0.5 bar).
- Valve CLOSED ⇒ indicative flow ≤ 5% of full-open after settling.
- Relief holds setpoint under deadhead (±2 bar).
- Spool step −1→+1: cylinder extension becomes monotonic after a short transient.

Each test declares units and numerical tolerance explicitly.
