function adminDashboard() {
    return {
        loading: false,
        stats: {
            total_clients: 24,
            active_onboardings: 9,
            avg_progress: 76,
            db_latency_ms: 3.8,
            completed_count: 15,
            kickoff_count: 3
        },
        activityLogs: [
            {
                id: 1,
                actor: "Superadmin (System)",
                action: "provisioned new enterprise workspace for",
                target: "Nexus Bank International",
                time: "10 minutes ago",
                badgeBg: "bg-indigo-50 text-indigo-600",
                icon: '<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>'
            },
            {
                id: 2,
                actor: "Alex Rivera",
                action: "uploaded production cutover signoff document for",
                target: "MedLife Health Systems",
                time: "32 minutes ago",
                badgeBg: "bg-sky-50 text-sky-600",
                icon: '<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>'
            },
            {
                id: 3,
                actor: "Security Engine",
                action: "verified HIPAA compliance encryption standards for",
                target: "Nordic Retail Group",
                time: "1 hour ago",
                badgeBg: "bg-emerald-50 text-emerald-600",
                icon: '<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/></svg>'
            },
            {
                id: 4,
                actor: "Elena Rostova",
                action: "advanced project status to In Progress for",
                target: "Pacific Freight Logistics",
                time: "2 hours ago",
                badgeBg: "bg-amber-50 text-amber-600",
                icon: '<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>'
            }
        ],

        init() {
            this.fetchAdminStats();
            this.$nextTick(() => {
                this.renderCharts();
            });
        },

        async fetchAdminStats() {
            this.loading = true;
            try {
                const res = await fetch('/api/admin/stats');
                if (res.ok) {
                    const data = await res.json();
                    this.stats = Object.assign(this.stats, data);
                }
            } catch (e) {
                console.warn("Using fallback admin stats:", e);
            } finally {
                this.loading = false;
            }
        },

        refreshData() {
            this.fetchAdminStats();
        },

        renderCharts() {
            const ctxVelocity = document.getElementById('velocityChart');
            if (ctxVelocity) {
                new Chart(ctxVelocity, {
                    type: 'line',
                    data: {
                        labels: ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct (Proj)'],
                        datasets: [
                            {
                                label: 'Completed Onboardings',
                                data: [6, 11, 15, 18, 24, 30],
                                borderColor: '#4f46e5',
                                backgroundColor: 'rgba(79, 70, 229, 0.08)',
                                fill: true,
                                tension: 0.4,
                                borderWidth: 2.5
                            },
                            {
                                label: 'Active Pipeline',
                                data: [4, 7, 9, 8, 11, 14],
                                borderColor: '#0284c7',
                                borderDash: [5, 5],
                                fill: false,
                                tension: 0.4,
                                borderWidth: 2
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'top', labels: { font: { family: 'Plus Jakarta Sans', size: 11 } } }
                        },
                        scales: {
                            y: { grid: { color: 'rgba(226, 232, 240, 0.6)' } },
                            x: { grid: { display: false } }
                        }
                    }
                });
            }

            const ctxDonut = document.getElementById('statusDonutChart');
            if (ctxDonut) {
                new Chart(ctxDonut, {
                    type: 'doughnut',
                    data: {
                        labels: ['Completed', 'In Progress', 'Kickoff'],
                        datasets: [{
                            data: [15, 8, 3],
                            backgroundColor: ['#10b981', '#0284c7', '#f59e0b'],
                            borderWidth: 0,
                            hoverOffset: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        cutout: '72%',
                        plugins: {
                            legend: { display: false }
                        }
                    }
                });
            }
        }
    };
}

function adminClientsManager() {
    return {
        searchQuery: '',
        statusFilter: '',
        clients: [],

        init() {
            this.fetchClients();
        },

        async fetchClients() {
            try {
                const res = await fetch('/onboarding/list?format=json');
                if (res.ok) {
                    this.clients = await res.json();
                }
            } catch (err) {
                console.error("Failed to load clients:", err);
            }
        },

        filteredClients() {
            return this.clients.filter(c => {
                const matchSearch = !this.searchQuery || 
                    c.company_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    c.contact_person.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    c.email.toLowerCase().includes(this.searchQuery.toLowerCase());
                const matchStatus = !this.statusFilter || c.status === this.statusFilter;
                return matchSearch && matchStatus;
            });
        },

        formatDate(dateStr) {
            if (!dateStr) return 'Recently';
            const d = new Date(dateStr);
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        },

        statusBadgeClass(status) {
            switch (status) {
                case 'Active': return 'badge-success text-white';
                case 'Completed': return 'badge-info text-white';
                case 'Pending': return 'badge-warning text-slate-900';
                default: return 'badge-ghost text-slate-600';
            }
        }
    };
}
