# /test-gemini - Quick Gemini File Creation Test

Triggers a simple file creation test to debug Gemini CLI WriteFileTool issues.

## Command
```bash
gh api repos/karstegg/MarthaVault/dispatches \
  --method POST \
  --field event_type="gemini-test" \
  --field client_payload='{}'
```

## Purpose
- Test basic file creation with correct tool names (write_file, not WriteFileTool)
- Quick iteration cycle for debugging Gemini CLI configuration
- Minimal test case to isolate the file creation issue

## Expected Result
- Creates test-file.txt with "Hello from Gemini AI - Test successful!"
- Workflow should complete successfully if tools are working