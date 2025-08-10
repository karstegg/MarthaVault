#!/usr/bin/env python3
"""
Autonomous Setup Verification Script
Checks if Codespace + WhatsApp MCP + Autonomous system is properly configured
"""

import os
import sys
import subprocess
import json
from datetime import datetime

class AutonomousSetupVerifier:
    def __init__(self):
        self.codespaces_env = os.getenv('CODESPACES')
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo_root = "/workspaces/MarthaVault" if self.codespaces_env else os.getcwd()
        
    def verify_environment(self):
        """Verify we're in the correct environment"""
        
        print("🏠 ENVIRONMENT VERIFICATION")
        print("=" * 30)
        
        checks = {
            "codespaces": self._check_codespaces(),
            "repository": self._check_repository(),
            "github_token": self._check_github_token(),
            "git_config": self._check_git_config()
        }
        
        return checks
    
    def verify_whatsapp_mcp(self):
        """Verify WhatsApp MCP server setup"""
        
        print("\n📱 WHATSAPP MCP VERIFICATION")
        print("=" * 30)
        
        checks = {
            "mcp_server_path": self._check_mcp_server_path(),
            "mcp_server_status": self._check_mcp_server_status(),
            "mcp_dependencies": self._check_mcp_dependencies(),
            "whatsapp_session": self._check_whatsapp_session()
        }
        
        return checks
    
    def verify_autonomous_system(self):
        """Verify autonomous system components"""
        
        print("\n🤖 AUTONOMOUS SYSTEM VERIFICATION")
        print("=" * 35)
        
        checks = {
            "orchestration_workflows": self._check_workflows(),
            "trigger_scripts": self._check_trigger_scripts(),
            "processing_pipeline": self._check_processing_pipeline(),
            "devcontainer_config": self._check_devcontainer_config()
        }
        
        return checks
    
    def _check_codespaces(self):
        """Check Codespaces environment"""
        if self.codespaces_env:
            print(f"  ✅ Running in Codespaces: {self.codespaces_env}")
            return {"status": "ok", "details": f"Codespace: {self.codespaces_env}"}
        else:
            print("  ⚠️  Not running in Codespaces")
            return {"status": "warning", "details": "Local environment"}
    
    def _check_repository(self):
        """Check repository setup"""
        if os.path.exists(os.path.join(self.repo_root, ".git")):
            try:
                # Get current branch
                result = subprocess.run(['git', 'branch', '--show-current'], 
                                      capture_output=True, text=True, cwd=self.repo_root)
                branch = result.stdout.strip()
                print(f"  ✅ Git repository on branch: {branch}")
                return {"status": "ok", "details": f"Branch: {branch}"}
            except:
                print("  ❌ Git repository issues")
                return {"status": "error", "details": "Git command failed"}
        else:
            print("  ❌ Not in git repository")
            return {"status": "error", "details": "No .git directory"}
    
    def _check_github_token(self):
        """Check GitHub token availability"""
        if self.github_token:
            masked_token = self.github_token[:8] + "..." + self.github_token[-4:] if len(self.github_token) > 12 else "***"
            print(f"  ✅ GitHub token available: {masked_token}")
            return {"status": "ok", "details": "Token configured"}
        else:
            print("  ❌ GitHub token not found")
            return {"status": "error", "details": "GITHUB_TOKEN missing"}
    
    def _check_git_config(self):
        """Check git configuration"""
        try:
            user_result = subprocess.run(['git', 'config', 'user.name'], 
                                       capture_output=True, text=True, cwd=self.repo_root)
            email_result = subprocess.run(['git', 'config', 'user.email'], 
                                        capture_output=True, text=True, cwd=self.repo_root)
            
            if user_result.stdout.strip() and email_result.stdout.strip():
                print(f"  ✅ Git configured: {user_result.stdout.strip()}")
                return {"status": "ok", "details": "Git user configured"}
            else:
                print("  ⚠️  Git user not configured")
                return {"status": "warning", "details": "No git user/email"}
        except:
            print("  ❌ Cannot check git config")
            return {"status": "error", "details": "Git config check failed"}
    
    def _check_mcp_server_path(self):
        """Check if WhatsApp MCP server exists"""
        possible_paths = [
            "/workspaces/MarthaVault/whatsapp-mcp-server",
            "/workspaces/whatsapp-mcp-server",
            "/workspaces/whatsapp-mcp"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"  ✅ WhatsApp MCP found at: {path}")
                return {"status": "ok", "details": f"Server at: {path}"}
        
        print("  ❌ WhatsApp MCP server not found")
        return {"status": "error", "details": "MCP server missing"}
    
    def _check_mcp_server_status(self):
        """Check if WhatsApp MCP server is running"""
        try:
            result = subprocess.run(['pgrep', '-f', 'whatsapp.*mcp'], 
                                  capture_output=True, text=True)
            
            if result.stdout.strip():
                pids = result.stdout.strip().split('\n')
                print(f"  ✅ WhatsApp MCP server running (PIDs: {', '.join(pids)})")
                return {"status": "ok", "details": f"Running PIDs: {pids}"}
            else:
                print("  ⚠️  WhatsApp MCP server not running")
                return {"status": "warning", "details": "Server not running"}
        except:
            print("  ❌ Cannot check MCP server status")
            return {"status": "error", "details": "Status check failed"}
    
    def _check_mcp_dependencies(self):
        """Check MCP server dependencies"""
        # This would check for Python packages, etc.
        try:
            # Check if python is available
            result = subprocess.run(['python3', '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"  ✅ Python available: {version}")
                return {"status": "ok", "details": version}
            else:
                print("  ❌ Python not available")
                return {"status": "error", "details": "No Python"}
        except:
            print("  ❌ Cannot check dependencies")
            return {"status": "error", "details": "Dependency check failed"}
    
    def _check_whatsapp_session(self):
        """Check WhatsApp session status"""
        # Check for session files or indicators
        session_paths = [
            "/workspaces/sessions",
            "/tmp/whatsapp-session"
        ]
        
        for path in session_paths:
            if os.path.exists(path):
                print(f"  ✅ WhatsApp session directory found: {path}")
                return {"status": "ok", "details": f"Session dir: {path}"}
        
        print("  ⚠️  WhatsApp session directory not found")
        return {"status": "warning", "details": "No session directory"}
    
    def _check_workflows(self):
        """Check GitHub Actions workflows"""
        workflow_files = [
            ".github/workflows/claude-orchestrated-processing.yml",
            ".github/workflows/claude-review-orchestrated-results.yml"
        ]
        
        found_workflows = 0
        for workflow in workflow_files:
            workflow_path = os.path.join(self.repo_root, workflow)
            if os.path.exists(workflow_path):
                found_workflows += 1
        
        if found_workflows == len(workflow_files):
            print(f"  ✅ All {len(workflow_files)} orchestration workflows present")
            return {"status": "ok", "details": f"{found_workflows} workflows"}
        else:
            print(f"  ⚠️  {found_workflows}/{len(workflow_files)} workflows found")
            return {"status": "warning", "details": f"Missing workflows"}
    
    def _check_trigger_scripts(self):
        """Check autonomous trigger scripts"""
        script_files = [
            ".devcontainer/claude-orchestration-trigger.py",
            ".devcontainer/autonomous-system-status.py",
            ".devcontainer/codespace-direct-processing.py"
        ]
        
        found_scripts = 0
        for script in script_files:
            script_path = os.path.join(self.repo_root, script)
            if os.path.exists(script_path):
                found_scripts += 1
        
        if found_scripts == len(script_files):
            print(f"  ✅ All {len(script_files)} trigger scripts present")
            return {"status": "ok", "details": f"{found_scripts} scripts"}
        else:
            print(f"  ⚠️  {found_scripts}/{len(script_files)} scripts found")
            return {"status": "warning", "details": "Missing scripts"}
    
    def _check_processing_pipeline(self):
        """Check processing pipeline components"""
        # Check for key configuration files
        config_files = [
            "GEMINI.md",
            "Report Templates/Standard Mine Site Report Template.md",
            "Report Templates/Shafts & Winders Report Template.md"
        ]
        
        found_configs = 0
        for config in config_files:
            config_path = os.path.join(self.repo_root, config)
            if os.path.exists(config_path):
                found_configs += 1
        
        if found_configs == len(config_files):
            print(f"  ✅ All {len(config_files)} pipeline configs present")
            return {"status": "ok", "details": f"{found_configs} configs"}
        else:
            print(f"  ⚠️  {found_configs}/{len(config_files)} configs found")
            return {"status": "warning", "details": "Missing configs"}
    
    def _check_devcontainer_config(self):
        """Check devcontainer configuration"""
        devcontainer_path = os.path.join(self.repo_root, ".devcontainer/devcontainer.json")
        
        if os.path.exists(devcontainer_path):
            print("  ✅ Devcontainer configuration present")
            return {"status": "ok", "details": "Config present"}
        else:
            print("  ❌ Devcontainer configuration missing")
            return {"status": "error", "details": "Missing devcontainer.json"}
    
    def generate_report(self, env_checks, mcp_checks, system_checks):
        """Generate comprehensive verification report"""
        
        print("\n📊 AUTONOMOUS SETUP VERIFICATION REPORT")
        print("=" * 45)
        print(f"**Verification Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        all_checks = {**env_checks, **mcp_checks, **system_checks}
        
        # Count status types
        ok_count = len([c for c in all_checks.values() if c['status'] == 'ok'])
        warning_count = len([c for c in all_checks.values() if c['status'] == 'warning'])
        error_count = len([c for c in all_checks.values() if c['status'] == 'error'])
        total_checks = len(all_checks)
        
        # Calculate health percentage
        health_percentage = (ok_count / total_checks) * 100
        
        print(f"**Overall Health**: {health_percentage:.0f}% ({ok_count}/{total_checks} passed)")
        print(f"✅ OK: {ok_count} | ⚠️ Warnings: {warning_count} | ❌ Errors: {error_count}")
        print()
        
        # Determine overall status
        if health_percentage >= 90:
            print("🎉 **AUTONOMOUS SYSTEM STATUS: FULLY OPERATIONAL**")
            recommendation = "Ready for autonomous processing!"
        elif health_percentage >= 75:
            print("⚡ **AUTONOMOUS SYSTEM STATUS: MOSTLY OPERATIONAL**") 
            recommendation = "Minor issues to address, but system can function"
        elif health_percentage >= 50:
            print("⚠️ **AUTONOMOUS SYSTEM STATUS: DEGRADED**")
            recommendation = "Several issues need fixing before autonomous processing"
        else:
            print("❌ **AUTONOMOUS SYSTEM STATUS: CRITICAL ISSUES**")
            recommendation = "Major setup problems - manual intervention required"
        
        print(f"**Recommendation**: {recommendation}")
        print()
        
        # List specific issues
        if warning_count > 0 or error_count > 0:
            print("🔧 **Issues to Address:**")
            for check_name, result in all_checks.items():
                if result['status'] in ['warning', 'error']:
                    status_icon = "⚠️" if result['status'] == 'warning' else "❌"
                    print(f"  {status_icon} {check_name}: {result['details']}")
            print()
        
        # Next steps
        if health_percentage >= 90:
            print("🚀 **Ready for Testing:**")
            print("  1. Test autonomous trigger: `python3 .devcontainer/claude-orchestration-trigger.py 2025-08-09`")
            print("  2. Monitor system: `python3 .devcontainer/autonomous-system-status.py`")
        else:
            print("🔧 **Setup Steps Required:**")
            if error_count > 0:
                print("  1. Fix critical errors listed above")
            if warning_count > 0:
                print("  2. Address warnings for optimal performance")
            print("  3. Re-run verification: `python3 .devcontainer/verify-autonomous-setup.py`")
        
        return health_percentage >= 75  # Return True if system is ready

def main():
    print("🔍 AUTONOMOUS DAILY PRODUCTION REPORT SYSTEM")
    print("Setup Verification & Health Check")
    print("=" * 50)
    print()
    
    verifier = AutonomousSetupVerifier()
    
    # Run all verifications
    env_checks = verifier.verify_environment()
    mcp_checks = verifier.verify_whatsapp_mcp()
    system_checks = verifier.verify_autonomous_system()
    
    # Generate comprehensive report
    system_ready = verifier.generate_report(env_checks, mcp_checks, system_checks)
    
    return 0 if system_ready else 1

if __name__ == "__main__":
    sys.exit(main())