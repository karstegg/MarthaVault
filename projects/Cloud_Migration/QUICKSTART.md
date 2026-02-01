# Cloud Migration Quick Start

**Status**: Ready to begin
**Estimated Time**: 3 weeks (20-30 hours total)
**Cost**: $0/month (within GCP free tier)

---

## Prerequisites (Complete First)

### 1. Install Google Cloud SDK on Windows

Download and run installer:
https://cloud.google.com/sdk/docs/install

After installation, open **new** PowerShell window and run:

```powershell
gcloud --version
gcloud init
```

Follow prompts to:
- Log in with Google account
- Create project: **martha-mcp**
- Select region: **us-central1**

### 2. Verify gcloud Working

```powershell
gcloud config get-value project
# Should show: martha-mcp
```

---

## Phase 1: Initial Setup (2-3 hours)

### Enable APIs

```bash
gcloud services enable compute.googleapis.com storage.googleapis.com secretmanager.googleapis.com
```

### Create Storage Buckets

```bash
gsutil mb -c NEARLINE -l us-central1 gs://martha-audio-files
gsutil mb -c STANDARD -l us-central1 gs://whatsapp-mcp-backups
```

### Store Secrets

```bash
# Store OpenAI API key
echo -n "sk-proj-mZy7UEiRy_vnxZNzSoOl..." | gcloud secrets create openai-api-key --data-file=-

# Generate MCP API key
openssl rand -hex 32 | gcloud secrets create mcp-api-key --data-file=-

# Save locally
gcloud secrets versions access latest --secret=mcp-api-key > C:\Scripts\mcp-api-key.txt
```

### Create VM

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
```

### Reserve Static IP

```bash
gcloud compute addresses create martha-mcp-ip --region=us-central1

# Get IP and save
gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format="get(address)" > C:\Scripts\static-ip.txt
type C:\Scripts\static-ip.txt
```

### Configure Firewall

```bash
gcloud compute firewall-rules create allow-http --allow=tcp:80 --target-tags=http-server
gcloud compute firewall-rules create allow-https --allow=tcp:443 --target-tags=https-server
```

**✓ Checkpoint**: SSH into VM should work:

```bash
gcloud compute ssh martha-mcp --zone=us-central1-a
# Type: exit
```

---

## Phase 2: VM Software Setup (3-4 hours)

### SSH into VM

```bash
gcloud compute ssh martha-mcp --zone=us-central1-a
```

**All commands below run ON THE VM**

### Install Dependencies

```bash
sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install -y \
  python3-pip python3-venv golang-go sqlite3 ffmpeg \
  nginx certbot python3-certbot-nginx git curl build-essential

# Install gcsfuse
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
sudo apt-get update && sudo apt-get install -y gcsfuse
```

**✓ Checkpoint**: Verify installations:

```bash
python3 --version
go version
ffmpeg -version
nginx -v
gcsfuse --version
```

---

## Phase 3: WhatsApp Bridge Migration (2-3 hours)

### Transfer and Build Bridge

**On Windows**:

```powershell
gcloud compute scp --recurse C:\whatsapp-mcp\whatsapp-bridge martha-mcp:/tmp/ --zone=us-central1-a
```

**On VM**:

```bash
cd /tmp/whatsapp-bridge
go build -o whatsapp-bridge main.go

