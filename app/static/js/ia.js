/**
 * IA Chat Assistant
 * Professional chat functionality with responsive design
 */

class IAChatAssistant {
    constructor() {
        // DOM Elements
        this.elements = {
            chatMessages: document.getElementById('chat-messages'),
            chatForm: document.getElementById('chat-form'),
            chatInput: document.getElementById('chat-input'),
            sendButton: document.getElementById('send-button'),
            typingStatus: document.getElementById('typing-status'),
            popularQuestions: document.querySelectorAll('.popular-question'),
            popularContainer: document.getElementById('popular-questions-container'),
            welcomeMessage: document.getElementById('welcome-message')
        };

        // State
        this.isFirstMessage = true;
        this.isProcessing = false;
        this.messageHistory = [];

        // Configuration
        this.config = {
            maxMessageLength: 500,
            typingDelay: 300,
            scrollBehavior: 'smooth',
            apiEndpoint: '/ia-chat/chat'
        };

        // Initialize
        this.init();
    }

    /**
     * Initialize the chat assistant
     */
    init() {
        this.setupEventListeners();
        this.setupResizeObserver();
        this.focusInput();
        this.checkViewport();
    }

    /**
     * Setup all event listeners
     */
    setupEventListeners() {
        // Form submission
        if (this.elements.chatForm) {
            this.elements.chatForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.handleSubmit();
            });
        }

        // Popular questions
        if (this.elements.popularQuestions) {
            this.elements.popularQuestions.forEach(btn => {
                btn.addEventListener('click', () => {
                    const questionText = this.extractQuestionText(btn);
                    this.sendMessage(questionText);
                });
                
                // Touch optimization
                btn.addEventListener('touchstart', (e) => {
                    e.preventDefault();
                }, { passive: true });
            });
        }

        // Input events
        if (this.elements.chatInput) {
            this.elements.chatInput.addEventListener('input', () => {
                this.autoResizeInput();
            });
            
            this.elements.chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.handleSubmit();
                }
            });
        }

        // Window events
        window.addEventListener('resize', () => {
            this.debounce(this.handleResize.bind(this), 250);
        });

        window.addEventListener('orientationchange', () => {
            this.handleOrientationChange();
        });
    }

    /**
     * Handle form submission
     */
    async handleSubmit() {
        const message = this.elements.chatInput.value.trim();
        if (message && !this.isProcessing) {
            await this.sendMessage(message);
            this.elements.chatInput.value = '';
            this.resetInputHeight();
        }
    }

    /**
     * Send a message to the API
     */
    async sendMessage(message) {
        // Validate message
        if (!this.validateMessage(message)) {
            this.addMessage('Please enter a valid question (1-500 characters).', 'bot');
            return;
        }

        // Remove popular questions on first message
        if (this.isFirstMessage) {
            this.removePopularQuestions();
            this.isFirstMessage = false;
        }

        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Disable input and show typing indicator
        this.setInputState(true);
        this.showTypingIndicator();

        // Send to API
        const response = await this.callAPI(message);
        
        // Hide typing indicator
        this.hideTypingIndicator();

        // Handle response
        if (response.success) {
            this.addMessage(response.data.respuesta, 'bot');
        } else {
            this.addMessage(`⚠️ ${response.error}`, 'bot');
        }

        // Re-enable input
        this.setInputState(false);
        this.focusInput();
    }

    /**
     * Call the chat API
     */
    async callAPI(message) {
        try {
            const response = await fetch(this.config.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ pregunta: message })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('API Error:', error);
            return { 
                success: false, 
                error: 'Connection error. Please try again.' 
            };
        }
    }

    /**
     * Add a message to the chat
     */
    addMessage(message, sender) {
        const messageDiv = this.createMessageElement(message, sender);
        this.elements.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
        
        // Save to history
        this.messageHistory.push({ message, sender, timestamp: new Date() });
    }

    /**
     * Create a message element
     */
    createMessageElement(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message';
        
        const time = this.formatTime(new Date());
        
        if (sender === 'user') {
            messageDiv.innerHTML = `
                <div class="user-content">
                    <p>${this.escapeHtml(message)}</p>
                    <div class="message-time">
                        <i class="far fa-clock"></i>
                        <span>${time}</span>
                    </div>
                </div>
                <div class="user-avatar">
                    <i class="fas fa-user"></i>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="bot-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="bot-content">
                    <p>${this.escapeHtml(message)}</p>
                    <div class="message-time">
                        <i class="far fa-clock"></i>
                        <span>${time}</span>
                    </div>
                </div>
            `;
        }
        
        return messageDiv;
    }

    /**
     * Remove popular questions with animation
     */
    removePopularQuestions() {
        if (this.elements.popularContainer) {
            this.elements.popularContainer.classList.add('fade-out');
            
            setTimeout(() => {
                if (this.elements.popularContainer) {
                    this.elements.popularContainer.remove();
                }
            }, 300);
        }
    }

    /**
     * Set input state (enabled/disabled)
     */
    setInputState(disabled) {
        this.isProcessing = disabled;
        if (this.elements.chatInput) {
            this.elements.chatInput.disabled = disabled;
        }
        if (this.elements.sendButton) {
            this.elements.sendButton.disabled = disabled;
        }
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        if (this.elements.typingStatus) {
            this.elements.typingStatus.classList.remove('hidden');
            this.scrollToBottom();
        }
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        if (this.elements.typingStatus) {
            this.elements.typingStatus.classList.add('hidden');
        }
    }

    /**
     * Scroll to bottom of chat
     */
    scrollToBottom() {
        if (this.elements.chatMessages) {
            this.elements.chatMessages.scrollTo({
                top: this.elements.chatMessages.scrollHeight,
                behavior: this.config.scrollBehavior
            });
        }
    }

    /**
     * Focus input field
     */
    focusInput() {
        if (this.elements.chatInput && !this.isProcessing) {
            setTimeout(() => {
                this.elements.chatInput.focus();
            }, 100);
        }
    }

    /**
     * Auto-resize input field
     */
    autoResizeInput() {
        const input = this.elements.chatInput;
        if (input) {
            input.style.height = 'auto';
            input.style.height = input.scrollHeight + 'px';
        }
    }

    /**
     * Reset input height
     */
    resetInputHeight() {
        if (this.elements.chatInput) {
            this.elements.chatInput.style.height = 'auto';
        }
    }

    /**
     * Extract question text from button
     */
    extractQuestionText(button) {
        const textSpan = button.querySelector('.popular-question-text span') || 
                        button.querySelector('span span') || 
                        button.querySelector('span');
        return textSpan ? textSpan.textContent.trim() : button.textContent.trim();
    }

    /**
     * Validate message
     */
    validateMessage(message) {
        if (!message || !message.trim()) return false;
        if (message.length > this.config.maxMessageLength) return false;
        return true;
    }

    /**
     * Format timestamp
     */
    formatTime(date) {
        return date.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
        });
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Check viewport and adjust layout
     */
    checkViewport() {
        this.handleResize();
    }

    /**
     * Handle window resize
     */
    handleResize() {
        // Adjust chat height for different devices
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
        
        // Ensure messages are visible
        this.scrollToBottom();
    }

    /**
     * Handle orientation change
     */
    handleOrientationChange() {
        // Small delay for orientation change to complete
        setTimeout(() => {
            this.handleResize();
            this.scrollToBottom();
        }, 100);
    }

    /**
     * Setup resize observer for chat container
     */
    setupResizeObserver() {
        if (window.ResizeObserver && this.elements.chatMessages) {
            const observer = new ResizeObserver(() => {
                this.scrollToBottom();
            });
            
            observer.observe(this.elements.chatMessages);
        }
    }

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.chatAssistant = new IAChatAssistant();
});

// Re-initialize on page show (for bfcache)
window.addEventListener('pageshow', () => {
    if (window.chatAssistant) {
        window.chatAssistant.focusInput();
        window.chatAssistant.checkViewport();
    }
});