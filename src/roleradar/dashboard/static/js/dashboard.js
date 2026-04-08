// RoleRadar Dashboard JavaScript

// Import tooltip handler
import { tooltipHandler } from './core/tooltip-handler.js';

document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();
    
    // Refresh data every 5 minutes
    setInterval(loadDashboardData, 5 * 60 * 1000);
});

async function loadDashboardData() {
    try {
        await loadSummary();
        await loadCompanies();
        await loadOpportunities();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

async function loadSummary() {
    try {
        const response = await fetch('/api/summary');
        const data = await response.json();
        
        document.getElementById('total-companies').textContent = data.total_companies || 0;
        document.getElementById('total-opportunities').textContent = data.total_opportunities || 0;
        document.getElementById('total-signals').textContent = data.total_signals || 0;
        document.getElementById('summary-text').textContent = data.summary || 'No summary available.';
        
        if (data.last_updated) {
            const date = new Date(data.last_updated);
            document.getElementById('last-updated').textContent = date.toLocaleString();
        }
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

async function loadCompanies() {
    try {
        const response = await fetch('/api/companies?limit=20');
        const companies = await response.json();
        
        const tbody = document.getElementById('companies-tbody');
        
        if (companies.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5">No companies found. Run a search to discover opportunities.</td></tr>';
            return;
        }
        
        tbody.innerHTML = companies.map(company => `
            <tr>
                <td><strong>${escapeHtml(company.name)}</strong></td>
                <td class="score-cell"
                    data-company-id="${company.id}"
                    onmouseenter="showScoreTooltip(event, ${company.id}, ${company.score})"
                    onmouseleave="hideTooltip()">
                  ${getScoreBadge(company.score)}
                </td>
                <td>${company.active_opportunities}</td>
                <td>${company.signals_count}</td>
                <td>${escapeHtml(company.location || 'N/A')}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading companies:', error);
    }
}

async function loadOpportunities() {
    try {
        const response = await fetch('/api/opportunities?limit=50');
        const opportunities = await response.json();
        
        const tbody = document.getElementById('opportunities-tbody');
        
        if (opportunities.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6">No opportunities found. Run a search to discover opportunities.</td></tr>';
            return;
        }
        
        tbody.innerHTML = opportunities.map(opp => `
            <tr>
                <td><strong>${escapeHtml(opp.title)}</strong></td>
                <td>${escapeHtml(opp.company_name)}</td>
                <td>${getRoleTypeBadge(opp.role_type)}</td>
                <td>${escapeHtml(opp.location || 'N/A')}</td>
                <td>${formatDate(opp.discovered_date)}</td>
                <td>${opp.url ? `<a href="${escapeHtml(opp.url)}" target="_blank" rel="noopener noreferrer" class="job-link">🔗 View Job</a>` : 'N/A'}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading opportunities:', error);
    }
}

function getScoreBadge(score) {
    const roundedScore = Math.round(score);
    let className = 'score-low';
    
    if (roundedScore >= 70) {
        className = 'score-high';
    } else if (roundedScore >= 40) {
        className = 'score-medium';
    }
    
    return `<span class="score-badge ${className}">${roundedScore}</span>`;
}

function getRoleTypeBadge(roleType) {
    if (!roleType) return '<span class="role-type">N/A</span>';
    
    const type = roleType.toLowerCase();
    let className = 'role-type';
    
    if (type.includes('security')) {
        className += ' role-security';
    } else if (type.includes('compliance')) {
        className += ' role-compliance';
    } else if (type.includes('grc')) {
        className += ' role-grc';
    }
    
    return `<span class="${className}">${escapeHtml(roleType)}</span>`;
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
