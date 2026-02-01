# WhatsApp & Whisper MCP Cloud Migration - Implementation Guide

**Status**: Ready to begin
**Target**: Google Cloud Platform e2-micro VM (free tier)
**Timeline**: 3 weeks
**Cost**: $0/month (within always-free tier)

---

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Google Cloud Platform account created
- [ ] GCP billing account set up (required even for free tier)
- [ ] `gcloud` CLI installed on Windows: https://cloud.google.com/sdk/docs/install
- [ ] OpenAI API key accessible (for Whisper)
- [ ] WhatsApp session currently working on Windows bridge

---

## Phase 1: GCP Setup (Week 1)

### Step 1.1: Install gcloud CLI on Windows

```powershell
# Download installer from: https://cloud.google.com/sdk/docs/install
# Run installer: GoogleCloudSDKInstaller.exe

# After installation, open new PowerShell and verify:
gcloud --version

# Initialize gcloud
gcloud init

# Follow prompts to:
# 1. Log in with your Google account
# 2. Create new project: martha-mcp
# 3. Select default region: us-central1
```

### Step 1.2: Enable Required APIs

```bash
gcloud config set project martha-mcp

gcloud services enable compute.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

### Step 1.3: Create Cloud Storage Buckets

```bash
# For audio files (nearline storage for cost optimization)
gsutil mb -c NEARLINE -l us-central1 gs://martha-audio-files

# For WhatsApp database backups
gsutil mb -c STANDARD -l us-central1 gs://whatsapp-mcp-backups
```

### Step 1.4: Store Secrets

```bash
# Store OpenAI API key
echo -n "sk-proj-mZy7UEiRy_vnxZNzSoOl..." | gcloud secrets create openai-api-key --data-file=-

# Generate and store MCP API key for authentication
powershell -Command "[System.Convert]::ToHexString((1..32 | ForEach-Object {Get-Random -Maximum 256}))" | gcloud secrets create mcp-api-key --data-file=-

# Retrieve and save API key locally for later
gcloud secrets versions access latest --secret=mcp-api-key > C:\Scripts\mcp-api-key.txt
```

**Checkpoint**: Verify secrets created:
```bash
gcloud secrets list
```

---

## Phase 2: VM Provisioning (Week 1)

### Step 2.1: Create VM Instance

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

**Expected output**: VM created with external IP

### Step 2.2: Reserve Static IP

```bash
gcloud compute addresses create martha-mcp-ip \
  --region=us-central1

# Get IP address and save it
gcloud compute addresses describe martha-mcp-ip \
  --region=us-central1 --format="get(address)" > C:\Scripts\static-ip.txt

type C:\Scripts\static-ip.txt
```

### Step 2.3: Assign Static IP to VM

```bash
gcloud compute instances delete-access-config martha-mcp \
  --access-config-name="external-nat" --zone=us-central1-a

gcloud compute instances add-access-config martha-mcp \
  --access-config-name="external-nat" \
  --address=$(type C:\Scripts\static-ip.txt) \
  --zone=us-central1-a
```

### Step 2.4: Configure Firewall Rules

```bash
gcloud compute firewall-rules create allow-http \
  --allow=tcp:80 \
  --target-tags=http-server

gcloud compute firewall-rules create allow-https \
  --allow=tcp:443 \
  --target-tags=https-server
```

**Checkpoint**: SSH into VM and verify connectivity:
```bash
gcloud compute ssh martha-mcp --zone=us-central1-a
# Once connected, type: exit
```

---

## Phase 3: Software Installation (Week 2)

### Step 3.1: SSH into VM

```bash
gcloud compute ssh martha-mcp --zone=us-central1-a
```

**All commands below run on the VM unless noted otherwise**

### Step 3.2: Update System and Install Dependencies

```bash
sudo apt-get update && sudo apt-get upgrade -y

sudo apt-get install -y \
  python3-pip \
  python3-venv \
  golang-go \
  sqlite3 \
  ffmpeg \
  nginx \
  certbot \
  python3-certbot-nginx \
  git \
  curl \
  build-essential
