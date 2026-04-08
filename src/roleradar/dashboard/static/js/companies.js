// Companies Page JavaScript

// Import tooltip handler
import { tooltipHandler } from './core/tooltip-handler.js';
// Import table sorter
import { TableSorter } from './core/table-sorting.js';
// Import loading states
import { LoadingState } from './core/loading-states.js';

let allCompanies = []; // Store all data for client-side filtering
let tableSorter;

document.addEventListener('DOMContentLoaded', function() {
    loadCompanies();
});

async function loadCompanies() {
    const tbody = document.getElementById('companies-tbody');

    // Show loading state
    LoadingState.showSkeleton('companies-tbody');

    try {
        const response = await fetch('/api/companies?limit=1000');

        if (!response.ok) {
            throw new Error('Failed to load companies');
        }

        allCompanies = await response.json();

        document.getElementById('total-count').textContent = allCompanies.length;

        if (allCompanies.length === 0) {
            LoadingState.showEmpty('companies-tbody', 'No companies found. Run a search to discover opportunities.');
            return;
        }

        tableSorter = new TableSorter(allCompanies, renderCompanies);
        tableSorter.applySortAndRender();
    } catch (error) {
        console.error('Error loading companies:', error);
        LoadingState.showError(
            'companies-tbody',
            'Failed to load companies. Please check your connection.',
            'loadCompanies()'
        );
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

    // Update table sorter with filtered data
    tableSorter.data = filtered;
    tableSorter.applySortAndRender();
}

function clearFilters() {
    document.getElementById('company-search').value = '';
    document.getElementById('score-filter').value = '';
    document.getElementById('location-filter').value = '';
    filterCompanies();
}

function sortTable(column) {
    tableSorter.sort(column);
}

function renderCompanies(companies) {
    const tbody = document.getElementById('companies-tbody');

    if (companies.length === 0) {
        LoadingState.showEmpty('companies-tbody', 'No companies match your filters.');
        return;
    }

    tbody.innerHTML = companies.map(company => `
        <tr>
            <td><strong>${escapeHtml(company.name)}</strong></td>
            <td>${getScoreBadge(company.score, company.id)}</td>
            <td>${company.active_opportunities}</td>
            <td class="signal-count"
                data-company-id="${company.id}"
                onmouseenter="showSignalTooltip(event, ${company.id})"
                onmouseleave="hideTooltip()">
              <span class="badge badge-signal">${company.signals_count}</span>
            </td>
            <td>${escapeHtml(company.location || 'N/A')}</td>
            <td>${formatDate(company.last_updated)}</td>
        </tr>
    `).join('');
}

function getScoreBadge(score, companyId) {
    const roundedScore = Math.round(score);
    let className = 'score-low';

    if (roundedScore >= 70) {
        className = 'score-high';
    } else if (roundedScore >= 40) {
        className = 'score-medium';
    }

    return `<span class="score-badge ${className}"
                  onmouseenter="showScoreTooltip(event, ${companyId}, ${score})"
                  onmouseleave="hideTooltip()">${roundedScore}</span>`;
}

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

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
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

function hideTooltip() {
  tooltipHandler.hide();
}
