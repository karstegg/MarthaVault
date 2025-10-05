---
Status:: Draft
Priority:: Med
Assignee:: Greg
DueDate:: 
Tags:: #year/2025 #personal
---

# Phase 2 — Spec + Sound/Seq parity

## A) 303/RB-338 behavior (engine)

**Goals**

- True **legato slide**: if `Slide=ON` and the next step is gated, envelopes don’t retrigger; pitch glides with the classic curve.
    
- **Accent** coupling: boosts VCF env depth + VCA level, and slightly shortens amp decay (303 vibe).
    
- More accurate **waveforms**: 303 saw is slightly band-limited; square not exactly 50% at all freqs.
    
- Filter feel: keep 18dB TPT but tune **resonance/drive** to match RB-338 (clip stage pre/post).
    
- Envelope shapes: tweak **VCF/AMP decay law** (expo-ish, different constants).
    

**Code changes (worklet)**

- Add params: `accentDecayTrim`, `accentDriveTrim`, `slideShape` (0..1).
    
- Gate handling: on slide steps keep `gate=1`, don’t reset envs; interpolate `freqNow` with time-constant derived from **Slide** and a slight **velocity on second step** (RB-338 quirk).
    
- Pre-filter soft clip, post-filter tanh gain-comp.
    
- Square duty micro-offset vs frequency.
    

**Self-tests to add**

- “Slide keeps gate high”: trigger two steps with Slide=ON, assert we never send `gate:0` between them (logic-level test).
    
- “Accent raises energy”: RMS with Accent ON is > RMS with Accent OFF at same cutoff/amp (± tolerance).
    
- “Gate retrigger when Slide=OFF”: ensure a note-off is scheduled between steps.
    

## B) Sequencer completeness

**Goals**

- Step **REST** toggle, **TIE** (alt to Slide when you want legato without glide).
    
- **Per-step transpose** range ±12 we already have, keep it.
    
- **Pattern ops**: copy/paste/clear, randomize (musical), 4 banks × 8 patterns, **chain**.
    
- **Tap write** + **shift** left/right.
    

**Code/UI**

- Add a REST column (checkbox), TIE column (mutually exclusive with Slide).
    
- Pattern store in memory; add export/import **JSON**.
    

**Self-tests**

- “No sound on REST”: gate low over REST steps.
    
- “TIE joins gates”: gate stays high; no pitch glide unless Slide also ON.
    

## C) Timing & sync

**Goals**

- Solid internal clock (AudioContext time) with our swing implementation.
    
- Optional **WebMIDI clock** in/out; start/stop; ppqn 24.
    
- Optional Ableton Link later.
    

**Self-tests**

- Jitter check: schedule 64 steps, compute timing deltas in JS (target jitter < a few ms).
    
- Clock follow: basic simulation (if MIDI not available) behind a flag.
    

## D) UI/UX fidelity (RB-338 look)

**Goals**

- Panel skin with the **RB-338** 303 module layout (knobs order/labels: TUNE, CUTOFF, RESO, ENV MOD, DECAY, ACCENT).
    
- Step editor mirroring their 16-LED grid and mode buttons (Pitch, Step, Back, Clear, etc.).
    
- Keyboard/shortcut parity.
    

**Tasks**

- Move to a skinnable CSS layer; SVG assets for knob caps; LED palette.
    
- Accessibility: focus rings, keyboard nav.
    

**Self-tests**

- DOM presence of required controls in expected order (no dupes).
    
- Visual “smoke” test: computed styles for LED/knob classes exist.
    

## E) Persistence & sharing

**Goals**

- Pattern save to **localStorage** (banks).
    
- Export/import **.rb338.json** (includes tempo, swing, pattern bank).
    

**Self-tests**

- Round-trip: export → import reproduces the same pattern arrays.
    

## F) Interop (optional but nice)

- **MIDI input** for notes/accents (key-on with velocity>100 → accent).
    
- **Audio Recorder**: render 2 bars to WAV (OfflineAudioContext).
    

---

## What I need from you (to lock the spec)

1. **Legato rule**: match real 303—non-slide steps retrigger; slide steps keep gate high and don’t retrigger. Is that what you want?
    
2. **Accent behavior**: should accent also **shorten amp decay** (classic) or only boost loudness/brightness?
    
3. **Filter drive**: do we chase **RB-338** exact feel, or “OG 303-ish” even if it differs slightly?
    
4. **UI fidelity**: do you want the RB-338 **exact panel** next (same knob order/labels), or keep the current neutral skin until features are done?
    
5. **Sync**: is **WebMIDI clock in/out** a must for Phase 2, or can it wait?
    

If you’re happy with that scope, I’ll start with **A) engine behavior** + the **slide/accent tests**, then **B) sequencer REST/TIE & banks**, and finally **D) RB-338 skin**.