```

### Step 3.3: Install gcsfuse

```bash
export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb https://packages.cloud.google.com/apt $GCSFUSE_REPO main" | \
  sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
  sudo apt-key add -
sudo apt-get update
sudo apt-get install -y gcsfuse
```

**Checkpoint**: Verify installations:
```bash
python3 --version
go version
ffmpeg -version
nginx -v
gcsfuse --version
```

---

## Phase 4: WhatsApp Bridge Migration (Week 2)

### Step 4.1: Build Go Bridge for Linux

**On your Windows machine**, open PowerShell:

```powershell
cd C:\whatsapp-mcp\whatsapp-bridge

# Install cross-compilation toolchain if needed
# This requires GCC for Linux - we'll build directly on VM instead

# Alternative: Transfer source and build on VM
gcloud compute scp --recurse C:\whatsapp-mcp\whatsapp-bridge martha-mcp:/tmp/ --zone=us-central1-a
```

### Step 4.2: Build Bridge on VM

**On VM**:

```bash
cd /tmp/whatsapp-bridge
go build -o whatsapp-bridge main.go

# Move to installation directory
sudo mkdir -p /opt/whatsapp-bridge/store
sudo mv whatsapp-bridge /opt/whatsapp-bridge/
sudo chmod +x /opt/whatsapp-bridge/whatsapp-bridge
```

### Step 4.3: Create systemd Service for Bridge

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
```

### Step 4.4: Start Bridge and Authenticate WhatsApp

```bash
# Start bridge
sudo systemctl start whatsapp-bridge

# Watch logs for QR code
sudo journalctl -u whatsapp-bridge -f
```

**ACTION REQUIRED**: You'll see a QR code in the logs. Scan it with your phone:
1. Open WhatsApp on your phone
2. Go to Settings > Linked Devices
3. Tap "Link a Device"
4. Scan the QR code shown in the terminal

Once you see "Connected" in the logs, press Ctrl+C to stop watching logs.

**Checkpoint**: Verify bridge is running:
```bash
curl http://localhost:8080/api
# Should return JSON with bridge status
```

---

## Phase 5: WhatsApp MCP Server Setup (Week 2)

### Step 5.1: Transfer MCP Server Code

**On Windows**:

```powershell
gcloud compute scp --recurse C:\whatsapp-mcp\whatsapp-mcp-server martha-mcp:/tmp/ --zone=us-central1-a
```

**On VM**:

```bash
sudo mkdir -p /opt/whatsapp-mcp
sudo mv /tmp/whatsapp-mcp-server/* /opt/whatsapp-mcp/
cd /opt/whatsapp-mcp

# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
deactivate
```

### Step 5.2: Modify main.py for HTTP Transport

**On VM**, create modified main.py:

