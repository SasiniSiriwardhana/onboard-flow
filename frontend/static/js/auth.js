/**
 * OnboardFlow Authentication & Client State Handler
 * Supports JWT localStorage persistence, HTMX bearer header injection,
 * client-side route guards, and Alpine.js reactive store integration.
 */

const TOKEN_KEY = 'onboardflow_token';
const USER_KEY = 'onboardflow_user';

// Core Token Helpers
function getToken() {
    return localStorage.getItem(TOKEN_KEY);
}

function getUser() {
    try {
        const u = localStorage.getItem(USER_KEY);
        return u ? JSON.parse(u) : null;
    } catch (e) {
        return null;
    }
}

function setAuth(token, user) {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    if (user) localStorage.setItem(USER_KEY, JSON.stringify(user));
    window.dispatchEvent(new CustomEvent('auth-state-changed'));
}

function clearAuth() {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    window.dispatchEvent(new CustomEvent('auth-state-changed'));
}

function logout() {
    clearAuth();
    window.location.href = '/login?logged_out=true';
}

// Protected Route Guard
function requireAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = '/login?redirect=' + encodeURIComponent(window.location.pathname);
        return false;
    }
    return true;
}

// Guest Guard (for /login and /register)
function requireGuest() {
    const token = getToken();
    if (token) {
        window.location.href = '/dashboard';
        return false;
    }
    return true;
}

// HTMX Global Authorization Header Injection
document.addEventListener('htmx:configRequest', function (evt) {
    const token = getToken();
    if (token) {
        evt.detail.headers['Authorization'] = 'Bearer ' + token;
    }
});

// HTMX Custom Response Event Listeners
document.addEventListener('DOMContentLoaded', function () {
    // Listen for custom HTMX event triggers dispatched via HX-Trigger header
    document.body.addEventListener('loginSuccess', function (evt) {
        const data = evt.detail;
        if (data && data.token) {
            setAuth(data.token, data.user);
            // Brief pause for UI animation before redirect
            setTimeout(() => {
                const urlParams = new URLSearchParams(window.location.search);
                const redirect = urlParams.get('redirect') || '/dashboard';
                window.location.href = redirect;
            }, 600);
        }
    });

    document.body.addEventListener('registerSuccess', function (evt) {
        setTimeout(() => {
            window.location.href = '/login?registered=1';
        }, 900);
    });
});

// Alpine.js Global Auth Component Store
function authStore() {
    return {
        isAuthenticated: !!getToken(),
        currentUser: getUser(),

        init() {
            window.addEventListener('auth-state-changed', () => {
                this.isAuthenticated = !!getToken();
                this.currentUser = getUser();
            });
        },

        get userInitials() {
            if (!this.currentUser || !this.currentUser.name) return 'U';
            return this.currentUser.name
                .split(' ')
                .map(n => n[0])
                .join('')
                .toUpperCase()
                .slice(0, 2);
        },

        logout() {
            logout();
        }
    };
}
