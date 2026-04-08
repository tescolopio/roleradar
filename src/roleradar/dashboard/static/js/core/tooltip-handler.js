// File: dashboard/static/js/core/tooltip-handler.js (NEW)

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

// Initialize global tooltip handler
const tooltipHandler = new TooltipHandler();

// Hide tooltip helper
function hideTooltip() {
  tooltipHandler.hide();
}

// Expose functions to global scope for inline HTML event handlers
window.showScoreTooltip = showScoreTooltip;
window.hideTooltip = hideTooltip;
window.tooltipHandler = tooltipHandler;

// Export for use in other modules
export { tooltipHandler, showScoreTooltip, hideTooltip };