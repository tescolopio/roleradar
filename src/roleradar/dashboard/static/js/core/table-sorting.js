// File: dashboard/static/js/core/table-sorting.js (NEW)

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

// Export for use in other modules
export { TableSorter };