```bash
sudo tee /opt/whatsapp-mcp/main.py <<'EOF'
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from whatsapp import (
    search_contacts as whatsapp_search_contacts,
    list_messages as whatsapp_list_messages,
    list_chats as whatsapp_list_chats,
    get_chat as whatsapp_get_chat,
    get_direct_chat_by_contact as whatsapp_get_direct_chat_by_contact,
    get_contact_chats as whatsapp_get_contact_chats,
    get_last_interaction as whatsapp_get_last_interaction,
    get_message_context as whatsapp_get_message_context,
    send_message as whatsapp_send_message,
    send_file as whatsapp_send_file,
    send_audio_message as whatsapp_audio_voice_message,
    download_media as whatsapp_download_media
)

# Initialize FastMCP server
mcp = FastMCP("whatsapp")

# [All @mcp.tool() functions remain the same - copy from original]

@mcp.tool()
def search_contacts(query: str) -> List[Dict[str, Any]]:
    contacts = whatsapp_search_contacts(query)
    return contacts

@mcp.tool()
def list_messages(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sender_phone_number: Optional[str] = None,
    chat_jid: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_context: bool = True,
    context_before: int = 1,
    context_after: int = 1
) -> List[Dict[str, Any]]:
    messages = whatsapp_list_messages(
        after=after, before=before, sender_phone_number=sender_phone_number,
        chat_jid=chat_jid, query=query, limit=limit, page=page,
        include_context=include_context, context_before=context_before,
        context_after=context_after
    )
    return messages

@mcp.tool()
def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
    sort_by: str = "last_active"
) -> List[Dict[str, Any]]:
    chats = whatsapp_list_chats(
        query=query, limit=limit, page=page,
        include_last_message=include_last_message, sort_by=sort_by
    )
    return chats

@mcp.tool()
def get_chat(chat_jid: str, include_last_message: bool = True) -> Dict[str, Any]:
    chat = whatsapp_get_chat(chat_jid, include_last_message)
    return chat

@mcp.tool()
def get_direct_chat_by_contact(sender_phone_number: str) -> Dict[str, Any]:
    chat = whatsapp_get_direct_chat_by_contact(sender_phone_number)
    return chat

@mcp.tool()
def get_contact_chats(jid: str, limit: int = 20, page: int = 0) -> List[Dict[str, Any]]:
    chats = whatsapp_get_contact_chats(jid, limit, page)
    return chats

@mcp.tool()
def get_last_interaction(jid: str) -> str:
    message = whatsapp_get_last_interaction(jid)
    return message

@mcp.tool()
def get_message_context(
    message_id: str,
    before: int = 5,
    after: int = 5
) -> Dict[str, Any]:
    context = whatsapp_get_message_context(message_id, before, after)
    return context

@mcp.tool()
def send_message(recipient: str, message: str) -> Dict[str, Any]:
    if not recipient:
        return {"success": False, "message": "Recipient must be provided"}
    success, status_message = whatsapp_send_message(recipient, message)
    return {"success": success, "message": status_message}

@mcp.tool()
def send_file(recipient: str, media_path: str) -> Dict[str, Any]:
    success, status_message = whatsapp_send_file(recipient, media_path)
    return {"success": success, "message": status_message}

@mcp.tool()
def send_audio_message(recipient: str, media_path: str) -> Dict[str, Any]:
    success, status_message = whatsapp_audio_voice_message(recipient, media_path)
    return {"success": success, "message": status_message}

@mcp.tool()
def download_media(message_id: str, chat_jid: str) -> Dict[str, Any]:
    file_path = whatsapp_download_media(message_id, chat_jid)
    if file_path:
        return {"success": True, "message": "Media downloaded successfully", "file_path": file_path}
    else:
        return {"success": False, "message": "Failed to download media"}

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="stdio", choices=["stdio", "http"])
    parser.add_argument("--port", type=int, default=8081)
    args = parser.parse_args()

    if args.transport == "http":
        # HTTP transport for cloud deployment
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        import uvicorn

        sse = SseServerTransport("/messages")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await mcp.run(
                    streams[0], streams[1], mcp.create_initialization_options()
                )

        async def handle_messages(request):
            return await sse.handle_post_message(request.scope, request.receive, request._send)

        app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Route("/messages", endpoint=handle_messages, methods=["POST"]),
            ]
        )

        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        # Default stdio transport
        mcp.run(transport='stdio')
EOF
```

### Step 5.3: Install Additional Dependencies

```bash
cd /opt/whatsapp-mcp
source .venv/bin/activate
pip install uvicorn starlette
deactivate
```

### Step 5.4: Create systemd Service for WhatsApp MCP

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

**Checkpoint**: Verify WhatsApp MCP is running:
```bash
sudo systemctl status whatsapp-mcp
curl http://localhost:8081/sse
# Should return SSE connection or error (expected without proper client)
```

---

## Phase 6: Whisper MCP Server Setup (Week 2)

### Step 6.1: Mount Cloud Storage for Audio Files

```bash
# Create mount point
sudo mkdir -p /mnt/audio

# Mount Cloud Storage bucket
sudo gcsfuse martha-audio-files /mnt/audio

# Add to fstab for auto-mount on reboot
echo "martha-audio-files /mnt/audio gcsfuse rw,allow_other,file_mode=777,dir_mode=777,_netdev" | sudo tee -a /etc/fstab
```

