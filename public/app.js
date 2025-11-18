// API Configuration
const API_BASE_URL = 'http://localhost:5000';

// Update status card with current access information
function updateStatus() {
    fetch(`${API_BASE_URL}/api/ultimo_acesso`)
        .then(response => response.json())
        .then(data => {
            const card = document.getElementById('statusCard');
            
            if (data.status === 'LIBERADO') {
                card.className = 'status-card approved';
                card.innerHTML = `
                    <div class="status-content">
                        <div class="status-icon">
                            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                                <polyline points="22 4 12 14.01 9 11.01"></polyline>
                            </svg>
                        </div>
                        <h2 class="status-title">Acesso Liberado</h2>
                        <p class="status-description">Entrada autorizada com sucesso</p>
                        <div class="status-details">
                            <div class="status-detail-row">
                                <span class="detail-label">ID:</span>
                                <span class="detail-value">${data.id}</span>
                            </div>
                            <div class="status-detail-row">
                                <span class="detail-label">Nome:</span>
                                <span class="detail-value">${data.nome}</span>
                            </div>
                            <div class="status-detail-row">
                                <span class="detail-label">Departamento:</span>
                                <span class="detail-value">${data.departamento}</span>
                            </div>
                            <div class="status-detail-row">
                                <span class="detail-label">Horário:</span>
                                <span class="detail-value">${data.timestamp}</span>
                            </div>
                        </div>
                    </div>
                `;
            } else if (data.status === 'NEGADO') {
                card.className = 'status-card denied';
                card.innerHTML = `
                    <div class="status-content">
                        <div class="status-icon">
                            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="15" y1="9" x2="9" y2="15"></line>
                                <line x1="9" y1="9" x2="15" y2="15"></line>
                            </svg>
                        </div>
                        <h2 class="status-title">Acesso Negado</h2>
                        <p class="status-description">Identificação não autorizada</p>
                        <div class="status-details">
                            <div class="status-detail-row">
                                <span class="detail-label">ID:</span>
                                <span class="detail-value">${data.id}</span>
                            </div>
                            <div class="status-detail-row">
                                <span class="detail-label">Motivo:</span>
                                <span class="detail-value">ID não cadastrado</span>
                            </div>
                            <div class="status-detail-row">
                                <span class="detail-label">Horário:</span>
                                <span class="detail-value">${data.timestamp}</span>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                card.className = 'status-card waiting';
                card.innerHTML = `
                    <div class="status-content">
                        <div class="status-icon">
                            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <polyline points="12 6 12 12 16 14"></polyline>
                            </svg>
                        </div>
                        <h2 class="status-title">Aguardando Identificação</h2>
                        <p class="status-description">Insira um ID para verificar o acesso</p>
                    </div>
                `;
            }
        })
        .catch(error => console.error('Erro ao buscar status:', error));
}

// Update history list
function updateHistory() {
    fetch(`${API_BASE_URL}/api/historico_recente`)
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById('historicoLista');
            
            if (data.historico.length === 0) {
                lista.innerHTML = `
                    <div class="empty-state">
                        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M3 3h18v18H3zM3 9h18M9 21V9"></path>
                        </svg>
                        <p>Nenhum acesso registrado ainda</p>
                    </div>
                `;
                return;
            }
            
            lista.innerHTML = '';
            
            data.historico.slice(0, 10).forEach(item => {
                const statusClass = item.status.toLowerCase() === 'liberado' ? 'approved' : 'denied';
                const statusText = item.status.toLowerCase() === 'liberado' ? 'Liberado' : 'Negado';
                
                const div = document.createElement('div');
                div.className = `history-item ${statusClass}`;
                div.innerHTML = `
                    <div class="history-info">
                        <div class="history-id">ID: ${item.id}</div>
                        <div class="history-name">${item.nome}</div>
                        <div class="history-time">${item.timestamp}</div>
                    </div>
                    <div class="history-badge ${statusClass}">${statusText}</div>
                `;
                lista.appendChild(div);
            });
        })
        .catch(error => console.error('Erro ao buscar histórico:', error));
}

// Update statistics
function updateStatistics() {
    fetch(`${API_BASE_URL}/api/estatisticas`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalAcessos').textContent = data.total;
            document.getElementById('liberados').textContent = data.liberados;
            document.getElementById('negados').textContent = data.negados;
        })
        .catch(error => console.error('Erro ao buscar estatísticas:', error));
}

// Initialize and set up auto-refresh
function init() {
    updateStatus();
    updateHistory();
    updateStatistics();
    
    // Auto-refresh every 1 second
    setInterval(() => {
        updateStatus();
        updateHistory();
        updateStatistics();
    }, 1000);
}

// Start application when DOM is ready
document.addEventListener('DOMContentLoaded', init);
