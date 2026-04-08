// File: dashboard/static/js/core/loading-states.js (NEW)

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

// Export for use in other modules
export { LoadingState };