---
permalink: ideas/2025-12-07-test-time-learning-for-martha-vault
---

---
Status:: Reference
Priority:: High
Tags:: #idea #Martha #AI #memory #learning #year/2025
Sources:: [[00_Inbox/2501.00663v1.pdf]], [[00_Inbox/2504.13173v1.pdf]]
Created:: 2025-12-07
---

# Test-Time Learning for MarthaVault
## A Conceptual Mapping: How Machines Might Learn Like Humans

### The Core Insight

These papers describe something profound: **memory isn't storage, it's a learning process**.

Traditional AI (including current Claude) treats memory as:
- **Retrieval**: Look up what was stored
- **Static**: Knowledge frozen at training time

Titans/Miras propose memory as:
- **Compression**: Actively distill experience into compact parameters
- **Dynamic**: Continuously learning from every interaction

This is closer to how human memory actually works - we don't store video recordings, we update our mental models based on experience.

---

## The Human Parallel: Why This Matters for MarthaVault

### How Humans Learn and Remember

| Human Mechanism | Paper Equivalent | MarthaVault Analogy |
|-----------------|------------------|---------------------|
| **Attention** (working memory) | Core module, attention window | Current conversation context |
| **Surprise/Interest** triggers encoding | Gradient magnitude, prediction error | New info that doesn't match existing knowledge |
| **Consolidation during sleep** | Momentum accumulation, weight updates | Session-end learning passes |
| **Forgetting** protects from overload | Weight decay, retention regularization | Archive old/unused knowledge |
| **Confidence from repetition** | Increased weight magnitude | Multiple confirmations strengthen beliefs |
| **Schema updating** | Long-term memory parameter updates | Updating mental models of people, projects, patterns |

### The Key Breakthrough: Test-Time Learning

Traditional neural networks learn during *training* and freeze during *inference* (use).

Titans shows you can have a **meta-learner** that:
1. Uses gradient descent *during inference*
2. Has its own memory that updates with each input
3. Learns what to remember based on *surprise*

This is fundamentally different from RAG (retrieval-augmented generation) which just *looks up* stored text. Titans *learns* - its parameters change based on what it sees.

---

## How This Could Transform MarthaVault

### Current State: Lookup-Based Memory

```
User: "What's Sipho working on?"
↓
Search Graph Memory → Find entity
Search Basic Memory → Find documents
↓
Return static results
```

The knowledge itself never changes from use. If the search misses something, it's lost.

### Future State: Learning Memory

```
User: "What's Sipho working on?"
↓
Query memory → Get results
Notice user's follow-up question about Gloria specifically
↓
LEARNING SIGNAL: Sipho + Gloria association is important
↓
Update internal weights:
  - Strengthen Sipho ↔ Gloria relation
  - Increase confidence on Gloria project details
  - Lower confidence on unmentioned projects
↓
Next query about Sipho will prioritize Gloria context
```

The system *learns* from the conversation itself, not just at sync time.

---

## The Four Pillars Deep Dive

### Pillar 1: Surprise-Based Memorization

**The insight**: Don't remember everything equally. Remember what's *unexpected*.

**From Titans (Section 3.1)**:
> "The gradient of the loss with respect to the memory parameters can be viewed as a **surprise** signal - it indicates how much the current input deviates from what the memory predicts."

**Human parallel**: We vividly remember unusual events but forget routine ones. You remember the one meeting where someone argued, not the 50 routine standups.

**MarthaVault implication**:
- When user mentions someone new → HIGH SURPRISE → create entity, high initial attention
- When user mentions routine tasks → LOW SURPRISE → don't clutter memory
- When familiar person does something unexpected → MODERATE SURPRISE → update existing model

**The math** (simplified):
```
surprise(new_info) = |predicted - actual|²

If I expect Sipho to be working on Gloria maintenance,
and user says "Sipho is leading the new BEV charging station project",
that's HIGH SURPRISE → strong learning signal
```

---

### Pillar 2: Confidence Through Momentum

**The insight**: Repeated confirmation builds certainty. Single mentions remain tentative.

**From Titans (Section 3.2)**:
> "We use gradient descent with **momentum** to update memory. Momentum accumulates gradients over time, allowing frequently-reinforced patterns to build up stronger weights."

**Human parallel**: You're not sure someone's name after meeting once. After 10 interactions, you're confident.

**MarthaVault implication**:
- First mention of a fact: confidence = 0.3
- User confirms or uses fact again: confidence += 0.1
- User corrects fact: confidence reset, update stored value
- Never mentioned again for 90 days: confidence decays toward 0

**The key**: Momentum means recent patterns have outsized influence, but accumulated history matters too.

