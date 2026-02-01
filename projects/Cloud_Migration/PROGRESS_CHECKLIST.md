# Cloud Migration Progress Checklist

**Project**: WhatsApp & Whisper MCP Cloud Migration
**Target**: Google Cloud Platform (e2-micro, always-free tier)
**Start Date**: _____________
**Target Completion**: _____________

---

## Week 1: GCP Setup & VM Provisioning

### Prerequisites
- [ ] Google Cloud Platform account created
- [ ] Billing account configured (required even for free tier)
- [ ] gcloud CLI downloaded and installed on Windows
- [ ] gcloud initialized (`gcloud init`)
- [ ] Project created: `martha-mcp`
- [ ] Default region set: `us-central1`

**Estimated Time**: 1-2 hours
**Date Completed**: _____________

---

### Phase 1: Initial GCP Setup

- [ ] APIs enabled: Compute, Storage, Secret Manager
- [ ] Cloud Storage bucket created: `martha-audio-files` (nearline, us-central1)
- [ ] Cloud Storage bucket created: `whatsapp-mcp-backups` (standard, us-central1)
- [ ] OpenAI API key stored in Secret Manager
- [ ] MCP API key generated and stored in Secret Manager
- [ ] MCP API key saved locally: `C:\Scripts\mcp-api-key.txt`

**Commands Run**:
```bash
gcloud services enable compute.googleapis.com storage.googleapis.com secretmanager.googleapis.com
gsutil mb -c NEARLINE -l us-central1 gs://martha-audio-files
gsutil mb -c STANDARD -l us-central1 gs://whatsapp-mcp-backups
echo -n "sk-proj-..." | gcloud secrets create openai-api-key --data-file=-
openssl rand -hex 32 | gcloud secrets create mcp-api-key --data-file=-
gcloud secrets versions access latest --secret=mcp-api-key > C:\Scripts\mcp-api-key.txt
```

**Verification**:
```bash
gcloud secrets list
# Should show: openai-api-key, mcp-api-key
```

**Estimated Time**: 30 minutes
**Date Completed**: _____________

---

### Phase 2: VM Provisioning

- [ ] VM instance created: `martha-mcp` (e2-micro, Debian 12, us-central1-a)
- [ ] Boot disk: 30GB standard persistent disk
- [ ] Tags applied: `http-server`, `https-server`
- [ ] Scopes set: `cloud-platform`
- [ ] Static IP reserved: `martha-mcp-ip`
- [ ] Static IP saved locally: `C:\Scripts\static-ip.txt`
- [ ] Static IP assigned to VM
- [ ] Firewall rules created: `allow-http` (port 80)
- [ ] Firewall rules created: `allow-https` (port 443)
- [ ] SSH connectivity tested

**Commands Run**:
```bash
gcloud compute instances create martha-mcp \
  --machine-type=e2-micro \
  --zone=us-central1-a \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-standard \
  --tags=http-server,https-server \
  --scopes=cloud-platform

gcloud compute addresses create martha-mcp-ip --region=us-central1
gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format="get(address)" > C:\Scripts\static-ip.txt

gcloud compute firewall-rules create allow-http --allow=tcp:80 --target-tags=http-server
gcloud compute firewall-rules create allow-https --allow=tcp:443 --target-tags=https-server
```

**Verification**:
```bash
gcloud compute ssh martha-mcp --zone=us-central1-a
# Should connect successfully
exit
```

**Static IP**: _____________
**Date Completed**: _____________

---

## Week 2: Software Installation & Service Migration

### Phase 3: VM Software Installation

- [ ] SSH into VM: `gcloud compute ssh martha-mcp --zone=us-central1-a`
- [ ] System updated: `apt-get update && upgrade`
- [ ] Python 3 installed and verified
- [ ] Go installed and verified
- [ ] SQLite3 installed
- [ ] ffmpeg installed
- [ ] nginx installed
- [ ] certbot installed
- [ ] git, curl, build-essential installed
- [ ] gcsfuse installed
- [ ] All installations verified

