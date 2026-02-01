# WhatsApp & Whisper MCP Cloud Migration

**Project Status**: Implementation plan ready
**Timeline**: 3 weeks (20-30 hours)
**Cost**: $0/month (within GCP free tier)
**Target**: Google Cloud Platform e2-micro VM

---

## 📁 Project Structure

```
Cloud_Migration/
├── README.md                          # This file - project overview
├── QUICKSTART.md                      # Quick start guide (start here!)
├── Implementation_Guide.md            # Detailed step-by-step guide
└── modified_files/
    ├── whatsapp_mcp_main.py          # Modified WhatsApp MCP server
    └── whisper_mcp_server.py         # Modified Whisper MCP server
```

---

## 🎯 What This Project Does

Migrates your WhatsApp and Whisper MCP servers from local Windows desktop to Google Cloud Platform, enabling:

- **24/7 availability** - No dependency on desktop being powered on
- **Mobile access** - Use MCP tools from Claude mobile app anywhere
- **Fast response** - <2s for WhatsApp, <5s for Whisper operations
- **Zero cost** - Runs entirely within GCP always-free tier
- **Session persistence** - WhatsApp stays connected across restarts
- **Automated backups** - Database backups every 6 hours to Cloud Storage

---

## 🚀 Quick Start

### 1. Prerequisites

- Google Cloud Platform account
- `gcloud` CLI installed on Windows
- OpenAI API key (for Whisper)
- WhatsApp session currently working

### 2. Get Started

1. **Read** `QUICKSTART.md` for condensed step-by-step guide
2. **Refer to** `Implementation_Guide.md` for detailed explanations
3. **Use** modified server files from `modified_files/` directory

### 3. Estimated Timeline

- **Week 1**: GCP setup, VM provisioning (5-8 hours)
- **Week 2**: Software installation, service migration (10-15 hours)
- **Week 3**: Testing, monitoring, cutover (5-8 hours)

---

## 🏗️ Architecture Overview

```
Claude Mobile App
    ↓ HTTPS (with Bearer token auth)
Nginx Reverse Proxy (VM)
    ├─ /whatsapp/* → WhatsApp MCP Server (port 8081)
    │   ↓ HTTP
    │   WhatsApp Bridge (Go) (port 8080)
    │   ↓ WebSocket
    │   WhatsApp Web API
    │
    └─ /whisper/* → Whisper MCP Server (port 8082)
        ↓ OpenAI API
        Audio Files (Cloud Storage bucket mounted via gcsfuse)
```

**Key Components:**

1. **e2-micro VM** (1GB RAM, 2 vCPU, 30GB disk) - Always-free tier
2. **WhatsApp Bridge** - Go binary connecting to WhatsApp Web
3. **WhatsApp MCP** - Python FastMCP server with SSE transport
4. **Whisper MCP** - Python FastMCP server with audio processing
5. **Nginx** - Reverse proxy with SSL and API key authentication
6. **Cloud Storage** - Audio files + WhatsApp database backups

---

## 📋 Implementation Phases

### Phase 1: GCP Setup
- Create project and enable APIs
- Create Cloud Storage buckets
- Store secrets (OpenAI key, MCP API key)
- Create VM instance
- Reserve static IP
- Configure firewall

### Phase 2: VM Software
- Install system dependencies
- Install gcsfuse for Cloud Storage mounting
- Verify installations

### Phase 3: WhatsApp Bridge
- Transfer and build Go binary
- Create systemd service
- Authenticate WhatsApp session (scan QR code)
- Verify bridge connectivity

### Phase 4: WhatsApp MCP
- Transfer code
- Apply HTTP transport modification
- Install Python dependencies
- Create systemd service
- Test local connectivity

### Phase 5: Whisper MCP
- Sync audio files to Cloud Storage
- Mount bucket on VM
- Transfer code
- Apply HTTP transport modification
- Configure OpenAI API key
- Create systemd service
- Test local connectivity

### Phase 6: Nginx Reverse Proxy
- Generate SSL certificate
- Configure nginx with authentication
- Set up rate limiting
- Test external access

### Phase 7: Testing & Configuration
- Test from Windows
- Configure Claude mobile app
- Verify all tools working
- Monitor performance

### Phase 8: Monitoring & Backups
- Set up automated database backups
- Configure service health monitoring
- Set up disk space monitoring
- Configure audio sync automation

---

## 🔧 Key Technical Modifications

### WhatsApp MCP Server
**Original**: stdio transport only (local use)
**Modified**: Supports both stdio and HTTP/SSE transport

**Changes**:
- Added argparse for `--transport` and `--port` flags
- Added SSE transport using Starlette/uvicorn
- Maintained all existing tool functionality
- Added startup logging

**File**: `modified_files/whatsapp_mcp_main.py`

### Whisper MCP Server
**Original**: stdio transport only (local use)
**Modified**: Supports both stdio and HTTP/SSE transport

**Changes**:
- Added argparse for `--transport` and `--port` flags
- Added SSE transport using Starlette/uvicorn
- Maintained all existing tool functionality
- Added startup logging

**File**: `modified_files/whisper_mcp_server.py`

### Transport Protocol
**SSE (Server-Sent Events)** chosen over WebSocket for:
- Better compatibility with mobile clients
- Simpler nginx configuration
- Native HTTP/2 support
- Easier debugging and monitoring

---

## 💰 Cost Breakdown

### Within Always-Free Tier (✅ $0/month)
- e2-micro VM: 1 instance in us-central1 (720 hours/month)
- 30GB Standard Persistent Disk
- 1GB network egress per month (monitor usage)
- 5GB Cloud Storage standard class
- Secret Manager: 6 active secret versions