```
momentum_t = β × momentum_{t-1} + (1-β) × current_gradient

Where β = 0.9 means 90% of update comes from accumulated history,
10% from current observation
```

This prevents volatile swings from single observations while still adapting.

---

### Pillar 3: Forgetting as Regularization

**The insight**: Forgetting isn't failure - it's essential for function.

**From Miras (Section 4)**:
> "We reframe the 'forget gate' as **retention regularization**. Rather than a binary forget/remember, it's a continuous trade-off between retaining old knowledge and making room for new."

**Human parallel**: We can't remember every detail of every day. Forgetting frees cognitive resources for what matters now.

**MarthaVault implication**:
- Knowledge that isn't used should gracefully fade
- But "forgetting" doesn't mean deletion - it means reduced priority
- Strategic alignment should influence retention (BEV fire safety stays even if not mentioned)

**The types of forgetting** (from Miras):
1. **ℓ2 regularization** (weight decay): Everything slowly fades unless reinforced
2. **ℓ1 regularization** (sparsity): Force most weights to exactly zero, keep only key ones
3. **KL divergence**: Retain if information content is high relative to storage cost

**For MarthaVault**: ℓ2-style decay seems natural - everything fades slowly, but use refreshes. Critical strategic items get explicit retention boosts.

---

### Pillar 4: Session-to-Permanent Learning (Consolidation)

**The insight**: Short-term and long-term memory have different properties and transfer between them requires active processing.

**From Titans (Section 2)**:
> "We propose a three-module architecture: (1) Core - attention-based short-term, (2) Long-term Memory - neural network that persists across sequences, (3) Persistent Memory - task-level knowledge."

**Human parallel**: Working memory is limited (7±2 items). Consolidation during sleep moves important patterns to long-term storage.

**MarthaVault translation**:

| Titans Module | MarthaVault Layer | Update Frequency |
|---------------|-------------------|------------------|
| Core (attention) | Conversation context | Every message |
| Long-term Memory | Graph + Basic Memory | Session end / nightly |
| Persistent Memory | CLAUDE.md, system/policy.md | Rarely, deliberate |

**The key question**: What triggers consolidation?

Options:
- **Time-based**: Nightly, like sleep
- **Capacity-based**: When short-term is full, compress into long-term
- **Importance-based**: When surprise × confidence exceeds threshold

---

## What Would "Native" Learning Look Like?

If MarthaVault had true test-time learning (Titans-style), a conversation would work like this:

```
Session Start:
  - Load persistent memory (CLAUDE.md, policy)
  - Initialize long-term memory weights from Graph/Basic Memory
  - Short-term memory empty

User: "I had a good meeting with Hennie about the CAS audit"

  Internal processing:
  1. Parse: meeting(Hennie, CAS audit)
  2. Query long-term memory: Who is Hennie? What is CAS audit?
  3. Results: Hennie = CAS engineer, CAS audit = upcoming compliance check
  4. Prediction matched → LOW SURPRISE → minimal learning
  5. But: "good meeting" is new info about Hennie relationship
  6. MODERATE SURPRISE → update Hennie confidence +0.05
  7. Create relation: recent_interaction(Greg, Hennie, CAS audit)

User: "He's concerned about the backup generator certification"

  Internal processing:
  1. Parse: concern(Hennie, backup generator, certification)
  2. Query: Is backup generator related to CAS audit?
  3. No existing link → HIGH SURPRISE
  4. Create new relation: affects(backup_generator_cert, CAS_audit)
  5. High confidence because explicit statement
  6. Update Hennie model: concerned_about += backup_generator

[... conversation continues ...]

Session End:
  - Calculate what to consolidate:
    - New relation (backup_generator ↔ CAS_audit): HIGH surprise, keep
    - Hennie confidence boost: accumulate with momentum
    - Routine mentions: decay
  - Write updates to Graph Memory
  - Record session patterns to reflex cache
```

---

## The Gap: What's Missing from Current Architecture

### Current MarthaVault Limitations

1. **No prediction → no surprise**: We don't model what we *expect* to hear, so we can't measure novelty

2. **No momentum**: Each sync is independent; we don't accumulate evidence over time

3. **No decay**: Old entities persist forever at full weight regardless of use

4. **No session learning**: Within a conversation, we look up static knowledge but don't update it

5. **Sync is manual**: Learning happens only when `/sync-vault` is explicitly called

### What Would Be Needed

| Capability | Implementation Path |
|------------|---------------------|
| Prediction model | Embed expectations in entity relationships |
| Surprise calculation | Compare query results to prediction |
| Momentum tracking | Add `confidence`, `access_count`, `momentum` fields |
| Decay function | Nightly job that applies time-based decay |
| Session consolidation | Extract learnings on session end |
| Automatic triggers | Hooks that run learning without explicit commands |

