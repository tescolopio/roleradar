# RoleRadar Secure Configuration Guide

## Overview

RoleRadar now features **encrypted credential storage** to protect your API keys, database passwords, and other sensitive configuration data. All sensitive information is encrypted using AES-256 encryption with PBKDF2 key derivation, protected by a master password.

## Security Features

✅ **AES-256 Encryption** - Military-grade encryption for all credentials  
✅ **Master Password Protection** - Single password to unlock configuration  
✅ **PBKDF2 Key Derivation** - 390,000 iterations (OWASP recommended)  
✅ **Secure File Permissions** - Configuration files are owner-only (0600)  
✅ **No Plaintext Secrets** - API keys never stored in plain text  
✅ **Automatic Migration** - Easy migration from .env files  

## Quick Start

### 1. Initialize Secure Configuration

```bash
python secure_config_manager.py init
```

This will:
- Create a master password (minimum 8 characters)
- Generate an encrypted configuration file at `~/.roleradar/config.enc`
- Prompt you to enter your API keys securely
- Set up database credentials

### 2. Migrate from .env (Optional)

If you have existing configuration in a `.env` file:

```bash
python secure_config_manager.py migrate
```

This will:
- Read credentials from `.env`
- Encrypt and store them securely
- Prompt you to remove sensitive data from `.env`

### 3. Verify Configuration

```bash
python secure_config_manager.py show
```

View your configuration with sensitive values hidden:

```
🔐 Security Status: ENCRYPTED
📍 Storage: /home/user/.roleradar/config.enc

⚙️  Application Settings
──────────────────────────────────────────────────────────────────────
Timezone: America/New_York
Flask Host: 0.0.0.0:5000

🔍 Search Configuration
──────────────────────────────────────────────────────────────────────
Search Roles (8):
  1. security engineer
  2. compliance officer
  3. GRC analyst
  ...

🔑 API Keys & Credentials
──────────────────────────────────────────────────────────────────────
Tavily API Key: ✅ SET
Groq API Key: ✅ SET

💾 Database Configuration
──────────────────────────────────────────────────────────────────────
Host: localhost:5433
Database: roleradar
User: roleradar
Password: ✅ SET
```

## Managing Configuration

### View with Sensitive Data

```bash
python secure_config_manager.py show --show-sensitive
```

### Update API Keys

```bash
python secure_config_manager.py set-key TAVILY_API_KEY
# You'll be prompted to enter the value securely

python secure_config_manager.py set-key GROQ_API_KEY
```

### Update Database Password

```bash
python secure_config_manager.py set-key DB_PASSWORD
```

### Update Search Roles

```bash
python secure_config_manager.py set-roles "security engineer, CISO, GRC analyst, compliance officer"
```

### Update Schedule Times

```bash
python secure_config_manager.py set-schedule "08:00, 12:00, 16:00, 20:00"
```

### Change Master Password

```bash
python secure_config_manager.py change-password
```

## Configuration Commands Reference

| Command | Description |
|---------|-------------|
| `init` | Initialize new secure configuration |
| `migrate` | Migrate from .env to secure storage |
| `show` | Display current configuration (sensitive hidden) |
| `show --show-sensitive` | Display with sensitive values visible |
| `set-key <KEY>` | Set or update a configuration value |
| `set-roles <ROLES>` | Update search roles (comma-separated) |
| `set-schedule <TIMES>` | Update schedule times (comma-separated) |
| `change-password` | Change master password |
| `export <FILE>` | Export configuration to JSON (redacted) |
| `export <FILE> --include-sensitive` | Export with sensitive data |
| `import <FILE>` | Import configuration from JSON |

## Backup & Recovery

### Export Configuration (Safe for Version Control)

```bash
python secure_config_manager.py export config-backup.json
```

This exports with sensitive data redacted - safe to commit to version control.

### Export with Sensitive Data (For Backup)

```bash
python secure_config_manager.py export config-full-backup.json --include-sensitive
```

⚠️ **Store this backup securely** - it contains unencrypted credentials!

### Import Configuration

```bash
python secure_config_manager.py import config-backup.json
```

### Manual Backup

Simply copy the encrypted configuration file:

```bash
cp ~/.roleradar/config.enc ~/.roleradar/config.enc.backup
```

## Application Integration

### Automatic Mode

When you start RoleRadar, it automatically detects and uses secure configuration:

```bash
python roleradar.py
python scheduler.py
```

If secure configuration exists, you'll be prompted for your master password once per session.

### Configuration Priority

1. **Secure Storage** (if `~/.roleradar/config.enc` exists)
2. **Environment Variables** (.env file) - fallback only
3. **Default Values**

### Migration Notice

If API keys are detected in `.env` while secure storage is not initialized, you'll see:

```
⚠️  API keys detected in environment variables
For better security, run: python secure_config_manager.py init
This will migrate your credentials to encrypted storage.
```

## Security Best Practices

### ✅ DO

- Use secure configuration for all sensitive credentials
- Choose a strong master password (12+ characters recommended)
- Back up your encrypted configuration regularly
- Use `export` without `--include-sensitive` for version control
- Store full backups in a secure location (password manager, encrypted drive)

