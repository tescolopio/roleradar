# RoleRadar Production Deployment Guide

For deploying RoleRadar to a server that runs 24/7 for your organization.

## 📋 Pre-Deployment Requirements

### Server Requirements
- **CPU:** 2+ cores recommended
- **RAM:** 4+ GB recommended
- **Storage:** 50+ GB for database
- **Network:** Stable internet connection
- **OS:** Linux (Ubuntu 20.04+) or Windows Server recommended

### Software Requirements
- **Python:** 3.8 or higher
- **Database:** PostgreSQL 12+ (optional, falls back to SQLite)

### Access Requirements
- SSH access to server (for Linux)
- Remote Desktop access (for Windows Server)
- Administrator/root access

---

## 🚀 Deployment Steps

### Phase 1: Server Setup (30 minutes)

#### 1a. Update System
```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade -y

# Install Python if needed
sudo apt install -y python3 python3-pip python3-venv

# Verify Python version
python3 --version  # Should be 3.8+
```

#### 1b. Create Service User (Optional but Recommended)
```bash
# Create a dedicated user for RoleRadar
sudo useradd -m -s /bin/bash roleradar

# Switch to the user
sudo su - roleradar
```

#### 1c. Install RoleRadar
```bash
# Clone or download RoleRadar
cd /home/roleradar  # Or your preferred location
git clone https://github.com/tescolopio/roleradar.git
cd roleradar

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Phase 2: Configure Credentials (15 minutes)

#### 2a. Start Dashboard (First Time Only)
```bash
# Run the dashboard in the foreground
python roleradar.py dashboard
```

#### 2b. Open Admin Panel
- On the server machine, open: `http://localhost:5000`
- Click the ⚙️ button
- Go to **Credentials** tab

#### 2c. Enter API Keys
1. **Tavily API Key**
   - Go to https://tavily.com
   - Log in to your account
   - Find API key in settings
   - Paste in Credentials tab
   - Click Test ✓

2. **Groq API Key**
   - Go to https://console.groq.com
   - Log in to your account
   - Find API key in settings
   - Paste in Credentials tab
   - Click Test ✓

#### 2d. Configure Database (Optional)
If using PostgreSQL on the server:

1. Create a PostgreSQL user and database
2. In Credentials tab, enter:
   ```
   postgresql://username:password@localhost:5432/roleradar
   ```
3. Click Test ✓
4. Click Save

Otherwise, the system uses SQLite automatically (perfectly fine for most uses).

#### 2e. Save Credentials
- Click **Save Credentials**
- You'll see: "Credentials saved successfully"
- Close the dashboard (Ctrl+C in terminal)

---

### Phase 3: Configure Search Roles (10 minutes)

Start the dashboard again:
```bash
python roleradar.py dashboard
```

Configure your search roles:
1. Click ⚙️ Admin Panel
2. Click **Configuration** tab
3. Add all the roles you want to search for
   - Example: "CISO", "VP of Security", "Security Director"
4. Roles save automatically

Stop the dashboard when done (Ctrl+C).

---

### Phase 4: Set Up Automated Searches (10 minutes)

This makes the application run searches 24/7 without user intervention.

#### 4a. Configure Schedule
```bash
# Start dashboard
python roleradar.py dashboard
```

In the browser:
1. Click ⚙️ Admin Panel
2. Click **Schedule** tab
3. Set your preferred search times
   - Example: 6 AM, 12 PM, 6 PM, 11 PM
4. Enable "Automated Search" checkbox
5. Click **Save Schedule**
6. Close dashboard

#### 4b. Create System Service (Linux)

Create a service file:
```bash
sudo nano /etc/systemd/system/roleradar.service
```

Paste this content:
```ini
[Unit]
Description=RoleRadar Scheduler Service
After=network.target

[Service]
Type=simple
User=roleradar
WorkingDirectory=/home/roleradar/roleradar
ExecStart=/home/roleradar/roleradar/venv/bin/python scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable roleradar
sudo systemctl start roleradar

# Check status
sudo systemctl status roleradar
```

#### 4c. Create Windows Service (Windows Server)

Use NSSM (Non-Sucking Service Manager):

```powershell
# Download NSSM if not installed
# https://nssm.cc/download

# Install service
nssm install RoleRadar C:\path\to\roleradar\venv\Scripts\python.exe C:\path\to\roleradar\scheduler.py

# Start service
nssm start RoleRadar

# Check status
nssm status RoleRadar
```

---

### Phase 5: Expose Dashboard to Network (20 minutes)

To access from other computers on the network:

#### 5a. Configure Port (if not 5000)
```bash
# Set environment variable before starting
export FLASK_PORT=8000
python roleradar.py dashboard
```

