# RoleRadar Deployment Checklist

## ✅ Pre-Deployment Checklist (For Non-Technical Users)

### 1. Get API Keys (5 minutes)
- [ ] **Tavily API Key**
  - Go to: https://tavily.com
  - Sign up or log in
  - Find your API key in settings
  - Copy the key (you'll need this soon)

- [ ] **Groq API Key**
  - Go to: https://console.groq.com
  - Sign up or log in
  - Find API keys in settings
  - Copy the key (you'll need this soon)

### 2. Install Software (10 minutes)
- [ ] Have Python 3.8+ installed
  - Check: Open terminal/command prompt
  - Type: `python --version`
  - Should show Python 3.8 or higher
  - If not, download from https://python.org

### 3. Install RoleRadar (5 minutes)
- [ ] Downloaded RoleRadar source code
- [ ] Opened terminal/command prompt in RoleRadar folder
- [ ] Ran: `pip install -r requirements.txt`
- [ ] Wait for installation to complete

## 🚀 Deployment Steps (No CLI Knowledge Needed!)

### Step 1: Start the Application
```
Open terminal/command prompt
Navigate to RoleRadar folder
Type: python roleradar.py dashboard
Press Enter
```

**You should see:**
```
✅ Starting RoleRadar Dashboard
📱 Opening browser to http://localhost:5000
```

### Step 2: Enter Your API Keys
1. A browser window opens automatically
2. Click the **⚙️ (gear) button** in the top right
3. You're now in the Admin Panel
4. The **Credentials** tab is already selected
5. Enter:
   - **Tavily API Key:** (paste the key you copied earlier)
   - **Groq API Key:** (paste the key you copied earlier)
6. Click **Test Credentials**
7. If green checkmarks appear, continue
8. Click **Save Credentials**

### Step 3: Set Up Search Roles
1. Click the **Configuration** tab
2. Click **Add New Role**
3. Enter a role name, e.g., "CISO"
4. Click **Add**
5. Repeat for other roles you want to search
   - Examples: "VP of Security", "Security Director", "Compliance Officer"
6. Roles are saved automatically

### Step 4: Set Up Automated Searches (Optional)
1. Click the **Schedule** tab
2. Check the **Enable Automated Search** box
3. Click the time fields to set your preferred times
4. Examples: 8:00 AM, 12:00 PM, 4:00 PM
5. Click **Save Schedule**

### Step 5: Run Your First Search
1. Click the **Search Control** tab
2. Click **Search Now**
3. Wait for the search to complete (2-5 minutes)
4. You'll see updates as results come in

### Step 6: View Your Results
1. Click the RoleRadar logo to go back to main dashboard
2. You'll see:
   - **Hot Opportunities** (best matches)
   - **By Role** (organized by job title)
   - **Recent Signals** (hiring activity)
   - **Companies** (sorted by opportunity score)

## 📊 Understanding Your Dashboard

### Hot Opportunities
- Shows the best hiring opportunities
- Sorted by opportunity score
- Green = high priority
- Orange = medium priority
- Red = lower priority

### By Role
- Lists opportunities organized by job title
- Click a role to see details
- Shows company and hiring signals

### Recent Signals
- Shows recent hiring activity
- New job postings
- LinkedIn activity
- News mentions

### Company Scores
- Overall opportunity score (0-100)
- Hiring activity level
- Company size and growth

## 🔧 Customization (Optional)

### Customize What Gets Analyzed
1. Click **Admin Panel** (⚙️)
2. Click **Prompts** tab
3. Modify the AI extraction prompts
4. Click **Save Prompts**
5. Prompts apply to next search

### Adjust Scoring Algorithm
1. Click **Admin Panel** (⚙️)
2. Click **Weights** tab
3. Adjust the weight sliders
4. Higher weight = more important
5. Click **Save Weights**
6. Changes apply to next search

## ⚠️ Troubleshooting

### Dashboard won't open?
- Check if browser window opened automatically
- If not, open browser and type: `http://localhost:5000`
- If still blank, wait 10 seconds and refresh

### API key test failed?
- Double-check you copied the entire key (no spaces)
- Keys are case-sensitive
- Try clicking **Test** again
- If still failing, check that you have internet connection

### Search takes too long?
- First search takes 2-5 minutes
- Subsequent searches may be faster (cached data)
- Don't close the browser window while searching
- Check the "Search Control" tab for status

### Automated search not running?
- Make sure you enabled it in **Schedule** tab
- Check that you saved the settings
- If computer sleeps, searches won't run (keep awake)

## 📞 Getting Help

**Before deploying to production:**
1. Run 3-5 test searches
2. Verify results accuracy with your team
3. Check that API key limits aren't exceeded
4. Adjust scoring weights based on results

**Common Issues:**
- "API key invalid" → Check you copied it correctly
- "Database error" → System uses fallback SQLite (OK)
- "Search timeout" → Normal on first run, wait 5 minutes
- "Port 5000 in use" → System auto-switches to 5001+

## ✨ You're All Set!

Once you complete all steps:
1. Your RoleRadar instance is running
2. Automated searches will run at set times
3. New opportunities appear daily
4. You can run manual searches anytime
5. Results update in real-time

**Tip:** Bookmark http://localhost:5000 for quick access!