### Step 6.2: Sync Audio Files to Cloud Storage

**On Windows**, run once to populate bucket:

```powershell
gsutil -m rsync -r "C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio" gs://martha-audio-files/
```

**Checkpoint**: Verify files visible on VM:
```bash
ls -lh /mnt/audio | head -20
```

### Step 6.3: Transfer Whisper MCP Code

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

### Step 6.4: Modify Whisper MCP for HTTP Transport

```bash
sudo tee /opt/whisper-mcp/src/mcp_server_whisper/server.py <<'EOF'
"""Whisper MCP server - Minimal server setup with tool registration."""

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("whisper", dependencies=["openai", "pydub", "aiofiles"])


def main() -> None:
    """Run main entrypoint."""
    from .tools import register_all_tools
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--transport", default="stdio", choices=["stdio", "http"])
    parser.add_argument("--port", type=int, default=8082)
    args = parser.parse_args()

    register_all_tools(mcp)

    if args.transport == "http":
        # HTTP transport for cloud deployment
        from mcp.server.sse import SseServerTransport
        from starlette.applications import Starlette
        from starlette.routing import Route
        import uvicorn

        sse = SseServerTransport("/messages")

        async def handle_sse(request):
            async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
                await mcp.run(
                    streams[0], streams[1], mcp.create_initialization_options()
                )

        async def handle_messages(request):
            return await sse.handle_post_message(request.scope, request.receive, request._send)

        app = Starlette(
            routes=[
                Route("/sse", endpoint=handle_sse),
                Route("/messages", endpoint=handle_messages, methods=["POST"]),
            ]
        )

        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
EOF
```

### Step 6.5: Retrieve OpenAI API Key

```bash
gcloud secrets versions access latest --secret=openai-api-key | sudo tee /opt/whisper-mcp/.env.secret
sudo chmod 600 /opt/whisper-mcp/.env.secret
```

### Step 6.6: Create systemd Service for Whisper MCP

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

# Update .env.secret to proper format
echo "OPENAI_API_KEY=$(cat /opt/whisper-mcp/.env.secret)" | sudo tee /opt/whisper-mcp/.env.secret

sudo systemctl daemon-reload
sudo systemctl enable whisper-mcp.service
sudo systemctl start whisper-mcp.service
```

**Checkpoint**: Verify Whisper MCP is running:
```bash
sudo systemctl status whisper-mcp
curl http://localhost:8082/sse
```

---

## Phase 7: Nginx Reverse Proxy & SSL (Week 3)

### Step 7.1: Get Static IP and API Key

```bash
STATIC_IP=$(gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format='get(address)')
API_KEY=$(gcloud secrets versions access latest --secret=mcp-api-key)

echo "Static IP: $STATIC_IP"
echo "API Key: $API_KEY"

# Save for later use
echo $API_KEY | sudo tee /etc/nginx/mcp-api-key
sudo chmod 600 /etc/nginx/mcp-api-key
```

### Step 7.2: Configure Nginx

```bash
sudo tee /etc/nginx/sites-available/martha-mcp <<'EOF'
# Rate limiting
limit_req_zone $binary_remote_addr zone=mcp_limit:10m rate=10r/s;

upstream whatsapp_mcp {
    server localhost:8081;
}

upstream whisper_mcp {
    server localhost:8082;
}