#### 5b. For Local Network Access
1. Find server's IP address:
   ```bash
   # Linux
   hostname -I
   
   # Windows
   ipconfig
   ```
2. Access from other computers:
   ```
   http://[server-ip]:5000
   ```

#### 5c. For Remote Access (Internet)
For access from outside the network, set up a reverse proxy:

**Using Nginx:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Using Apache:**
```apache
ProxyPreserveHost On
ProxyPass / http://localhost:5000/
ProxyPassReverse / http://localhost:5000/
```

---

### Phase 6: Security Configuration (15 minutes)

#### 6a. Set Up Firewall (Linux)
```bash
# Allow only necessary ports
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

#### 6b. Create Master Password
On first credential entry, you'll be prompted for a master password:
- **Minimum 12 characters** for production
- Use mix of letters, numbers, symbols
- Store securely in password manager
- Don't share with users

#### 6c. Enable HTTPS
For remote access, always use HTTPS:

```bash
# Using Let's Encrypt (free)
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d your-domain.com
```

Update Nginx config to use SSL:
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://localhost:5000;
    }
}
```

---

## ✅ Verification Checklist

After deployment, verify everything works:

- [ ] Dashboard accessible at http://localhost:5000
- [ ] API keys configured and tested successfully
- [ ] Search roles configured
- [ ] Can run manual search from Admin Panel
- [ ] Schedule is set and enabled
- [ ] Automated searches run at scheduled times
- [ ] Results appear in dashboard
- [ ] Database is persisting data
- [ ] Service/scheduler starts automatically after reboot
- [ ] Dashboard accessible from other computers (if needed)

---

## 📊 Monitoring

### Check Service Status
```bash
# Linux
sudo systemctl status roleradar

# Windows
nssm status RoleRadar
```

### View Logs
```bash
# Linux
sudo journalctl -u roleradar -f

# Windows
# Open Event Viewer or
nssm reset RoleRadar 0
```

### Monitor Database
```bash
# Check database size
du -sh roleradar.db

# If using PostgreSQL, connect and run:
SELECT pg_database.datname, pg_size_pretty(pg_database_size(pg_database.datname))
FROM pg_database
WHERE datname = 'roleradar';
```

---

## 🔧 Maintenance

### Weekly
- Check logs for errors
- Verify recent searches completed
- Review dashboard data quality

### Monthly
- Back up database
- Check API key usage
- Review and optimize search roles

### Quarterly
- Update Python packages
- Review scoring weights
- Adjust search schedule if needed

### Backup Strategy
```bash
# Daily database backup (add to cron)
0 2 * * * cp /path/to/roleradar.db /backups/roleradar-$(date +\%Y\%m\%d).db

# Keep last 30 days
find /backups -name "roleradar-*.db" -mtime +30 -delete
```

---

## 🐛 Troubleshooting

### Service Won't Start
```bash
# Check Python path
which python3

# Test scheduler manually
python roleradar.py search
python roleradar.py process

# Verify credentials
python secure_config_manager.py show
```

### Searches Not Running
```bash
# Check if scheduler is running
ps aux | grep scheduler

# Check system logs
sudo journalctl -u roleradar -n 50

# Manually run search
python roleradar.py search
```

### Database Connection Error
```bash
# Check PostgreSQL running
sudo systemctl status postgresql

# Test connection
psql -U username -d roleradar -h localhost

# Or fall back to SQLite (remove DATABASE_URL from config)
```

### Dashboard Not Accessible
```bash
# Check port is open
sudo netstat -tlnp | grep 5000

# Check firewall
sudo ufw status

# Check Flask is running
ps aux | grep flask
```

---

## 🎯 Next Steps

1. **Monitor first week** - Watch logs, verify searches
2. **Adjust scoring weights** based on results
3. **Fine-tune search roles** as needed
4. **Set up backup** - Important for production!
5. **Document configuration** - For team handoff

---

## 📞 Support

For issues:
1. Check logs first
2. Verify all credentials are correct
3. Test API keys manually
4. Check internet connection
5. See [QUICK_START.md](QUICK_START.md) for more help

---

## 🔐 Security Best Practices

- ✅ Use strong master password (12+ characters)
- ✅ Store master password in secure password manager
- ✅ Use HTTPS for remote access
- ✅ Keep firewall enabled
- ✅ Regular backups of database
- ✅ Monitor logs for suspicious activity
- ✅ Don't share API keys or master password
- ✅ Update Python packages quarterly

---

**Deployment Complete!** 🎉

Your RoleRadar instance is now running 24/7 and searching for opportunities automatically.
