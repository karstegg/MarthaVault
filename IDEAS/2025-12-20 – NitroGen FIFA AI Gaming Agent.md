---
'Status:': Draft
'Priority:': Medium
'Tags:': null
'Source:': https://nitrogen.minedojo.org/
permalink: ideas/2025-12-20-nitro-gen-fifa-ai-gaming-agent
---

# NitroGen - AI Gaming Agent (FIFA Project)

## The Idea

Train an AI to play FIFA on PS4 by learning from gameplay videos. NitroGen is a vision-action foundation model that watches gameplay and outputs controller inputs.

## Resources

- **Project Page:** https://nitrogen.minedojo.org/
- **Hugging Face:** Search for NitroGen/MineDojo models
- **GitHub:** Check project page for repo links
- **Paper:** Available on project page

## Model Specs

- 500M parameters (manageable size)
- Trained on 40,000 hours of gameplay across 1,000+ games
- Gamepad output: joysticks (0.84 R²) + buttons (0.96 accuracy)

## Google Colab Feasibility

**Free Tier (T4 GPU, 16GB VRAM):**
- Inference: Should work for 500M params
- Training: Very limited (session timeouts, disk space)
- Fine-tuning on FIFA: Possible with small dataset

**Colab Pro ($10/mo):**
- Better GPUs (A100, V100)
- Longer sessions
- More viable for fine-tuning

## Option A: PS4 Integration

1. **Capture card** - Record PS4 gameplay to PC (~R1,500-3,000)
2. **Titan Two or similar** - Send AI controller inputs to PS4 (~R2,000)
3. **PC with GPU** - Run inference in real-time

## Option B: PC Gaming (Recommended - Simpler!)

No capture card or controller adapter needed. Game and AI run on same PC.

### Software Stack
```
FIFA (PC via EA App/Steam)
    ↓ screen capture (mss/dxcam)
Python + PyTorch + NitroGen model
    ↓ action prediction
Virtual Controller (vgamepad)
    ↓ input injection
FIFA receives inputs
```

### PC Build Costs (ZAR - Dec 2025)

#### Budget Build (~R18,000-22,000)
| Component | Spec | Price |
|-----------|------|-------|
| GPU | RTX 3060 12GB | R7,000-8,500 |
| CPU | Ryzen 5 5600 / i5-12400F | R2,200-2,800 |
| Motherboard | B550 / B660 | R1,800-2,500 |
| RAM | 16GB DDR4 3200MHz | R1,000-1,200 |
| SSD | 500GB NVMe | R700-900 |
| PSU | 550W 80+ Bronze | R900-1,200 |
| Case | Basic Mid-tower | R600-800 |
| **Total** | | **R14,200-17,900** |
| + FIFA PC | EA App | R1,200 |
| + Monitor (if needed) | 1080p 75Hz | R2,000-3,000 |
| + KB/Mouse | Basic combo | R500-800 |
| **Grand Total** | | **~R18,000-22,000** |

#### Recommended Build (~R28,000-35,000)
| Component | Spec | Price |
|-----------|------|-------|
| GPU | RTX 4060 Ti 8GB / RTX 3070 | R9,000-12,000 |
| CPU | Ryzen 5 7600 / i5-13400F | R3,500-4,500 |
| Motherboard | B650 / B760 | R2,500-3,500 |
| RAM | 32GB DDR5 5200MHz | R2,500-3,000 |
| SSD | 1TB NVMe Gen4 | R1,200-1,500 |
| PSU | 650W 80+ Gold | R1,400-1,800 |
| Case | Quality Mid-tower | R1,200-1,800 |
| **Total** | | **R21,300-28,100** |
| + FIFA PC | EA App | R1,200 |
| + Monitor | 1080p 144Hz | R3,000-4,000 |
| + KB/Mouse | Decent combo | R1,000-1,500 |
| **Grand Total** | | **~R28,000-35,000** |

#### High-End Build (~R45,000-55,000)
| Component | Spec | Price |
|-----------|------|-------|
| GPU | RTX 4070 Super 12GB | R14,000-16,000 |
| CPU | Ryzen 7 7700X / i7-13700K | R6,000-7,500 |
| Motherboard | B650 / Z790 | R3,500-5,000 |
| RAM | 32GB DDR5 6000MHz | R3,000-4,000 |
| SSD | 2TB NVMe Gen4 | R2,200-2,800 |
| PSU | 750W 80+ Gold | R1,800-2,200 |
| Case | Premium | R2,000-3,000 |
| CPU Cooler | Tower/AIO | R1,000-2,000 |
| **Total** | | **R33,500-42,500** |
| + FIFA PC | EA App | R1,200 |
| + Monitor | 1440p 165Hz | R5,000-7,000 |
| + Peripherals | Quality | R2,000-3,000 |
| **Grand Total** | | **~R45,000-55,000** |

### Why PC is Better Than PS4 for This

- No capture card needed (direct screen grab)
- No Titan Two needed (virtual controller via Python)
- Lower latency (same machine)
- Easier debugging and iteration
- Can run training locally too

### Where to Buy (SA)

- Evetech.co.za
- Wootware.co.za
- Takealot.com
- Rebeltech.co.za

## Approach: Behavior Cloning (Option 1)

**Strategy:** Learn from videos → Play at fixed skill level

```
Pro FIFA videos (YouTube)
    ↓ extract frames + controller inputs
NitroGen training/fine-tuning
    ↓ trained model
Real-time inference on PC
    ↓ screen → action
FIFA plays itself!
```

**Why start here:**
- Simpler to implement
- NitroGen already supports this
- Can migrate to RL later for self-improvement

## Project Phases

### Phase 1: Test on Colab (Free - before buying PC)
- [ ] Find and download NitroGen model from Hugging Face
- [ ] Set up Colab notebook for inference test
- [ ] Run basic inference on sample game footage
- [ ] Confirm model works before spending money

### Phase 2: Build PC (~R20,000-24,000)
- [ ] Order budget build components
- [ ] Assemble PC, install Windows + drivers
- [ ] Install FIFA PC (EA App)
- [ ] Install Python, PyTorch, CUDA

### Phase 3: Get It Playing
- [ ] Set up screen capture (dxcam)
- [ ] Set up virtual controller (vgamepad)
- [ ] Connect NitroGen model to capture → action loop
- [ ] Test in FIFA - watch it play!

### Phase 4: Fine-tune on FIFA (Optional)
- [ ] Record your own FIFA gameplay sessions
- [ ] Extract frames + controller inputs
- [ ] Fine-tune NitroGen on FIFA-specific data
- [ ] Improve FIFA-specific skills

### Future: Migrate to Reinforcement Learning
- Add reward detection (goals, wins)
- Implement PPO/SAC learning loop
- Let it play and improve overnight
- Watch it surpass your skill level!

## Quick Start Checklist

1. [ ] Test NitroGen on Colab first (free!)
2. [ ] If it works → Order PC parts
3. [ ] If PC works → Get FIFA playing
4. [ ] If playing works → Consider RL upgrade

## Dream Use Case

Train on pro player videos, let it grind Ultimate Team while you sleep!

## Notes

Discovered via ClaudeBox triage 2025-12-20.