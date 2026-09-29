function tasksManager() {
    return {
        viewMode: 'kanban',
        searchQuery: '',
        priorityFilter: '',
        tasks: [],
        newTask: {
            title: '',
            description: '',
            priority: 'Medium',
            status: 'To Do',
            due_date: ''
        },

        init() {
            this.fetchTasks();
        },

        async fetchTasks() {
            try {
                const res = await fetch('/tasks/data');
                if (res.ok) {
                    this.tasks = await res.json();
                }
            } catch (err) {
                console.error("Failed to fetch tasks:", err);
            }
        },

        filteredTasks() {
            return this.tasks.filter(t => {
                const matchSearch = !this.searchQuery || 
                    t.title.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
                    (t.description && t.description.toLowerCase().includes(this.searchQuery.toLowerCase()));
                const matchPriority = !this.priorityFilter || t.priority === this.priorityFilter;
                return matchSearch && matchPriority;
            });
        },

        getColumnTasks(status) {
            return this.filteredTasks().filter(t => t.status === status);
        },

        countByStatus(status) {
            return this.tasks.filter(t => t.status === status).length;
        },

        completionPercent() {
            if (this.tasks.length === 0) return 0;
            const done = this.countByStatus('Done');
            return Math.round((done / this.tasks.length) * 100);
        },

        async updateTaskStatus(taskId, newStatus) {
            try {
                const res = await fetch(`/tasks/${taskId}/status`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status: newStatus })
                });
                if (res.ok) {
                    const updated = await res.json();
                    const index = this.tasks.findIndex(t => t.id === taskId);
                    if (index !== -1) {
                        this.tasks[index].status = newStatus;
                    }
                }
            } catch (err) {
                console.error("Failed to update task status:", err);
            }
        },

        async createTask() {
            if (!this.newTask.title) return;
            try {
                const payload = {
                    title: this.newTask.title,
                    description: this.newTask.description,
                    priority: this.newTask.priority,
                    status: this.newTask.status,
                    due_date: this.newTask.due_date ? new Date(this.newTask.due_date).toISOString() : null
                };
                const res = await fetch('/tasks/create', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (res.ok) {
                    const created = await res.json();
                    this.tasks.unshift(created);
                    this.newTask = { title: '', description: '', priority: 'Medium', status: 'To Do', due_date: '' };
                    document.getElementById('task_create_modal').close();
                }
            } catch (err) {
                console.error("Failed to create task:", err);
            }
        },

        async deleteTask(taskId) {
            if (!confirm('Are you sure you want to delete this task?')) return;
            try {
                const res = await fetch(`/tasks/${taskId}`, { method: 'DELETE' });
                if (res.ok) {
                    this.tasks = this.tasks.filter(t => t.id !== taskId);
                }
            } catch (err) {
                console.error("Failed to delete task:", err);
            }
        },

        formatDate(dateStr) {
            if (!dateStr) return 'No due date';
            const d = new Date(dateStr);
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        },

        priorityBadgeClass(priority) {
            switch (priority) {
                case 'Critical': return 'badge-error text-white';
                case 'High': return 'badge-warning text-slate-900';
                case 'Medium': return 'badge-info text-white';
                case 'Low': return 'badge-ghost text-slate-600';
                default: return 'badge-ghost';
            }
        }
    };
}
