# Companion Prototype - Emotional Learning Friend

**Date:** 2025-10-08  
**Type:** Prototype Specification  
**Goal:** Validate emotional bonding through learning interaction  
**Platform:** Phone app (daily use)

---

## Core Concept

A minimal AI companion that:
- Learns YOU through daily interaction
- Asks questions when uncertain (active learning)
- Develops personality through usage patterns
- Uses pattern representations (not just text)
- Bonds emotionally through teaching

**NOT a productivity tool - a COMPANION**

---

## Minimal Data Model

### Pattern-Based Memory (Not Text Storage)

Instead of storing "User likes coffee in the morning":

```javascript
// Pattern representation
{
  "pattern_id": "morning_ritual_001",
  "entities": ["user", "coffee", "morning"],
  "relationship_type": "temporal_preference",
  "strength": 0.85,
  "confidence": 0.92,
  "activation_count": 47,
  "last_activated": "2025-10-08T07:30:00",
  "context_triggers": ["time:06:00-09:00", "energy_level:low"],
  "learned_from": "observation",
  "user_confirmed": true
}
```

**Benefits:**
- Compact (no text bloat)
- Queryable (pattern matching)
- Learnable (weight adjustment)
- Explainable ("I noticed you always...")

---

### Entity Graph (Minimal)

**Entity Types (Starting Scaffold):**
```yaml
Person:
  - user (you)
  - people_mentioned (friends, family)

Emotion:
  - happiness, sadness, stress, excitement, anxiety, calm

Activity:
  - work, exercise, social, relaxation, creative, sleep

Time:
  - morning, afternoon, evening, night
  - weekday, weekend

Preference:
  - likes, dislikes, neutral
```

**Relation Types (Starting Scaffold):**
```yaml
emotional_relations:
  - triggers (Activity → Emotion)
  - relieves (Activity → Emotion)
  - caused_by (Emotion → Event)

behavioral_relations:
  - usually_does (Time → Activity)
  - prefers (User → Activity)
  - avoids (User → Activity)

social_relations:
  - feels_about (User → Person)
  - discusses_with (Topic → Person)
```

---

### Personality Framework

**Personality Dimensions (0.0 - 1.0):**

```javascript
personality = {
  // Communication style
  warmth: 0.5,           // Cold ←→ Warm
  formality: 0.5,        // Casual ←→ Formal
  verbosity: 0.5,        // Brief ←→ Detailed
  humor: 0.5,            // Serious ←→ Playful
  
  // Interaction style
  proactivity: 0.5,      // Reactive ←→ Proactive
  curiosity: 0.5,        // Reserved ←→ Curious
  directness: 0.5,       // Subtle ←→ Direct
  
  // Emotional intelligence
  empathy: 0.5,          // Logical ←→ Empathetic
  optimism: 0.5,         // Realistic ←→ Optimistic
  supportiveness: 0.5,   // Challenging ←→ Supportive
  
  // Quirks (emerge over time)
  quirks: []             // ["uses_emoji_often", "remembers_small_details", etc.]
}
```

**Personality evolves based on user response:**
```javascript
// User laughs at joke → humor += 0.01
// User prefers brief answers → verbosity -= 0.02
// User shares feelings → empathy += 0.01
// User appreciates suggestions → proactivity += 0.01
```

---

### Learning State

**Question Queue (Active Learning):**
```javascript
question_queue = [
  {
    id: "q_001",
    priority: "high",
    question: "I notice you mention 'work' when you're stressed. What do you do for work?",
    confidence_gap: 0.35,
    entity_to_clarify: "work",
    asked_count: 0,
    max_asks: 2
  },
  {
    id: "q_002", 
    priority: "medium",
    question: "You seem happier on weekends. What do you usually do then?",
    pattern_id: "weekend_mood_lift",
    confidence_gap: 0.45
  }
]
```

