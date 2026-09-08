// Customer Onboarding SaaS Frontend Logic
document.addEventListener('DOMContentLoaded', () => {
    // Configure HTMX global error handling
    document.body.addEventListener('htmx:responseError', (event) => {
        console.error('HTMX Request Failed:', event.detail);
        if (window.Alpine) {
            window.Alpine.store('notifications').notify(
                'Action failed: Could not communicate with server.',
                'error'
            );
        }
    });

    // Notify after successful HTMX creation
    document.body.addEventListener('htmx:afterOnLoad', (event) => {
        if (event.detail.target && event.detail.target.id === 'projects-table-body') {
            console.log('Project table refreshed');
        }
    });
});

// Alpine Store for global UI state
document.addEventListener('alpine:init', () => {
    Alpine.store('notifications', {
        items: [],
        notify(message, type = 'info') {
            const id = Date.now();
            this.items.push({ id, message, type });
            setTimeout(() => {
                this.items = this.items.filter(item => item.id !== id);
            }, 4000);
        }
    });
});
