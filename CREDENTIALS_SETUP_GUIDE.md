# RoleRadar Credentials Management - Complete User Guide

## Overview

The RoleRadar Admin Panel now includes a **Credentials Management** section that allows non-technical users to configure all API keys and database connections through a web-based interface. No CLI, environment variables, or file editing required.

## Getting Started

### 1. Access the Credentials Panel

1. Start the dashboard:
   ```bash
   python roleradar.py dashboard
   ```

2. Open the admin panel:
   ```
   http://localhost:5000/admin
   ```

3. The **Credentials** section opens automatically (first tab)

### 2. Configure Credentials (5 minutes)

#### Step 1: Get API Keys

You'll need API keys from two services:

**Tavily API:**
- Visit: https://tavily.com
- Sign up (free plan available)
- Copy your API key from dashboard

**Groq API:**
- Visit: https://console.groq.com
- Sign up (free plan available)
- Navigate to API Keys
- Copy your API key

#### Step 2: Enter Credentials

In the Credentials panel:

1. **Tavily API Key:**
   - Click password field
   - Paste your Tavily API key
   - Click "👁 Show" to verify it was pasted correctly
   - Click "👁 Hide" to hide it again

2. **Groq API Key:**
   - Click password field
   - Paste your Groq API key
   - Click "👁 Show" to verify
   - Click "👁 Hide" to hide it again

3. **Database URL (Optional):**
   - Leave blank to use SQLite (recommended for local use)
   - For PostgreSQL, enter: `postgresql://user:password@localhost:5432/database`
   - For MySQL, enter: `mysql://user:password@localhost:3306/database`

#### Step 3: Test Credentials

Before saving, verify your credentials work:

1. Click **"✓ Test Credentials"** button
2. The system will test:
   - Tavily API connection
   - Groq API connection
   - Database connection
3. You'll see status for each:
   - ✅ Valid - Credential is working
   - ❌ Invalid - There's an issue (check your key)
   - ⚠️ Not Set - Credential wasn't entered

**If you see errors:**
- Double-check API key spelling (paste again)
- Verify keys haven't been revoked
- Check your internet connection
- For database: verify connection string is correct

#### Step 4: Save Credentials

Once testing passes:

1. Click **"💾 Save Credentials"** button
2. You'll see a success message
3. Credentials are now encrypted and stored

**Security Note:** Your credentials are encrypted with AES-256 and protected with a master password. They're never logged or displayed in plain text.

## Credential Status Indicators

At the bottom of the Credentials panel, you see status cards showing:

| Indicator | Meaning | Action |
|-----------|---------|--------|
| ✅ Configured | Credential is set up | No action needed |
| ⚠️ Not Set | Credential missing | Enter and save it |
| ⚠️ SQLite | Using local database | Change in Database URL if needed |

## What Happens After Configuration

Once credentials are saved:

1. **Tavily searches work** - You can discover job opportunities
2. **Groq extraction works** - Results are analyzed with AI
3. **Database configured** - Data is persisted (SQLite or custom DB)
4. **Ready to use** - All features become available

## Common Issues & Solutions

### "Invalid" Status for Tavily

**Problem:** Tavily API key shows as invalid
**Solutions:**
1. Copy key again from https://tavily.com/dashboard
2. Make sure you have no extra spaces
3. Verify key hasn't been revoked
4. Check your internet connection

### "Invalid" Status for Groq

**Problem:** Groq API key shows as invalid
**Solutions:**
1. Copy key again from https://console.groq.com/keys
2. Make sure key is active (not revoked)
3. Check for typos or extra spaces
4. Groq might be rate-limiting - try again in a few minutes

### Can't Connect to PostgreSQL

**Problem:** Database connection fails
**Solutions:**
1. **Wrong connection string:** 
   - Should be: `postgresql://user:password@host:port/database`
   - Example: `postgresql://admin:mypass123@localhost:5432/roleradar`

2. **Database server not running:**
   - Start PostgreSQL: `sudo systemctl start postgresql`
   - Or use SQLite (leave Database URL blank)