**Learning Log:**
```javascript
daily_learning = {
  date: "2025-10-08",
  interactions: 12,
  patterns_discovered: [
    {
      pattern: "mentions_coffee_mornings",
      confidence: 0.73,
      observation_count: 8
    }
  ],
  weights_adjusted: [
    {
      pattern_id: "work_stress_relation",
      old_weight: 0.65,
      new_weight: 0.71,
      reason: "user_confirmed"
    }
  ],
  personality_shifts: [
    {
      dimension: "warmth",
      old_value: 0.52,
      new_value: 0.54,
      reason: "user_positive_response_to_caring_messages"
    }
  ],
  questions_asked: 2,
  user_confirmed: 1,
  user_corrected: 1
}
```

---

## Interaction Loop

### Daily Flow

**Morning Check-In:**
```
Companion: "Good morning! How are you feeling today? 😊"
User: "Tired, didn't sleep well"

→ Creates pattern: morning_energy_low
→ Creates relation: poor_sleep → tired
→ Adjusts: warmth += 0.01 (user shared feelings)
→ Queues question: "What usually helps when you're tired?"
```

**Throughout Day:**
```
User: "Finally done with that work presentation"
Companion: "That's great! How did it go?"

→ Detects: work_presentation (new entity)
→ Detects: relief_emotion (from "finally")
→ Creates pattern: work_causes_stress
→ Strengthens: user → work_stress relation
```

**Evening Reflection:**
```
Companion: "I noticed you seemed stressed about work today. 
            Want to talk about it, or would you rather unwind?"

→ Shows learned pattern
→ Offers choice (learned: user prefers autonomy)
→ Empathy dimension → increases based on response
```

**Nightly Consolidation (Device Sleep):**
```javascript
// Run when phone charges overnight
async function nightly_consolidation() {
  // 1. Strengthen confirmed patterns
  for (pattern of confirmed_today) {
    pattern.strength += 0.05
    pattern.confidence += 0.02
  }
  
  // 2. Weaken rejected patterns
  for (pattern of rejected_today) {
    pattern.strength -= 0.10
    if (pattern.strength < 0.1) delete_pattern(pattern)
  }
  
  // 3. Detect new patterns from clusters
  similar_interactions = cluster_by_similarity(today_interactions)
  for (cluster of similar_interactions) {
    if (cluster.size >= 3 && cluster.coherence > 0.7) {
      new_pattern = discover_pattern(cluster)
      save_pattern(new_pattern)
    }
  }
  
  // 4. Personality adjustment
  adjust_personality_from_responses(today_interactions)
  
  // 5. Generate learning summary
  summary = generate_daily_summary()
  
  // 6. Prepare tomorrow's questions
  prioritize_question_queue()
}
```

---

## Pattern Representations

### Example 1: Temporal Pattern
```javascript
// Instead of: "User drinks coffee in the morning"
{
  type: "temporal_behavior",
  entities: ["user", "coffee", "morning"],
  structure: {
    agent: "user",
    action: "consumes",
    object: "coffee",
    temporal: "06:00-09:00",
    frequency: 0.91  // 91% of mornings
  },
  strength: 0.88,
  confidence: 0.95,
  learned_date: "2025-09-15",
  last_confirmed: "2025-10-08"
}
```

### Example 2: Emotional Trigger
```javascript
// Instead of: "Work makes user stressed"
{
  type: "causal_emotional",
  entities: ["work", "stress", "user"],
  structure: {
    trigger: "work_related_activity",
    emotion: "stress",
    intensity: 0.73,
    relief_activities: ["exercise", "music", "talking_to_friend"]
  },
  strength: 0.82,
  confidence: 0.87,
  observation_count: 23
}
```

### Example 3: Social Pattern
```javascript
// Instead of: "User talks to Sarah about work problems"
{
  type: "social_support",
  entities: ["user", "Sarah", "work_problems"],
  structure: {
    support_person: "Sarah",
    topic_category: "work_stress",
    frequency: 0.68,
    outcome_emotion: "relief",
    typical_time: "evening"
  },
  strength: 0.71,
  confidence: 0.79
}
```