**Commands Run**:
```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-venv golang-go sqlite3 ffmpeg nginx certbot python3-certbot-nginx git curl build-essential

# Install gcsfuse
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install -y gcsfuse
```

**Verification**:
```bash
python3 --version
go version
ffmpeg -version
nginx -v
gcsfuse --version
```

**Estimated Time**: 1 hour
**Date Completed**: _____________

---

### Phase 4: WhatsApp Bridge Migration

- [ ] Bridge source transferred from Windows to VM
- [ ] Go binary compiled on VM
- [ ] Binary moved to `/opt/whatsapp-bridge/`
- [ ] Executable permissions set
- [ ] systemd service file created: `/etc/systemd/system/whatsapp-bridge.service`
- [ ] systemd daemon reloaded
- [ ] Service enabled for auto-start
- [ ] Service started
- [ ] WhatsApp QR code displayed in logs
- [ ] QR code scanned with phone
- [ ] "Connected" message seen in logs
- [ ] Bridge API tested: `curl http://localhost:8080/api` returns JSON

**Commands Run**:
```powershell
# On Windows
gcloud compute scp --recurse C:\whatsapp-mcp\whatsapp-bridge martha-mcp:/tmp/ --zone=us-central1-a
```

```bash
# On VM
cd /tmp/whatsapp-bridge
go build -o whatsapp-bridge main.go
sudo mkdir -p /opt/whatsapp-bridge/store
sudo mv whatsapp-bridge /opt/whatsapp-bridge/
sudo chmod +x /opt/whatsapp-bridge/whatsapp-bridge

# Create systemd service (see Implementation_Guide.md Phase 4.3)

sudo systemctl daemon-reload
sudo systemctl enable whatsapp-bridge.service
sudo systemctl start whatsapp-bridge.service
sudo journalctl -u whatsapp-bridge -f
# Scan QR code when shown
```

**Verification**:
```bash
sudo systemctl status whatsapp-bridge
curl http://localhost:8080/api
```

**Estimated Time**: 2-3 hours
**Date Completed**: _____________

---

### Phase 5: WhatsApp MCP Server Setup

- [ ] MCP server code transferred from Windows to VM
- [ ] Code moved to `/opt/whatsapp-mcp/`
- [ ] Python virtual environment created
- [ ] Dependencies installed from `requirements.txt`
- [ ] uvicorn and starlette installed
- [ ] `main.py` replaced with HTTP transport version
- [ ] systemd service file created: `/etc/systemd/system/whatsapp-mcp.service`
- [ ] systemd daemon reloaded
- [ ] Service enabled for auto-start
- [ ] Service started
- [ ] Service status checked: active and running
- [ ] HTTP endpoint tested: `curl http://localhost:8081/sse`

**Commands Run**:
```powershell
# On Windows
gcloud compute scp --recurse C:\whatsapp-mcp\whatsapp-mcp-server martha-mcp:/tmp/ --zone=us-central1-a
```

```bash
# On VM
sudo mkdir -p /opt/whatsapp-mcp
sudo mv /tmp/whatsapp-mcp-server/* /opt/whatsapp-mcp/
cd /opt/whatsapp-mcp

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install uvicorn starlette
deactivate

# Replace main.py with modified version from Cloud_Migration/modified_files/
# Create systemd service (see Implementation_Guide.md Phase 5.3)

sudo systemctl daemon-reload
sudo systemctl enable whatsapp-mcp.service
sudo systemctl start whatsapp-mcp.service
```

**Verification**:
```bash
sudo systemctl status whatsapp-mcp
curl http://localhost:8081/sse
```

**Estimated Time**: 2-3 hours
**Date Completed**: _____________

---

### Phase 6: Whisper MCP Server Setup

