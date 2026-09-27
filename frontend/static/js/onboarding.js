/**
 * OnboardFlow - Client Onboarding Form Validation Controller
 * Provides client-side real-time validation, field feedback, and HTMX form hooks.
 */

// Validation Rules & Regular Expressions
const VALIDATION_RULES = {
    email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    phone: /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/,
    minCompanyNameLength: 2,
    minContactPersonLength: 2,
    minAddressLength: 5,
};

/**
 * Validate email format
 * @param {string} email 
 * @returns {boolean}
 */
function isValidEmail(email) {
    if (!email) return false;
    return VALIDATION_RULES.email.test(email.trim());
}

/**
 * Validate phone number format (optional field, but if filled must be valid)
 * @param {string} phone 
 * @returns {boolean}
 */
function isValidPhone(phone) {
    if (!phone || phone.trim() === '') return true;
    return VALIDATION_RULES.phone.test(phone.trim());
}

/**
 * Validate text field minimum length
 * @param {string} text 
 * @param {number} minLength 
 * @returns {boolean}
 */
function hasMinLength(text, minLength) {
    return text && text.trim().length >= minLength;
}

/**
 * Alpine.js component for client onboarding form state and real-time validation
 */
document.addEventListener('alpine:init', () => {
    Alpine.data('onboardingForm', () => ({
        // Form field models
        company_name: '',
        contact_person: '',
        email: '',
        phone: '',
        address: '',
        tier: 'Enterprise VIP',
        status: 'Active',

        // Field touched states
        touched: {
            company_name: false,
            contact_person: false,
            email: false,
            phone: false,
            address: false,
        },

        // Submission state
        isSubmitting: false,
        submitError: '',

        /**
         * Extract and suggest domain name from corporate email
         */
        get suggestedDomain() {
            if (!this.email || !this.email.includes('@')) return '';
            const parts = this.email.split('@');
            if (parts.length > 1 && parts[1].includes('.')) {
                return parts[1].toLowerCase();
            }
            return '';
        },

        /**
         * Auto-fill company name based on email domain if company name is empty
         */
        suggestCompanyName() {
            const domain = this.suggestDomain;
            if (domain && !this.company_name) {
                const namePart = domain.split('.')[0];
                this.company_name = namePart.charAt(0).toUpperCase() + namePart.slice(1) + ' Inc.';
                this.touch('company_name');
            }
        },

        /**
         * Mark field as touched when user focuses or types
         */
        touch(field) {
            this.touched[field] = true;
        },

        /**
         * Validation checks per field
         */
        get errors() {
            const errs = {};

            // Company Name: Required, min 2 chars
            if (this.touched.company_name) {
                if (!this.company_name.trim()) {
                    errs.company_name = 'Company Name is required.';
                } else if (this.company_name.trim().length < VALIDATION_RULES.minCompanyNameLength) {
                    errs.company_name = `Company name must be at least ${VALIDATION_RULES.minCompanyNameLength} characters.`;
                }
            }

            // Contact Person: Required, min 2 chars
            if (this.touched.contact_person) {
                if (!this.contact_person.trim()) {
                    errs.contact_person = 'Contact Person name is required.';
                } else if (this.contact_person.trim().length < VALIDATION_RULES.minContactPersonLength) {
                    errs.contact_person = `Contact person must be at least ${VALIDATION_RULES.minContactPersonLength} characters.`;
                }
            }

            // Email: Required, standard email regex
            if (this.touched.email) {
                if (!this.email.trim()) {
                    errs.email = 'Corporate Email is required.';
                } else if (!isValidEmail(this.email)) {
                    errs.email = 'Please enter a valid business email address.';
                }
            }

            // Phone: Optional, but if provided must match phone pattern
            if (this.touched.phone && this.phone.trim()) {
                if (!isValidPhone(this.phone)) {
                    errs.phone = 'Please enter a valid phone number format (e.g. +1 555-123-4567).';
                }
            }

            // Address: Optional, but if provided must be descriptive
            if (this.touched.address && this.address.trim()) {
                if (this.address.trim().length < VALIDATION_RULES.minAddressLength) {
                    errs.address = `Address must be at least ${VALIDATION_RULES.minAddressLength} characters.`;
                }
            }

            return errs;
        },

        /**
         * Determine if the form is valid and ready for submission
         */
        get isValid() {
            const hasCompany = hasMinLength(this.company_name, VALIDATION_RULES.minCompanyNameLength);
            const hasContact = hasMinLength(this.contact_person, VALIDATION_RULES.minContactPersonLength);
            const hasValidEmail = isValidEmail(this.email);
            const phoneValid = isValidPhone(this.phone);
            const addressValid = !this.address.trim() || this.address.trim().length >= VALIDATION_RULES.minAddressLength;

            return hasCompany && hasContact && hasValidEmail && phoneValid && addressValid;
        },

        /**
         * Check if all required fields are filled
         */
        validateAll() {
            this.touched.company_name = true;
            this.touched.contact_person = true;
            this.touched.email = true;
            this.touched.phone = true;
            this.touched.address = true;
            return this.isValid;
        },
    }));
});

// Setup HTMX Global Interceptors for Onboarding Form
document.addEventListener('DOMContentLoaded', () => {
    // Inject Authorization token if stored in localStorage
    document.body.addEventListener('htmx:configRequest', (event) => {
        const token = localStorage.getItem('onboardflow_token');
        if (token) {
            event.detail.headers['Authorization'] = `Bearer ${token}`;
        }
    });

    // Track submission state for spinner and button disabling
    document.body.addEventListener('htmx:beforeRequest', (event) => {
        const formEl = document.getElementById('onboarding-form');
        if (formEl && event.detail.elt === formEl) {
            const alpineData = Alpine.$data(formEl);
            if (alpineData) {
                alpineData.isSubmitting = true;
            }
            const submitBtn = document.getElementById('submit-btn');
            if (submitBtn) {
                submitBtn.disabled = true;
            }
        }
    });

    document.body.addEventListener('htmx:afterRequest', (event) => {
        const formEl = document.getElementById('onboarding-form');
        if (formEl && event.detail.elt === formEl) {
            const alpineData = Alpine.$data(formEl);
            if (alpineData) {
                alpineData.isSubmitting = false;
            }
            const submitBtn = document.getElementById('submit-btn');
            if (submitBtn && alpineData && alpineData.isValid) {
                submitBtn.disabled = false;
            }
        }
    });

    // Handle HTMX response errors
    document.body.addEventListener('htmx:responseError', (event) => {
        const feedbackEl = document.getElementById('form-feedback');
        if (feedbackEl && event.detail.xhr) {
            let errorMsg = 'Failed to submit onboarding form. Please check the backend service.';
            try {
                const parsed = JSON.parse(event.detail.xhr.responseText);
                if (parsed.detail) errorMsg = parsed.detail;
            } catch (e) {
                // If response is HTML alert, it will be swapped automatically
            }
            console.error('Onboarding Submission Error:', errorMsg);
        }
    });
});
