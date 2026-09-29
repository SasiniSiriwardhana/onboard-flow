function documentUploader() {
    return {
        isDragging: false,
        selectedFile: null,
        docCategory: 'Contract & MSA',
        uploadedBy: 'Admin User',
        isUploading: false,

        handleDrop(e) {
            this.isDragging = false;
            if (e.dataTransfer.files.length > 0) {
                this.selectedFile = e.dataTransfer.files[0];
            }
        },

        handleFileSelect(e) {
            if (e.target.files.length > 0) {
                this.selectedFile = e.target.files[0];
            }
        },

        formatSize(bytes) {
            if (!bytes) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        },

        async uploadFile() {
            if (!this.selectedFile) return;
            this.isUploading = true;
            try {
                const formData = new FormData();
                formData.append('file', this.selectedFile);
                formData.append('uploaded_by', this.uploadedBy);

                const res = await fetch('/documents/upload-api', {
                    method: 'POST',
                    body: formData
                });
                if (res.ok) {
                    window.location.href = '/documents';
                }
            } catch (err) {
                console.error("Upload failed:", err);
            } finally {
                this.isUploading = false;
            }
        }
    };
}

function documentVault() {
    return {
        documents: [],
        searchQuery: '',

        init() {
            this.fetchDocuments();
        },

        async fetchDocuments() {
            try {
                const res = await fetch('/documents/data');
                if (res.ok) {
                    this.documents = await res.json();
                }
            } catch (err) {
                console.error("Failed to load documents:", err);
            }
        },

        filteredDocuments() {
            return this.documents.filter(d => {
                return !this.searchQuery ||
                    d.file_name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    (d.uploaded_by && d.uploaded_by.toLowerCase().includes(this.searchQuery.toLowerCase()));
            });
        },

        async deleteDoc(docId) {
            if (!confirm('Are you sure you want to delete this document?')) return;
            try {
                const res = await fetch(`/documents/${docId}`, { method: 'DELETE' });
                if (res.ok) {
                    this.documents = this.documents.filter(d => d.id !== docId);
                }
            } catch (err) {
                console.error("Delete failed:", err);
            }
        },

        formatSize(bytes) {
            if (!bytes) return '0 B';
            const k = 1024;
            const sizes = ['B', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
        },

        formatDate(dateStr) {
            if (!dateStr) return 'Recently';
            const d = new Date(dateStr);
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
        }
    };
}

function reportsManager() {
    return {
        report: {},
        sendingEmail: false,
        notificationMessage: '',

        init() {
            this.fetchReport();
            this.$nextTick(() => {
                this.renderChart();
            });
        },

        async fetchReport() {
            try {
                const res = await fetch('/reports/data');
                if (res.ok) {
                    this.report = await res.json();
                }
            } catch (e) {
                console.warn("Using fallback reports:", e);
            }
        },

        async sendEmailNotification() {
            this.sendingEmail = true;
            try {
                const res = await fetch('/reports/notify', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ recipient_email: 'stakeholder@enterprise.com', report_title: 'Executive Onboarding Review' })
                });
                if (res.ok) {
                    const data = await res.json();
                    this.notificationMessage = data.message || "Email notification dispatched successfully!";
                    setTimeout(() => { this.notificationMessage = ''; }, 5000);
                }
            } catch (err) {
                console.error(err);
            } finally {
                this.sendingEmail = false;
            }
        },

        renderChart() {
            const ctx = document.getElementById('stageChart');
            if (ctx) {
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Kickoff', 'Security/Arch', 'Data/API', 'UAT/Cutover'],
                        datasets: [{
                            label: 'Average Days in Stage',
                            data: [5.2, 8.1, 11.4, 4.8],
                            backgroundColor: ['#6366f1', '#8b5cf6', '#0284c7', '#10b981'],
                            borderRadius: 8
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true, grid: { color: 'rgba(226, 232, 240, 0.6)' } } }
                    }
                });
            }
        }
    };
}
