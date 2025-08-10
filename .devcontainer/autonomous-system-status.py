#!/usr/bin/env python3
"""
Autonomous System Status Monitor
Tracks the health and performance of the Claude-orchestrated processing pipeline
"""

import requests
import json
import os
from datetime import datetime, timedelta
import subprocess

class AutonomousSystemMonitor:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.repo = "karstegg/MarthaVault"
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def check_system_health(self):
        """Check overall health of the autonomous system"""
        
        print("🏥 AUTONOMOUS SYSTEM HEALTH CHECK")
        print("=" * 40)
        print()
        
        health_status = {
            "codespace": self._check_codespace_status(),
            "whatsapp_mcp": self._check_whatsapp_mcp(),
            "github_actions": self._check_github_actions(),
            "recent_processing": self._check_recent_processing(),
            "claude_reviews": self._check_claude_reviews()
        }
        
        # Calculate overall health score
        total_checks = len(health_status)
        passed_checks = sum(1 for status in health_status.values() if status["status"] == "healthy")
        health_percentage = (passed_checks / total_checks) * 100
        
        print(f"\n📊 OVERALL SYSTEM HEALTH: {health_percentage:.0f}% ({passed_checks}/{total_checks})")
        
        if health_percentage >= 80:
            print("✅ System Status: OPERATIONAL")
        elif health_percentage >= 60:
            print("⚠️  System Status: DEGRADED")  
        else:
            print("❌ System Status: CRITICAL")
        
        return health_status
    
    def _check_codespace_status(self):
        """Check if Codespace is running and accessible"""
        
        print("🔍 Checking Codespace Status...")
        
        try:
            # Use GitHub CLI to check codespace status
            result = subprocess.run([
                'gh', 'codespace', 'list', '--repo', self.repo, '--json', 'name,state'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                codespaces = json.loads(result.stdout)
                active_codespaces = [cs for cs in codespaces if cs['state'] == 'Available']
                
                if active_codespaces:
                    print(f"  ✅ {len(active_codespaces)} active Codespace(s) found")
                    return {"status": "healthy", "details": f"{len(active_codespaces)} codespaces available"}
                else:
                    print("  ⚠️  No active Codespaces found")
                    return {"status": "warning", "details": "No active codespaces"}
            else:
                print("  ❌ Cannot check Codespace status")
                return {"status": "error", "details": "GitHub CLI error"}
                
        except Exception as e:
            print(f"  💥 Codespace check failed: {e}")
            return {"status": "error", "details": str(e)}
    
    def _check_whatsapp_mcp(self):
        """Check WhatsApp MCP server status"""
        
        print("🔍 Checking WhatsApp MCP Server...")
        
        try:
            # This would ideally ping the MCP server
            # For now, check if we can find running processes
            result = subprocess.run([
                'gh', 'codespace', 'ssh', '--', 'pgrep -f whatsapp-mcp'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and result.stdout.strip():
                print("  ✅ WhatsApp MCP server process detected")
                return {"status": "healthy", "details": "MCP server running"}
            else:
                print("  ⚠️  Cannot confirm WhatsApp MCP server status")
                return {"status": "warning", "details": "MCP status unknown"}
                
        except Exception as e:
            print("  ❌ Cannot check MCP server")
            return {"status": "warning", "details": "Cannot verify MCP status"}
    
    def _check_github_actions(self):
        """Check recent GitHub Actions workflow runs"""
        
        print("🔍 Checking GitHub Actions...")
        
        try:
            url = f"https://api.github.com/repos/{self.repo}/actions/runs"
            params = {"per_page": 10}
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                runs = response.json()["workflow_runs"]
                
                # Check for recent orchestration runs
                orchestration_runs = [run for run in runs 
                                    if "orchestrated" in run["name"].lower()]
                
                if orchestration_runs:
                    latest_run = orchestration_runs[0]
                    status = latest_run["status"]
                    conclusion = latest_run.get("conclusion", "")
                    
                    print(f"  ✅ Latest orchestration run: {status} ({conclusion})")
                    
                    if conclusion == "success":
                        return {"status": "healthy", "details": f"Recent run successful"}
                    elif status == "in_progress":
                        return {"status": "healthy", "details": f"Run in progress"}  
                    else:
                        return {"status": "warning", "details": f"Last run: {conclusion}"}
                else:
                    print("  ⚠️  No recent orchestration runs found")
                    return {"status": "warning", "details": "No recent runs"}
            else:
                print("  ❌ Cannot check GitHub Actions")
                return {"status": "error", "details": "API error"}
                
        except Exception as e:
            print(f"  💥 GitHub Actions check failed: {e}")
            return {"status": "error", "details": str(e)}
    
    def _check_recent_processing(self):
        """Check for recently processed reports"""
        
        print("🔍 Checking Recent Report Processing...")
        
        try:
            # Check git log for recent processing commits
            result = subprocess.run([
                'git', 'log', '--oneline', '--since=1 week ago', 
                '--grep=Process daily production reports'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                commits = result.stdout.strip().split('\n')
                commit_count = len([c for c in commits if c.strip()])
                
                if commit_count > 0:
                    print(f"  ✅ {commit_count} processing commits in last week")
                    return {"status": "healthy", "details": f"{commit_count} recent commits"}
                else:
                    print("  ⚠️  No recent processing commits found")
                    return {"status": "warning", "details": "No recent processing"}
            else:
                print("  ❌ Cannot check git history")
                return {"status": "error", "details": "Git error"}
                
        except Exception as e:
            print(f"  💥 Processing check failed: {e}")
            return {"status": "error", "details": str(e)}
    
    def _check_claude_reviews(self):
        """Check recent Claude review activity"""
        
        print("🔍 Checking Claude Review Activity...")
        
        try:
            # Check for recent issues with claude-review label
            url = f"https://api.github.com/repos/{self.repo}/issues"
            params = {
                "labels": "claude-review",
                "state": "all",
                "per_page": 10,
                "sort": "updated"
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                issues = response.json()
                
                if issues:
                    recent_issues = [i for i in issues 
                                   if (datetime.now() - datetime.fromisoformat(i["updated_at"].replace('Z', '+00:00'))).days <= 7]
                    
                    approved_count = len([i for i in recent_issues 
                                        if any("claude-approved" in label["name"] for label in i["labels"])])
                    
                    print(f"  ✅ {len(recent_issues)} recent reviews, {approved_count} approved")
                    return {"status": "healthy", "details": f"{approved_count}/{len(recent_issues)} approved"}
                else:
                    print("  ⚠️  No recent Claude review activity")
                    return {"status": "warning", "details": "No recent reviews"}
            else:
                print("  ❌ Cannot check Claude reviews")
                return {"status": "error", "details": "API error"}
                
        except Exception as e:
            print(f"  💥 Claude review check failed: {e}")
            return {"status": "error", "details": str(e)}
    
    def get_processing_queue(self):
        """Get current processing queue status"""
        
        print("\n📋 PROCESSING QUEUE STATUS")
        print("-" * 30)
        
        try:
            # Get autonomous processing issues
            url = f"https://api.github.com/repos/{self.repo}/issues"
            params = {
                "labels": "autonomous-processing",
                "state": "open",
                "sort": "created"
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                queue_issues = response.json()
                
                if queue_issues:
                    print(f"📊 {len(queue_issues)} items in processing queue:")
                    for issue in queue_issues[:5]:  # Show first 5
                        title = issue["title"]
                        created = issue["created_at"][:10]  # Date only
                        print(f"  🔄 #{issue['number']}: {title} (created {created})")
                    
                    if len(queue_issues) > 5:
                        print(f"  ... and {len(queue_issues) - 5} more")
                else:
                    print("✅ Processing queue is empty")
                
                return queue_issues
            else:
                print("❌ Cannot check processing queue")
                return []
                
        except Exception as e:
            print(f"💥 Queue check failed: {e}")
            return []

def main():
    print("🤖 AUTONOMOUS DAILY PRODUCTION REPORT SYSTEM")
    print("Status Monitor & Health Dashboard")
    print("=" * 50)
    print(f"Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable required")
        return 1
    
    monitor = AutonomousSystemMonitor()
    
    # Run health checks
    health_status = monitor.check_system_health()
    
    # Show processing queue
    queue = monitor.get_processing_queue()
    
    # Summary recommendations
    print("\n💡 SYSTEM RECOMMENDATIONS")
    print("-" * 25)
    
    unhealthy_components = [comp for comp, status in health_status.items() 
                           if status["status"] != "healthy"]
    
    if not unhealthy_components:
        print("✅ System is operating optimally")
        print("🚀 Ready for autonomous report processing")
    else:
        print("⚠️  Issues detected in:")
        for comp in unhealthy_components:
            print(f"   - {comp}: {health_status[comp]['details']}")
        print()
        print("🔧 Recommended actions:")
        if "codespace" in unhealthy_components:
            print("   - Start a new Codespace")
        if "whatsapp_mcp" in unhealthy_components:
            print("   - Restart WhatsApp MCP server in Codespace")
    
    print(f"\n📊 Queue Status: {len(queue)} pending processing requests")
    
    return 0

if __name__ == "__main__":
    exit(main())