- [ ] Audio files synced to Cloud Storage from Windows
- [ ] Cloud Storage bucket mounted on VM: `/mnt/audio`
- [ ] Mount added to `/etc/fstab` for auto-mount
- [ ] Audio files visible on VM: `ls /mnt/audio`
- [ ] Whisper MCP code transferred from Windows to VM
- [ ] Code moved to `/opt/whisper-mcp/`
- [ ] Python virtual environment created
- [ ] Package installed with `pip install -e .`
- [ ] uvicorn and starlette installed
- [ ] OpenAI API key retrieved from Secret Manager
- [ ] `.env.secret` file created with API key
- [ ] File permissions set to 600
- [ ] `server.py` replaced with HTTP transport version
- [ ] systemd service file created: `/etc/systemd/system/whisper-mcp.service`
- [ ] systemd daemon reloaded
- [ ] Service enabled for auto-start
- [ ] Service started
- [ ] Service status checked: active and running
- [ ] HTTP endpoint tested: `curl http://localhost:8082/sse`

**Commands Run**:
```powershell
# On Windows
gsutil -m rsync -r "C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio" gs://martha-audio-files/
gcloud compute scp --recurse "C:\Users\10064957\.claude\mcp-servers\mcp-server-whisper" martha-mcp:/tmp/ --zone=us-central1-a
```

```bash
# On VM
sudo mkdir -p /mnt/audio
sudo gcsfuse martha-audio-files /mnt/audio
echo "martha-audio-files /mnt/audio gcsfuse rw,allow_other,file_mode=777,dir_mode=777,_netdev" | sudo tee -a /etc/fstab
ls /mnt/audio

sudo mkdir -p /opt/whisper-mcp
sudo mv /tmp/mcp-server-whisper/* /opt/whisper-mcp/
cd /opt/whisper-mcp

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install uvicorn starlette
deactivate

gcloud secrets versions access latest --secret=openai-api-key | sudo tee /opt/whisper-mcp/.env.secret
echo "OPENAI_API_KEY=$(cat /opt/whisper-mcp/.env.secret)" | sudo tee /opt/whisper-mcp/.env.secret
sudo chmod 600 /opt/whisper-mcp/.env.secret

# Replace server.py with modified version
# Create systemd service (see Implementation_Guide.md Phase 6.6)

sudo systemctl daemon-reload
sudo systemctl enable whisper-mcp.service
sudo systemctl start whisper-mcp.service
```

**Verification**:
```bash
sudo systemctl status whisper-mcp
ls /mnt/audio | head -20
curl http://localhost:8082/sse
```

**Estimated Time**: 2-3 hours
**Date Completed**: _____________

---

## Week 3: Nginx, Testing, & Monitoring

### Phase 7: Nginx Reverse Proxy & SSL

- [ ] Static IP retrieved and saved
- [ ] MCP API key retrieved and saved to `/etc/nginx/mcp-api-key`
- [ ] Self-signed SSL certificate generated
- [ ] Private key permissions set to 600
- [ ] nginx configuration file created: `/etc/nginx/sites-available/martha-mcp`
- [ ] Configuration includes rate limiting
- [ ] Configuration includes API key authentication
- [ ] Configuration includes SSL settings
- [ ] Configuration includes WhatsApp proxy (/whatsapp/)
- [ ] Configuration includes Whisper proxy (/whisper/)
- [ ] Configuration includes health endpoint (/health)
- [ ] Site enabled: symlink in `/etc/nginx/sites-enabled/`
- [ ] Default site removed
- [ ] Configuration tested: `nginx -t` successful
- [ ] nginx reloaded
- [ ] Health endpoint tested locally: `curl -k https://localhost/health` returns "OK"
- [ ] Authenticated endpoint tested locally with API key

**Commands Run**:
```bash
STATIC_IP=$(gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format='get(address)')
API_KEY=$(gcloud secrets versions access latest --secret=mcp-api-key)

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt \
  -subj "/CN=$STATIC_IP"

sudo chmod 600 /etc/ssl/private/nginx-selfsigned.key

echo $API_KEY | sudo tee /etc/nginx/mcp-api-key
sudo chmod 600 /etc/nginx/mcp-api-key

# Create nginx config (see QUICKSTART.md Phase 6)

sudo ln -s /etc/nginx/sites-available/martha-mcp /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

**Verification**:
```bash
curl -k https://localhost/health
# Should return: OK

