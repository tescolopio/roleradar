// Opportunities Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    loadOpportunities();
});

async function loadOpportunities() {
    try {
        const response = await fetch('/api/opportunities?limit=200');
        const opportunities = await response.json();

        const tbody = document.getElementById('opportunities-tbody');

        if (opportunities.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7">No opportunities found. Run a search to discover opportunities.</td></tr>';
            return;
        }

        tbody.innerHTML = opportunities.map(opp => `
            <tr>
                <td><strong>${escapeHtml(opp.title)}</strong></td>
                <td>${escapeHtml(opp.company_name)}</td>
                <td>${getScoreBadge(opp.company_score)}</td>
                <td>${getRoleTypeBadge(opp.role_type)}</td>
                <td>${escapeHtml(opp.location || 'N/A')}</td>
                <td>${formatDate(opp.discovered_date)}</td>
                <td>${opp.url ? `<a href="${escapeHtml(opp.url)}" target="_blank" rel="noopener noreferrer" class="job-link">🔗 View Job</a>` : 'N/A'}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading opportunities:', error);
        document.getElementById('opportunities-tbody').innerHTML = '<tr><td colspan="7">Error loading opportunities. Please refresh the page.</td></tr>';
    }
}

function getScoreBadge(score) {
    if (!score) return '<span class="score-badge score-low">N/A</span>';
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
