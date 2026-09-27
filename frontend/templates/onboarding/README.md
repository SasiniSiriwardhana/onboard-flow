# Onboarding Templates & UI Components (Phase 5)

This directory contains client onboarding presentation templates, HTMX dynamic partials, and interactive Alpine.js controllers for Phase 5: Client Onboarding.

## 📄 Template Structure

| Template | Route | Description |
| :--- | :--- | :--- |
| `form.html` | `GET /onboarding` | 3-step visual wizard registration form with live company name and email validation |
| `list.html` | `GET /onboarding/list` | Full client directory hub with summary metrics cards and quick action toolbars |
| `list_partial.html` | `GET /onboarding/list` (HTMX) | HTMX partial table rows with click-to-copy email helpers and real-time progress bars |
| `success.html` | `GET /onboarding/success` | Onboarding confirmation portal with project milestones checklist and print summary |

## ⚡ Key Interactive Features
- **3-Step Visual Progress Bar**: Visual stepper guiding the user through company credentials, tier SLAs, and automated project provisioning.
- **Debounced Live HTMX Validators**: Instant feedback for `/onboarding/check-company` and `/auth/validate-email`.
- **Smart Domain Extraction**: Client-side domain parsing to assist with corporate identity.
- **DaisyUI Glassmorphism Design**: Modern SaaS aesthetics with rounded cards, smooth transitions, and responsive tables.