API_KEY=$(cat /etc/nginx/mcp-api-key)
curl -k -H "Authorization: Bearer $API_KEY" https://localhost/whatsapp/sse
```

**Estimated Time**: 2-3 hours
**Date Completed**: _____________

---

### Phase 8: External Testing & Claude Mobile Configuration

- [ ] Static IP and API key retrieved from VM
- [ ] Health endpoint tested from Windows: `https://<STATIC_IP>/health`
- [ ] WhatsApp endpoint tested from Windows with auth header
- [ ] Whisper endpoint tested from Windows with auth header
- [ ] Claude mobile app MCP configuration updated
- [ ] WhatsApp MCP server added to Claude mobile config
- [ ] Whisper MCP server added to Claude mobile config
- [ ] Authentication headers configured
- [ ] Claude mobile app restarted
- [ ] WhatsApp tools tested from mobile: "List my recent chats"
- [ ] Whisper tools tested from mobile: "List audio files"
- [ ] Response time verified: <2s for WhatsApp
- [ ] Response time verified: <5s for Whisper
- [ ] Full workflow tested: Search messages, transcribe audio, send message

**Static IP**: _____________
**API Key**: _____________

**Claude Mobile Config**:
```json
{
  "mcpServers": {
    "whatsapp": {
      "url": "https://YOUR_STATIC_IP/whatsapp",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    },
    "whisper": {
      "url": "https://YOUR_STATIC_IP/whisper",
      "transport": "sse",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

**Tests from Claude Mobile**:
- [ ] "Show me my recent WhatsApp conversations"
- [ ] "Find WhatsApp messages from [name] about [topic]"
- [ ] "Send a test message to [contact]"
- [ ] "List audio files in my vault"
- [ ] "Transcribe the latest audio file"

**Estimated Time**: 2-3 hours
**Date Completed**: _____________

---

### Phase 9: Monitoring & Backups Setup

- [ ] Database backup script created: `/usr/local/bin/backup-whatsapp-db.sh`
- [ ] Backup script made executable
- [ ] Backup script tested manually
- [ ] Cron job created: Run backups every 6 hours
- [ ] Service health check script created: `/usr/local/bin/check-services.sh`
- [ ] Health check script made executable
- [ ] Health check script tested manually
- [ ] Cron job created: Run health checks every 5 minutes
- [ ] Disk space monitoring script created: `/usr/local/bin/check-disk-space.sh`
- [ ] Disk space script made executable
- [ ] Disk space script tested manually
- [ ] Cron job created: Run disk space check daily
- [ ] Verified backups appearing in Cloud Storage bucket
- [ ] GCP budget alert configured: $10/month with thresholds at 50%, 90%, 100%

**Commands Run**:
```bash
# Create scripts (see Implementation_Guide.md Phase 9)
sudo chmod +x /usr/local/bin/backup-whatsapp-db.sh
sudo chmod +x /usr/local/bin/check-services.sh
sudo chmod +x /usr/local/bin/check-disk-space.sh

# Test scripts
sudo /usr/local/bin/backup-whatsapp-db.sh
sudo /usr/local/bin/check-services.sh
sudo /usr/local/bin/check-disk-space.sh