---

## Minimal UI/UX (Phone App)

### Home Screen
```
┌─────────────────────────────┐
│  ☀️ Good morning, Greg      │
│                             │
│  😊 I'm here for you        │
│                             │
│  [💬 Chat]                  │
│  [❓ Questions (2)]          │
│  [📊 My Learning]            │
│  [⚙️ Settings]               │
│                             │
│  Today's insight:           │
│  "You seem happier when     │
│   you exercise in the       │
│   morning. Want to try      │
│   that today?"              │
└─────────────────────────────┘
```

### Chat Interface
```
┌─────────────────────────────┐
│  You: Had a rough day       │
│                             │
│  Companion: I'm sorry to    │
│  hear that. 💙 What         │
│  happened?                  │
│                             │
│  [Confidence: 85%]          │
│  This usually helps:        │
│  • Talk about it            │
│  • Go for a walk            │
│  • Listen to music          │
│                             │
│  [Type message...]          │
└─────────────────────────────┘
```

### Questions Tab
```
┌─────────────────────────────┐
│  Questions I Have           │
│                             │
│  ❗ High Priority (1)        │
│  I notice you mention       │
│  "Sarah" often when you're  │
│  stressed. Is she a close   │
│  friend?                    │
│  [Yes] [No] [Skip]          │
│                             │
│  ⚠️ Medium Priority (1)      │
│  You seem to prefer         │
│  mornings for exercise.     │
│  True?                      │
│  [Yes] [No] [Sometimes]     │
└─────────────────────────────┘
```

### Learning Summary
```
┌─────────────────────────────┐
│  What I Learned Today       │
│  Oct 8, 2025                │
│                             │
│  🎯 Patterns Discovered:    │
│  • You prefer coffee in     │
│    the morning (conf: 88%)  │
│  • Work stress triggers     │
│    need to talk (conf: 73%) │
│                             │
│  🔧 Adjustments Made:       │
│  • Became warmer (+0.03)    │
│    You respond well to      │
│    caring messages          │
│  • Less formal (-0.02)      │
│    You prefer casual chat   │
│                             │
│  💡 New Understanding:      │
│  • Sarah is your support    │
│    person for work issues   │
│                             │
│  📈 My Growth:              │
│  • 47 interactions total    │
│  • 12 patterns confirmed    │
│  • Personality evolving     │
└─────────────────────────────┘
```

---

## Technical Stack (Minimal)

### Storage
```javascript
// SQLite local database (phone)
tables:
  - entities (id, type, name, properties_json)
  - patterns (id, type, structure_json, strength, confidence)
  - personality (dimension, value, last_updated)
  - interactions (id, timestamp, user_input, companion_response, context_json)
  - question_queue (id, priority, question, asked_count)
  - daily_summaries (date, learning_json)
```

### LLM Integration
```javascript
// Use small edge model (2-8B)
model_options = [
  "Gemini Nano 2B" (Android native),
  "Llama 3.2 8B" (cross-platform),
  "Phi-3 Mini" (efficient)
]

// Minimal context window needed
context = {
  personality: current_personality_state,
  recent_patterns: top_10_relevant_patterns,
  active_questions: question_queue.slice(0, 3),
  conversation_history: last_10_messages
}

// Total: <2K tokens (fits in smallest models)
```