### ❌ DON'T

- Share your master password
- Commit `.env` files with real credentials to version control
- Export sensitive data to shared locations
- Use weak or default passwords
- Store plaintext credential exports in unsecured locations

## Configuration File Location

**Default Location:** `~/.roleradar/config.enc`

This location:
- Is outside your project directory
- Is protected by user-only file permissions (0600)
- Is persistent across project updates
- Can be backed up independently

**Custom Location:**

```python
from roleradar.secure_config import SecureConfigStore

store = SecureConfigStore(config_path="/custom/path/config.enc")
```

## Troubleshooting

### "Failed to unlock configuration"

- Ensure you're entering the correct master password
- Check file permissions: `ls -l ~/.roleradar/config.enc`
- Try re-initializing if the file is corrupted

### "No secure configuration found"

Run initialization:
```bash
python secure_config_manager.py init
```

### Application Not Using Secure Config

1. Verify config exists: `ls -l ~/.roleradar/config.enc`
2. Check it unlocks: `python secure_config_manager.py show`
3. Ensure no conflicting environment variables override settings

### Forgot Master Password

Unfortunately, encrypted data cannot be recovered without the master password. Options:

1. Restore from a backup (if available)
2. Re-initialize and re-enter credentials:
   ```bash
   rm ~/.roleradar/config.enc
   python secure_config_manager.py init
   ```

## Technical Details

### Encryption Specification

- **Algorithm:** AES-256 (via Fernet)
- **Key Derivation:** PBKDF2-HMAC-SHA256
- **Iterations:** 390,000 (OWASP 2023 recommendation)
- **Salt:** 32 bytes random (unique per save)
- **File Format:** `[32-byte salt][encrypted JSON]`

### File Permissions

Configuration files are automatically created with `0600` permissions (owner read/write only), preventing access by other users on the system.

### Password Requirements

- Minimum length: 8 characters
- Recommendations:
  - Use 12+ characters
  - Include uppercase, lowercase, numbers, symbols
  - Use a unique password not used elsewhere
  - Consider using a password manager

## Comparison: Secure vs .env

| Feature | Secure Storage | .env File |
|---------|---------------|-----------|
| Encryption | ✅ AES-256 | ❌ Plain text |
| Master Password | ✅ Yes | ❌ No |
| Safe for Git | ✅ Yes (when exported without sensitive) | ⚠️ Requires .gitignore |
| Multi-user Safe | ✅ Yes (0600 permissions) | ⚠️ Depends on file perms |
| Audit Trail | ✅ Possible | ❌ No |
| Credential Rotation | ✅ Easy | ⚠️ Manual edit |
| Compliance Ready | ✅ Yes | ❌ No |

## Examples

### Complete Setup Flow

```bash
# 1. Initialize secure configuration
python secure_config_manager.py init
# Enter master password when prompted
# Enter API keys when prompted

# 2. Set database password
python secure_config_manager.py set-key DB_PASSWORD

# 3. Customize search roles
python secure_config_manager.py set-roles "security engineer, CISO, privacy officer"

# 4. Set schedule
python secure_config_manager.py set-schedule "08:00, 14:00, 20:00"

# 5. Verify everything
python secure_config_manager.py show

# 6. Start RoleRadar
python scheduler.py
```

### Rotating API Keys

```bash
# Update Tavily API key
python secure_config_manager.py set-key TAVILY_API_KEY
# Enter new key when prompted

# Update Groq API key
python secure_config_manager.py set-key GROQ_API_KEY
# Enter new key when prompted

# Verify
python secure_config_manager.py show
```

### Team Setup (Without Sharing Credentials)

Each team member:

```bash
# 1. Get encrypted config template (no sensitive data)
python secure_config_manager.py init

# 2. Each team member sets their own API keys
python secure_config_manager.py set-key TAVILY_API_KEY
python secure_config_manager.py set-key GROQ_API_KEY

# 3. Import shared non-sensitive settings
python secure_config_manager.py import team-config.json
```

## Migration from Legacy Configuration

If you're upgrading from a version that used only `.env`:

1. **Backup your .env:**
   ```bash
   cp .env .env.backup
   ```

2. **Run migration:**
   ```bash
   python secure_config_manager.py migrate
   ```

3. **Verify migration:**
   ```bash
   python secure_config_manager.py show
   ```

4. **Clean .env (optional):**
   - Remove sensitive values from `.env`
   - Keep only non-sensitive defaults
   - Use `.env.example` as reference

5. **Update .gitignore:**
   ```bash
   echo ".env" >> .gitignore
   echo "*.backup" >> .gitignore
   ```

## Support

For issues or questions about secure configuration:

1. Check this guide thoroughly
2. Verify file permissions and paths
3. Test with `show` command first
4. Check application logs for errors
5. Report issues with details about your setup

---

**Next Steps:**
- Run `python secure_config_manager.py init` to get started
- See [CONFIGURATION.md](CONFIGURATION.md) for role and schedule customization
- See [README.md](README.md) for general usage instructions