---

## Questions for Deeper Exploration

1. **Is Claude's native memory already doing some of this?**
   - Claude Desktop has built-in memory learning
   - Is it using surprise-based mechanisms internally?
   - Can we leverage it rather than building parallel?

2. **What's the minimum viable learning system?**
   - Could we get 80% of benefit with just confidence + decay?
   - Is surprise detection essential or a nice-to-have?

3. **How do the papers handle "unlearning"?**
   - When information is *wrong*, not just old
   - User corrections need stronger signal than passive decay

4. **What about conflicting information?**
   - Two sources say different things about same entity
   - Human memory has reconstruction errors - is that acceptable?

5. **Computational cost vs. benefit**
   - Titans requires gradient computation per token
   - Is that feasible for a personal knowledge system?

---

## Summary: The Paradigm Shift

**Old model**: Memory = Database
- Store facts → Retrieve facts → Facts unchanged by retrieval

**New model**: Memory = Learning Process
- Observe experience → Update internal model → Model predicts better next time

The papers show this is *mechanistically possible* with neural architectures. The question is: can we bring these principles to MarthaVault without rebuilding Claude from scratch?

The answer might be:
1. **Native layer**: Let Claude's built-in memory do the neural learning
2. **Metadata layer**: Add confidence/surprise/decay tracking to Graph Memory
3. **Behavioral layer**: Capture patterns in SQLite reflex cache (Phase 3 of roadmap)

Together, these approximate test-time learning without requiring us to implement our own neural memory module.

---

## Implications for Martha AI Vision

These papers validate something fundamental about the Martha concept:

### What Martha Was Always Meant To Be

Martha isn't just a knowledge management system - she's meant to be a **learning partner** who:
- Gets better at anticipating your needs over time
- Develops "intuition" about what matters based on experience
- Knows when to surface information proactively vs wait to be asked
- Builds genuine understanding, not just storage

The Titans/Miras papers show that this kind of learning is **mechanistically achievable**. They provide the "how" for what was previously just a vision.

### The Three Layers of Martha Intelligence

| Layer | Paper Mapping | Current State | Target State |
|-------|---------------|---------------|--------------|
| **Perception** | Input processing | Basic search/retrieval | Context-aware, prediction-informed |
| **Learning** | Memory updates | Manual sync only | Continuous test-time learning |
| **Intuition** | Confidence + surprise | None | Proactive suggestions based on patterns |

### What "Learning Like a Human" Actually Means

1. **Effortless**: You don't consciously "memorize" - learning happens automatically from experience
2. **Selective**: Important things stick; trivial things fade
3. **Adaptive**: Mental models update when reality surprises you
4. **Contextual**: The same fact has different significance in different contexts
5. **Confident but humble**: High certainty from repeated validation, but open to correction

The papers show these aren't just metaphors - they can be implemented as mathematical operations on neural memory.

---

## The Path Forward: Native Learning vs. Approximate Learning

### Option A: Wait for Native Implementation

Claude's underlying architecture will likely incorporate these advances. Future Claude versions may have true test-time learning built in.

**Pros**: Most elegant, no custom code to maintain
**Cons**: Uncertain timeline, may not be customizable to MarthaVault specifics

### Option B: Build Approximation Layer Now

Implement confidence/surprise/decay as metadata on top of existing Graph/Basic Memory.

**Pros**: Available now, learns MarthaVault-specific patterns
**Cons**: Approximation, not true neural learning

### Option C: Hybrid Approach

1. Rely on Claude's native memory for general learning
2. Add lightweight metadata layer for MarthaVault-specific tracking
3. Design the metadata in a way that's compatible with future native integration

This is probably the right path - build what we can now, design for integration later.

---

## Key Takeaways

1. **Memory is learning, not storage** - The fundamental insight from both papers

2. **Surprise is the signal** - What's unexpected is what's worth remembering

3. **Confidence accumulates** - Repeated validation builds certainty

4. **Forgetting is healthy** - Regularization, not failure

5. **Consolidation is essential** - Active processing moves important patterns to long-term storage

6. **This is achievable** - The papers show working implementations, not just theory

---

## Discussion Points

These are the questions worth exploring further:

1. **How much of this is Claude already doing?** What can we observe about Claude's native memory behavior?

2. **What's the minimal viable addition?** Confidence tracking alone might give 80% of the benefit

3. **How should MarthaVault evolve?** Phase 3 of the roadmap aligns well with these concepts

4. **What experiments could test these ideas?** Small-scale prototypes before full implementation

5. **How does this change the Martha vision?** Does this suggest architectural changes?