# RoleRadar Admin GUI - Reference Card

## 🚀 Quick Access

| Feature | How to Access |
|---------|--------------|
| Main Dashboard | http://localhost:5000 |
| Admin Panel | http://localhost:5000/admin or click ⚙️ button |
| API Documentation | See ADMIN_GUI_GUIDE.md |

## 📋 Admin Panel Sections

### 🔍 Search Control
| Action | Button | Result |
|--------|--------|--------|
| Run full search | ▶️ Start Search Now | Searches all configured roles |
| Search specific term | 🔎 Search | Custom role/query search |
| Process results | ⚙️ Process Results | AI extraction & analysis |

### ⚙️ Configuration
| Task | Steps |
|------|-------|
| Add role | Type name → + Add Role → 💾 Save Roles |
| Remove role | Click ✕ on role tag → 💾 Save Roles |
| See active count | View status in search control section |

### 📅 Schedule
| Task | Steps |
|------|-------|
| Add time | Pick time → + Add Time → 💾 Save Schedule |
| Remove time | Click ✕ on time tag → 💾 Save Schedule |
| View timezone | See under "Recommendations" |

### 💬 Prompts
| Prompt | Purpose |
|--------|---------|
| Entity Extraction | Extract companies, titles, locations |
| Hiring Signals | Detect growth, expansion, hiring |
| Growth Detection | Find company trajectory & opportunities |

### ⚖️ Weights
| Component | Default | Adjustment |
|-----------|---------|------------|
| Explicit Job Posting | 40% | ← → |
| Hiring Signals | 30% | ← → |
| Company Growth | 20% | ← → |
| Recent Activity | 10% | ← → |
| **Total** | **100%** | Green when valid ✓ |

### 🔧 System
| Status | What It Shows |
|--------|--------------|
| Database | SQLite/PostgreSQL + status |
| Config Mode | Secure ✅ or Environment 📋 |
| Active Roles | Count of search roles |
| Schedule Times | Count of scheduled search times |

## 🎯 Common Tasks (30 seconds each)

### Add a CISO Search Role
```
1. Click ⚙️ Configuration
2. Type "CISO" in input field
3. Click + Add Role
4. Click 💾 Save Roles
✅ Done
```

### Set 3x Daily Schedule
```
1. Click 📅 Schedule
2. Pick 08:00 → + Add Time
3. Pick 14:00 → + Add Time
4. Pick 18:00 → + Add Time
5. Click 💾 Save Schedule
✅ Done
```

### Increase Job Posting Weight
```
1. Click ⚖️ Weights
2. Drag "Explicit Job Posting" to 50%
3. Adjust others to reach 100%
4. Click 💾 Save Weights
✅ Done
```

### Run Manual Search
```
1. Click 🔍 Search Control
2. Click ▶️ Start Search Now
3. Wait for results
✅ Done
```

## 🔌 API Endpoints (For Power Users)

### Get Configuration
```bash
curl http://localhost:5000/api/config/search-roles
curl http://localhost:5000/api/config/schedule
curl http://localhost:5000/api/config/weights
```

### Update Configuration
```bash
curl -X PUT http://localhost:5000/api/config/search-roles \
  -H "Content-Type: application/json" \
  -d '{"roles": ["CISO", "Security Director"]}'

curl -X PUT http://localhost:5000/api/config/schedule \
  -H "Content-Type: application/json" \
  -d '{"schedule_times": ["08:00", "14:00", "18:00"]}'
```

### Trigger Actions
```bash
# Run manual search
curl -X POST http://localhost:5000/api/search/manual

# Process results
curl -X POST http://localhost:5000/api/search/process

# Check system status
curl http://localhost:5000/api/system/status
curl http://localhost:5000/api/system/health
```

## ✅ Valid Input Formats

| Field | Format | Examples |
|-------|--------|----------|
| Search Role | Text | CISO, Security Director, GRC Analyst |
| Schedule Time | HH:MM (24h) | 08:00, 14:30, 18:45 |
| Weight | 0.0 - 1.0 | 0.4, 0.3, 0.2, 0.1 |
| Weight Slider | 0-100 | 40 (= 0.4), 30 (= 0.3) |
| Custom Query | Any text | "CISO job openings", "security hiring" |

## ⚠️ Validation Rules

| Field | Rule | If Invalid |
|-------|------|-----------|
| Roles | At least 1 required | Error message appears |
| Schedule | HH:MM format | Rejected/highlighted in red |
| Weights | Must sum to 1.0 | Turns amber until valid |
| Prompts | Any text allowed | Can be saved anytime |

## 🎓 Learning Path

**Level 1: Basic (5 minutes)**
1. Open admin panel
2. Add 3 search roles
3. Set 2 schedule times
4. Click "Save"

**Level 2: Intermediate (15 minutes)**
1. Complete Level 1
2. Adjust scoring weights
3. Run manual search
4. Check system status

**Level 3: Advanced (30 minutes)**
1. Complete Level 2
2. Customize extraction prompts
3. Test custom query search
4. Process results
5. Experiment with weight tuning

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Changes won't save | Check database status (🔧 System tab) |
| No search results | Verify API keys configured, try manual search |
| Admin page won't load | Dashboard must be running: `python roleradar.py dashboard` |
| Port already in use | Dashboard auto-detects and uses alternate port |
| Can't reach localhost:5000 | Check firewall, verify dashboard is running |

## 📚 Documentation Map

| Document | For |
|----------|-----|
| ADMIN_GUI_QUICK_START.md | 5-minute setup & common tasks |
| ADMIN_GUI_GUIDE.md | Complete feature reference |
| QUICK_START.md | General RoleRadar setup |
| README.md | Project overview |

## 🎯 Dashboard Navigation

```
┌─────────────────────────────────────────┐
│  🎯 RoleRadar Dashboard                │
│                    [⚙️ Admin Panel] │
├─────────────────────────────────────────┤
│ Summary (Companies, Opportunities, etc) │
├─────────────────────────────────────────┤
│ Top Companies Table                     │
├─────────────────────────────────────────┤
│ Recent Opportunities Table              │
└─────────────────────────────────────────┘

Click [⚙️ Admin Panel] to open admin interface
```

## 💡 Pro Tips

- **Tip 1:** Space searches 3-4 hours apart for best coverage
- **Tip 2:** Start with weight defaults, adjust based on quality
- **Tip 3:** Use specific job titles (CISO vs "Security")
- **Tip 4:** Test custom searches before adding to schedule
- **Tip 5:** Check system status before running large searches
- **Tip 6:** All changes take effect immediately for manual searches
- **Tip 7:** Prompts only affect NEW processing (not historical data)

## 🔐 Security Notes

- ✅ All changes saved to encrypted storage
- ✅ Master password protects credentials
- ✅ No API keys exposed in admin panel
- ✅ Consider using authentication for production
- ✅ Admin panel at /admin (no special access currently)

---

**Need Help?** Check ADMIN_GUI_GUIDE.md for comprehensive documentation
**Want to Start?** Run `python roleradar.py dashboard` and click ⚙️ button
