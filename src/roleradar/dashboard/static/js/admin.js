/**
 * Admin Dashboard JavaScript
 * Handles all admin panel functionality
 */

class AdminDashboard {
    constructor() {
        this.currentSection = 'credentials';
        this.originalConfig = {};
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadSystemStatus();
        await this.loadCredentialsStatus();
        await this.loadConfiguration();
        this.showSection('credentials');
    }

    // ==================== Event Setup ====================

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-item[data-section]').forEach(item => {
            item.addEventListener('click', (e) => {
                e.preventDefault();
                const section = item.getAttribute('data-section');
                this.showSection(section);
            });
        });

        // Credentials
        document.getElementById('btn-show-tavily')?.addEventListener('click', () => this.togglePasswordField('tavily-key'));
        document.getElementById('btn-show-groq')?.addEventListener('click', () => this.togglePasswordField('groq-key'));
        document.getElementById('btn-test-credentials')?.addEventListener('click', () => this.testCredentials());
        document.getElementById('btn-save-credentials')?.addEventListener('click', () => this.saveCredentials());

        // Search Control
        document.getElementById('btn-run-search')?.addEventListener('click', () => this.runSearch());
        document.getElementById('btn-custom-search')?.addEventListener('click', () => this.runCustomSearch());
        document.getElementById('btn-process')?.addEventListener('click', () => this.processResults());

        // Configuration - Roles
        document.getElementById('btn-add-role')?.addEventListener('click', () => this.addRoleUI());
        document.getElementById('new-role-input')?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.addRoleUI();
        });
        document.getElementById('btn-save-roles')?.addEventListener('click', () => this.saveRoles());
        document.getElementById('btn-reset-roles')?.addEventListener('click', () => this.resetRoles());

        // Schedule
        document.getElementById('btn-add-time')?.addEventListener('click', () => this.addTimeUI());
        document.getElementById('btn-save-schedule')?.addEventListener('click', () => this.saveSchedule());
        document.getElementById('btn-reset-schedule')?.addEventListener('click', () => this.resetSchedule());

        // Prompts
        document.getElementById('btn-save-prompts')?.addEventListener('click', () => this.savePrompts());
        document.getElementById('btn-reset-prompts')?.addEventListener('click', () => this.resetPrompts());

        // Weights
        document.querySelectorAll('.weight-slider').forEach(slider => {
            slider.addEventListener('input', () => this.updateWeightDisplay());
        });
        document.getElementById('btn-save-weights')?.addEventListener('click', () => this.saveWeights());
        document.getElementById('btn-reset-weights')?.addEventListener('click', () => this.resetWeights());
    }

    // ==================== Navigation ====================

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.admin-section').forEach(section => {
            section.classList.remove('active');
        });

        // Show selected section
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.add('active');
        }

        // Update navigation
        document.querySelectorAll('.nav-item[data-section]').forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('data-section') === sectionId) {
                item.classList.add('active');
            }
        });

        // Update title
        const titles = {
            'credentials': '🔐 Credentials',
            'search-control': '🔍 Search Control',
            'configuration': '⚙️ Configuration',
            'schedule': '📅 Schedule',
            'prompts': '💬 Prompts',
            'weights': '⚖️ Weights',
            'system': '🔧 System'
        };

        document.getElementById('section-title').textContent = titles[sectionId] || 'Dashboard';
        this.currentSection = sectionId;
    }

    // ==================== Credentials Management ====================

    async loadCredentialsStatus() {
        try {
            const response = await fetch('/api/credentials/status');
            const data = await response.json();

            // Update credential status indicators
            document.getElementById('tavily-check').textContent = 
                data.tavily_configured ? '✅ Configured' : '⚠️ Not Set';
            document.getElementById('groq-check').textContent = 
                data.groq_configured ? '✅ Configured' : '⚠️ Not Set';
            document.getElementById('database-check').textContent = 
                data.database_configured ? '✅ Custom' : '⚠️ SQLite';
        } catch (error) {
            console.error('Error loading credentials status:', error);
        }
    }

    togglePasswordField(fieldId) {
        const field = document.getElementById(fieldId);
        const btn = event.target;
        
        if (field.type === 'password') {
            field.type = 'text';
            btn.textContent = '🙈 Hide';
        } else {
            field.type = 'password';
            btn.textContent = '👁 Show';
        }
    }

    async testCredentials() {
        try {
            const btn = document.querySelector('#btn-test-credentials');
            btn.disabled = true;
            btn.textContent = '⏳ Testing...';

            const response = await fetch('/api/credentials/test', {
                method: 'POST'
            });

            const data = await response.json();

            if (response.ok) {
                // Update individual credential status
                if (data.results.tavily) {
                    const tavily = data.results.tavily;
                    const tavStatus = document.getElementById('tavily-status');
                    tavStatus.className = `credential-status ${tavily.status === 'valid' ? 'success' : 'error'}`;
                    tavStatus.textContent = `${tavily.status === 'valid' ? '✅' : '❌'} ${tavily.message}`;
                }

                if (data.results.groq) {
                    const groq = data.results.groq;
                    const groqStatus = document.getElementById('groq-status');
                    groqStatus.className = `credential-status ${groq.status === 'valid' ? 'success' : 'error'}`;
                    groqStatus.textContent = `${groq.status === 'valid' ? '✅' : '❌'} ${groq.message}`;
                }

                if (data.results.database) {
                    const db = data.results.database;
                    const dbStatus = document.getElementById('database-status');
                    dbStatus.className = `credential-status ${db.status === 'valid' ? 'success' : 'error'}`;
                    dbStatus.textContent = `${db.status === 'valid' ? '✅' : '❌'} ${db.message}`;
                }

                this.showStatus('credentials', '✅ Credential testing completed', 'success');
            } else {
                this.showStatus('credentials', `❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showStatus('credentials', `❌ Error: ${error.message}`, 'error');
        } finally {
            const btn = document.querySelector('#btn-test-credentials');
            btn.disabled = false;
            btn.textContent = '✓ Test Credentials';
        }
    }

    async saveCredentials() {
        try {
            const tavilyKey = document.getElementById('tavily-key').value.trim();
            const groqKey = document.getElementById('groq-key').value.trim();
            const databaseUrl = document.getElementById('database-url').value.trim();

            if (!tavilyKey && !groqKey && !databaseUrl) {
                this.showStatus('credentials', '❌ At least one credential must be provided', 'error');
                return;
            }

            const btn = document.querySelector('#btn-save-credentials');
            btn.disabled = true;
            btn.textContent = '💾 Saving...';

            const response = await fetch('/api/credentials/update', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    tavily_api_key: tavilyKey,
                    groq_api_key: groqKey,
                    database_url: databaseUrl
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showStatus('credentials', `✅ ${data.message}`, 'success');
                
                // Clear password fields after successful save
                document.getElementById('tavily-key').value = '';
                document.getElementById('groq-key').value = '';
                
                // Update credential status
                await this.loadCredentialsStatus();
            } else {
                this.showStatus('credentials', `❌ ${data.error || data.message}`, 'error');
            }
        } catch (error) {
            this.showStatus('credentials', `❌ Error: ${error.message}`, 'error');
        } finally {
            const btn = document.querySelector('#btn-save-credentials');
            btn.disabled = false;
            btn.textContent = '💾 Save Credentials';
        }
    }

    // ==================== System Status ====================

    async loadSystemStatus() {
        try {
            const response = await fetch('/api/system/status');
            const data = await response.json();

            // Update status display
            document.getElementById('status-db').textContent = 
                `${data.database.type} ${data.database.status === 'ready' ? '✅' : '⚠️'}`;
            document.getElementById('status-config-mode').textContent = 
                data.config_secure ? 'Secure ✅' : 'Environment 📋';
            document.getElementById('status-roles-count').textContent = data.search_roles;
            document.getElementById('status-schedule-count').textContent = data.schedule_times;
        } catch (error) {
            console.error('Error loading system status:', error);
        }
    }

    // ==================== Configuration Loading ====================

    async loadConfiguration() {
        try {
            const [rolesResp, scheduleResp, weightsResp, promptsResp] = await Promise.all([
                fetch('/api/config/search-roles'),
                fetch('/api/config/schedule'),
                fetch('/api/config/weights'),
                fetch('/api/config/extraction-prompts')
            ]);

            const roles = await rolesResp.json();
            const schedule = await scheduleResp.json();
            const weights = await weightsResp.json();
            const prompts = await promptsResp.json();

            // Store original config
            this.originalConfig = { roles, schedule, weights, prompts };

            // Load roles
            this.loadRoles(roles.roles);

            // Load schedule
            document.getElementById('timezone-display').textContent = schedule.timezone;
            this.loadSchedule(schedule.schedule_times);

            // Load weights
            this.loadWeights(weights);

            // Load prompts
            this.loadPrompts(prompts);

            // Load search status
            await this.loadSearchStatus();
        } catch (error) {
            console.error('Error loading configuration:', error);
            this.showStatus('system', 'Error loading configuration', 'error');
        }
    }

    async loadSearchStatus() {
        try {
            const response = await fetch('/api/search/status');
            const data = await response.json();

            document.getElementById('status-active-roles').textContent = data.active_roles;
            document.getElementById('status-schedule').textContent = 
                data.schedule_times.join(', ') || 'Not configured';
            document.getElementById('status-last-search').textContent = 
                data.last_search || 'Never';
        } catch (error) {
            console.error('Error loading search status:', error);
        }
    }

    // ==================== Roles Management ====================

    loadRoles(roles) {
        const container = document.getElementById('roles-list');
        container.innerHTML = '';

        roles.forEach(role => {
            const tag = document.createElement('div');
            tag.className = 'role-tag';
            tag.innerHTML = `
                ${role}
                <button type="button" data-role="${role}">✕</button>
            `;
            tag.querySelector('button').addEventListener('click', () => {
                this.removeRoleUI(role);
            });
            container.appendChild(tag);
        });
    }

    addRoleUI() {
        const input = document.getElementById('new-role-input');
        const role = input.value.trim();

        if (!role) {
            this.showStatus('roles', 'Please enter a role name', 'error');
            return;
        }

        const roles = Array.from(document.querySelectorAll('.role-tag'))
            .map(tag => tag.textContent.trim().replace('✕', '').trim());

        if (roles.includes(role)) {
            this.showStatus('roles', 'This role already exists', 'error');
            return;
        }

        roles.push(role);
        this.loadRoles(roles);
        input.value = '';
    }

    removeRoleUI(role) {
        const roles = Array.from(document.querySelectorAll('.role-tag'))
            .map(tag => tag.textContent.trim().replace('✕', '').trim())
            .filter(r => r !== role);

        this.loadRoles(roles);
    }

    async saveRoles() {
        try {
            const roles = Array.from(document.querySelectorAll('.role-tag'))
                .map(tag => tag.textContent.trim().replace('✕', '').trim());

            const response = await fetch('/api/config/search-roles', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ roles })
            });

            const data = await response.json();
            if (response.ok) {
                this.showStatus('roles', '✅ Roles saved successfully', 'success');
            } else {
                this.showStatus('roles', `❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showStatus('roles', `❌ Error: ${error.message}`, 'error');
        }
    }

    resetRoles() {
        if (this.originalConfig.roles) {
            this.loadRoles(this.originalConfig.roles.roles);
            this.showStatus('roles', '↻ Reset to original roles', 'info');
        }
    }

    // ==================== Schedule Management ====================

    loadSchedule(times) {
        const container = document.getElementById('schedule-list');
        container.innerHTML = '';

        times.forEach(time => {
            const tag = document.createElement('div');
            tag.className = 'schedule-tag';
            tag.innerHTML = `
                ${time}
                <button type="button" data-time="${time}">✕</button>
            `;
            tag.querySelector('button').addEventListener('click', () => {
                this.removeTimeUI(time);
            });
            container.appendChild(tag);
        });
    }

    addTimeUI() {
        const input = document.getElementById('new-time-input');
        const time = input.value.trim();

        if (!time) {
            this.showStatus('schedule', 'Please select a time', 'error');
            return;
        }

        const times = Array.from(document.querySelectorAll('.schedule-tag'))
            .map(tag => tag.textContent.trim().replace('✕', '').trim());

        if (times.includes(time)) {
            this.showStatus('schedule', 'This time already exists', 'error');
            return;
        }

        times.push(time);
        times.sort();
        this.loadSchedule(times);
        input.value = '';
    }

    removeTimeUI(time) {
        const times = Array.from(document.querySelectorAll('.schedule-tag'))
            .map(tag => tag.textContent.trim().replace('✕', '').trim())
            .filter(t => t !== time);

        this.loadSchedule(times);
    }

    async saveSchedule() {
        try {
            const times = Array.from(document.querySelectorAll('.schedule-tag'))
                .map(tag => tag.textContent.trim().replace('✕', '').trim());

            const response = await fetch('/api/config/schedule', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ schedule_times: times })
            });

            const data = await response.json();
            if (response.ok) {
                this.showStatus('schedule', '✅ Schedule saved successfully', 'success');
            } else {
                this.showStatus('schedule', `❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showStatus('schedule', `❌ Error: ${error.message}`, 'error');
        }
    }

    resetSchedule() {
        if (this.originalConfig.schedule) {
            this.loadSchedule(this.originalConfig.schedule.schedule_times);
            this.showStatus('schedule', '↻ Reset to original schedule', 'info');
        }
    }

    // ==================== Weights Management ====================

    loadWeights(weights) {
        const mapping = {
            'explicit_job_posting': 'weight-explicit',
            'hiring_signals': 'weight-signals',
            'company_growth': 'weight-growth',
            'recent_activity': 'weight-activity'
        };

        for (const [key, value] of Object.entries(weights)) {
            const elementId = mapping[key];
            if (elementId) {
                const percentage = Math.round(value * 100);
                document.getElementById(elementId).value = percentage;
            }
        }

        this.updateWeightDisplay();
    }

    updateWeightDisplay() {
        const sliders = {
            'weight-explicit': 'weight-explicit-value',
            'weight-signals': 'weight-signals-value',
            'weight-growth': 'weight-growth-value',
            'weight-activity': 'weight-activity-value'
        };

        let total = 0;
        for (const [sliderId, valueId] of Object.entries(sliders)) {
            const slider = document.getElementById(sliderId);
            const value = parseInt(slider.value);
            const percentage = value / 100;
            total += percentage;

            document.getElementById(valueId).textContent = 
                percentage.toFixed(2);
        }

        const totalPercent = Math.round(total * 100);
        document.getElementById('weight-total').textContent = `${totalPercent}%`;

        if (Math.abs(total - 1.0) > 0.01) {
            document.getElementById('weight-total').style.color = 'var(--warning-color)';
        } else {
            document.getElementById('weight-total').style.color = 'var(--success)';
        }
    }

    async saveWeights() {
        try {
            const sliders = {
                'explicit_job_posting': 'weight-explicit',
                'hiring_signals': 'weight-signals',
                'company_growth': 'weight-growth',
                'recent_activity': 'weight-activity'
            };

            const weights = {};
            for (const [key, sliderId] of Object.entries(sliders)) {
                weights[key] = parseInt(document.getElementById(sliderId).value) / 100;
            }

            const response = await fetch('/api/config/weights', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ weights })
            });

            const data = await response.json();
            if (response.ok) {
                this.showStatus('weights', '✅ Weights saved successfully', 'success');
            } else {
                this.showStatus('weights', `❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showStatus('weights', `❌ Error: ${error.message}`, 'error');
        }
    }

    resetWeights() {
        if (this.originalConfig.weights) {
            this.loadWeights(this.originalConfig.weights);
            this.showStatus('weights', '↻ Reset to original weights', 'info');
        }
    }

    // ==================== Prompts Management ====================

    loadPrompts(prompts) {
        document.getElementById('prompt-entity-extraction').value = 
            prompts.entity_extraction || '';
        document.getElementById('prompt-hiring-signals').value = 
            prompts.hiring_signals || '';
        document.getElementById('prompt-growth-detection').value = 
            prompts.growth_detection || '';
    }

    async savePrompts() {
        try {
            const prompts = {
                entity_extraction: document.getElementById('prompt-entity-extraction').value,
                hiring_signals: document.getElementById('prompt-hiring-signals').value,
                growth_detection: document.getElementById('prompt-growth-detection').value
            };

            const response = await fetch('/api/config/extraction-prompts', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(prompts)
            });

            const data = await response.json();
            if (response.ok) {
                this.showStatus('prompts', '✅ Prompts saved successfully', 'success');
            } else {
                this.showStatus('prompts', `❌ ${data.error}`, 'error');
            }
        } catch (error) {
            this.showStatus('prompts', `❌ Error: ${error.message}`, 'error');
        }
    }

    resetPrompts() {
        // Load default prompts from server
        this.loadPrompts(this.originalConfig.prompts || {});
        this.showStatus('prompts', '↻ Reset to default prompts', 'info');
    }

    // ==================== Search Control ====================

    async runSearch() {
        const btn = document.getElementById('btn-run-search');
        const statusBox = document.getElementById('search-status');

        try {
            btn.disabled = true;
            btn.textContent = '⏳ Searching...';

            const response = await fetch('/api/search/manual', {
                method: 'POST'
            });

            const data = await response.json();

            if (response.ok) {
                statusBox.className = 'status-box success';
                statusBox.innerHTML = `
                    ✅ ${data.message}<br>
                    Found <strong>${data.results_found}</strong> results
                `;
            } else {
                statusBox.className = 'status-box error';
                statusBox.textContent = `❌ ${data.error}`;
            }
        } catch (error) {
            statusBox.className = 'status-box error';
            statusBox.textContent = `❌ Error: ${error.message}`;
        } finally {
            btn.disabled = false;
            btn.textContent = '▶️ Start Search Now';
        }
    }

    async runCustomSearch() {
        const query = document.getElementById('custom-query').value.trim();
        const statusBox = document.getElementById('custom-search-status');

        if (!query) {
            statusBox.className = 'status-box error';
            statusBox.textContent = '❌ Please enter a search query';
            return;
        }

        try {
            const response = await fetch(`/api/search/manual?query=${encodeURIComponent(query)}`, {
                method: 'POST'
            });

            const data = await response.json();

            if (response.ok) {
                statusBox.className = 'status-box success';
                statusBox.innerHTML = `
                    ✅ ${data.message}<br>
                    Found <strong>${data.results_found}</strong> results
                `;
            } else {
                statusBox.className = 'status-box error';
                statusBox.textContent = `❌ ${data.error}`;
            }
        } catch (error) {
            statusBox.className = 'status-box error';
            statusBox.textContent = `❌ Error: ${error.message}`;
        }
    }

    async processResults() {
        const btn = document.getElementById('btn-process');
        const statusBox = document.getElementById('process-status');

        try {
            btn.disabled = true;
            btn.textContent = '⏳ Processing...';

            const response = await fetch('/api/search/process', {
                method: 'POST'
            });

            const data = await response.json();

            if (response.ok) {
                statusBox.className = 'status-box success';
                statusBox.innerHTML = `
                    ✅ ${data.message}<br>
                    Processed <strong>${data.processed_count}</strong> results
                `;
            } else {
                statusBox.className = 'status-box error';
                statusBox.textContent = `❌ ${data.error}`;
            }
        } catch (error) {
            statusBox.className = 'status-box error';
            statusBox.textContent = `❌ Error: ${error.message}`;
        } finally {
            btn.disabled = false;
            btn.textContent = '⚙️ Process Results';
        }
    }

    // ==================== Utilities ====================

    showStatus(elementId, message, type) {
        const box = document.getElementById(`${elementId}-status`);
        if (box) {
            box.className = `status-box ${type}`;
            box.textContent = message;
        }
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new AdminDashboard();
});
