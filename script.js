/**
 * NewsVerify AI Frontend JavaScript
 * Handles API calls, UI interactions, and dynamic content loading
 */

// Configuration
const API_BASE_URL = 'https://newsradar-production.up.railway.app';
const DEBOUNCE_TIME = 300;

// DOM Elements
const elements = {
    // Tabs
    tabButtons: document.querySelectorAll('.tab-btn'),
    tabPanes: document.querySelectorAll('.tab-pane'),

    // Predictor
    predictForm: document.getElementById('predictForm'),
    newsInput: document.getElementById('newsInput'),
    charCount: document.getElementById('charCount'),
    resultSection: document.getElementById('resultSection'),
    resultCard: document.getElementById('resultCard'),
    loadingSpinner: document.getElementById('loadingSpinner'),
    errorMessage: document.getElementById('errorMessage'),

    // Dashboard
    dashboardContent: document.getElementById('dashboardContent'),

    // History
    historyContent: document.getElementById('historyContent'),
    clearHistoryBtn: document.getElementById('clearHistoryBtn'),
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadDashboard();
    loadHistory();
});

/**
 * Initialize all event listeners
 */
function initializeEventListeners() {
    // Tab navigation
    elements.tabButtons.forEach(btn => {
        btn.addEventListener('click', handleTabClick);
    });

    // Form submission
    elements.predictForm.addEventListener('submit', handlePredictSubmit);

    // Character count
    elements.newsInput.addEventListener('input', updateCharCount);

    // Clear history
    elements.clearHistoryBtn.addEventListener('click', handleClearHistory);
}

/**
 * Handle tab switching
 */
function handleTabClick(e) {
    const tabName = e.currentTarget.dataset.tab;

    // Update active tab button
    elements.tabButtons.forEach(btn => btn.classList.remove('active'));
    e.currentTarget.classList.add('active');

    // Update active tab pane
    elements.tabPanes.forEach(pane => pane.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');

    // Load content when switching to dashboard or history
    if (tabName === 'dashboard') {
        loadDashboard();
    } else if (tabName === 'history') {
        loadHistory();
    }
}

/**
 * Update character count display
 */
function updateCharCount() {
    const count = elements.newsInput.value.length;
    elements.charCount.textContent = count;
}

/**
 * Handle form submission for prediction
 */
async function handlePredictSubmit(e) {
    e.preventDefault();

    const text = elements.newsInput.value.trim();

    // Clear previous messages
    hideError();
    hideResult();

    // Validate input
    if (!text) {
        showError('Please enter some text to analyze');
        return;
    }

    if (text.length < 10) {
        showError('Text must be at least 10 characters long');
        return;
    }

    // Show loading spinner
    showSpinner();

    try {
        // Make API call
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'An error occurred');
        }

        // Display result
        hideSpinner();
        displayResult(data, text);

        // Clear form
        elements.newsInput.value = '';
        updateCharCount();

        // Reload dashboard and history
        loadDashboard();
        loadHistory();

    } catch (error) {
        hideSpinner();
        console.error('Error:', error);
        showError(error.message || 'Failed to analyze text. Please try again.');
    }
}

/**
 * Display prediction result
 */
function displayResult(data, originalText) {
    const { prediction, confidence, message } = data;
    const isPredictionFake = prediction === 'FAKE';

    const resultHTML = `
        <div class="result-label ${isPredictionFake ? 'fake' : 'real'}">
            ${isPredictionFake ? '⚠️ Warning' : '✓ Verified'}
        </div>
        <h3 class="result-title ${isPredictionFake ? 'fake' : 'real'}">
            ${prediction}
        </h3>
        <div class="result-confidence">
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${confidence}%"></div>
            </div>
            <div class="confidence-text">${confidence}%</div>
        </div>
        <p class="result-message">${message}</p>
        <p class="result-message" style="margin-top: 15px; color: #6b7280; font-size: 0.9rem;">
            <strong>Original Text:</strong> ${escapeHtml(originalText.substring(0, 200))}${originalText.length > 200 ? '...' : ''}
        </p>
    `;

    elements.resultCard.innerHTML = resultHTML;
    elements.resultCard.className = `result-card ${isPredictionFake ? 'fake' : 'real'}`;
    showResult();
}

/**
 * Load dashboard statistics
 */
async function loadDashboard() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/dashboard`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to load dashboard');
        }

        displayDashboard(data);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        elements.dashboardContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📊</div>
                <p>Unable to load dashboard. Please try again.</p>
            </div>
        `;
    }
}

/**
 * Display dashboard content
 */
