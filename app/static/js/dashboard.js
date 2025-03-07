document.addEventListener('DOMContentLoaded', function() {
    const metrics = window.dashboardMetrics;
    if (!metrics) {
        console.error('Dashboard metrics not provided.');
        return;
    }

    // Bar Chart
    const ctxBar = document.getElementById('metricsChart').getContext('2d');
    const barData = {
        labels: ['Projects', 'Total Tasks', 'Completed Tasks'],
        datasets: [{
            label: 'Metrics',
            data: [metrics.total_projects, metrics.total_tasks, metrics.completed_tasks],
            backgroundColor: [
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)'
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)'
            ],
            borderWidth: 1
        }]
    };

    const barConfig = {
        type: 'bar',
        data: barData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    };

    new Chart(ctxBar, barConfig);

    // First Pie Chart: Completed vs Pending Tasks
    const ctxPie = document.getElementById('tasksPieChart').getContext('2d');
    const pendingTasks = metrics.total_tasks - metrics.completed_tasks;
    const pieData = {
        labels: ['Completed Tasks', 'Pending Tasks'],
        datasets: [{
            data: [metrics.completed_tasks, pendingTasks],
            backgroundColor: [
                'rgba(75, 192, 192, 0.6)',
                'rgba(255, 99, 132, 0.6)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    };

    const pieConfig = {
        type: 'pie',
        data: pieData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    };

    new Chart(ctxPie, pieConfig);

    // Updated Another Pie Chart: Tasks by Project
    const ctxAnother = document.getElementById('anotherPieChart').getContext('2d');
    const projectLabels = Object.keys(metrics.tasks_by_project);
    const tasksCounts = Object.values(metrics.tasks_by_project);
    const backgroundColors = [
        'rgba(75, 192, 192, 0.6)',
        'rgba(255, 159, 64, 0.6)',
        'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)'
    ];
    const borderColors = [
        'rgba(75, 192, 192, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)'
    ];
    
    const projectPieData = {
        labels: projectLabels,
        datasets: [{
            data: tasksCounts,
            backgroundColor: backgroundColors.slice(0, projectLabels.length),
            borderColor: borderColors.slice(0, projectLabels.length),
            borderWidth: 1
        }]
    };

    const projectPieConfig = {
        type: 'pie',
        data: projectPieData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            }
        }
    };

    new Chart(ctxAnother, projectPieConfig);
});