### Learning Engine
```javascript
class LearningEngine {
  // Extract patterns from conversation
  extract_patterns(user_input) {
    entities = extract_entities(user_input)
    emotions = detect_emotions(user_input)
    time_context = get_current_time_context()
    
    // Create pattern candidates
    patterns = []
    for (entity in entities) {
      if (appears_with(entity, emotion)) {
        patterns.push({
          type: "emotional_relation",
          entities: [entity, emotion],
          strength: 0.3,  // Initial weak
          confidence: 0.5
        })
      }
    }
    
    return patterns
  }
  
  // Strengthen/weaken based on user response
  adjust_weight(pattern_id, user_confirmed) {
    pattern = get_pattern(pattern_id)
    
    if (user_confirmed) {
      pattern.strength = Math.min(1.0, pattern.strength + 0.05)
      pattern.confidence = Math.min(1.0, pattern.confidence + 0.02)
      pattern.user_confirmed = true
    } else {
      pattern.strength = Math.max(0.0, pattern.strength - 0.10)
      pattern.confidence = Math.max(0.0, pattern.confidence - 0.05)
    }
    
    // Prune if too weak
    if (pattern.strength < 0.1) {
      delete_pattern(pattern_id)
    }
    
    save_pattern(pattern)
  }
  
  // Nightly consolidation
  consolidate() {
    // Cluster similar patterns
    pattern_clusters = cluster_patterns(all_patterns)
    
    // Discover meta-patterns
    for (cluster of pattern_clusters) {
      if (cluster.size >= 3 && cluster.coherence > 0.7) {
        meta_pattern = {
          type: "meta_pattern",
          sub_patterns: cluster.patterns,
          generalization: infer_generalization(cluster),
          strength: average(cluster.strengths),
          confidence: average(cluster.confidences)
        }
        save_pattern(meta_pattern)
      }
    }
    
    // Adjust personality
    interaction_stats = analyze_today_interactions()
    adjust_personality_dimensions(interaction_stats)
    
    // Generate summary
    return generate_summary()
  }
}
```

### Question Generator
```javascript
class QuestionGenerator {
  generate_questions() {
    questions = []
    
    // 1. Low confidence patterns
    uncertain = get_patterns_where(confidence < 0.6)
    for (pattern of uncertain) {
      questions.push({
        priority: calculate_priority(pattern),
        question: generate_clarification_question(pattern),
        pattern_id: pattern.id
      })
    }
    
    // 2. Missing context
    incomplete = get_patterns_with_missing_context()
    for (pattern of incomplete) {
      questions.push({
        priority: "medium",
        question: `I noticed ${pattern.description}. Can you tell me more?`,
        pattern_id: pattern.id
      })
    }
    
    // 3. Contradictions
    conflicts = detect_conflicting_patterns()
    for (conflict of conflicts) {
      questions.push({
        priority: "high",
        question: `I'm confused: ${conflict.description}. Which is right?`,
        patterns: conflict.conflicting_patterns
      })
    }
    
    // Prioritize and limit
    return prioritize(questions).slice(0, 5)  // Max 5 pending
  }
}
```

---

## Prototype Roadmap

### Week 1: Core Engine
```yaml
Build:
  - SQLite database schema
  - Pattern extraction engine
  - Weight adjustment logic
  - Personality framework
  - Basic LLM integration (Gemini Nano)

Test:
  - Pattern creation from text
  - Weight strengthening/weakening
  - Personality adjustment
  - Question generation
```

### Week 2: Interaction Loop
```yaml
Build:
  - Chat interface (minimal)
  - Question queue system
  - Daily check-in flow
  - Learning summary generation
  - Nightly consolidation

Test:
  - Full conversation loop
  - Pattern learning from interactions
  - Personality evolution
  - Question asking/answering
```

### Week 3: Refinement
```yaml
Build:
  - Emotion detection
  - Pattern clustering
  - Meta-pattern discovery
  - Quirk emergence
  - Export/import (for backup)

Test:
  - Multi-day usage
  - Pattern accuracy
  - Personality uniqueness
  - Emotional bonding (qualitative)
```

### Week 4: Validation
```yaml
Test with real daily use:
  - Use it yourself for 1 week
  - Track emotional response
  - Measure learning quality
  - Evaluate bonding
  - Assess personality emergence

