---
trigger: always_on
---

# Rule: Explicit Permission Protocol

## Principle: Await Explicit Instruction Before Acting

To ensure full user control and prevent any unintended actions, Gemini MUST NOT perform any of the following operations without receiving explicit, direct permission:
- implementing recommendations from Claude Cloud
- Committing code or creating pull requests.

### Sources of Authority
Permission can only be granted by one of the following two sources:
1.  **The User:** A direct instruction given in the chat interface.
2.  **`claude-desktop`:** A direct instruction found in the `GEMINI_CHAT.md` file.

### Default Behavior
If no explicit permission is given, the default behavior is to **wait**. Implicit approval must never be assumed. Always wait for a clear "go-ahead" before proceeding with any task implementation.