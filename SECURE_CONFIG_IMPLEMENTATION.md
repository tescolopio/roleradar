# RoleRadar Secure Configuration Implementation

## Summary

RoleRadar now features **encrypted credential storage** to securely manage API keys, database passwords, and other sensitive configuration data within the application itself.

## What Changed

### New Files

1. **[src/roleradar/secure_config.py](src/roleradar/secure_config.py)**
   - `SecureConfigStore` class for encrypted configuration management
   - AES-256 encryption with PBKDF2 key derivation (390k iterations)
   - Master password protection
   - Secure file permissions (0600)
   - JSON export/import with optional credential redaction

2. **[secure_config_manager.py](secure_config_manager.py)**
   - CLI tool for managing secure configuration
   - Commands: init, migrate, show, set-key, set-roles, set-schedule, change-password
   - Interactive credential prompts (hidden input for passwords)
   - Configuration backup and restore

3. **[SECURE_CONFIGURATION.md](SECURE_CONFIGURATION.md)**
   - Comprehensive security documentation
   - Setup instructions and best practices
   - Command reference and examples
   - Troubleshooting guide

4. **[.env.example](.env.example)**
   - Template for environment variables
   - Security warnings and migration instructions
   - Best practices documentation

### Modified Files

1. **[src/roleradar/config.py](src/roleradar/config.py)**
   - Now supports both secure storage and .env fallback
   - Automatically detects and uses encrypted configuration
   - Prompts users to migrate from .env when API keys detected
   - Instance-based configuration (was class-based)

2. **[requirements.txt](requirements.txt)**
   - Added `cryptography==42.0.0` for encryption support

3. **[README.md](README.md)**
   - Updated installation instructions with secure configuration
   - Added security features to features list
   - Updated configuration section with secure_config_manager.py commands

## Security Features

✅ **AES-256 Encryption** - Military-grade encryption for all credentials  
✅ **Master Password Protection** - Single password to unlock configuration  
✅ **PBKDF2 Key Derivation** - 390,000 iterations (OWASP recommended)  
✅ **Secure File Permissions** - Configuration files are owner-only (0600)  
✅ **No Plaintext Secrets** - API keys never stored in plain text  
✅ **Automatic Migration** - Easy migration from .env files  
✅ **Safe Exports** - Configuration can be exported with credentials redacted  

## How It Works

### Storage Location

Encrypted configuration is stored at: `~/.roleradar/config.enc`

This location:
- Is outside the project directory (safe from accidental commits)
- Has owner-only permissions (0600)
- Persists across project updates

### Encryption Process

1. User provides master password
2. Password is hashed with PBKDF2 (390k iterations) using random salt
3. Configuration is serialized to JSON
4. JSON is encrypted with AES-256 (via Fernet)
5. Salt + encrypted data is written to file

### Decryption Process

1. Read encrypted file
2. Extract salt (first 32 bytes)
3. Derive key from master password + salt
4. Decrypt remaining data with AES-256
5. Parse JSON configuration

## Usage

### Quick Start

```bash
# 1. Initialize secure configuration
python secure_config_manager.py init
# Enter master password and API keys when prompted

# 2. Verify setup
python secure_config_manager.py show

# 3. Use RoleRadar normally - it will automatically use secure storage
python roleradar.py search
python scheduler.py
```

### Migration from .env

```bash
# Migrate existing credentials
python secure_config_manager.py migrate

# Verify migration
python secure_config_manager.py show

# Clean up .env (optional but recommended)
# Remove sensitive values, keep only non-sensitive defaults
```

### Managing Credentials

```bash
# Update API keys
python secure_config_manager.py set-key TAVILY_API_KEY
python secure_config_manager.py set-key GROQ_API_KEY

# Update database password
python secure_config_manager.py set-key DB_PASSWORD

# Change master password
python secure_config_manager.py change-password
```

### Configuration Management

```bash
# Update search roles
python secure_config_manager.py set-roles "security engineer, CISO, compliance officer"

# Update schedule
python secure_config_manager.py set-schedule "08:00, 12:00, 16:00, 20:00"

# Export configuration (safe for version control)
python secure_config_manager.py export config-backup.json

# Export with sensitive data (for secure backup only)
python secure_config_manager.py export config-full.json --include-sensitive
```

## Backward Compatibility

The implementation maintains full backward compatibility:

1. **Existing .env files continue to work** - No forced migration
2. **Automatic detection** - Uses secure storage if available, falls back to .env
3. **Migration helper** - Easy one-command migration from .env
4. **Prompts for security** - Suggests migration when API keys detected in .env

### Configuration Priority

1. Secure Storage (`~/.roleradar/config.enc`) - if exists and unlocks
2. Environment Variables (`.env` file) - fallback
3. Default Values - if neither available

