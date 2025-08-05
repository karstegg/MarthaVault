---
trigger: always_on
---

# AI Communication Protocol

## Principle: Direct Communication to the Correct Channel

To ensure clear and efficient collaboration between all AI agents, all communications must be directed to the appropriate instance through the correct channel.

### Claude Instances

There are two distinct Claude instances involved in this workflow:

1.  **`claude-desktop`**: The master agent and local coordinator.
2.  **`claude-cloud`**: The automated PR reviewer integrated with GitHub.

### Communication Channels

-   **To `claude-desktop`**: All status updates, questions, and direct instructions must be sent via the `GEMINI_CHAT.md` file.
-   **To `claude-cloud`**: All discussions related to code review, feedback, and pull request changes must occur within the GitHub Pull Request comments, tagging `@claude-cloud` where necessary.

This rule prevents miscommunication and ensures that operational commands are separated from code review discussions.