function displayDashboard(data) {
    const { total_predictions, stats, recent_predictions } = data;

    let statsHTML = `
        <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-number">${total_predictions}</div>
            <div class="stat-label">Total Analyses</div>
        </div>
    `;

    // Add FAKE stats
    if (stats.FAKE !== undefined) {
        statsHTML += `
            <div class="stat-card fake">
                <div class="stat-icon">⚠️</div>
                <div class="stat-number">${stats.FAKE}</div>
                <div class="stat-label">Fake News Detected</div>
            </div>
        `;
    }

    // Add REAL stats
    if (stats.REAL !== undefined) {
        statsHTML += `
            <div class="stat-card real">
                <div class="stat-icon">✓</div>
                <div class="stat-number">${stats.REAL}</div>
                <div class="stat-label">Real News Verified</div>
            </div>
        `;
    }

    // Add recent predictions section
    if (recent_predictions && recent_predictions.length > 0) {
        statsHTML += `
            <div style="grid-column: 1 / -1;">
                <div class="recent-section">
                    <h3>Recent Predictions</h3>
                    <div>
                        ${recent_predictions.map(pred => `
                            <div class="recent-item ${pred.prediction === 'FAKE' ? 'fake' : 'real'}">
                                <div class="recent-info">
                                    <div class="recent-text">${escapeHtml(pred.text.substring(0, 100))}...</div>
                                    <div class="recent-meta">${formatDate(pred.created_at)}</div>
                                </div>
                                <div class="recent-badge ${pred.prediction === 'FAKE' ? 'fake' : 'real'}">
                                    ${pred.prediction} (${(pred.confidence * 100).toFixed(1)}%)
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    elements.dashboardContent.innerHTML = statsHTML;
}

/**
 * Load prediction history
 */
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/history?limit=50`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to load history');
        }

        displayHistory(data.predictions);
    } catch (error) {
        console.error('Error loading history:', error);
        elements.historyContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📜</div>
                <p>Unable to load history. Please try again.</p>
            </div>
        `;
    }
}

/**
 * Display prediction history
 */
function displayHistory(predictions) {
    if (!predictions || predictions.length === 0) {
        elements.historyContent.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📜</div>
                <p>No predictions yet. Start analyzing news articles to build your history!</p>
            </div>
        `;
        return;
    }

    const historyHTML = predictions.map(pred => `
        <div class="history-item ${pred.prediction === 'FAKE' ? 'fake' : 'real'}">
            <div class="history-text">${escapeHtml(pred.text)}</div>
            <div class="history-meta">
                <span>${formatDate(pred.created_at)}</span>
                <div>
                    <span class="history-badge ${pred.prediction === 'FAKE' ? 'fake' : 'real'}">
                        ${pred.prediction}
                    </span>
                    <span style="margin-left: 10px; color: #6b7280;">
                        Confidence: ${(pred.confidence * 100).toFixed(1)}%
                    </span>
                </div>
            </div>
        </div>
    `).join('');

    elements.historyContent.innerHTML = historyHTML;
}

/**
 * Handle clear history button
 */
async function handleClearHistory() {
    if (!confirm('Are you sure you want to clear all prediction history? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/clear`, {
            method: 'POST',
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to clear history');
        }

        // Reload history
        loadHistory();
        loadDashboard();

        // Show success message
        showSuccessMessage('History cleared successfully!');

    } catch (error) {
        console.error('Error clearing history:', error);
        showError('Failed to clear history. Please try again.');
    }
}

/**
 * UI Helper Functions
 */

function showResult() {
    elements.resultSection.classList.remove('hidden');
}

function hideResult() {
    elements.resultSection.classList.add('hidden');
}

function showSpinner() {
    elements.loadingSpinner.classList.remove('hidden');
}

function hideSpinner() {
    elements.loadingSpinner.classList.add('hidden');
}

function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorMessage.classList.remove('hidden');
}

function hideError() {
    elements.errorMessage.classList.add('hidden');
}

function showSuccessMessage(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'alert alert-success';
    successDiv.textContent = message;
    elements.historyContent.parentElement.insertBefore(successDiv, elements.historyContent);

    setTimeout(() => {
        successDiv.remove();
    }, 3000);
}

/**
 * Utility Functions
 */

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function formatDate(dateString) {
    try {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays === 0) {
            const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
            if (diffHours === 0) {
                return 'Just now';
            }
            return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        } else if (diffDays === 1) {
            return 'Yesterday';
        } else if (diffDays < 7) {
            return `${diffDays} days ago`;
        } else {
            return date.toLocaleDateString();
        }
    } catch (error) {
        return dateString;
    }
}