### Potential Costs (⚠️ Monitor)
- **Network egress** beyond 1GB: $0.12/GB
- **Cloud Storage** beyond 5GB: $0.020/GB/month nearline

### Budget Alert Configured
- Alert at 50%, 90%, and 100% of $10/month budget
- Expected actual cost: $0-2/month

---

## 🔐 Security Features

1. **API Key Authentication** - All endpoints require Bearer token
2. **SSL/TLS** - HTTPS only (self-signed certificate)
3. **Rate Limiting** - 10 requests/second with burst allowance
4. **Secret Manager** - API keys stored securely in GCP
5. **Firewall Rules** - Only HTTP/HTTPS traffic allowed
6. **Private Endpoints** - MCP servers only accessible via nginx proxy

---

## 🔍 Monitoring & Maintenance

### Automated Monitoring
- **Service health checks** - Every 5 minutes
- **Database backups** - Every 6 hours
- **Disk space monitoring** - Daily
- **Service logs** - Stored in systemd journal

### Manual Checks
- **Weekly**: Review service logs for errors
- **Monthly**: Check Cloud Storage costs and cleanup old backups
- **As needed**: Re-authenticate WhatsApp if session lost

### Key Commands

```bash
# SSH into VM
gcloud compute ssh martha-mcp --zone=us-central1-a

# Check service status
sudo systemctl status whatsapp-bridge whatsapp-mcp whisper-mcp nginx

# View logs
sudo journalctl -u whatsapp-mcp -f

# Restart services
sudo systemctl restart whatsapp-bridge whatsapp-mcp whisper-mcp nginx

# Re-authenticate WhatsApp
sudo systemctl stop whatsapp-mcp whatsapp-bridge
sudo rm /opt/whatsapp-bridge/store/whatsapp.db
sudo systemctl start whatsapp-bridge
sudo journalctl -u whatsapp-bridge -f
# Scan QR code
sudo systemctl start whatsapp-mcp
```

---

## ✅ Success Criteria

Migration is successful when:

- [ ] WhatsApp MCP accessible from Claude mobile via HTTPS
- [ ] Whisper MCP accessible from Claude mobile via HTTPS
- [ ] Response time <2s for WhatsApp operations
- [ ] Response time <5s for Whisper operations
- [ ] WhatsApp session persists across VM restarts
- [ ] Monthly cost ≤ $10 (target: $0-2)
- [ ] Automated backups running every 6 hours
- [ ] Service health monitoring active
- [ ] Audio files syncing bidirectionally
- [ ] All MCP tools working from mobile app

---

## 🐛 Troubleshooting

### WhatsApp Session Lost
**Symptom**: "Not connected" errors
**Solution**: Re-authenticate by scanning QR code (see commands above)

### Service Not Responding
**Symptom**: 502 Bad Gateway or timeout
**Solution**: Check logs, restart services
```bash
sudo systemctl restart whatsapp-bridge whatsapp-mcp whisper-mcp nginx
sudo journalctl -u whatsapp-mcp -n 100
```

### SSL Certificate Warning
**Expected**: Self-signed certificates show browser warnings (normal)
**For production**: Use Let's Encrypt with domain name
```bash
sudo certbot --nginx -d yourdomain.com
```

### Disk Space Full
**Solution**: Clean up logs and old backups
```bash
df -h
sudo journalctl --vacuum-time=7d
gsutil ls gs://whatsapp-mcp-backups/ | head -n -20 | xargs gsutil rm
```

### Audio Files Not Syncing
**Check**: Cloud Storage bucket mounted
```bash
ls /mnt/audio
sudo gcsfuse martha-audio-files /mnt/audio
```

---

## 📚 Additional Resources

### Documentation Files
- `QUICKSTART.md` - Condensed step-by-step guide
- `Implementation_Guide.md` - Detailed guide with explanations
- `modified_files/whatsapp_mcp_main.py` - Modified WhatsApp server
- `modified_files/whisper_mcp_server.py` - Modified Whisper server

### External Links
- [Google Cloud SDK Install](https://cloud.google.com/sdk/docs/install)
- [GCP Always Free Tier](https://cloud.google.com/free/docs/free-cloud-features)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [gcsfuse Documentation](https://github.com/GoogleCloudPlatform/gcsfuse)

### GCP Console Links
- Project: https://console.cloud.google.com/home/dashboard?project=martha-mcp
- VM Instances: https://console.cloud.google.com/compute/instances?project=martha-mcp
- Cloud Storage: https://console.cloud.google.com/storage/browser?project=martha-mcp
- Secret Manager: https://console.cloud.google.com/security/secret-manager?project=martha-mcp

---

## 🎯 Next Steps

1. **Install gcloud CLI** on Windows
2. **Open** `QUICKSTART.md`
3. **Follow** phases sequentially
4. **Test** thoroughly before relying on mobile access
5. **Document** any issues or deviations

**Estimated Start to Finish**: 3 weeks part-time, or 1 week full-time

---

## 📝 Notes

- Self-signed SSL certificates will show warnings in browsers (normal)
- WhatsApp session may occasionally require re-authentication
- First audio transcription may be slower due to cold start
- Network egress is metered - monitor usage via GCP console
- VM can be stopped when not needed to save network costs (will lose static IP)
- Always-free tier limits are per account, not per project

---

## 🤝 Support

For issues during implementation:
- Check `Implementation_Guide.md` troubleshooting section
- Review systemd service logs: `sudo journalctl -u <service-name>`
- Verify GCP quotas and free tier limits
- Test connectivity step by step (don't skip checkpoints)

**Remember**: Each phase has verification checkpoints - don't proceed until current phase works!

---

**Project Created**: 2026-02-01
**Last Updated**: 2026-02-01
**Status**: Ready for implementation
