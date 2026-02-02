# Phase 3: Manual Installation Steps

**VM Details**:
- Name: martha-mcp
- IP: 35.192.143.229
- Zone: us-central1-a

---

## Step 1: Transfer Installation Script

Open PowerShell and run:

```powershell
$env:CLOUDSDK_PYTHON = "C:\Python312\python.exe"
cd C:\Scripts

# Transfer script to VM
gcloud compute scp vm-phase3-install.sh martha-mcp:~/ --zone=us-central1-a
```

---

## Step 2: SSH into VM

```powershell
gcloud compute ssh martha-mcp --zone=us-central1-a
```

This will open an SSH session to your VM.

---

## Step 3: Run Installation Script

**On the VM**, run:

```bash
chmod +x vm-phase3-install.sh
./vm-phase3-install.sh
```

This will:
- Update system packages
- Install Python, Go, SQLite, ffmpeg, nginx, certbot, git
- Install gcsfuse for Cloud Storage mounting
- Verify all installations

**Expected time**: 10-15 minutes

---

## Step 4: Build WhatsApp Bridge

**Still on the VM**, run these commands:

```bash
# Create directories
sudo mkdir -p /opt/whatsapp-bridge/store

# Exit SSH to transfer bridge source
exit
```

**Back on Windows**, transfer the bridge source:

```powershell
gcloud compute scp --recurse C:\whatsapp-mcp\whatsapp-bridge martha-mcp:/tmp/ --zone=us-central1-a
```

**SSH back into VM**:

```powershell
gcloud compute ssh martha-mcp --zone=us-central1-a
```

**On the VM**, build the bridge:

```bash
cd /tmp/whatsapp-bridge
go build -o whatsapp-bridge main.go

# Move to installation directory
sudo mv whatsapp-bridge /opt/whatsapp-bridge/
sudo chmod +x /opt/whatsapp-bridge/whatsapp-bridge
```

---

## Step 5: Create systemd Service for Bridge

**On the VM**:

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

---

## Step 6: Authenticate WhatsApp

**Monitor logs for QR code**:

```bash
sudo journalctl -u whatsapp-bridge -f
```

**You'll see a QR code** displayed as ASCII art in the terminal.

**To authenticate**:
1. Open WhatsApp on your phone
2. Go to Settings > Linked Devices
3. Tap "Link a Device"
4. Scan the QR code shown in the terminal

Once you see **"Connected"** in the logs, press **Ctrl+C** to stop watching logs.

---

## Step 7: Verify Bridge is Running

```bash
curl http://localhost:8080/api
```

Should return JSON with bridge status.

---

## 🎯 Status Check

After completing these steps, you should have:
- ✅ All system packages installed
- ✅ WhatsApp bridge built and running
- ✅ WhatsApp session authenticated
- ✅ Bridge API responding on localhost:8080

---

## ⏭️ Next Steps

Once Phase 3 is complete, we'll proceed with:
- **Phase 4**: WhatsApp MCP server setup
- **Phase 5**: Whisper MCP server setup
- **Phase 6**: Nginx reverse proxy configuration
- **Phase 7**: Testing and mobile configuration

Type **"phase3 done"** when you've completed these steps and I'll guide you through the remaining phases.

---

## 🆘 Troubleshooting

### If Go build fails
```bash
# Install Go from official source
cd /tmp
wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
go version
```

### If bridge won't start
```bash
# Check logs
sudo journalctl -u whatsapp-bridge -n 50

# Check if port 8080 is in use
sudo lsof -i :8080
```

### If SSH connection times out
```bash
# Check firewall rules allow SSH (should be enabled by default)
gcloud compute firewall-rules list --filter="name:default-allow-ssh"
```
