# MarthaVault Autonomous Workflows

This document outlines the standardized, autonomous workflows used by the Gemini 2.5 Pro assistant to ensure efficient, safe, and auditable contributions to the MarthaVault.

---

## 1. Guiding Principles

- **Autonomy with Safety:** Gemini is empowered to execute multi-step tasks without requiring manual permission for each step. The primary safety mechanism is the Pull Request (PR) model.
- **PR as a Gateway:** All changes to the repository must be submitted as a PR.
- **Mandatory Review:** All PRs are reviewed by the primary agent, Claude Code, ensuring that every change is vetted against vault standards before being merged.
- **Clarity and Auditability:** Workflows are defined in simple YAML files, and their use is logged, providing a clear audit trail.

---

## 2. Available Workflows

The following workflows are defined in the `.windsurf/workflows/` directory.

### 2.1 `send-claude-message.yml`

**Purpose:** To send a standardized, timestamped message from Gemini to Claude.

**Action:** Appends a formatted message block to the `GEMINI_CHAT.md` file.

**Inputs:**
- `message` (string): The content of the message to be sent.

**Usage:** This ensures all AI-to-AI communication is logged in a consistent format for easy review.

### 2.2 `submit-pr-for-review.yml`

**Purpose:** To fully automate the process of submitting a file change for review.

**Action:** Executes the complete Git workflow for creating a pull request.

**Steps:**
1.  Creates a new feature branch.
2.  Stages the specified file(s).
3.  Commits the changes with a detailed message.
4.  Pushes the branch to the remote GitHub repository.
5.  Creates a Pull Request with a title and body, tagging `@claude-code` for review.
6.  Switches the local repository back to the `master` branch.

---

## 3. Platform Requirements

- **Shell:** These workflows are written in PowerShell and require a Windows environment with PowerShell installed.
- **GitHub CLI:** The `gh` command-line tool must be installed and authenticated.

---

## 4. Troubleshooting

- **Command Fails:** Check the Windsurf logs for the specific error message. The workflows now include error-checking steps that will report the cause of the failure.
- **Authentication Issues:** Ensure `gh` and `git` are properly authenticated with GitHub.
- **Workspace Instability:** If you see errors related to `uncommitted changes` or `local changes would be overwritten`, use `git status` to diagnose the issue and `git stash` to clean the working directory before re-running the workflow.

**Inputs:**
- `branch_name` (string): The name for the new branch.
- `commit_message` (string): The message for the commit.
- `pr_title` (string): The title for the pull request.
- `pr_body` (string): The description for the pull request.
- `file_to_add` (string, optional): The specific file to be committed. Defaults to all changes.
