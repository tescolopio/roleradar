# RoleRadar Dashboard - Complete Feature Guide

## ✅ Yes to All Your Questions!

### 🎨 **Dashboard is Visually Pleasing**
- Modern, clean design with card-based layouts
- Professional color scheme with visual indicators
- Responsive tables with hover effects
- Status badges and progress indicators
- Emoji-enhanced navigation for clarity

---

## 📊 **Main Dashboard** (http://localhost:5000)

### Pages & Sections

#### 1. **Summary Section**
- **Companies Tracked**: Real-time count (currently: 23)
- **Active Opportunities**: Live job postings (currently: 18)
- **Hiring Signals**: Detected signals (currently: 21)
- **AI-Generated Summary**: Groq-powered executive summary
- **Last Updated**: Timestamp of latest refresh

#### 2. **Top Companies Table**
Displays scored companies with:
- Company Name
- Opportunity Score (0-100)
- Number of Active Roles
- Hiring Signals Count
- Location
- Sorted by score (highest first)

**Current Top Companies:**
1. Workday - Score: 51.0
2. Hotman Group, LLC - Score: 48.0
3. Robert Half - Score: 48.0
4. Included Health - Score: 48.0
5. Largeton Group - Score: 48.0

#### 3. **Recent Opportunities Table**
Shows active job postings with:
- Role Title
- Company Name (with score)
- Role Type (security/compliance/GRC)
- Location
- Discovered Date
- Direct Link to Job Posting

**Example Opportunities:**
- Lead Information Security Architect @ Stefanini
- Security Engineer @ Disney
- Security Architect @ Fanatics
- CISO @ SHI International
- Chief Information Security Officer @ InstantServe

---

## ⚙️ **Admin Panel** (http://localhost:5000/admin)

Professional sidebar navigation with 8 management sections:

### 1. 🔐 **Credentials Management**
**YES - Easy API Key Management!**
- Add/Update Tavily API key
- Add/Update Groq API key
- Configure Database URL (PostgreSQL/MySQL/SQLite)
- **Test Credentials** button (validates before saving)
- **Save Credentials** button
- Visual status indicators:
  - ✅ Configured & Working
  - ⚠️ Not Set
  - ❌ Error
- AES-256 encryption for all credentials
- Password masking with show/hide toggle

### 2. 🔍 **Search Control** (Manual Search)
**YES - Full Manual Search Control!**

#### Options Available:
- **"Start Search Now"** - Run full search across all configured roles immediately
- **Custom Query Search** - Search for specific role/query
  - Input field for custom searches
  - Example: "DevOps engineer", "Privacy Officer", "SOC Manager"
- **Process Results** - Manually trigger AI processing
  - Real-time progress bar
  - Shows: "Processing 15/47 results..."
  - Displays current item being processed

#### Search Status Display:
- Results found count
- Processing progress
- Success/error messages
- Real-time updates

### 3. ⚙️ **Configuration** (Search Roles)
**YES - Easy Add/Remove Search Parameters!**

#### Edit Search Roles:
- **Add New Role**: Text input + "Add Role" button
- **Current Roles List**: Shows all configured roles
- **Remove Button**: Delete any role instantly
- **Save Configuration**: Persist changes

**Current Roles (8 total):**
1. security engineer
2. compliance officer
3. GRC analyst
4. Chief Information Security Officer (CISO)
5. data protection officer (DPO)
6. security leadership
7. security architect
8. InfoSec director

**How to Add a Role:**
1. Type role name in input field
2. Click "Add Role"
3. Role appears in list
4. Click "Save Configuration"

**How to Remove a Role:**
1. Click "Remove" button next to role
2. Click "Save Configuration"

### 4. 📅 **Schedule** (Automated Search Times)
**YES - Fully Configurable Schedule!**

#### Configure Search Times:
- **Add New Time**: Time picker (HH:MM format)
- **Current Schedule**: Shows all scheduled times
- **Remove Time**: Delete any time slot
- **Timezone Display**: Shows current timezone (America/New_York)
- **Save Schedule**: Persist changes

**Current Schedule (3 times per day):**
- 08:00 (8:00 AM)
- 12:00 (12:00 PM)
- 15:00 (3:00 PM)

**How to Add a Search Time:**
1. Enter time in HH:MM format (e.g., "06:00", "18:30")
2. Click "Add Time"
3. Time appears in schedule list
4. Click "Save Schedule"

**How to Remove a Search Time:**
1. Click "Remove" next to the time
2. Click "Save Schedule"

**Examples:**
- Multiple searches per day: `["06:00", "10:00", "14:00", "18:00", "22:00"]`
- Business hours only: `["09:00", "13:00", "17:00"]`
- Every hour: `["00:00", "01:00", "02:00", ... "23:00"]`

### 5. 💬 **Prompts** (AI Extraction)
Customize how Groq AI processes results:
- **Entity Extraction Prompt**: How to find companies/jobs
- **Hiring Signals Prompt**: How to detect signals
- **Growth Detection Prompt**: How to identify growth
- **Reset to Defaults**: Restore original prompts
- **Save Prompts**: Apply changes

### 6. 🔍 **Search Results** (Transparency)
View raw search results with AI extraction details:
- Filter by processed/unprocessed
- Filter by query
- See extraction results:
  - Extracted company name
  - Extracted job title
  - Detected role type
  - Location
  - Keywords
- Signal detection:
  - Signal type
  - Confidence score
  - Description
