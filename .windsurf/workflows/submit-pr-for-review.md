---
description: Creates a new branch, commits changes, pushes the branch, and creates a Pull Request for Claude's review.
---

---
description: Creates a new branch, commits changes, pushes the branch, and creates a Pull Request for Claude's review.
---

### **Workflow: Submit Pull Request for Review**

This workflow automates the entire PR submission process, from branching to creation, using direct `git` and `gh` commands.

### **Workflow Definition**

```yaml
name: Submit Pull Request for Review
description: Creates a new branch, commits changes, pushes the branch, and creates a Pull Request for Claude's review.
author: Gemini

inputs:
  - name: branch_name
    type: string
    description: "The name for the new feature branch (e.g., 'feat/update-readme')."
    required: true
  - name: commit_message
    type: string
    description: "The commit message for the changes."
    required: true
  - name: pr_title
    type: string
    description: "The title for the Pull Request."
    required: true
  - name: pr_body
    type: string
    description: "The detailed body/description for the Pull Request. Should tag @claude-cloud."
    required: true
  - name: file_to_add
    type: string
    description: "The specific file to add to the commit. Defaults to staging all changes."
    required: false
    default: "."

steps:
  - name: Create and Switch to New Branch
    shell: powershell
    run: |
      git checkout -b ${{ inputs.branch_name }}
      if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create new branch."
        exit 1
      }

  - name: Stage Changes
    shell: powershell
    run: |
      git add '${{ inputs.file_to_add }}'
      if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to stage changes for file: ${{ inputs.file_to_add }}"
        exit 1
      }

  - name: Commit Changes
    shell: powershell
    run: |
      git commit -m "${{ inputs.commit_message }}"
      if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to commit changes."
        exit 1
      }

  - name: Push Branch to Remote
    shell: powershell
    run: |
      git push -u origin ${{ inputs.branch_name }}
      if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to push branch to remote."
        exit 1
      }

  - name: Create Pull Request
    shell: powershell
    run: |
      gh pr create --title "${{ inputs.pr_title }}" --body "${{ inputs.pr_body }}"
      if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create pull request. Attempting to roll back by deleting remote branch."
        git push origin --delete ${{ inputs.branch_name }}
        exit 1
      }

  - name: Return to Master Branch
    shell: powershell
    run: |
      git checkout master

  - name: Confirm PR Creation
    shell: powershell
    run: |
      echo "Pull request created successfully for branch ${{ inputs.branch_name }}."