# Add cron jobs
(sudo crontab -l 2>/dev/null; echo "0 */6 * * * /usr/local/bin/backup-whatsapp-db.sh") | sudo crontab -
(sudo crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/check-services.sh") | sudo crontab -
(sudo crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/check-disk-space.sh") | sudo crontab -
```

**Verification**:
```bash
gsutil ls gs://whatsapp-mcp-backups/
# Should show recent backup files

sudo crontab -l
# Should show all 3 cron jobs
```

**Estimated Time**: 1-2 hours
**Date Completed**: _____________

---

### Phase 10: Audio Sync Automation

- [ ] Sync script created on Windows: `C:\Scripts\sync-audio-to-cloud.ps1`
- [ ] Script tested manually
- [ ] Windows Task Scheduler task created: "SyncAudioToCloud"
- [ ] Task configured to run hourly
- [ ] Task tested (run once manually)
- [ ] Verified files syncing to Cloud Storage
- [ ] Verified files syncing back to local (TTS files)
- [ ] Task running successfully on schedule

**PowerShell Script**: `C:\Scripts\sync-audio-to-cloud.ps1`

**Commands Run**:
```powershell
# Create script (see Implementation_Guide.md Phase 10.1)

# Test script
.\sync-audio-to-cloud.ps1

# Create scheduled task (see Implementation_Guide.md Phase 10.2)
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File 'C:\Scripts\sync-audio-to-cloud.ps1'"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 365)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "SyncAudioToCloud" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
```

**Verification**:
```powershell
Get-ScheduledTask -TaskName "SyncAudioToCloud"
# Should show task ready and enabled
```

**Estimated Time**: 1 hour
**Date Completed**: _____________

---

## Final Verification & Cutover

### Success Criteria

- [ ] ✅ WhatsApp MCP accessible from Claude mobile via HTTPS
- [ ] ✅ Whisper MCP accessible from Claude mobile via HTTPS
- [ ] ✅ Response time <2s for WhatsApp operations
- [ ] ✅ Response time <5s for Whisper operations
- [ ] ✅ WhatsApp session persists across VM restarts (tested)
- [ ] ✅ Monthly cost ≤ $10 (verified in GCP console)
- [ ] ✅ Automated backups running every 6 hours
- [ ] ✅ Service health monitoring active (every 5 minutes)
- [ ] ✅ Audio files syncing bidirectionally (hourly)
- [ ] ✅ All MCP tools working from mobile app

**Date All Criteria Met**: _____________

---

### Post-Migration Tasks

- [ ] Local WhatsApp MCP server stopped on Windows desktop
- [ ] Local Whisper MCP server stopped on Windows desktop
- [ ] Local `.mcp.json` updated to remove local servers (if desired)
- [ ] Document VM IP address and API key in password manager
- [ ] Set calendar reminder: Weekly log review
- [ ] Set calendar reminder: Monthly cost review
- [ ] Create incident response plan for WhatsApp session loss
- [ ] Create runbook for common maintenance tasks
- [ ] Schedule first backup restoration test (verify backups work)

**Migration Completed**: _____________
**Time Spent**: _____________ hours

---

## Troubleshooting Log

Use this section to track any issues encountered during implementation:

### Issue 1
**Date**: _____________
**Phase**: _____________
**Description**:


**Resolution**:


**Time Lost**: _____________ minutes

---

### Issue 2
**Date**: _____________
**Phase**: _____________
**Description**:


**Resolution**:


**Time Lost**: _____________ minutes

---

### Issue 3
**Date**: _____________
**Phase**: _____________
**Description**:


**Resolution**:


**Time Lost**: _____________ minutes

---

## Notes & Learnings

Use this section for any important observations or lessons learned:

1.


2.


3.


---

## Cost Tracking

Track monthly costs here to ensure staying within budget:

### Month 1 (________________)
- Compute Engine: $__________
- Network Egress: $__________
- Cloud Storage: $__________
- **Total**: $__________

### Month 2 (________________)
- Compute Engine: $__________
- Network Egress: $__________
- Cloud Storage: $__________
- **Total**: $__________

### Month 3 (________________)
- Compute Engine: $__________
- Network Egress: $__________
- Cloud Storage: $__________
- **Total**: $__________

**Expected Monthly Cost**: $0-2 (within always-free tier)
**Budget Alert Threshold**: $10/month

---

## Maintenance Schedule

### Weekly Tasks
- [ ] Review service logs for errors
- [ ] Check WhatsApp session status
- [ ] Verify audio sync working
- [ ] Verify backups created successfully

**Last Completed**: _____________

### Monthly Tasks
- [ ] Review GCP billing and usage
- [ ] Clean up old backups (>30 days)
- [ ] Test backup restoration
- [ ] Verify all monitoring scripts running
- [ ] Check disk space usage
- [ ] Review and rotate logs if needed

**Last Completed**: _____________

### Quarterly Tasks
- [ ] Review and update SSL certificate (if needed)
- [ ] Review and update dependencies (security patches)
- [ ] Performance review and optimization
- [ ] Disaster recovery drill (full system restoration)

**Last Completed**: _____________

---

**Project Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Completed
**Current Phase**: _____________
**Blockers**: _____________