## Security Best Practices

### For Developers

- Use `secure_config_manager.py init` for new setups
- Never commit `.env` with real credentials
- Use `export` (without `--include-sensitive`) for sharing configs
- Store full backups in secure location only

### For Production

- Always use secure configuration in production
- Use strong master passwords (12+ characters)
- Restrict access to `~/.roleradar/` directory
- Regular backups of encrypted configuration
- Rotate credentials periodically

### For Teams

- Each team member has their own encrypted config
- Share non-sensitive settings via JSON export
- Don't share master passwords or encrypted files
- Use separate API keys per team member when possible

## Technical Details

### Encryption Specification

- **Algorithm:** AES-256 via Fernet (cryptography library)
- **Key Derivation:** PBKDF2-HMAC-SHA256
- **Iterations:** 390,000 (OWASP 2023 recommendation)
- **Salt:** 32 bytes random per save operation
- **File Format:** `[32-byte salt][Fernet-encrypted JSON]`

### File Permissions

```bash
# Configuration directory
~/.roleradar/          # 0700 (drwx------)

# Configuration file
~/.roleradar/config.enc  # 0600 (-rw-------)
```

### Dependencies

- `cryptography>=42.0.0` - Provides Fernet (AES-256) and PBKDF2

## Testing

### Verify Encryption

```python
from pathlib import Path

config_path = Path.home() / ".roleradar" / "config.enc"

# Check file exists
assert config_path.exists()

# Check permissions (Unix-like systems)
import stat
mode = config_path.stat().st_mode
assert stat.S_IMODE(mode) == 0o600  # Owner read/write only

# Check content is encrypted (not JSON)
with open(config_path, 'rb') as f:
    content = f.read()
    assert not content.startswith(b'{')  # Not plain JSON
```

### Test Commands

```bash
# Test initialization
python secure_config_manager.py init

# Test show (should prompt for password)
python secure_config_manager.py show

# Test set-key
python secure_config_manager.py set-key TEST_KEY test_value

# Test export
python secure_config_manager.py export test-export.json

# Verify export is safe (no real credentials)
grep -i "REDACTED" test-export.json
```

## Migration Path

### From .env to Secure Storage

1. **Phase 1: Introduction (Current)**
   - Secure storage is available but optional
   - .env files still work
   - Users are prompted to migrate

2. **Phase 2: Deprecation (Future)**
   - Add deprecation warnings for .env
   - Document .env as legacy method
   - Emphasize secure storage in all docs

3. **Phase 3: Migration (Future)**
   - Require secure storage for sensitive values
   - .env only for non-sensitive defaults
   - Clear migration guides

## Comparison

### Before (Plain .env)

```bash
# .env file (plaintext, risky to commit)
TAVILY_API_KEY=tvly-abc123...
GROQ_API_KEY=gsk_xyz789...
DB_PASSWORD=secret123
```

### After (Secure Storage)

```bash
# ~/.roleradar/config.enc (encrypted, binary)
# [random 32-byte salt][AES-256 encrypted JSON]
# Requires master password to decrypt
```

```bash
# .env.example (safe template, no secrets)
TAVILY_API_KEY=
GROQ_API_KEY=
DB_PASSWORD=
# ... instructions to use secure_config_manager.py ...
```

## Future Enhancements

Potential improvements for future versions:

1. **Key Rotation** - Automated API key rotation
2. **Vault Integration** - Support for HashiCorp Vault, AWS Secrets Manager
3. **MFA** - Multi-factor authentication for sensitive operations
4. **Audit Logging** - Track configuration access and changes
5. **Team Secrets** - Shared secrets with role-based access
6. **Auto-locking** - Automatic re-lock after timeout
7. **Biometric Unlock** - Fingerprint/FaceID support on supported platforms

## Troubleshooting

### Common Issues

**"Failed to unlock configuration"**
- Verify correct password
- Check file permissions: `ls -l ~/.roleradar/config.enc`
- Try re-initializing if corrupted

**"No secure configuration found"**
- Run: `python secure_config_manager.py init`

**Application still using .env**
- Check if `~/.roleradar/config.enc` exists
- Verify it unlocks: `python secure_config_manager.py show`
- Remove conflicting environment variables

**Forgot master password**
- Cannot recover encrypted data without password
- Must re-initialize and re-enter credentials
- Restore from backup if available

## Support

For questions or issues:

1. Read [SECURE_CONFIGURATION.md](SECURE_CONFIGURATION.md)
2. Check file paths and permissions
3. Test with `secure_config_manager.py show`
4. Review application logs
5. Open issue with details

---

**Status:** ✅ Fully Implemented and Tested  
**Version:** 1.0  
**Date:** 2026-01-19
