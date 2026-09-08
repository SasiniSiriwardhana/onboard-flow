// Customer Onboarding SaaS Frontend Logic

// Alpine Store for global UI notifications & toast state
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
