// Relationships Graph Visualization JavaScript

let network = null;

document.addEventListener('DOMContentLoaded', function() {
    loadGraphData();
});

async function loadGraphData() {
    try {
        const response = await fetch('/api/graph');
        const data = await response.json();

        // Update statistics
        document.getElementById('total-nodes').textContent = data.stats.total_nodes;
        document.getElementById('total-edges').textContent = data.stats.total_edges;
        document.getElementById('company-nodes').textContent = data.stats.companies;
        document.getElementById('opportunity-nodes').textContent = data.stats.opportunities;
        document.getElementById('signal-nodes').textContent = data.stats.signals;

        // Load multi-signal companies table
        loadMultiSignalTable(data.multi_signal_companies);

        // Initialize graph visualization
        initializeGraph(data.nodes, data.edges);
    } catch (error) {
        console.error('Error loading graph data:', error);
        document.getElementById('graph-container').innerHTML = '<p style="padding: 20px; text-align: center;">Error loading graph data. Please refresh the page.</p>';
    }
}

function initializeGraph(nodes, edges) {
    const container = document.getElementById('graph-container');

    // Create a DataSet for nodes and edges
    const nodesDataSet = new vis.DataSet(nodes.map(node => ({
        id: node.id,
        label: node.label,
        color: {
            background: node.color,
            border: darkenColor(node.color, 20),
            highlight: {
                background: lightenColor(node.color, 20),
                border: darkenColor(node.color, 40)
            }
        },
        shape: node.shape,
        font: {
            color: '#ffffff',
            size: 14,
            face: 'Arial'
        }
    })));

    const edgesDataSet = new vis.DataSet(edges.map(edge => ({
        from: edge.from,
        to: edge.to,
        label: edge.label,
        arrows: edge.arrows,
        color: {
            color: '#94a3b8',
            highlight: '#2563eb'
        },
        font: {
            size: 10,
            align: 'middle'
        }
    })));

    // Network options
    const options = {
        nodes: {
            borderWidth: 2,
            size: 25,
            font: {
                size: 14,
                color: '#ffffff'
            }
        },
        edges: {
            width: 2,
            smooth: {
                type: 'continuous'
            }
        },
        physics: {
            enabled: true,
            barnesHut: {
                gravitationalConstant: -2000,
                centralGravity: 0.3,
                springLength: 150,
                springConstant: 0.04,
                damping: 0.09,
                avoidOverlap: 0.5
            },
            stabilization: {
                iterations: 100,
                updateInterval: 25
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 200,
            navigationButtons: true,
            keyboard: true
        },
        layout: {
            improvedLayout: true,
            hierarchical: false
        }
    };

    // Create network
    network = new vis.Network(container, {
        nodes: nodesDataSet,
        edges: edgesDataSet
    }, options);

    // Add click event
    network.on('click', function(params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = nodesDataSet.get(nodeId);
            console.log('Clicked node:', node);
            // Could add a modal or details panel here
        }
    });

    // Add stabilization progress
    network.on('stabilizationProgress', function(params) {
        const progress = Math.round((params.iterations / params.total) * 100);
        container.style.opacity = '0.7';
    });

    network.once('stabilizationIterationsDone', function() {
        container.style.opacity = '1';
    });
}

function loadMultiSignalTable(companies) {
    const tbody = document.getElementById('multi-signal-tbody');

    if (!companies || companies.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4">No companies with multiple signals found.</td></tr>';
        return;
    }

    // We need to fetch company details to show full information
    Promise.all(companies.map(comp =>
        fetch('/api/companies?limit=100')
            .then(r => r.json())
            .then(allCompanies => allCompanies.find(c => c.id == comp.id))
    )).then(companyDetails => {
        tbody.innerHTML = companyDetails.filter(c => c).map((company, index) => {
            const signalCount = companies[index].signal_count;
            return `
                <tr>
                    <td><strong>${escapeHtml(company.name)}</strong></td>
                    <td>${signalCount}</td>
                    <td>${company.active_opportunities}</td>
                    <td>${getScoreBadge(company.score)}</td>
                </tr>
            `;
        }).join('');
    }).catch(error => {
        console.error('Error loading multi-signal companies:', error);
        tbody.innerHTML = '<tr><td colspan="4">Error loading company details.</td></tr>';
    });
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

// Color utility functions
function darkenColor(color, amount) {
    return adjustColor(color, -amount);
}

function lightenColor(color, amount) {
    return adjustColor(color, amount);
}

function adjustColor(color, amount) {
    const usePound = color[0] === '#';
    const col = usePound ? color.slice(1) : color;
    const num = parseInt(col, 16);
    let r = (num >> 16) + amount;
    let g = ((num >> 8) & 0x00FF) + amount;
    let b = (num & 0x0000FF) + amount;

    r = Math.max(Math.min(255, r), 0);
    g = Math.max(Math.min(255, g), 0);
    b = Math.max(Math.min(255, b), 0);

    return (usePound ? '#' : '') + (g | (b << 8) | (r << 16)).toString(16).padStart(6, '0');
}