- Processing errors (if any)
- Direct link to source

### 7. ⚖️ **Weights** (Scoring Algorithm)
Adjust how opportunities are scored:
- **Explicit Job Posting**: 0.4 (40%)
- **Hiring Signals**: 0.3 (30%)
- **Company Growth**: 0.2 (20%)
- **Recent Activity**: 0.1 (10%)

Sliders to adjust (must sum to 1.0)

### 8. 🔧 **System Status**
Monitor system health:
- Database connection status
- Secure mode indicator
- Active search roles count
- Scheduled times count
- Last search timestamp
- Pending results count

---

## 🔗 **Relationship Tracking**

### Graph Database Views

While not a visual graph on the dashboard (yet), the relationships are tracked and queryable:

**Available via API & CLI:**
```bash
# View graph relationships
python view_graph.py
```

**Relationships Tracked:**
1. **Company → has_opening → Opportunity**
   - Example: "Robert Half → has_opening → CISO position"

2. **Company → shows_signal → Hiring Signal**
   - Example: "Workday → shows_signal → expansion signal"

**Current Graph Stats:**
- 63 total nodes
- 50 relationship edges
- 23 company nodes
- 19 opportunity nodes
- 21 signal nodes

**API Endpoints for Relationships:**
- `GET /api/companies` - Companies with opportunity counts
- `GET /api/opportunities` - Opportunities with company links
- `GET /api/search-results` - Raw results with extraction details

---

## 🎯 **Quick Actions Summary**

### ✅ **Manual Search** (2 ways)
1. **Admin Panel** → Search Control → "Start Search Now"
2. **Admin Panel** → Search Control → Custom Query + "Search"

### ✅ **Add Search Role**
**Admin Panel** → Configuration → Type role name → "Add Role" → "Save"

### ✅ **Remove Search Role**
**Admin Panel** → Configuration → Click "Remove" → "Save"

### ✅ **Add Schedule Time**
**Admin Panel** → Schedule → Enter time (HH:MM) → "Add Time" → "Save"

### ✅ **Remove Schedule Time**
**Admin Panel** → Schedule → Click "Remove" → "Save"

### ✅ **Change API Keys**
**Admin Panel** → Credentials → Enter keys → "Test" → "Save"

---

## 📱 **Visual Design Features**

### Professional UI Elements:
- **Color-coded status indicators**
  - Green (✅): Working
  - Yellow (⚠️): Warning
  - Red (❌): Error
  - Blue (ℹ️): Info

- **Card-based layouts** for statistics
- **Hover effects** on tables and buttons
- **Progress bars** for processing
- **Toasts/notifications** for actions
- **Responsive tables** with scrolling
- **Emoji navigation** for quick recognition
- **Sidebar navigation** for easy access
- **Input validation** with helpful errors

### CSS Styling:
- Modern sans-serif fonts
- Smooth transitions and animations
- Card shadows and borders
- Consistent spacing and padding
- Mobile-responsive design

---

## 🚀 **Automation**

### Automated Daily Searches:
```bash
# Run scheduler for 24/7 automated searches
python scheduler.py
```

This will:
- Run searches at configured times (8 AM, 12 PM, 3 PM by default)
- Automatically process results with Groq AI
- Update dashboard data in real-time
- Continue running until stopped

---

## 📊 **Data Display**

### What You Can See:

1. **Dashboard Home**
   - ✅ Summary statistics
   - ✅ Top companies with scores
   - ✅ Recent job opportunities
   - ✅ AI-generated summaries

2. **Admin Panel**
   - ✅ All search results (with filtering)
   - ✅ Processing status
   - ✅ Configuration values
   - ✅ System health
   - ✅ API status

3. **Via CLI**
   - ✅ Graph relationships (`python view_graph.py`)
   - ✅ Statistics (`python roleradar.py stats`)
   - ✅ Raw data inspection

---

## ✨ **Key Features**

### 1. **Fully Web-Based Configuration**
No need to edit config files - everything through the UI!

### 2. **Real-Time Updates**
Dashboard refreshes automatically to show latest data.

### 3. **Manual Control**
Run searches and processing on-demand anytime.

### 4. **Flexible Scheduling**
Configure any number of search times per day.

### 5. **Easy Role Management**
Add/remove search roles with simple buttons.

### 6. **Transparency**
See exactly what was extracted from each search result.

### 7. **Secure**
All credentials encrypted with AES-256.

### 8. **Groq Model Zoo**
Automatic fallback between 5 different AI models for reliability.

---

## 🎉 **Summary of Your Questions**

| Question | Answer |
|----------|--------|
| Are results shown on dashboard? | ✅ YES - Companies, opportunities, signals, summaries |
| Is dashboard visually pleasing? | ✅ YES - Modern design with cards, tables, status indicators |
| Shows companies? | ✅ YES - Top companies table with scores |
| Shows job postings? | ✅ YES - Recent opportunities table with links |
| Shows relationships? | ✅ YES - Via graph database (CLI) & API endpoints |
| Are search times configurable? | ✅ YES - Add/remove times via Admin Panel → Schedule |
| Can I enable manual search? | ✅ YES - Two options: full search or custom query |
| Easy to edit search parameters? | ✅ YES - Add/remove roles via Admin Panel → Configuration |

---

**Access Your Dashboard Now:**
- Main Dashboard: http://localhost:5000
- Admin Panel: http://localhost:5000/admin
