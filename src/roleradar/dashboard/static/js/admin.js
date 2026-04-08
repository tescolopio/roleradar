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
        await this.loadDataStatistics();
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
        document.getElementById('btn-show-brave')?.addEventListener('click', () => this.togglePasswordField('brave-key'));
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
        
        // Results
        document.getElementById('btn-refresh-results')?.addEventListener('click', () => this.loadSearchResults());
        document.getElementById('results-filter')?.addEventListener('input', () => this.loadSearchResults());
        document.getElementById('show-processed-only')?.addEventListener('change', () => this.loadSearchResults());

        // Data Management
        this.setupDataManagementListeners();
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
            'results': '🔍 Search Results',
            'weights': '⚖️ Weights',
            'system': '🔧 System'
        };

        document.getElementById('section-title').textContent = titles[sectionId] || 'Dashboard';
        this.currentSection = sectionId;
        
        // Load data for specific sections
        if (sectionId === 'results') {
            this.loadSearchResults();
        }
    }

    // ==================== Credentials Management ====================

    async loadCredentialsStatus() {
        try {
            const response = await fetch('/api/credentials/status');
            const data = await response.json();

            // Update credential status indicators
            document.getElementById('tavily-check').textContent = 
                data.tavily_configured ? '✅ Configured' : '⚠️ Not Set';
            document.getElementById('brave-check').textContent = 
                data.brave_configured ? '✅ Configured' : '⚠️ Not Set';
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

                if (data.results.brave) {
                    const brave = data.results.brave;
                    const braveStatus = document.getElementById('brave-status');
                    braveStatus.className = `credential-status ${brave.status === 'valid' ? 'success' : 'error'}`;
                    braveStatus.textContent = `${brave.status === 'valid' ? '✅' : '❌'} ${brave.message}`;
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
            const braveKey = document.getElementById('brave-key').value.trim();
            const groqKey = document.getElementById('groq-key').value.trim();
            const databaseUrl = document.getElementById('database-url').value.trim();

            if (!tavilyKey && !braveKey && !groqKey && !databaseUrl) {
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
                    brave_api_key: braveKey,
                    groq_api_key: groqKey,
                    database_url: databaseUrl
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showStatus('credentials', `✅ ${data.message}`, 'success');
                
                // Clear password fields after successful save
                document.getElementById('tavily-key').value = '';
                document.getElementById('brave-key').value = '';
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
            
            statusBox.className = 'status-box info';
            statusBox.innerHTML = '🔄 Starting processing...';

            const eventSource = new EventSource('/api/search/process');
            
            eventSource.onmessage = (event) => {
                const data = JSON.parse(event.data);
                
                if (data.type === 'start') {
                    statusBox.innerHTML = `
                        🔄 Processing <strong>${data.total}</strong> results...<br>
                        <div class="progress-bar">
                            <div class="progress-fill" id="progress-fill" style="width: 0%"></div>
                        </div>
                        <small id="current-item"></small>
                    `;
                } else if (data.type === 'progress') {
                    const percent = ((data.processed / data.total) * 100).toFixed(1);
                    const progressBar = document.getElementById('progress-fill');
                    const currentItem = document.getElementById('current-item');
                    
                    if (progressBar) {
                        progressBar.style.width = `${percent}%`;
                    }
                    if (currentItem) {
                        currentItem.textContent = `${data.processed}/${data.total}: ${data.current.title}`;
                    }
                } else if (data.type === 'error') {
                    const currentItem = document.getElementById('current-item');
                    if (currentItem) {
                        currentItem.innerHTML = `<span style="color: orange;">⚠️ Error on result ${data.result_id}: ${data.error}</span>`;
                    }
                } else if (data.type === 'complete') {
                    eventSource.close();
                    statusBox.className = 'status-box success';
                    statusBox.innerHTML = `
                        ✅ Processing complete!<br>
                        Processed <strong>${data.processed}</strong> of <strong>${data.total}</strong> results
                    `;
                    btn.disabled = false;
                    btn.textContent = '⚙️ Process Results';
                } else if (data.type === 'fatal_error') {
                    eventSource.close();
                    statusBox.className = 'status-box error';
                    statusBox.textContent = `❌ Fatal error: ${data.error}`;
                    btn.disabled = false;
                    btn.textContent = '⚙️ Process Results';
                }
            };
            
            eventSource.onerror = () => {
                eventSource.close();
                statusBox.className = 'status-box error';
                statusBox.textContent = '❌ Connection lost. Please refresh and try again.';
                btn.disabled = false;
                btn.textContent = '⚙️ Process Results';
            };
            
        } catch (error) {
            statusBox.className = 'status-box error';
            statusBox.textContent = `❌ Error: ${error.message}`;
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
    
    // ==================== Search Results Transparency ====================
    
    async loadSearchResults() {
        const container = document.getElementById('results-container');
        if (!container) return;
        
        try {
            container.innerHTML = '<div class="loading">Loading search results...</div>';
            
            const filter = document.getElementById('results-filter')?.value || '';
            const processedOnly = document.getElementById('show-processed-only')?.checked || false;
            
            let url = `/api/search-results?limit=100`;
            if (filter) url += `&query=${encodeURIComponent(filter)}`;
            if (processedOnly) url += `&processed=true`;
            
            const response = await fetch(url);
            const results = await response.json();
            
            if (results.length === 0) {
                container.innerHTML = '<div class="info-box">No search results found. Run a search to see data.</div>';
                return;
            }
            
            container.innerHTML = results.map(r => this.renderSearchResult(r)).join('');
            
            // Add click handlers for detail view
            container.querySelectorAll('.result-card').forEach(card => {
                card.addEventListener('click', () => {
                    const resultId = card.getAttribute('data-result-id');
                    this.showResultDetail(resultId);
                });
            });
        } catch (error) {
            container.innerHTML = `<div class="error">Error loading results: ${error.message}</div>`;
        }
    }
    
    renderSearchResult(result) {
        const processed = result.processed ? '✅' : '⏳';
        const hasSignal = result.signal.detected ? '🚨' : '';
        const hasError = result.error ? '⚠️' : '';
        
        return `
            <div class="result-card" data-result-id="${result.id}">
                <div class="result-header">
                    <div class="result-title">
                        <strong>${this.escapeHtml(result.title)}</strong>
                        <span class="result-badges">${processed} ${hasSignal} ${hasError}</span>
                    </div>
                    <div class="result-meta">
                        Query: <em>${this.escapeHtml(result.query)}</em> | 
                        Retrieved: ${this.formatDate(result.retrieved_date)}
                    </div>
                </div>
                
                ${result.processed ? `
                    <div class="result-extraction">
                        <div class="extraction-item">
                            <strong>Company:</strong> ${this.escapeHtml(result.extraction.company) || 'None'}
                        </div>
                        <div class="extraction-item">
                            <strong>Job Title:</strong> ${this.escapeHtml(result.extraction.job_title) || 'None'}
                        </div>
                        <div class="extraction-item">
                            <strong>Role Type:</strong> ${this.escapeHtml(result.extraction.role_type) || 'None'}
                        </div>
                        ${result.signal.detected ? `
                            <div class="extraction-item signal">
                                <strong>Signal:</strong> ${this.escapeHtml(result.signal.type)} 
                                (${Math.round(result.signal.confidence * 100)}% confidence)
                            </div>
                        ` : ''}
                    </div>
                ` : '<div class="result-pending">Not yet processed</div>'}
                
                ${result.error ? `<div class="result-error">❌ ${this.escapeHtml(result.error)}</div>` : ''}
            </div>
        `;
    }
    
    async showResultDetail(resultId) {
        try {
            const response = await fetch(`/api/search-result/${resultId}`);
            const result = await response.json();
            
            // Create modal or expanded view
            const modal = document.createElement('div');
            modal.className = 'result-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>Search Result Details</h3>
                        <button class="btn-close" onclick="this.closest('.result-modal').remove()">✕</button>
                    </div>
                    <div class="modal-body">
                        <h4>${this.escapeHtml(result.title)}</h4>
                        <p><strong>URL:</strong> <a href="${result.url}" target="_blank">${result.url}</a></p>
                        <p><strong>Query:</strong> ${this.escapeHtml(result.query)}</p>
                        
                        <h5>Original Content</h5>
                        <div class="content-box">${this.escapeHtml(result.content)}</div>
                        
                        <h5>AI Extraction</h5>
                        <table class="extraction-table">
                            <tr><td><strong>Company:</strong></td><td>${this.escapeHtml(result.extraction.company) || 'None'}</td></tr>
                            <tr><td><strong>Job Title:</strong></td><td>${this.escapeHtml(result.extraction.job_title) || 'None'}</td></tr>
                            <tr><td><strong>Role Type:</strong></td><td>${this.escapeHtml(result.extraction.role_type) || 'None'}</td></tr>
                            <tr><td><strong>Location:</strong></td><td>${this.escapeHtml(result.extraction.location) || 'None'}</td></tr>
                            <tr><td><strong>Keywords:</strong></td><td>${result.extraction.keywords.join(', ') || 'None'}</td></tr>
                        </table>
                        
                        ${result.signal.detected ? `
                            <h5>Hiring Signal Detected 🚨</h5>
                            <table class="extraction-table">
                                <tr><td><strong>Type:</strong></td><td>${this.escapeHtml(result.signal.type)}</td></tr>
                                <tr><td><strong>Confidence:</strong></td><td>${Math.round(result.signal.confidence * 100)}%</td></tr>
                                <tr><td><strong>Description:</strong></td><td>${this.escapeHtml(result.signal.description)}</td></tr>
                            </table>
                        ` : '<p><em>No hiring signals detected</em></p>'}
                        
                        ${result.error ? `
                            <h5>Processing Error ⚠️</h5>
                            <div class="error-box">${this.escapeHtml(result.error)}</div>
                        ` : ''}
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        } catch (error) {
            alert(`Error loading details: ${error.message}`);
        }
    }
    
    formatDate(dateString) {
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        return date.toLocaleString();
    }
    
    escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return String(text).replace(/[&<>"']/g, m => map[m]);
    }

    // Data Management Functions
    async loadDataStatistics() {
        try {
            const response = await fetch('/api/companies');
            const companies = await response.json();
            document.getElementById('stat-companies').textContent = companies.length;

            const oppResponse = await fetch('/api/opportunities');
            const opportunities = await oppResponse.json();
            document.getElementById('stat-opportunities').textContent = opportunities.length;

            const signalResponse = await fetch('/api/hiring-signals');
            const signals = await signalResponse.json();
            document.getElementById('stat-signals').textContent = signals.length;

            // Populate company select dropdown
            const select = document.getElementById('company-select');
            const options = companies.map(c => `<option value="${c.id}">${c.name} (Score: ${c.score.toFixed(1)})</option>`);
            select.innerHTML = '<option value="">-- Select a company --</option>' + options.join('');

            // Enable delete button if there are companies
            document.getElementById('btn-delete-company').disabled = companies.length === 0;
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }

    setupDataManagementListeners() {
        document.getElementById('btn-clear-all')?.addEventListener('click', () => this.clearAllData());
        document.getElementById('btn-delete-company')?.addEventListener('click', () => this.deleteSelectedCompany());
    }

    async clearAllData() {
        if (!confirm('⚠️ This will delete ALL data (companies, opportunities, signals). This cannot be undone. Are you sure?')) {
            return;
        }

        try {
            const response = await fetch('/api/data/clear', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (response.ok) {
                const statusEl = document.getElementById('clear-status');
                statusEl.className = 'status-box success';
                statusEl.innerHTML = `
                    <strong>✓ Data cleared successfully</strong><br>
                    Deleted: ${result.deleted.companies} companies,
                    ${result.deleted.opportunities} opportunities,
                    ${result.deleted.signals} signals
                `;

                // Refresh statistics
                await this.loadDataStatistics();
            } else {
                throw new Error(result.error || 'Failed to clear data');
            }
        } catch (error) {
            const statusEl = document.getElementById('clear-status');
            statusEl.className = 'status-box error';
            statusEl.textContent = `❌ Error: ${error.message}`;
        }
    }

    async deleteSelectedCompany() {
        const select = document.getElementById('company-select');
        const companyId = select.value;
        const companyName = select.options[select.selectedIndex].text;

        if (!companyId) {
            alert('Please select a company');
            return;
        }

        if (!confirm(`Delete "${companyName}" and all its data? This cannot be undone.`)) {
            return;
        }

        try {
            const response = await fetch(`/api/data/delete-company/${companyId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (response.ok) {
                const statusEl = document.getElementById('delete-company-status');
                statusEl.className = 'status-box success';
                statusEl.textContent = `✓ ${result.message}`;

                // Refresh statistics
                await this.loadDataStatistics();
            } else {
                throw new Error(result.error || 'Failed to delete company');
            }
        } catch (error) {
            const statusEl = document.getElementById('delete-company-status');
            statusEl.className = 'status-box error';
            statusEl.textContent = `❌ Error: ${error.message}`;
        }
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    new AdminDashboard();
});