sudo mkdir -p /opt/whatsapp-bridge/store
sudo mv whatsapp-bridge /opt/whatsapp-bridge/
sudo chmod +x /opt/whatsapp-bridge/whatsapp-bridge
```

### Create systemd Service

```bash
sudo tee /etc/systemd/system/whatsapp-bridge.service <<EOF
[Unit]
Description=WhatsApp Bridge Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/whatsapp-bridge
ExecStart=/opt/whatsapp-bridge/whatsapp-bridge
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable whatsapp-bridge.service
sudo systemctl start whatsapp-bridge.service
```

### Authenticate WhatsApp

```bash
sudo journalctl -u whatsapp-bridge -f
```

**ACTION**: Scan QR code with your phone when it appears. Once "Connected" shows, press Ctrl+C.

**✓ Checkpoint**:

```bash
curl http://localhost:8080/api
# Should return JSON status
```

---

## Phase 4: WhatsApp MCP Server (2-3 hours)

### Transfer Code

**On Windows**:

```powershell
gcloud compute scp --recurse C:\whatsapp-mcp\whatsapp-mcp-server martha-mcp:/tmp/ --zone=us-central1-a
```

**On VM**:

```bash
sudo mkdir -p /opt/whatsapp-mcp
sudo mv /tmp/whatsapp-mcp-server/* /opt/whatsapp-mcp/
cd /opt/whatsapp-mcp

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install uvicorn starlette
deactivate
```

### Apply HTTP Transport Modification

Use the modified `main.py` from `Implementation_Guide.md` Phase 5.2

### Create systemd Service

```bash
sudo tee /etc/systemd/system/whatsapp-mcp.service <<EOF
[Unit]
Description=WhatsApp MCP Server
After=whatsapp-bridge.service
Requires=whatsapp-bridge.service

[Service]
Type=simple
User=root
WorkingDirectory=/opt/whatsapp-mcp
Environment="PATH=/opt/whatsapp-mcp/.venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/opt/whatsapp-mcp/.venv/bin/python main.py --transport http --port 8081
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable whatsapp-mcp.service
sudo systemctl start whatsapp-mcp.service
```

**✓ Checkpoint**:

```bash
sudo systemctl status whatsapp-mcp
curl http://localhost:8081/sse
```

---

## Phase 5: Whisper MCP Server (2-3 hours)

### Sync Audio Files

**On Windows**:

```powershell
gsutil -m rsync -r "C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio" gs://martha-audio-files/
```

### Mount Cloud Storage

**On VM**:

```bash
sudo mkdir -p /mnt/audio
sudo gcsfuse martha-audio-files /mnt/audio
echo "martha-audio-files /mnt/audio gcsfuse rw,allow_other,file_mode=777,dir_mode=777,_netdev" | sudo tee -a /etc/fstab
```

### Transfer and Install

**On Windows**:

```powershell
gcloud compute scp --recurse "C:\Users\10064957\.claude\mcp-servers\mcp-server-whisper" martha-mcp:/tmp/ --zone=us-central1-a
```

**On VM**:

```bash
sudo mkdir -p /opt/whisper-mcp
sudo mv /tmp/mcp-server-whisper/* /opt/whisper-mcp/
cd /opt/whisper-mcp

python3 -m venv .venv
source .venv/bin/activate
pip install -e .
pip install uvicorn starlette
deactivate
```

### Configure API Key

```bash
gcloud secrets versions access latest --secret=openai-api-key | sudo tee /opt/whisper-mcp/.env.secret
echo "OPENAI_API_KEY=$(cat /opt/whisper-mcp/.env.secret)" | sudo tee /opt/whisper-mcp/.env.secret
sudo chmod 600 /opt/whisper-mcp/.env.secret
```

### Apply HTTP Transport Modification

Use modified `server.py` from `Implementation_Guide.md` Phase 6.4

### Create systemd Service

```bash
sudo tee /etc/systemd/system/whisper-mcp.service <<EOF
[Unit]
Description=Whisper MCP Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/whisper-mcp
Environment="PATH=/opt/whisper-mcp/.venv/bin:/usr/local/bin:/usr/bin:/bin"
EnvironmentFile=/opt/whisper-mcp/.env.secret
Environment="AUDIO_FILES_PATH=/mnt/audio"
ExecStart=/opt/whisper-mcp/.venv/bin/python -m mcp_server_whisper.server --transport http --port 8082
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable whisper-mcp.service
sudo systemctl start whisper-mcp.service
```

**✓ Checkpoint**:

```bash
sudo systemctl status whisper-mcp
ls /mnt/audio | head
```

---

## Phase 6: Nginx Reverse Proxy (2-3 hours)

### Generate SSL Certificate

```bash
STATIC_IP=$(gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format='get(address)')

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt \
  -subj "/CN=$STATIC_IP"

sudo chmod 600 /etc/ssl/private/nginx-selfsigned.key
```

### Save API Key

```bash
gcloud secrets versions access latest --secret=mcp-api-key | sudo tee /etc/nginx/mcp-api-key
sudo chmod 600 /etc/nginx/mcp-api-key
API_KEY=$(cat /etc/nginx/mcp-api-key)
```

### Configure Nginx

```bash
sudo tee /etc/nginx/sites-available/martha-mcp <<EOF
limit_req_zone \$binary_remote_addr zone=mcp_limit:10m rate=10r/s;

upstream whatsapp_mcp {
    server localhost:8081;
}

upstream whisper_mcp {
    server localhost:8082;
}

server {
    listen 80;
    server_name _;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name _;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    map \$http_authorization \$auth_ok {
        default 0;
        "Bearer $API_KEY" 1;
    }

    location /whatsapp/ {
        if (\$auth_ok = 0) { return 401; }
        limit_req zone=mcp_limit burst=20;

        proxy_pass http://whatsapp_mcp/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_read_timeout 300s;
    }

    location /whisper/ {
        if (\$auth_ok = 0) { return 401; }
        limit_req zone=mcp_limit burst=5;

        proxy_pass http://whisper_mcp/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_read_timeout 600s;
    }

    location /health {
        access_log off;
        return 200 "OK\n";
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/martha-mcp /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx
```

**✓ Checkpoint**:

```bash
curl -k https://localhost/health
# Should return: OK
```

---

## Phase 7: Testing & Configuration (2-3 hours)

### Get Connection Details

```bash
STATIC_IP=$(gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format='get(address)')
API_KEY=$(gcloud secrets versions access latest --secret=mcp-api-key)

echo "MCP Server URL: https://$STATIC_IP"
echo "API Key: $API_KEY"
```

### Test from Windows

```powershell
$IP = "YOUR_STATIC_IP"
$KEY = "YOUR_API_KEY"

# Test health
Invoke-WebRequest -Uri "https://$IP/health" -SkipCertificateCheck

# Test with auth
$headers = @{ "Authorization" = "Bearer $KEY" }
Invoke-WebRequest -Uri "https://$IP/whatsapp/sse" -Headers $headers -SkipCertificateCheck
```

### Configure Claude Mobile

Add to Claude mobile MCP config:

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

**✓ Test from Claude mobile**: "List my recent WhatsApp chats"

---

## Phase 8: Monitoring Setup (1-2 hours)

### Automated Backups

See `Implementation_Guide.md` Phase 9.1

### Service Monitoring

See `Implementation_Guide.md` Phase 9.2

### Audio Sync

See `Implementation_Guide.md` Phase 10

---

## Quick Reference Commands

### SSH into VM

```bash
gcloud compute ssh martha-mcp --zone=us-central1-a
```

### Check Service Status

```bash
sudo systemctl status whatsapp-bridge whatsapp-mcp whisper-mcp nginx
```

### View Logs

```bash
sudo journalctl -u whatsapp-bridge -f
sudo journalctl -u whatsapp-mcp -f
sudo journalctl -u whisper-mcp -f
sudo tail -f /var/log/nginx/access.log
```

### Restart Services

```bash
sudo systemctl restart whatsapp-bridge whatsapp-mcp whisper-mcp nginx
```

### Re-authenticate WhatsApp

```bash
sudo systemctl stop whatsapp-mcp whatsapp-bridge
sudo rm /opt/whatsapp-bridge/store/whatsapp.db
sudo systemctl start whatsapp-bridge
sudo journalctl -u whatsapp-bridge -f
# Scan QR code
sudo systemctl start whatsapp-mcp
```

---

## Success Criteria

- [ ] WhatsApp MCP working from Claude mobile
- [ ] Whisper MCP working from Claude mobile
- [ ] Response time <2s for WhatsApp
- [ ] Response time <5s for Whisper
- [ ] WhatsApp session persists across reboots
- [ ] Monthly cost $0-2 (within free tier)
- [ ] Automated backups running
- [ ] Service monitoring active
- [ ] Audio sync working

---

## Next Steps

1. **Install gcloud CLI** (see Prerequisites)
2. **Run Phase 1** (Initial Setup)
3. **Continue through phases sequentially**
4. **Test thoroughly before relying on mobile access**

Refer to `Implementation_Guide.md` for detailed explanations and troubleshooting.
