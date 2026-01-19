# RoleRadar: 5-Minute Setup Guide

## What You'll Need (Before Starting)

1. **Tavily API Key** - Get at https://tavily.com
2. **Groq API Key** - Get at https://console.groq.com
3. **Python 3.8+** - Check with: `python --version`

> ⏱️ **Setup takes about 5 minutes total**

---

## Step 1: Download & Install (2 minutes)

### Windows
```powershell
# Open PowerShell (Windows key + R, type powershell)
cd \path\to\roleradar
pip install -r requirements.txt
```

### Mac/Linux
```bash
# Open Terminal
cd /path/to/roleradar
pip install -r requirements.txt
```

✅ **Wait for installation to complete** - You'll see "Successfully installed..." at the end

---

## Step 2: Start the Dashboard (30 seconds)

### Windows
```powershell
python roleradar.py dashboard
```

### Mac/Linux
```bash
python roleradar.py dashboard
```

**You should see:**
```
✅ Starting RoleRadar Dashboard...
📱 Opening browser to http://localhost:5000
🎯 RoleRadar Dashboard running on http://localhost:5000
```

> A browser window will automatically open. If not, go to http://localhost:5000

---

## Step 3: Add Your API Keys (2 minutes)

### In Your Browser:

1. **Click the ⚙️ button** (top right corner)
   - You're now in the Admin Panel
   - The "Credentials" tab is already selected

2. **Paste your Tavily API Key**
   - Find the field labeled "Tavily API Key"
   - Paste your key there (no spaces)

3. **Paste your Groq API Key**
   - Find the field labeled "Groq API Key"
   - Paste your key there (no spaces)

4. **Click "Test Credentials"**
   - Wait 2-3 seconds
   - You should see green checkmarks ✅
   - If red X, double-check the keys are correct

5. **Click "Save Credentials"**
   - You'll see a "Saved!" message
   - Your keys are now securely encrypted

✅ **Your API keys are now configured and secure!**

---

## Step 4: Set Up Search Roles (1 minute)

1. **Click the "Configuration" tab** (next to Credentials)

2. **Click "Add New Role"**

3. **Type a job title** you want to search for:
   - Example: "CISO"
   - Or: "VP of Security"
   - Or: "Security Director"

4. **Click "Add"**

5. **Repeat** for each role you want

Examples of good roles:
- CISO (Chief Information Security Officer)
- VP of Security
- Security Director
- Compliance Officer
- Risk Manager
- InfoSec Manager

✅ **Your search roles are set!**

---

## Step 5: Run Your First Search (2 minutes)

1. **Click the "Search Control" tab**

2. **Click "Search Now"**
   - A dialog appears asking if you're sure
   - Click "Yes, search now"

3. **Wait for the search to complete**
   - You'll see: "Search completed! X results found"
   - This takes 1-3 minutes depending on results
   - Don't close the browser window

4. **Go back to the main dashboard**
   - Click the RoleRadar logo (top left)
   - You'll see "Hot Opportunities"

✅ **You have your first search results!**

---

## Understanding Your Dashboard

### What You'll See:

**Hot Opportunities**
- The best matches
- Sorted by opportunity score
- Shows company name and hiring activity
- Green = high priority

**By Role**
- Opportunities grouped by job title
- Shows how many openings per role
- Click to see company details

**Recent Signals**
- Recent hiring activity
- New job postings
- LinkedIn updates
- News mentions

**Company Scores**
- Overall opportunity ranking (0-100)
- Hiring activity level
- Company size
- Growth indicators

---

## Set Up Automatic Searches (Optional)

If you want searches to run automatically every day:

1. **Click "Schedule" tab** (in Admin Panel)

2. **Check "Enable Automated Search"**

3. **Set your preferred times**
   - Example: 8:00 AM, 12:00 PM, 4:00 PM
   - Click the time fields to change

4. **Click "Save Schedule"**

✅ **Searches will now run automatically at those times!**

---

## Customization (Optional)

### Adjust Scoring Weights
- Admin Panel → Weights tab
- Higher value = more important
- Click Save when done

### Customize Analysis
- Admin Panel → Prompts tab
- Edit what data gets extracted
- Click Save when done

---

## Troubleshooting

### Browser won't open?
```
→ Manually open: http://localhost:5000
```

### API key test failed?
```
→ Copy the key again (check for spaces)
→ Keys are case-sensitive
→ Check internet connection
```

### Search shows no results?
```
→ Normal! First search might find nothing
→ Try tomorrow - scheduled searches are better
```

### Dashboard not loading?
```
→ Wait 10 seconds
→ Refresh the browser (Ctrl+R or Cmd+R)
→ Check that Python is still running
```

### Forgot to bookmark the dashboard?
```
→ http://localhost:5000
→ Add to favorites for quick access
```

---

## Key Keyboard Shortcuts

| Action | Windows | Mac |
|--------|---------|-----|
| Refresh | Ctrl + R | Cmd + R |
| Open Dashboard | Ctrl + T | Cmd + T |
| Go Back | Alt + ← | Cmd + ← |
| Bookmark | Ctrl + D | Cmd + D |

---

## You're Done! 🎉

**What happens next:**
- Searches run at configured times
- New opportunities appear daily
- Scoring gets better with more data
- You can run manual searches anytime
- Results update automatically

**Daily routine:**
1. Open http://localhost:5000
2. Review "Hot Opportunities"
3. Click on companies for details
4. Take notes for follow-up

---

## Next Steps

1. **Try a manual search** (Search Control tab)
2. **Adjust scoring weights** based on your priorities
3. **Add search roles** for different areas
4. **Enable automation** for 24/7 monitoring

---

## Still Need Help?

- **Setup questions:** See [QUICK_START.md](QUICK_START.md)
- **Deployment details:** See [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
- **API configuration:** See [CREDENTIALS_SETUP_GUIDE.md](CREDENTIALS_SETUP_GUIDE.md)
- **Admin panel:** See [ADMIN_GUI_QUICK_START.md](ADMIN_GUI_QUICK_START.md)

---

**Bookmark this:** http://localhost:5000

Enjoy RoleRadar! 🎯