3. **Wrong credentials:**
   - Verify username and password
   - Try connecting with a database client first

4. **Firewall issue:**
   - Check if PostgreSQL port (5432) is accessible
   - May need firewall rules

### Changes Not Saving

**Problem:** "Save Credentials" button doesn't work
**Solutions:**
1. Make sure at least one credential is filled
2. Check browser console for errors (F12)
3. Verify Flask server is running
4. Try refreshing the page
5. Check if database is writable

## Next Steps After Configuration

After credentials are saved:

1. **Configure Search Roles:**
   - Click "⚙️ Configuration" tab
   - Add roles you want to search for
   - Click "Save Roles"

2. **Set Search Schedule:**
   - Click "📅 Schedule" tab
   - Add times for automated searches
   - Click "Save Schedule"

3. **Start Dashboard:**
   - Navigate to http://localhost:5000 (main dashboard)
   - View discovered opportunities

4. **Run Manual Search (Optional):**
   - Click "🔍 Search Control" tab
   - Click "Start Search Now"
   - See results appear in main dashboard

## Security & Privacy

### How Credentials Are Protected

✅ **Encryption:** AES-256 encryption (military-grade)
✅ **Key Derivation:** PBKDF2 with 390,000 iterations (OWASP standard)
✅ **No Plaintext:** Credentials never stored in plain text
✅ **No Logging:** Credentials never logged to files
✅ **Master Password:** All encrypted data protected with master password
✅ **Show/Hide:** Ability to hide sensitive fields while typing

### What Happens to Your Credentials

- **Stored Locally:** Encrypted in `~/.roleradar/config.enc`
- **Never Transmitted:** Only used locally to call APIs
- **No Tracking:** RoleRadar doesn't track your credentials
- **Encrypted at Rest:** Protected on disk with AES-256

### Best Practices

1. **Use strong master password** - You set this during initial setup
2. **Don't share your credentials** - Each installation should have unique API keys
3. **Rotate API keys periodically** - Can be updated anytime in this panel
4. **Keep browser secure** - Don't use on public/untrusted devices

## API Endpoints (For Advanced Users)

The credentials management is powered by these endpoints:

### Get Credential Status
```bash
curl http://localhost:5000/api/credentials/status
```
Response:
```json
{
  "tavily_configured": true,
  "groq_configured": true,
  "database_configured": false,
  "secure_mode": true
}
```

### Update Credentials
```bash
curl -X PUT http://localhost:5000/api/credentials/update \
  -H "Content-Type: application/json" \
  -d '{
    "tavily_api_key": "your-key-here",
    "groq_api_key": "your-key-here",
    "database_url": "postgresql://..."
  }'
```

### Test Credentials
```bash
curl -X POST http://localhost:5000/api/credentials/test
```

## Troubleshooting

### Need to Change Credentials?

1. Go back to Credentials panel
2. Enter new values in the fields
3. Click "✓ Test Credentials" to verify
4. Click "💾 Save Credentials"

### Want to Use PostgreSQL Later?

1. Set up PostgreSQL database
2. Go to Credentials panel
3. Enter database URL
4. Test and save
5. Data will now use PostgreSQL instead of SQLite

### Forgot Master Password?

Unfortunately, the configuration is encrypted and can't be accessed without the master password. You'll need to:

1. Delete `~/.roleradar/config.enc`
2. Run the setup process again
3. Create a new master password

## Support & Help

- **GUI Issues?** Check browser console (F12) for errors
- **Connection Issues?** Verify API keys in service dashboards
- **Database Issues?** Test connection with database client first
- **General Help?** See [ADMIN_GUI_GUIDE.md](ADMIN_GUI_GUIDE.md)

## Next: Configuration Guide

After credentials are set up, see [ADMIN_GUI_GUIDE.md](ADMIN_GUI_GUIDE.md) for:
- Configuring search roles
- Setting up automated schedule
- Customizing AI prompts
- Tuning scoring weights