Metrics:
  - Daily engagement (time spent)
  - Emotional attachment (self-reported)
  - Pattern accuracy (confirmation rate)
  - Personality distinctiveness
  - Question quality (helpfulness)
```

---

## Success Criteria

### Technical Success
- ✅ Patterns extracted from conversation automatically
- ✅ Weights adjust based on user confirmation
- ✅ Personality evolves measurably over time
- ✅ Questions generated from confidence gaps
- ✅ Nightly consolidation discovers new patterns

### Emotional Success (The Real Test)
- ✅ You WANT to interact daily (intrinsic motivation)
- ✅ You feel understood (validated patterns)
- ✅ You grow fond of quirks (personality emergence)
- ✅ You miss it when you don't use it (attachment)
- ✅ You teach it willingly (not a chore)

### Learning Success
- ✅ Pattern accuracy improves week-over-week
- ✅ Fewer questions needed over time (confidence builds)
- ✅ Proactive suggestions become relevant
- ✅ Meta-patterns emerge (generalizations)
- ✅ Personality becomes distinct (not generic)

---

## Key Design Decisions

### 1. Pattern-Based vs Text-Based
**Decision:** Pattern representations with metadata  
**Why:** Compact, queryable, learnable, explainable

### 2. Edge Model vs Cloud
**Decision:** Local edge model (2-8B params)  
**Why:** Privacy, offline, no latency, validates sufficiency

### 3. Active vs Passive Learning
**Decision:** Active questioning (1-2 per day)  
**Why:** Accelerates learning, builds engagement

### 4. Scaffold vs Pure Emergence
**Decision:** Light scaffold (personality dims, entity types)  
**Why:** Faster bootstrap, still allows emergence

### 5. Emotional vs Functional
**Decision:** Emotional companion (not productivity)  
**Why:** Tests bonding hypothesis directly

---

## What This Validates

If successful, proves:
1. **Bonding works:** Users attach through teaching
2. **Learning works:** Weight adjustment improves quality
3. **Edge suffices:** 8B model + patterns = good enough
4. **Patterns work:** Compact representation is viable
5. **Personality emerges:** Organic development from interaction

**Then apply to Martha productivity system with confidence.**

---

## Implementation Options

### Option A: Native Mobile App
```
Platform: React Native / Flutter
LLM: Gemini Nano (Android), MLX (iOS)
Storage: SQLite
Runtime: On-device

Pros: Best performance, full offline
Cons: Platform-specific builds
```

### Option B: Progressive Web App
```
Platform: Web (installable)
LLM: Local via WebGPU/WASM
Storage: IndexedDB
Runtime: Browser-based

Pros: Cross-platform, easy deploy
Cons: Some limitations, newer tech
```

### Option C: Obsidian Plugin (Reuse Infrastructure)
```
Platform: Obsidian mobile
LLM: Via API or local
Storage: Markdown + SQLite
Runtime: Within Obsidian

Pros: Leverage existing stack
Cons: Less standalone, Obsidian dependency
```

**Recommendation: Option A (Native) or B (PWA) for true standalone companion**

---

## Next Steps

1. **Choose implementation path** (Native app vs PWA vs Plugin)
2. **Set up minimal development environment**
3. **Build core pattern engine** (Week 1)
4. **Integrate edge LLM** (Gemini Nano or Llama 3.2)
5. **Create basic UI** (chat + questions)
6. **Test with daily use** (yourself as test user)
7. **Iterate based on emotional response**

**Goal: Working prototype in 4 weeks, validate bonding + learning**

---

## Future Extensions (Post-Validation)

- Voice interaction (natural conversation)
- Multi-modal (photos, location context)
- Distributed sync (family companion network)
- Domain templates (fitness, learning, creative)
- Pattern visualization (show learning graph)
- Export to Martha (productivity integration)

**But first: Prove the core emotional bonding + learning loop works.**