server {
    listen 80;
    server_name _;

    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name _;

    # SSL certificates (will be configured by certbot or self-signed)
    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    # API key authentication
    set $api_key "";
    if ($http_authorization ~* "Bearer (.+)") {
        set $api_key $1;
    }

    # Load expected API key from file
    set_by_lua_block $expected_key {
        local f = io.open("/etc/nginx/mcp-api-key", "r")
        local key = f:read("*all")
        f:close()
        return key:gsub("%s+", "")
    }

    # Reject unauthorized requests (except health check)
    location / {
        if ($uri !~* "^/health$") {
            set $auth_check "${api_key}:${expected_key}";
            if ($auth_check !~* "^(.+):\1$") {
                return 401;
            }
        }
        try_files $uri @proxy;
    }

    location @proxy {
        return 404;
    }

    location /whatsapp/ {
        limit_req zone=mcp_limit burst=20;

        if ($uri !~* "^/health$") {
            set $auth_check "${api_key}:${expected_key}";
            if ($auth_check !~* "^(.+):\1$") {
                return 401;
            }
        }

        proxy_pass http://whatsapp_mcp/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 300s;
        proxy_connect_timeout 10s;
    }

    location /whisper/ {
        limit_req zone=mcp_limit burst=5;

        if ($uri !~* "^/health$") {
            set $auth_check "${api_key}:${expected_key}";
            if ($auth_check !~* "^(.+):\1$") {
                return 401;
            }
        }

        proxy_pass http://whisper_mcp/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        proxy_read_timeout 600s;
        proxy_connect_timeout 10s;
    }

    location /health {
        access_log off;
        return 200 "OK\n";
        add_header Content-Type text/plain;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/martha-mcp /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t
```

**Note**: The Lua-based auth may require nginx-extras. Alternative simpler approach:

```bash
# Simpler version without Lua (manual API key replacement)
API_KEY=$(cat /etc/nginx/mcp-api-key)

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

    location / {
        return 301 https://\$host\$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name _;

    ssl_certificate /etc/ssl/certs/nginx-selfsigned.crt;
    ssl_certificate_key /etc/ssl/private/nginx-selfsigned.key;

    # Simple bearer token check
    map \$http_authorization \$auth_ok {
        default 0;
        "Bearer $API_KEY" 1;
    }

    location /whatsapp/ {
        if (\$auth_ok = 0) {
            return 401;
        }

        limit_req zone=mcp_limit burst=20;

        proxy_pass http://whatsapp_mcp/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_read_timeout 300s;
    }

    location /whisper/ {
        if (\$auth_ok = 0) {
            return 401;
        }

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
```

### Step 7.3: Generate Self-Signed SSL Certificate

```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/nginx-selfsigned.key \
  -out /etc/ssl/certs/nginx-selfsigned.crt \
  -subj "/CN=$(gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format='get(address)')"

sudo chmod 600 /etc/ssl/private/nginx-selfsigned.key
```

### Step 7.4: Start Nginx

```bash
sudo systemctl reload nginx
sudo systemctl status nginx
```

**Checkpoint**: Test from VM:
```bash
curl -k https://localhost/health
# Should return: OK

# Test with authentication
API_KEY=$(cat /etc/nginx/mcp-api-key)
curl -k -H "Authorization: Bearer $API_KEY" https://localhost/whatsapp/sse
```

---

## Phase 8: External Testing & Claude Mobile Configuration

### Step 8.1: Get Connection Details

**On VM**:

```bash
STATIC_IP=$(gcloud compute addresses describe martha-mcp-ip --region=us-central1 --format='get(address)')
API_KEY=$(gcloud secrets versions access latest --secret=mcp-api-key)

echo "=== Claude Mobile MCP Configuration ==="
echo ""
echo "MCP Server URL: https://$STATIC_IP"
echo "API Key: $API_KEY"
echo ""
echo "Save these for Claude mobile app configuration"
```

### Step 8.2: Test from Windows

**On Windows PowerShell**:

```powershell
# Get IP and key from VM output above
$IP = "YOUR_STATIC_IP"
$KEY = "YOUR_API_KEY"

# Test health endpoint (no auth required)
Invoke-WebRequest -Uri "https://$IP/health" -SkipCertificateCheck

# Test WhatsApp endpoint with auth
$headers = @{
    "Authorization" = "Bearer $KEY"
}
Invoke-WebRequest -Uri "https://$IP/whatsapp/sse" -Headers $headers -SkipCertificateCheck
```

### Step 8.3: Configure Claude Mobile

**In Claude mobile app** (Settings > MCP Servers):

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

---

## Phase 9: Monitoring & Backups (Week 3)

### Step 9.1: Automated Database Backups

```bash
sudo tee /usr/local/bin/backup-whatsapp-db.sh <<'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /opt/whatsapp-bridge/store/whatsapp.db /tmp/whatsapp_$DATE.db
cp /opt/whatsapp-bridge/store/messages.db /tmp/messages_$DATE.db
gsutil cp /tmp/whatsapp_$DATE.db gs://whatsapp-mcp-backups/
gsutil cp /tmp/messages_$DATE.db gs://whatsapp-mcp-backups/
rm /tmp/whatsapp_$DATE.db /tmp/messages_$DATE.db

# Delete backups older than 30 days
gsutil ls gs://whatsapp-mcp-backups/ | grep -E "whatsapp_[0-9]{8}_" | sort | head -n -240 | xargs -r gsutil rm
EOF

sudo chmod +x /usr/local/bin/backup-whatsapp-db.sh

# Test backup
sudo /usr/local/bin/backup-whatsapp-db.sh

# Schedule every 6 hours
(sudo crontab -l 2>/dev/null; echo "0 */6 * * * /usr/local/bin/backup-whatsapp-db.sh") | sudo crontab -
```

### Step 9.2: Service Health Monitoring

```bash
sudo tee /usr/local/bin/check-services.sh <<'EOF'
#!/bin/bash
services=("whatsapp-bridge" "whatsapp-mcp" "whisper-mcp" "nginx")
for service in "${services[@]}"; do
  if ! systemctl is-active --quiet $service; then
    echo "$(date): ALERT - $service is down! Restarting..." | logger -t service-monitor
    systemctl restart $service
    echo "$(date): $service restarted" | logger -t service-monitor
  fi
done
EOF

sudo chmod +x /usr/local/bin/check-services.sh

# Test
sudo /usr/local/bin/check-services.sh

# Run every 5 minutes
(sudo crontab -l 2>/dev/null; echo "*/5 * * * * /usr/local/bin/check-services.sh") | sudo crontab -
```

### Step 9.3: Disk Space Monitoring

```bash
sudo tee /usr/local/bin/check-disk-space.sh <<'EOF'
#!/bin/bash
THRESHOLD=80
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')

if [ $USAGE -gt $THRESHOLD ]; then
    echo "$(date): ALERT - Disk usage at ${USAGE}%!" | logger -t disk-monitor

    # Clean up old logs
    find /var/log -name "*.log" -mtime +7 -exec truncate -s 0 {} \;

    # Clean up old audio cache if exists
    find /tmp -name "*.ogg" -mtime +1 -delete
    find /tmp -name "*.mp3" -mtime +1 -delete
fi
EOF

sudo chmod +x /usr/local/bin/check-disk-space.sh

# Run daily
(sudo crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/check-disk-space.sh") | sudo crontab -
```

---

## Phase 10: Audio Sync Automation (Week 3)

### Step 10.1: Create Sync Script on Windows

Create `C:\Scripts\sync-audio-to-cloud.ps1`:

```powershell
# Sync local audio to cloud
Write-Host "Syncing audio files to Cloud Storage..."
gsutil -m rsync -r "C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio" gs://martha-audio-files/

# Sync cloud audio back to local (for TTS-generated files)
Write-Host "Syncing cloud files back to local..."
gsutil -m rsync -r gs://martha-audio-files/ "C:\Users\10064957\My Drive\GDVault\MarthaVault\media\audio"

Write-Host "Sync complete: $(Get-Date)"
```

### Step 10.2: Schedule Hourly Sync

```powershell
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-ExecutionPolicy Bypass -File 'C:\Scripts\sync-audio-to-cloud.ps1'"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 1) -RepetitionDuration (New-TimeSpan -Days 365)
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType S4U -RunLevel Highest
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "SyncAudioToCloud" -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force
```

---

## Testing & Verification

### Test WhatsApp MCP from Mobile

Once configured in Claude mobile app, try:

1. **List chats**: "Show me my recent WhatsApp conversations"
2. **Send message**: "Send a test message to [contact name]"
3. **Search messages**: "Find WhatsApp messages from [name] about [topic]"

**Expected**: <2s response time, accurate results

### Test Whisper MCP from Mobile

1. **List audio**: "List audio files in my vault"
2. **Transcribe**: "Transcribe the latest audio file"
3. **Create TTS**: "Create an audio message saying 'Hello world'"

**Expected**:
- List/transcribe: <5s response
- TTS: <10s response

### Monitor Performance

**On VM**:

```bash
# Watch service resource usage
htop

# Watch logs in real-time
sudo journalctl -f -u whatsapp-mcp -u whisper-mcp -u whatsapp-bridge

# Check nginx access logs
sudo tail -f /var/log/nginx/access.log
```

---

## Troubleshooting Common Issues

### WhatsApp Session Lost

**Symptoms**: "Not connected" errors

**Solution**:
```bash
sudo systemctl stop whatsapp-mcp whatsapp-bridge
sudo rm /opt/whatsapp-bridge/store/whatsapp.db
sudo systemctl start whatsapp-bridge
sudo journalctl -u whatsapp-bridge -f
# Scan QR code, then:
sudo systemctl start whatsapp-mcp
```

### Service Not Responding

```bash
# Check all services
sudo systemctl status whatsapp-bridge whatsapp-mcp whisper-mcp nginx

# Restart all
sudo systemctl restart whatsapp-bridge whatsapp-mcp whisper-mcp nginx

# Check logs
sudo journalctl -u whatsapp-bridge -n 100
sudo journalctl -u whatsapp-mcp -n 100
sudo journalctl -u whisper-mcp -n 100
```

### SSL Certificate Warnings

**Expected**: Self-signed certificates will show warnings in browsers. This is normal.

**Solution for production**: Use Let's Encrypt (requires domain name):
```bash
sudo certbot --nginx -d yourdomain.com
```

### Disk Space Full

```bash
# Check usage
df -h

# Find large files
du -sh /opt/* /var/* 2>/dev/null | sort -h | tail -20

# Clean up
sudo journalctl --vacuum-time=7d
gsutil ls gs://whatsapp-mcp-backups/ | head -n -20 | xargs gsutil rm
```

---

## Cost Monitoring

### Check Current Usage

```bash
# View current month's usage
gcloud billing projects describe martha-mcp

# Set up budget alerts (one-time)
gcloud billing budgets create \
  --billing-account=$(gcloud billing projects describe martha-mcp --format="value(billingAccountName)") \
  --display-name="MCP Monthly Budget" \
  --budget-amount=10 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90
```

### Expected Monthly Costs

- **Compute Engine e2-micro**: $0 (within free tier)
- **Disk 30GB**: $0 (within free tier)
- **Network egress**: $0-2 (depends on usage, monitor)
- **Cloud Storage**: $0 (within 5GB free tier)

**Total**: $0-2/month (well within $10 budget)

---

## Success Criteria Checklist

- [ ] WhatsApp MCP accessible from Claude mobile via HTTPS
- [ ] Whisper MCP accessible from Claude mobile via HTTPS
- [ ] Response time <2s for WhatsApp operations
- [ ] Response time <5s for Whisper operations
- [ ] WhatsApp session persists across VM restarts
- [ ] Monthly cost ≤ $10 (target: $0-2)
- [ ] Automated backups running every 6 hours
- [ ] Service health monitoring active
- [ ] Audio sync working bidirectionally
- [ ] All tools working from mobile app

---

## Next Steps

1. **Week 1**: Complete Phases 1-2 (GCP setup, VM provisioning)
2. **Week 2**: Complete Phases 3-6 (software installation, service migration)
3. **Week 3**: Complete Phases 7-10 (nginx setup, testing, monitoring)

**Start here**: Install gcloud CLI on Windows, then proceed with Phase 1.1
