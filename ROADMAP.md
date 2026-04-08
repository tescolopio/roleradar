# 🗺️ RoleRadar Enhancement Roadmap

**Version**: 2.1.0
**Last Updated**: January 29, 2026
**Status**: Planning Phase

---

## 📋 Table of Contents

1. [Phase 1: Core UX Improvements](#phase-1-core-ux-improvements)
2. [Phase 2: User Engagement Features](#phase-2-user-engagement-features)
3. [Phase 3: Analytics & Insights](#phase-3-analytics--insights)
4. [Phase 4: Advanced Features](#phase-4-advanced-features)
5. [Technical Dependencies](#technical-dependencies)
6. [Success Metrics](#success-metrics)

---

## Phase 1: Core UX Improvements
**Timeline**: Week 1-2 | **Effort**: 10-15 hours | **Priority**: HIGH

### Feature 1.1: Comprehensive Tooltip System

**Objective**: Provide contextual information on hover for all interactive elements

#### Specifications

**1.1.1 Signal Count Tooltips**
- **Location**: Companies table, signal count column
- **Trigger**: Mouse hover
- **Display**: Custom tooltip showing signal breakdown

**Technical Implementation**:
```javascript
// File: dashboard/static/js/tooltip-handler.js (NEW)

class TooltipHandler {
  constructor() {
    this.tooltip = null;
    this.init();
  }

  init() {
    // Create tooltip container
    this.tooltip = document.createElement('div');
    this.tooltip.className = 'custom-tooltip';
    this.tooltip.style.display = 'none';
    document.body.appendChild(this.tooltip);
  }

  show(content, event) {
    this.tooltip.innerHTML = content;
    this.tooltip.style.display = 'block';
    this.position(event);
  }

  position(event) {
    const x = event.clientX + 10;
    const y = event.clientY + 10;
    this.tooltip.style.left = x + 'px';
    this.tooltip.style.top = y + 'px';
  }

  hide() {
    this.tooltip.style.display = 'none';
  }
}

// Initialize global tooltip handler
const tooltipHandler = new TooltipHandler();
```

**API Changes Required**:
```python
# File: app.py
@app.route('/api/companies/<int:company_id>/signals')
def get_company_signals(company_id):
    """Get detailed signal information for tooltip display."""
    with db_service.get_session() as session:
        signals = session.query(HiringSignal).filter_by(
            company_id=company_id
        ).order_by(
            desc(HiringSignal.confidence)
        ).all()

        return jsonify([{
            'type': s.signal_type,
            'confidence': round(s.confidence * 100, 1),
            'description': s.description,
            'detected_date': s.detected_date.isoformat()
        } for s in signals])
```

**UI Implementation**:
```javascript
// File: companies.js (MODIFY)

function renderSignalCount(company) {
  return `
    <td class="signal-count"
        data-company-id="${company.id}"
        onmouseenter="showSignalTooltip(event, ${company.id})"
        onmouseleave="hideTooltip()">
      <span class="badge badge-signal">${company.signals_count}</span>
    </td>
  `;
}

async function showSignalTooltip(event, companyId) {
  const response = await fetch(`/api/companies/${companyId}/signals`);
  const signals = await response.json();

  const content = `
    <div class="tooltip-header">
      ${signals.length} signal${signals.length !== 1 ? 's' : ''} detected
    </div>
    <div class="tooltip-body">
      ${signals.map(s => `
        <div class="tooltip-signal-item">
          <span class="signal-type">${s.type}</span>
          <span class="signal-confidence">${s.confidence}%</span>
        </div>
        <div class="signal-description">${s.description}</div>
      `).join('')}
    </div>
    <div class="tooltip-footer">
      Click company for full details
    </div>
  `;

  tooltipHandler.show(content, event);
}
```

**CSS Styling**:
```css
/* File: style.css (ADD) */

.custom-tooltip {
  position: fixed;
  background: #1e293b;
  color: white;
  padding: 12px 16px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  max-width: 300px;
  z-index: 10000;
  font-size: 0.9rem;
  pointer-events: none;
}

.tooltip-header {
  font-weight: 600;
  margin-bottom: 8px;
  padding-bottom: 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.tooltip-signal-item {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
}

.signal-type {
  text-transform: capitalize;
}

.signal-confidence {
  color: #10b981;
  font-weight: 600;
}

.signal-description {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 8px;
}

.tooltip-footer {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
  font-style: italic;
}
```

**1.1.2 Score Breakdown Tooltips**

**Technical Implementation**:
```javascript
// File: tooltip-handler.js (ADD)

async function showScoreTooltip(event, companyId, score) {
  const response = await fetch(`/api/companies/${companyId}/score-breakdown`);
  const breakdown = await response.json();

  const content = `
    <div class="tooltip-header">
      Score Breakdown: ${Math.round(score)}/100
    </div>
    <div class="tooltip-body">
      <div class="score-item">
        <span class="score-label">Job Postings</span>
        <div class="score-bar">
          <div class="score-fill" style="width: ${breakdown.job_postings}%"></div>
        </div>
        <span class="score-value">${breakdown.job_postings.toFixed(1)} pts</span>
      </div>
      <div class="score-item">
        <span class="score-label">Hiring Signals</span>
        <div class="score-bar">
          <div class="score-fill" style="width: ${breakdown.hiring_signals}%"></div>
        </div>
        <span class="score-value">${breakdown.hiring_signals.toFixed(1)} pts</span>
      </div>
      <div class="score-item">
        <span class="score-label">Company Growth</span>
        <div class="score-bar">
          <div class="score-fill" style="width: ${breakdown.company_growth}%"></div>
        </div>
        <span class="score-value">${breakdown.company_growth.toFixed(1)} pts</span>
      </div>
      <div class="score-item">
        <span class="score-label">Recent Activity</span>
        <div class="score-bar">
          <div class="score-fill" style="width: ${breakdown.recent_activity}%"></div>
        </div>
        <span class="score-value">${breakdown.recent_activity.toFixed(1)} pts</span>
      </div>
    </div>
  `;

  tooltipHandler.show(content, event);
}
```

**API Endpoint**:
```python
# File: app.py (ADD)

@app.route('/api/companies/<int:company_id>/score-breakdown')
def get_score_breakdown(company_id):
    """Get detailed score breakdown for tooltip display."""
    with db_service.get_session() as session:
        company = session.query(Company).get(company_id)
        if not company:
            return jsonify({'error': 'Company not found'}), 404

        weights = config.SCORING_WEIGHTS

        # Calculate individual components
        active_opps = session.query(Opportunity).filter_by(
            company_id=company_id,
            is_active=True
        ).count()

        job_score = min(active_opps * 10, 40) * weights['explicit_job_posting']

        recent_signals = session.query(HiringSignal).filter_by(
            company_id=company_id
        ).filter(
            HiringSignal.detected_date > datetime.now(timezone.utc) - timedelta(days=90)
        ).all()

        if recent_signals:
            avg_confidence = sum(s.confidence for s in recent_signals) / len(recent_signals)
            signal_score = avg_confidence * 100 * weights['hiring_signals']
        else:
            signal_score = 0

        has_funding = any(s.signal_type == 'funding' for s in recent_signals)
        has_expansion = any(s.signal_type == 'expansion' for s in recent_signals)
        growth_score = (50 if (has_funding or has_expansion) else 0) * weights['company_growth']

        activity_score = (100 if recent_signals else 0) * weights['recent_activity']

        return jsonify({
            'total_score': company.score,
            'job_postings': job_score,
            'hiring_signals': signal_score,
            'company_growth': growth_score,
            'recent_activity': activity_score,
            'weights': weights
        })
```

**1.1.3 Date Hover Tooltips**

**Implementation**:
```javascript
// File: dashboard.js (MODIFY)

function formatDate(dateString) {
  if (!dateString) return 'N/A';

  const date = new Date(dateString);
  const now = new Date();
  const diffTime = Math.abs(now - date);
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

  let relativeText;
  if (diffDays === 0) {
    relativeText = 'Today';
  } else if (diffDays === 1) {
    relativeText = 'Yesterday';
  } else if (diffDays < 7) {
    relativeText = `${diffDays} days ago`;
  } else {
    relativeText = date.toLocaleDateString();
  }

  // Create hoverable span with full date
  const fullDate = date.toLocaleString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'short'
  });

  return `<span class="date-hover" title="${fullDate}">${relativeText}</span>`;
}
```

**Testing Checklist**:
- [ ] Tooltip appears on hover with correct delay (200ms)
- [ ] Tooltip follows cursor within tolerance
- [ ] Tooltip disappears on mouse leave
- [ ] Tooltip content loads correctly from API
- [ ] Tooltip doesn't overflow screen boundaries
- [ ] Performance: No lag with multiple tooltips
- [ ] Mobile: Touch equivalents work

**Time Estimate**: 4 hours
**Dependencies**: None
**Priority**: HIGH

---

### Feature 1.2: Table Search and Filter

**Objective**: Enable real-time search and filtering on all table-based pages

#### Specifications

**1.2.1 Company Search Box**

**UI Mockup**:
```
┌─────────────────────────────────────────────────────┐
│ 🏢 All Companies                                    │
├─────────────────────────────────────────────────────┤
│ [🔍 Search companies...] [Score: All ▼] [Clear]   │
├─────────────────────────────────────────────────────┤
│ Company          | Score | Roles | Signals         │
│─────────────────────────────────────────────────────│
│ Workday          | 51    | 1     | 2               │
│ Disney           | 48    | 1     | 1               │
└─────────────────────────────────────────────────────┘
```

**HTML Template**:
```html
<!-- File: companies.html (MODIFY) -->

<div class="section">
  <div class="section-header">
    <h2>🏢 All Companies</h2>
    <div class="table-controls">
      <div class="search-box">
        <input type="text"
               id="company-search"
               placeholder="🔍 Search companies..."
               class="search-input"
               oninput="filterCompanies()">
      </div>
      <div class="filter-group">
        <select id="score-filter" onchange="filterCompanies()">
          <option value="">All Scores</option>
          <option value="high">High (70+)</option>
          <option value="medium">Medium (40-69)</option>
          <option value="low">Low (<40)</option>
        </select>
        <select id="location-filter" onchange="filterCompanies()">
          <option value="">All Locations</option>
          <option value="remote">Remote</option>
          <option value="onsite">On-site</option>
        </select>
        <button onclick="clearFilters()" class="btn btn-small">Clear</button>
      </div>
      <div class="results-count">
        Showing <span id="visible-count">0</span> of <span id="total-count">0</span>
      </div>
    </div>
  </div>

  <div class="table-container">
    <table id="companies-table">
      <!-- table content -->
    </table>
  </div>
</div>
```

**JavaScript Implementation**:
```javascript
// File: companies.js (ADD)

let allCompanies = []; // Store all data for client-side filtering

async function loadCompanies() {
  try {
    const response = await fetch('/api/companies?limit=1000');
    allCompanies = await response.json();

    document.getElementById('total-count').textContent = allCompanies.length;

    renderCompanies(allCompanies);
  } catch (error) {
    console.error('Error loading companies:', error);
  }
}

function filterCompanies() {
  const searchTerm = document.getElementById('company-search').value.toLowerCase();
  const scoreFilter = document.getElementById('score-filter').value;
  const locationFilter = document.getElementById('location-filter').value;

  let filtered = allCompanies;

  // Apply search filter
  if (searchTerm) {
    filtered = filtered.filter(company =>
      company.name.toLowerCase().includes(searchTerm) ||
      (company.location && company.location.toLowerCase().includes(searchTerm))
    );
  }

  // Apply score filter
  if (scoreFilter === 'high') {
    filtered = filtered.filter(c => c.score >= 70);
  } else if (scoreFilter === 'medium') {
    filtered = filtered.filter(c => c.score >= 40 && c.score < 70);
  } else if (scoreFilter === 'low') {
    filtered = filtered.filter(c => c.score < 40);
  }

  // Apply location filter
  if (locationFilter === 'remote') {
    filtered = filtered.filter(c =>
      c.location && c.location.toLowerCase().includes('remote')
    );
  } else if (locationFilter === 'onsite') {
    filtered = filtered.filter(c =>
      c.location && !c.location.toLowerCase().includes('remote')
    );
  }

  document.getElementById('visible-count').textContent = filtered.length;
  renderCompanies(filtered);
}

function clearFilters() {
  document.getElementById('company-search').value = '';
  document.getElementById('score-filter').value = '';
  document.getElementById('location-filter').value = '';
  filterCompanies();
}

function renderCompanies(companies) {
  const tbody = document.getElementById('companies-tbody');

  if (companies.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6">No companies match your filters.</td></tr>';
    return;
  }

  tbody.innerHTML = companies.map(company => `
    <tr>
      <td><strong>${escapeHtml(company.name)}</strong></td>
      <td>${getScoreBadge(company.score)}</td>
      <td>${company.active_opportunities}</td>
      <td>${company.signals_count}</td>
      <td>${escapeHtml(company.location || 'N/A')}</td>
      <td>${formatDate(company.last_updated)}</td>
    </tr>
  `).join('');
}
```

**CSS Styling**:
```css
/* File: style.css (ADD) */

.table-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 10px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.filter-group {
  display: flex;
  gap: 0.5rem;
}

.filter-group select {
  padding: 10px 16px;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  background: white;
  font-size: 0.9rem;
  cursor: pointer;
}

.results-count {
  color: var(--text-secondary);
  font-size: 0.9rem;
  white-space: nowrap;
}
```

**1.2.2 Opportunities Advanced Filter**

**UI Mockup**:
```
┌─────────────────────────────────────────────────────┐
│ 💼 All Job Opportunities                            │
├─────────────────────────────────────────────────────┤
│ [🔍 Search...] [Type ▼] [Location ▼] [Date ▼]     │
│ [☑ Remote Only] [☑ High Score] [Clear All]         │
├─────────────────────────────────────────────────────┤
│ Showing 15 of 18 opportunities                      │
└─────────────────────────────────────────────────────┘
```

**Implementation**:
```javascript
// File: opportunities.js (ADD)

function filterOpportunities() {
  const searchTerm = document.getElementById('opp-search').value.toLowerCase();
  const roleType = document.getElementById('role-type-filter').value;
  const location = document.getElementById('location-filter').value;
  const dateRange = document.getElementById('date-filter').value;
  const remoteOnly = document.getElementById('remote-only').checked;
  const highScore = document.getElementById('high-score').checked;

  let filtered = allOpportunities;

  // Text search (title or company)
  if (searchTerm) {
    filtered = filtered.filter(opp =>
      opp.title.toLowerCase().includes(searchTerm) ||
      opp.company_name.toLowerCase().includes(searchTerm)
    );
  }

  // Role type filter
  if (roleType) {
    filtered = filtered.filter(opp =>
      opp.role_type && opp.role_type.toLowerCase() === roleType
    );
  }

  // Location filter
  if (location === 'remote') {
    filtered = filtered.filter(opp =>
      opp.location && opp.location.toLowerCase().includes('remote')
    );
  } else if (location === 'us') {
    filtered = filtered.filter(opp =>
      opp.location && (
        opp.location.includes('NY') ||
        opp.location.includes('CA') ||
        opp.location.includes('TX') ||
        opp.location.match(/[A-Z]{2}/)  // State abbreviation
      )
    );
  }

  // Date range filter
  if (dateRange) {
    const now = new Date();
    const cutoffDate = new Date();

    switch(dateRange) {
      case 'today':
        cutoffDate.setHours(0, 0, 0, 0);
        break;
      case 'week':
        cutoffDate.setDate(cutoffDate.getDate() - 7);
        break;
      case 'month':
        cutoffDate.setMonth(cutoffDate.getMonth() - 1);
        break;
    }

    filtered = filtered.filter(opp => {
      const oppDate = new Date(opp.discovered_date);
      return oppDate >= cutoffDate;
    });
  }

  // Quick filters
  if (remoteOnly) {
    filtered = filtered.filter(opp =>
      opp.location && opp.location.toLowerCase().includes('remote')
    );
  }

  if (highScore) {
    filtered = filtered.filter(opp => opp.company_score >= 60);
  }

  updateOpportunitiesDisplay(filtered);
}
```

**Time Estimate**: 3 hours
**Dependencies**: None
**Priority**: HIGH

---

### Feature 1.3: Sortable Table Columns

**Objective**: Allow users to sort tables by clicking column headers

#### Specifications

**UI Behavior**:
- Click header once: Sort ascending (↑)
- Click header twice: Sort descending (↓)
- Click header third time: Reset to default
- Visual indicator shows current sort state

**HTML Implementation**:
```html
<!-- File: companies.html (MODIFY) -->

<thead>
  <tr>
    <th class="sortable" onclick="sortTable('name')" data-column="name">
      Company
      <span class="sort-indicator" data-column="name"></span>
    </th>
    <th class="sortable" onclick="sortTable('score')" data-column="score">
      Score
      <span class="sort-indicator" data-column="score"></span>
    </th>
    <th class="sortable" onclick="sortTable('active_opportunities')" data-column="active_opportunities">
      Active Roles
      <span class="sort-indicator" data-column="active_opportunities"></span>
    </th>
    <th class="sortable" onclick="sortTable('signals_count')" data-column="signals_count">
      Signals
      <span class="sort-indicator" data-column="signals_count"></span>
    </th>
    <th class="sortable" onclick="sortTable('location')" data-column="location">
      Location
      <span class="sort-indicator" data-column="location"></span>
    </th>
  </tr>
</thead>
```

**JavaScript Implementation**:
```javascript
// File: table-sorting.js (NEW)

class TableSorter {
  constructor(dataArray, renderFunction) {
    this.data = dataArray;
    this.renderFunction = renderFunction;
    this.currentSort = {
      column: null,
      direction: 'none' // 'none', 'asc', 'desc'
    };
  }

  sort(column) {
    // Cycle through sort states
    if (this.currentSort.column !== column) {
      this.currentSort = { column, direction: 'asc' };
    } else if (this.currentSort.direction === 'asc') {
      this.currentSort.direction = 'desc';
    } else if (this.currentSort.direction === 'desc') {
      this.currentSort = { column: null, direction: 'none' };
    } else {
      this.currentSort = { column, direction: 'asc' };
    }

    this.applySortAndRender();
  }

  applySortAndRender() {
    let sorted = [...this.data];

    if (this.currentSort.direction !== 'none') {
      sorted.sort((a, b) => {
        const aVal = a[this.currentSort.column];
        const bVal = b[this.currentSort.column];

        // Handle null/undefined
        if (aVal == null) return 1;
        if (bVal == null) return -1;

        // Numeric comparison
        if (typeof aVal === 'number' && typeof bVal === 'number') {
          return this.currentSort.direction === 'asc'
            ? aVal - bVal
            : bVal - aVal;
        }

        // String comparison
        const aStr = String(aVal).toLowerCase();
        const bStr = String(bVal).toLowerCase();

        if (this.currentSort.direction === 'asc') {
          return aStr.localeCompare(bStr);
        } else {
          return bStr.localeCompare(aStr);
        }
      });
    }

    this.updateSortIndicators();
    this.renderFunction(sorted);
  }

  updateSortIndicators() {
    // Clear all indicators
    document.querySelectorAll('.sort-indicator').forEach(el => {
      el.textContent = '↕';
      el.classList.remove('active');
    });

    // Set active indicator
    if (this.currentSort.direction !== 'none') {
      const indicator = document.querySelector(
        `.sort-indicator[data-column="${this.currentSort.column}"]`
      );
      if (indicator) {
        indicator.textContent = this.currentSort.direction === 'asc' ? '↑' : '↓';
        indicator.classList.add('active');
      }
    }
  }
}

// Usage in companies.js
let tableSorter;

async function loadCompanies() {
  const response = await fetch('/api/companies?limit=1000');
  allCompanies = await response.json();

  tableSorter = new TableSorter(allCompanies, renderCompanies);
  tableSorter.applySortAndRender();
}

function sortTable(column) {
  tableSorter.sort(column);
}
```

**CSS Styling**:
```css
/* File: style.css (ADD) */

.sortable {
  cursor: pointer;
  user-select: none;
  position: relative;
  padding-right: 25px;
}

.sortable:hover {
  background: rgba(37, 99, 235, 0.05);
}

.sort-indicator {
  position: absolute;
  right: 8px;
  color: var(--text-secondary);
  font-size: 0.9em;
  opacity: 0.5;
  transition: all 0.2s ease;
}

.sort-indicator.active {
  color: var(--primary-color);
  opacity: 1;
  font-weight: bold;
}

.sortable:hover .sort-indicator {
  opacity: 0.8;
}
```

**Time Estimate**: 2 hours
**Dependencies**: None
**Priority**: HIGH

---

### Feature 1.4: Loading States and Skeleton Screens

**Objective**: Provide visual feedback during data loading

#### Specifications

**UI States**:
1. Initial load: Skeleton loader
2. Partial load: Progress indicator
3. Refresh: Subtle spinner
4. Error: Error message with retry

**HTML Templates**:
```html
<!-- File: components/skeleton-loader.html (NEW) -->

<div class="skeleton-loader">
  <div class="skeleton-header">
    <div class="skeleton-title"></div>
    <div class="skeleton-subtitle"></div>
  </div>
  <div class="skeleton-table">
    <div class="skeleton-row" style="--delay: 0s"></div>
    <div class="skeleton-row" style="--delay: 0.1s"></div>
    <div class="skeleton-row" style="--delay: 0.2s"></div>
    <div class="skeleton-row" style="--delay: 0.3s"></div>
    <div class="skeleton-row" style="--delay: 0.4s"></div>
  </div>
</div>
```

**CSS Animation**:
```css
/* File: style.css (ADD) */

.skeleton-loader {
  padding: 30px;
}

.skeleton-title,
.skeleton-subtitle,
.skeleton-row {
  background: linear-gradient(
    90deg,
    #f0f0f0 0%,
    #f8f8f8 50%,
    #f0f0f0 100%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  animation-delay: var(--delay, 0s);
  border-radius: 4px;
}

.skeleton-title {
  height: 32px;
  width: 40%;
  margin-bottom: 12px;
}

.skeleton-subtitle {
  height: 20px;
  width: 60%;
  margin-bottom: 24px;
}

.skeleton-row {
  height: 48px;
  width: 100%;
  margin-bottom: 8px;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* Loading spinner for small loads */
.spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(37, 99, 235, 0.3);
  border-radius: 50%;
  border-top-color: var(--primary-color);
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
```

**JavaScript Implementation**:
```javascript
// File: loading-states.js (NEW)

class LoadingState {
  static showSkeleton(containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
      <div class="skeleton-loader">
        ${Array(5).fill(0).map((_, i) => `
          <div class="skeleton-row" style="--delay: ${i * 0.1}s"></div>
        `).join('')}
      </div>
    `;
  }

  static showSpinner(containerId, message = 'Loading...') {
    const container = document.getElementById(containerId);
    container.innerHTML = `
      <div class="loading-spinner-container">
        <div class="spinner"></div>
        <p>${message}</p>
      </div>
    `;
  }

  static showError(containerId, message, retryFn) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
      <div class="error-state">
        <div class="error-icon">⚠️</div>
        <p class="error-message">${message}</p>
        <button onclick="${retryFn}" class="btn btn-primary">
          Try Again
        </button>
      </div>
    `;
  }

  static showEmpty(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `
      <div class="empty-state">
        <div class="empty-icon">📭</div>
        <p class="empty-message">${message}</p>
      </div>
    `;
  }
}

// Usage
async function loadCompanies() {
  const tbody = document.getElementById('companies-tbody');

  // Show loading state
  LoadingState.showSkeleton('companies-tbody');

  try {
    const response = await fetch('/api/companies?limit=1000');

    if (!response.ok) {
      throw new Error('Failed to load companies');
    }

    const companies = await response.json();

    if (companies.length === 0) {
      LoadingState.showEmpty('companies-tbody', 'No companies found. Run a search to discover opportunities.');
    } else {
      renderCompanies(companies);
    }
  } catch (error) {
    console.error('Error loading companies:', error);
    LoadingState.showError(
      'companies-tbody',
      'Failed to load companies. Please check your connection.',
      'loadCompanies()'
    );
  }
}
```

**Time Estimate**: 2 hours
**Dependencies**: None
**Priority**: MEDIUM

---

## Phase 2: User Engagement Features
**Timeline**: Week 3-4 | **Effort**: 15-20 hours | **Priority**: MEDIUM

### Feature 2.1: Opportunity Tracking System

**Objective**: Allow users to track application status and add notes

#### Database Schema Changes

```sql
-- File: migrations/add_user_tracking.sql (NEW)

CREATE TABLE IF NOT EXISTS user_opportunity_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'interested',
    -- Status: interested, applied, interviewing, offer, rejected, not_interested
    notes TEXT,
    favorite BOOLEAN DEFAULT FALSE,
    applied_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id) ON DELETE CASCADE
);

CREATE INDEX idx_user_tracking_opportunity ON user_opportunity_tracking(opportunity_id);
CREATE INDEX idx_user_tracking_status ON user_opportunity_tracking(status);
CREATE INDEX idx_user_tracking_favorite ON user_opportunity_tracking(favorite);
```

**SQLAlchemy Model**:
```python
# File: models/database.py (ADD)

class UserOpportunityTracking(Base):
    """User tracking for opportunities."""
    __tablename__ = 'user_opportunity_tracking'

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id', ondelete='CASCADE'), nullable=False)
    status = Column(String(50), default='interested')
    notes = Column(Text)
    favorite = Column(Boolean, default=False)
    applied_date = Column(DateTime(timezone=True))
    last_updated = Column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationship
    opportunity = relationship('Opportunity', backref='tracking')
```

**API Endpoints**:
```python
# File: app.py (ADD)

@app.route('/api/opportunities/<int:opp_id>/tracking', methods=['GET'])
def get_opportunity_tracking(opp_id):
    """Get tracking information for an opportunity."""
    with db_service.get_session() as session:
        tracking = session.query(UserOpportunityTracking).filter_by(
            opportunity_id=opp_id
        ).first()

        if not tracking:
            return jsonify({
                'status': 'interested',
                'favorite': False,
                'notes': None
            })

        return jsonify({
            'status': tracking.status,
            'favorite': tracking.favorite,
            'notes': tracking.notes,
            'applied_date': tracking.applied_date.isoformat() if tracking.applied_date else None,
            'last_updated': tracking.last_updated.isoformat()
        })

@app.route('/api/opportunities/<int:opp_id>/tracking', methods=['PUT'])
def update_opportunity_tracking(opp_id):
    """Update tracking information for an opportunity."""
    data = request.get_json()

    with db_service.get_session() as session:
        tracking = session.query(UserOpportunityTracking).filter_by(
            opportunity_id=opp_id
        ).first()

        if not tracking:
            tracking = UserOpportunityTracking(opportunity_id=opp_id)
            session.add(tracking)

        # Update fields
        if 'status' in data:
            tracking.status = data['status']
            if data['status'] == 'applied' and not tracking.applied_date:
                tracking.applied_date = datetime.now(timezone.utc)

        if 'favorite' in data:
            tracking.favorite = data['favorite']

        if 'notes' in data:
            tracking.notes = data['notes']

        tracking.last_updated = datetime.now(timezone.utc)

        return jsonify({
            'success': True,
            'tracking': {
                'status': tracking.status,
                'favorite': tracking.favorite,
                'notes': tracking.notes
            }
        })

@app.route('/api/opportunities/favorites', methods=['GET'])
def get_favorite_opportunities():
    """Get all favorited opportunities."""
    with db_service.get_session() as session:
        tracking_records = session.query(UserOpportunityTracking).filter_by(
            favorite=True
        ).all()

        opportunities = []
        for tracking in tracking_records:
            opp = tracking.opportunity
            if opp and opp.is_active:
                opportunities.append({
                    'id': opp.id,
                    'title': opp.title,
                    'company_name': opp.company.name if opp.company else 'Unknown',
                    'company_score': opp.company.score if opp.company else 0,
                    'role_type': opp.role_type,
                    'location': opp.location,
                    'url': opp.url,
                    'discovered_date': opp.discovered_date.isoformat() if opp.discovered_date else None,
                    'tracking': {
                        'status': tracking.status,
                        'notes': tracking.notes
                    }
                })

        return jsonify(opportunities)
```

**UI Implementation**:
```javascript
// File: opportunity-tracking.js (NEW)

class OpportunityTracker {
  async toggleFavorite(oppId) {
    const currentTracking = await this.getTracking(oppId);
    const newFavorite = !currentTracking.favorite;

    await this.updateTracking(oppId, { favorite: newFavorite });

    // Update UI
    this.updateFavoriteButton(oppId, newFavorite);

    showToast(
      newFavorite ? '⭐ Added to favorites' : '✓ Removed from favorites',
      'success'
    );
  }

  async updateStatus(oppId, status) {
    await this.updateTracking(oppId, { status });

    // Update UI
    this.updateStatusBadge(oppId, status);

    const statusMessages = {
      'applied': '✓ Marked as applied',
      'interviewing': '🎯 Marked as interviewing',
      'offer': '🎉 Marked as offer received',
      'rejected': '✗ Marked as rejected',
      'not_interested': '⊗ Marked as not interested'
    };

    showToast(statusMessages[status] || '✓ Status updated', 'success');
  }

  async addNote(oppId, note) {
    await this.updateTracking(oppId, { notes: note });
    showToast('📝 Note saved', 'success');
  }

  async getTracking(oppId) {
    const response = await fetch(`/api/opportunities/${oppId}/tracking`);
    return await response.json();
  }

  async updateTracking(oppId, data) {
    const response = await fetch(`/api/opportunities/${oppId}/tracking`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return await response.json();
  }

  updateFavoriteButton(oppId, isFavorite) {
    const button = document.querySelector(`[data-opp-id="${oppId}"] .favorite-btn`);
    if (button) {
      button.classList.toggle('active', isFavorite);
      button.textContent = isFavorite ? '⭐' : '☆';
      button.title = isFavorite ? 'Remove from favorites' : 'Add to favorites';
    }
  }

  updateStatusBadge(oppId, status) {
    const row = document.querySelector(`[data-opp-id="${oppId}"]`);
    if (row) {
      const statusCell = row.querySelector('.status-cell');
      if (statusCell) {
        statusCell.innerHTML = this.getStatusBadge(status);
      }
    }
  }

  getStatusBadge(status) {
    const badges = {
      'interested': '<span class="status-badge status-interested">Interested</span>',
      'applied': '<span class="status-badge status-applied">✓ Applied</span>',
      'interviewing': '<span class="status-badge status-interviewing">🎯 Interviewing</span>',
      'offer': '<span class="status-badge status-offer">🎉 Offer</span>',
      'rejected': '<span class="status-badge status-rejected">✗ Rejected</span>',
      'not_interested': '<span class="status-badge status-hidden">⊗ Hidden</span>'
    };
    return badges[status] || badges['interested'];
  }
}

const opportunityTracker = new OpportunityTracker();
```

**HTML Template Updates**:
```html
<!-- File: opportunities.html (MODIFY) -->

<!-- Add action buttons column -->
<td class="actions-cell">
  <div class="action-buttons">
    <button class="action-btn favorite-btn"
            onclick="opportunityTracker.toggleFavorite(${opp.id})"
            title="Add to favorites">
      ☆
    </button>
    <button class="action-btn status-btn"
            onclick="showStatusMenu(${opp.id})"
            title="Update status">
      ✓
    </button>
    <button class="action-btn notes-btn"
            onclick="showNotesModal(${opp.id})"
            title="Add notes">
      📝
    </button>
  </div>
</td>

<!-- Status dropdown menu -->
<div id="status-menu-${opp.id}" class="status-menu" style="display: none;">
  <div class="status-menu-header">Update Status</div>
  <div class="status-menu-options">
    <button onclick="opportunityTracker.updateStatus(${opp.id}, 'applied')">
      ✓ Applied
    </button>
    <button onclick="opportunityTracker.updateStatus(${opp.id}, 'interviewing')">
      🎯 Interviewing
    </button>
    <button onclick="opportunityTracker.updateStatus(${opp.id}, 'offer')">
      🎉 Offer
    </button>
    <button onclick="opportunityTracker.updateStatus(${opp.id}, 'rejected')">
      ✗ Rejected
    </button>
    <button onclick="opportunityTracker.updateStatus(${opp.id}, 'not_interested')">
      ⊗ Not Interested
    </button>
  </div>
</div>

<!-- Notes modal -->
<div id="notes-modal" class="modal">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Add Notes</h3>
      <button class="close-btn" onclick="closeNotesModal()">×</button>
    </div>
    <div class="modal-body">
      <textarea id="notes-textarea"
                placeholder="Add your notes here..."
                rows="6"></textarea>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeNotesModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveNotes()">Save Notes</button>
    </div>
  </div>
</div>
```

**Time Estimate**: 6 hours
**Dependencies**: Database migration
**Priority**: MEDIUM

---

### Feature 2.2: Data Export Functions

**Objective**: Enable users to export data in various formats

#### Specifications

**2.2.1 CSV Export**

**Implementation**:
```javascript
// File: export-handler.js (NEW)

class DataExporter {
  async exportToCSV(dataType) {
    let data, filename, columns;

    switch(dataType) {
      case 'companies':
        data = await this.fetchAllCompanies();
        filename = `roleradar-companies-${this.getTimestamp()}.csv`;
        columns = ['name', 'score', 'active_opportunities', 'signals_count', 'location'];
        break;

      case 'opportunities':
        data = await this.fetchAllOpportunities();
        filename = `roleradar-opportunities-${this.getTimestamp()}.csv`;
        columns = ['title', 'company_name', 'company_score', 'role_type', 'location', 'url', 'discovered_date'];
        break;

      case 'favorites':
        data = await this.fetchFavorites();
        filename = `roleradar-favorites-${this.getTimestamp()}.csv`;
        columns = ['title', 'company_name', 'status', 'notes'];
        break;
    }

    const csv = this.generateCSV(data, columns);
    this.downloadCSV(csv, filename);

    showToast('✓ CSV exported successfully', 'success');
  }

  generateCSV(data, columns) {
    // Header row
    const header = columns.map(col => this.formatColumnName(col)).join(',');

    // Data rows
    const rows = data.map(row => {
      return columns.map(col => {
        let value = row[col];

        // Handle special cases
        if (value === null || value === undefined) {
          return '';
        }

        // Escape quotes and wrap in quotes if contains comma
        value = String(value).replace(/"/g, '""');
        if (value.includes(',') || value.includes('\n') || value.includes('"')) {
          value = `"${value}"`;
        }

        return value;
      }).join(',');
    });

    return [header, ...rows].join('\n');
  }

  downloadCSV(csv, filename) {
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');

    if (navigator.msSaveBlob) {
      // IE 10+
      navigator.msSaveBlob(blob, filename);
    } else {
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      link.style.display = 'none';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  }

  async fetchAllCompanies() {
    const response = await fetch('/api/companies?limit=10000');
    return await response.json();
  }

  async fetchAllOpportunities() {
    const response = await fetch('/api/opportunities?limit=10000');
    return await response.json();
  }

  async fetchFavorites() {
    const response = await fetch('/api/opportunities/favorites');
    return await response.json();
  }

  formatColumnName(col) {
    return col.split('_')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  getTimestamp() {
    const now = new Date();
    return now.toISOString().split('T')[0];
  }
}

const dataExporter = new DataExporter();
```

**2.2.2 PDF Export**

**Implementation** (using jsPDF):
```javascript
// File: export-handler.js (ADD)
// Requires: <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

class DataExporter {
  // ... existing methods ...

  async exportToPDF(dataType) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Header
    doc.setFontSize(20);
    doc.text('RoleRadar Report', 14, 22);

    doc.setFontSize(10);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 30);

    // Content
    let y = 40;

    switch(dataType) {
      case 'companies':
        y = await this.addCompaniesToPDF(doc, y);
        break;
      case 'opportunities':
        y = await this.addOpportunitiesToPDF(doc, y);
        break;
    }

    // Footer
    const pageCount = doc.internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.setFontSize(8);
      doc.text(
        `Page ${i} of ${pageCount}`,
        doc.internal.pageSize.getWidth() / 2,
        doc.internal.pageSize.getHeight() - 10,
        { align: 'center' }
      );
    }

    // Download
    doc.save(`roleradar-${dataType}-${this.getTimestamp()}.pdf`);

    showToast('✓ PDF exported successfully', 'success');
  }

  async addCompaniesToPDF(doc, startY) {
    const companies = await this.fetchAllCompanies();

    doc.setFontSize(14);
    doc.text('Top Companies', 14, startY);

    let y = startY + 10;

    companies.forEach((company, index) => {
      if (y > 270) {
        doc.addPage();
        y = 20;
      }

      doc.setFontSize(10);
      doc.setFont(undefined, 'bold');
      doc.text(`${index + 1}. ${company.name}`, 14, y);

      doc.setFont(undefined, 'normal');
      doc.setFontSize(9);
      doc.text(`Score: ${Math.round(company.score)} | Opportunities: ${company.active_opportunities} | Signals: ${company.signals_count}`, 14, y + 5);

      if (company.location) {
        doc.text(`Location: ${company.location}`, 14, y + 10);
        y += 15;
      } else {
        y += 10;
      }
    });

    return y;
  }
}
```

**2.2.3 Copy to Clipboard**

```javascript
// File: export-handler.js (ADD)

class DataExporter {
  // ... existing methods ...

  async copyToClipboard(dataType) {
    let data, text;

    switch(dataType) {
      case 'companies':
        data = await this.fetchAllCompanies();
        text = this.formatCompaniesAsText(data);
        break;
      case 'opportunities':
        data = await this.fetchAllOpportunities();
        text = this.formatOpportunitiesAsText(data);
        break;
    }

    try {
      await navigator.clipboard.writeText(text);
      showToast('✓ Copied to clipboard', 'success');
    } catch (err) {
      // Fallback for older browsers
      this.fallbackCopyToClipboard(text);
    }
  }

  formatCompaniesAsText(companies) {
    let text = 'RoleRadar Companies\n';
    text += '='.repeat(50) + '\n\n';

    companies.forEach((company, index) => {
      text += `${index + 1}. ${company.name}\n`;
      text += `   Score: ${Math.round(company.score)}\n`;
      text += `   Opportunities: ${company.active_opportunities}\n`;
      text += `   Signals: ${company.signals_count}\n`;
      if (company.location) {
        text += `   Location: ${company.location}\n`;
      }
      text += '\n';
    });

    return text;
  }

  fallbackCopyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();

    try {
      document.execCommand('copy');
      showToast('✓ Copied to clipboard', 'success');
    } catch (err) {
      showToast('❌ Failed to copy', 'error');
    }

    document.body.removeChild(textarea);
  }
}
```

**UI Integration**:
```html
<!-- File: companies.html (ADD) -->

<div class="export-menu">
  <button class="btn btn-secondary dropdown-toggle">
    Export ▼
  </button>
  <div class="dropdown-content">
    <button onclick="dataExporter.exportToCSV('companies')">
      📊 Export to CSV
    </button>
    <button onclick="dataExporter.exportToPDF('companies')">
      📄 Export to PDF
    </button>
    <button onclick="dataExporter.copyToClipboard('companies')">
      📋 Copy to Clipboard
    </button>
  </div>
</div>
```

**Time Estimate**: 4 hours
**Dependencies**: jsPDF library (optional)
**Priority**: MEDIUM

---

### Feature 2.3: Toast Notification System

**Objective**: Provide non-intrusive feedback for user actions

#### Specifications

**CSS Implementation**:
```css
/* File: style.css (ADD) */

.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast {
  background: white;
  padding: 16px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 250px;
  max-width: 400px;
  opacity: 0;
  transform: translateX(400px);
  transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
  pointer-events: auto;
}

.toast.show {
  opacity: 1;
  transform: translateX(0);
}

.toast-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.toast-content {
  flex: 1;
}

.toast-message {
  font-weight: 500;
  color: var(--text-primary);
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: var(--text-secondary);
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.toast-close:hover {
  background: var(--bg-color);
}

/* Toast types */
.toast.toast-success {
  border-left: 4px solid #10b981;
}

.toast.toast-error {
  border-left: 4px solid #ef4444;
}

.toast.toast-warning {
  border-left: 4px solid #f59e0b;
}

.toast.toast-info {
  border-left: 4px solid #3b82f6;
}
```

**JavaScript Implementation**:
```javascript
// File: toast.js (NEW)

class ToastManager {
  constructor() {
    this.container = null;
    this.toasts = [];
    this.init();
  }

  init() {
    this.container = document.createElement('div');
    this.container.className = 'toast-container';
    document.body.appendChild(this.container);
  }

  show(message, type = 'info', duration = 3000) {
    const toast = this.createToast(message, type);
    this.container.appendChild(toast);
    this.toasts.push(toast);

    // Trigger animation
    requestAnimationFrame(() => {
      toast.classList.add('show');
    });

    // Auto-dismiss
    const timeoutId = setTimeout(() => {
      this.dismiss(toast);
    }, duration);

    // Store timeout ID for manual dismissal
    toast.dataset.timeoutId = timeoutId;

    return toast;
  }

  createToast(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
      success: '✓',
      error: '✗',
      warning: '⚠',
      info: 'ℹ'
    };

    toast.innerHTML = `
      <div class="toast-icon">${icons[type] || icons.info}</div>
      <div class="toast-content">
        <div class="toast-message">${message}</div>
      </div>
      <button class="toast-close" onclick="toastManager.dismiss(this.parentElement)">×</button>
    `;

    return toast;
  }

  dismiss(toast) {
    if (toast.dataset.timeoutId) {
      clearTimeout(parseInt(toast.dataset.timeoutId));
    }

    toast.classList.remove('show');

    setTimeout(() => {
      if (toast.parentElement) {
        toast.parentElement.removeChild(toast);
      }
      const index = this.toasts.indexOf(toast);
      if (index > -1) {
        this.toasts.splice(index, 1);
      }
    }, 300);
  }

  success(message, duration) {
    return this.show(message, 'success', duration);
  }

  error(message, duration) {
    return this.show(message, 'error', duration);
  }

  warning(message, duration) {
    return this.show(message, 'warning', duration);
  }

  info(message, duration) {
    return this.show(message, 'info', duration);
  }
}

// Global instance
const toastManager = new ToastManager();

// Convenience function
function showToast(message, type = 'info', duration = 3000) {
  return toastManager.show(message, type, duration);
}
```

**Usage Examples**:
```javascript
// Success
showToast('✓ Company added to favorites', 'success');

// Error
showToast('❌ Failed to load data', 'error');

// Warning
showToast('⚠ API rate limit approaching', 'warning');

// Info
showToast('ℹ 5 new opportunities found', 'info');

// Custom duration
showToast('Processing...', 'info', 5000);
```

**Time Estimate**: 2 hours
**Dependencies**: None
**Priority**: LOW

---

## Phase 3: Analytics & Insights
**Timeline**: Week 5-6 | **Effort**: 20-25 hours | **Priority**: LOW

### Feature 3.1: Analytics Dashboard

**Objective**: Provide insights into search patterns and trends

#### New Page Structure

**Route**:
```python
# File: app.py (ADD)

@app.route('/analytics')
def analytics_page():
    """Analytics and insights page."""
    return render_template('analytics.html')
```

**Template**:
```html
<!-- File: templates/analytics.html (NEW) -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics - RoleRadar</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
</head>
<body>
    <div class="container">
        <header>
            <div class="header-main">
                <h1>🎯 RoleRadar</h1>
                <p class="subtitle">Security, Compliance & GRC Opportunity Tracker</p>
            </div>
            <nav class="main-nav">
                <a href="/" class="nav-link">📊 Dashboard</a>
                <a href="/companies" class="nav-link">🏢 Companies</a>
                <a href="/opportunities" class="nav-link">💼 Opportunities</a>
                <a href="/relationships" class="nav-link">🔗 Relationships</a>
                <a href="/analytics" class="nav-link active">📈 Analytics</a>
                <a href="/admin" class="nav-link admin-link">⚙️ Admin</a>
            </nav>
        </header>

        <div class="section">
            <h2>📈 Trends & Analytics</h2>

            <!-- Time range selector -->
            <div class="analytics-controls">
                <button onclick="loadAnalytics('7d')" class="btn btn-small">7 Days</button>
                <button onclick="loadAnalytics('30d')" class="btn btn-small">30 Days</button>
                <button onclick="loadAnalytics('90d')" class="btn btn-small active">90 Days</button>
                <button onclick="loadAnalytics('all')" class="btn btn-small">All Time</button>
            </div>

            <!-- Charts grid -->
            <div class="charts-grid">
                <div class="chart-card">
                    <h3>Opportunities Discovered</h3>
                    <canvas id="opportunities-timeline-chart"></canvas>
                </div>

                <div class="chart-card">
                    <h3>Top Companies by Score</h3>
                    <canvas id="top-companies-chart"></canvas>
                </div>

                <div class="chart-card">
                    <h3>Signal Types Distribution</h3>
                    <canvas id="signals-pie-chart"></canvas>
                </div>

                <div class="chart-card">
                    <h3>Geographic Distribution</h3>
                    <canvas id="location-chart"></canvas>
                </div>

                <div class="chart-card">
                    <h3>Role Types Breakdown</h3>
                    <canvas id="role-types-chart"></canvas>
                </div>

                <div class="chart-card">
                    <h3>Search Activity Heatmap</h3>
                    <canvas id="search-heatmap-chart"></canvas>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>📊 Key Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value" id="total-opportunities-metric">-</div>
                    <div class="metric-label">Total Opportunities</div>
                    <div class="metric-change positive">+12% this week</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="avg-score-metric">-</div>
                    <div class="metric-label">Average Company Score</div>
                    <div class="metric-change neutral">No change</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="high-score-companies-metric">-</div>
                    <div class="metric-label">High Score Companies (70+)</div>
                    <div class="metric-change positive">+3 this week</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value" id="new-signals-metric">-</div>
                    <div class="metric-label">New Signals This Week</div>
                    <div class="metric-change positive">+18 signals</div>
                </div>
            </div>
        </div>
    </div>

    <script src="{{ url_for('static', filename='js/analytics.js') }}"></script>
</body>
</html>
```

#### API Endpoints for Analytics

```python
# File: app.py (ADD)

from sqlalchemy import func, extract
from datetime import datetime, timedelta, timezone

@app.route('/api/analytics/timeline')
def get_analytics_timeline():
    """Get opportunities discovered over time."""
    days = int(request.args.get('days', 90))
    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    with db_service.get_session() as session:
        # Group opportunities by day
        results = session.query(
            func.date(Opportunity.discovered_date).label('date'),
            func.count(Opportunity.id).label('count')
        ).filter(
            Opportunity.discovered_date >= cutoff_date
        ).group_by(
            func.date(Opportunity.discovered_date)
        ).order_by('date').all()

        return jsonify([{
            'date': r.date.isoformat() if r.date else None,
            'count': r.count
        } for r in results])

@app.route('/api/analytics/signal-distribution')
def get_signal_distribution():
    """Get distribution of signal types."""
    with db_service.get_session() as session:
        results = session.query(
            HiringSignal.signal_type,
            func.count(HiringSignal.id).label('count')
        ).group_by(
            HiringSignal.signal_type
        ).all()

        return jsonify([{
            'type': r.signal_type,
            'count': r.count
        } for r in results])

@app.route('/api/analytics/role-distribution')
def get_role_distribution():
    """Get distribution of role types."""
    with db_service.get_session() as session:
        results = session.query(
            Opportunity.role_type,
            func.count(Opportunity.id).label('count')
        ).filter(
            Opportunity.is_active == True
        ).group_by(
            Opportunity.role_type
        ).all()

        return jsonify([{
            'type': r.role_type or 'Unknown',
            'count': r.count
        } for r in results])

@app.route('/api/analytics/search-activity')
def get_search_activity():
    """Get search activity by day and hour."""
    with db_service.get_session() as session:
        results = session.query(
            extract('dow', SearchResult.retrieved_date).label('day_of_week'),
            extract('hour', SearchResult.retrieved_date).label('hour'),
            func.count(SearchResult.id).label('count')
        ).group_by(
            'day_of_week', 'hour'
        ).all()

        # Create heatmap data
        heatmap = [[0 for _ in range(24)] for _ in range(7)]
        for r in results:
            if r.day_of_week is not None and r.hour is not None:
                heatmap[int(r.day_of_week)][int(r.hour)] = r.count

        return jsonify({
            'heatmap': heatmap,
            'days': ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
            'hours': list(range(24))
        })

@app.route('/api/analytics/metrics')
def get_analytics_metrics():
    """Get key metrics for analytics dashboard."""
    with db_service.get_session() as session:
        total_opps = session.query(Opportunity).filter_by(is_active=True).count()

        avg_score = session.query(func.avg(Company.score)).scalar() or 0

        high_score_companies = session.query(Company).filter(
            Company.score >= 70
        ).count()

        week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        new_signals = session.query(HiringSignal).filter(
            HiringSignal.detected_date >= week_ago
        ).count()

        return jsonify({
            'total_opportunities': total_opps,
            'average_score': round(avg_score, 1),
            'high_score_companies': high_score_companies,
            'new_signals_week': new_signals
        })
```

**JavaScript Implementation**:
```javascript
// File: analytics.js (NEW)

let charts = {};

document.addEventListener('DOMContentLoaded', function() {
    loadAnalytics('90d');
});

async function loadAnalytics(timeRange) {
    // Update active button
    document.querySelectorAll('.analytics-controls .btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');

    // Load data
    await Promise.all([
        loadTimelineChart(timeRange),
        loadSignalsChart(),
        loadRoleTypesChart(),
        loadSearchHeatmap(),
        loadMetrics()
    ]);
}

async function loadTimelineChart(timeRange) {
    const days = {
        '7d': 7,
        '30d': 30,
        '90d': 90,
        'all': 365
    }[timeRange] || 90;

    const response = await fetch(`/api/analytics/timeline?days=${days}`);
    const data = await response.json();

    const ctx = document.getElementById('opportunities-timeline-chart');

    if (charts.timeline) {
        charts.timeline.destroy();
    }

    charts.timeline = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data.map(d => d.date),
            datasets: [{
                label: 'Opportunities Discovered',
                data: data.map(d => d.count),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

async function loadSignalsChart() {
    const response = await fetch('/api/analytics/signal-distribution');
    const data = await response.json();

    const ctx = document.getElementById('signals-pie-chart');

    if (charts.signals) {
        charts.signals.destroy();
    }

    charts.signals = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: data.map(d => d.type),
            datasets: [{
                data: data.map(d => d.count),
                backgroundColor: [
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b',
                    '#ef4444',
                    '#8b5cf6',
                    '#ec4899'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

async function loadMetrics() {
    const response = await fetch('/api/analytics/metrics');
    const metrics = await response.json();

    document.getElementById('total-opportunities-metric').textContent = metrics.total_opportunities;
    document.getElementById('avg-score-metric').textContent = metrics.average_score;
    document.getElementById('high-score-companies-metric').textContent = metrics.high_score_companies;
    document.getElementById('new-signals-metric').textContent = metrics.new_signals_week;
}
```

**CSS Styling**:
```css
/* File: style.css (ADD) */

.charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 2rem;
    margin-top: 2rem;
}

.chart-card {
    background: var(--card-bg);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-card h3 {
    margin-bottom: 1rem;
    color: var(--text-primary);
}

.chart-card canvas {
    height: 300px !important;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-top: 1.5rem;
}

.metric-card {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
}

.metric-value {
    font-size: 3rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.metric-label {
    font-size: 1rem;
    opacity: 0.9;
    margin-bottom: 0.5rem;
}

.metric-change {
    font-size: 0.9rem;
    font-weight: 500;
}

.metric-change.positive {
    color: #86efac;
}

.metric-change.negative {
    color: #fca5a5;
}

.metric-change.neutral {
    color: rgba(255, 255, 255, 0.7);
}

.analytics-controls {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}
```

**Time Estimate**: 12 hours
**Dependencies**: Chart.js library
**Priority**: LOW

---

## Phase 4: Advanced Features
**Timeline**: Week 7-8+ | **Effort**: 30+ hours | **Priority**: FUTURE

### Feature 4.1: Dark Mode

**Time Estimate**: 3 hours
**Priority**: MEDIUM-LOW

### Feature 4.2: Smart Recommendations

**Time Estimate**: 8 hours
**Priority**: LOW

### Feature 4.3: Mobile Responsive Improvements

**Time Estimate**: 6 hours
**Priority**: MEDIUM

---

## Technical Dependencies

### Required Libraries

| Library | Version | Purpose | CDN/Install |
|---------|---------|---------|-------------|
| Chart.js | 4.4.0 | Analytics charts | `<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>` |
| jsPDF | 2.5.1 | PDF export | `<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>` |
| vis-network | 9.1.9 | Graph visualization | Already implemented |

### Database Migrations

**Migration Order**:
1. Add `user_opportunity_tracking` table
2. Add indexes for performance
3. Add `last_updated` column to companies

**Migration Script**:
```sql
-- File: migrations/001_user_tracking.sql

-- Phase 2.1
CREATE TABLE IF NOT EXISTS user_opportunity_tracking (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'interested',
    notes TEXT,
    favorite BOOLEAN DEFAULT FALSE,
    applied_date TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id) ON DELETE CASCADE
);

CREATE INDEX idx_user_tracking_opportunity ON user_opportunity_tracking(opportunity_id);
CREATE INDEX idx_user_tracking_status ON user_opportunity_tracking(status);
CREATE INDEX idx_user_tracking_favorite ON user_opportunity_tracking(favorite);

-- Performance indexes
CREATE INDEX idx_opportunities_discovered_date ON opportunities(discovered_date);
CREATE INDEX idx_hiring_signals_detected_date ON hiring_signals(detected_date);
CREATE INDEX idx_search_results_retrieved_date ON search_results(retrieved_date);
```

---

## Success Metrics

### Phase 1 Metrics
- [ ] Tooltip hover rate > 50%
- [ ] Search/filter usage > 30% of sessions
- [ ] Sort functionality used in > 40% of table views
- [ ] Perceived load time < 2s (skeleton screens)

### Phase 2 Metrics
- [ ] Favorite/tracking usage > 25% of opportunities
- [ ] Export functionality used weekly
- [ ] Toast notifications clear and helpful
- [ ] < 5% error rate on user actions

### Phase 3 Metrics
- [ ] Analytics page visited in > 20% of sessions
- [ ] Insights actionable and valuable
- [ ] Charts render in < 1s

### Phase 4 Metrics
- [ ] Dark mode adoption > 30%
- [ ] Mobile usage increase > 50%
- [ ] User satisfaction score > 4/5

---

## Testing Checklist

### Phase 1 Testing
- [ ] Tooltips display correctly on all elements
- [ ] Search filters work across all tables
- [ ] Sorting maintains filter state
- [ ] Loading states show appropriate feedback
- [ ] Cross-browser compatibility (Chrome, Firefox, Safari)
- [ ] Mobile responsiveness maintained

### Phase 2 Testing
- [ ] Tracking persists across sessions
- [ ] CSV export includes all data
- [ ] PDF export renders correctly
- [ ] Toast notifications don't stack infinitely
- [ ] Favorite state syncs with backend

### Phase 3 Testing
- [ ] Charts render with accurate data
- [ ] Analytics calculations are correct
- [ ] Date ranges filter properly
- [ ] Performance with large datasets

---

## Implementation Notes

### Best Practices
1. **Progressive Enhancement**: Features degrade gracefully
2. **Performance**: Lazy load charts and heavy components
3. **Accessibility**: ARIA labels, keyboard navigation
4. **Error Handling**: Graceful failures with user feedback
5. **Data Validation**: Client and server-side validation

### Code Organization
```
static/
├── js/
│   ├── core/
│   │   ├── tooltip-handler.js
│   │   ├── table-sorting.js
│   │   ├── loading-states.js
│   │   └── toast.js
│   ├── features/
│   │   ├── opportunity-tracking.js
│   │   ├── export-handler.js
│   │   └── analytics.js
│   └── pages/
│       ├── dashboard.js
│       ├── companies.js
│       ├── opportunities.js
│       └── relationships.js
└── css/
    ├── core/
    │   ├── variables.css
    │   ├── base.css
    │   └── utilities.css
    └── components/
        ├── tooltips.css
        ├── tables.css
        ├── modals.css
        └── charts.css
```

---

## Estimated Total Effort

| Phase | Features | Time Estimate |
|-------|----------|---------------|
| Phase 1 | Core UX | 10-15 hours |
| Phase 2 | Engagement | 15-20 hours |
| Phase 3 | Analytics | 20-25 hours |
| Phase 4 | Advanced | 30+ hours |
| **Total** | | **75-90 hours** |

---

## Next Steps

1. Review and prioritize features
2. Set up development environment
3. Begin Phase 1 implementation
4. Gather user feedback after each phase
5. Iterate based on usage metrics

---

**Document Version**: 1.0
**Last Updated**: January 29, 2026
**Status**: Ready for Implementation
