# RoleRadar Secure Configuration - Quick Reference

## 🔐 Security Status

RoleRadar now uses **encrypted credential storage** by default.

## 🚀 Quick Start

### First Time Setup

```bash
# 1. Initialize secure configuration
python secure_config_manager.py init

# 2. You'll be prompted for:
#    - Master password (minimum 8 characters)
#    - Tavily API Key
#    - Groq API Key
#    - Database password (optional)
#    - Redis password (optional)

# 3. Start using RoleRadar
python scheduler.py
```

### Migrating from .env

```bash
# One command to migrate everything
python secure_config_manager.py migrate

# Verify migration
python secure_config_manager.py show
```

## 📋 Common Commands

| Command | Description |
|---------|-------------|
| `python secure_config_manager.py show` | View configuration (sensitive hidden) |
| `python secure_config_manager.py show --show-sensitive` | View with API keys visible |
| `python secure_config_manager.py set-key KEY_NAME` | Update any configuration value |
| `python secure_config_manager.py set-roles "role1, role2"` | Update search roles |
| `python secure_config_manager.py set-schedule "08:00, 12:00"` | Update schedule times |
| `python secure_config_manager.py change-password` | Change master password |
| `python secure_config_manager.py export backup.json` | Export config (safe) |
| `python secure_config_manager.py import backup.json` | Import config |

## 🔑 Managing API Keys

```bash
# Update Tavily API Key
python secure_config_manager.py set-key TAVILY_API_KEY

# Update Groq API Key
python secure_config_manager.py set-key GROQ_API_KEY

# Update Database Password
python secure_config_manager.py set-key DB_PASSWORD
```

## 🔍 Customizing Search

```bash
# Change what roles to search for
python secure_config_manager.py set-roles "security engineer, CISO, DevOps engineer"

# Change when searches run (24-hour format)
python secure_config_manager.py set-schedule "06:00, 10:00, 14:00, 18:00"

# View current settings
python secure_config_manager.py show
```

## 💾 Backup & Restore

```bash
# Export without sensitive data (safe to share)
python secure_config_manager.py export my-config.json

# Export with sensitive data (secure storage only!)
python secure_config_manager.py export full-backup.json --include-sensitive

# Import configuration
python secure_config_manager.py import my-config.json

# Manual backup of encrypted file
cp ~/.roleradar/config.enc ~/.roleradar/config.enc.backup
```

## 🛡️ Security Features

- ✅ **AES-256 Encryption** - Military-grade security
- ✅ **Master Password** - Single password protects everything
- ✅ **No Plaintext** - API keys never in plain text
- ✅ **Secure Permissions** - Files are owner-only (0600)
- ✅ **PBKDF2** - 390,000 iterations for key derivation

## 📍 File Locations

- **Encrypted Config:** `~/.roleradar/config.enc`
- **Legacy .env:** `/mnt/d/roleradar/.env` (fallback only)

## ⚠️ Important Notes

### DO
- ✅ Use secure configuration for all sensitive data
- ✅ Choose a strong master password (12+ characters)
- ✅ Back up your encrypted config regularly
- ✅ Use `export` without `--include-sensitive` for sharing

### DON'T
- ❌ Share your master password
- ❌ Commit `.env` files with real credentials
- ❌ Share exports with `--include-sensitive`
- ❌ Use weak passwords

## 🔧 Troubleshooting

### Can't unlock configuration
```bash
# Check if file exists
ls -l ~/.roleradar/config.enc

# Re-initialize if needed
python secure_config_manager.py init
```

### Forgot master password
```bash
# Unfortunately, encrypted data cannot be recovered
# You must re-initialize:
rm ~/.roleradar/config.enc
python secure_config_manager.py init
```

### App still using .env
```bash
# Verify secure config exists and works
python secure_config_manager.py show

# If it works, remove API keys from .env
# Keep only non-sensitive defaults in .env
```

## 📚 Full Documentation

- **Security Guide:** [SECURE_CONFIGURATION.md](SECURE_CONFIGURATION.md)
- **Configuration Options:** [CONFIGURATION.md](CONFIGURATION.md)
- **Implementation Details:** [SECURE_CONFIG_IMPLEMENTATION.md](SECURE_CONFIG_IMPLEMENTATION.md)

## 🆘 Getting Help

1. Read [SECURE_CONFIGURATION.md](SECURE_CONFIGURATION.md)
2. Check file permissions: `ls -l ~/.roleradar/`
3. Test unlock: `python secure_config_manager.py show`
4. Review logs for errors
5. Open an issue with details

## 📝 Example Workflow

```bash
# Day 1: Setup
python secure_config_manager.py init
# Enter credentials when prompted

# Day 2: Change a role
python secure_config_manager.py set-roles "privacy officer, data protection officer, CISO"

# Day 3: Add a schedule time
python secure_config_manager.py show  # Check current schedule
python secure_config_manager.py set-schedule "08:00, 12:00, 16:00, 20:00"

# Day 4: Rotate API key
python secure_config_manager.py set-key TAVILY_API_KEY
# Enter new key when prompted

# Day 5: Backup
python secure_config_manager.py export config-backup-2026-01-19.json
# Store in secure location

# Day 30: Change master password
python secure_config_manager.py change-password
```

---

**Quick Tips:**

- All credentials are entered securely (hidden input)
- Configuration persists across project updates
- No restart needed after changes
- Backwards compatible with .env files
- Configuration is stored at `~/.roleradar/config.enc` (outside project)

**Remember:** Your master password is the only way to decrypt your credentials. Keep it safe!
