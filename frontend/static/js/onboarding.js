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
