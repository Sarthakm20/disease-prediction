// Initialize probability meters
function initProbabilityMeters() {
    document.querySelectorAll('.probability-meter-fill').forEach(meter => {
        const percent = meter.getAttribute('data-percent');
        meter.style.width = percent + '%';
    });
}

// Initialize all charts
function initCharts() {
    // Pie Chart for Match Percentage
    const pieDataElement = document.getElementById("pie-data");
    if (pieDataElement) {
        const data = JSON.parse(pieDataElement.dataset.chartData);
        
        new Chart(document.getElementById("matchPieChart"), {
            type: "pie",
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.values,
                    backgroundColor: data.colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { position: "bottom" },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.label}: ${context.raw} (${Math.round(context.parsed)}%)`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    // Bar Chart for Symptom Count
    const barDataElement = document.getElementById("bar-data");
    if (barDataElement) {
        const data = JSON.parse(barDataElement.dataset.chartData);
        
        new Chart(document.getElementById("matchBarChart"), {
            type: "bar",
            data: {
                labels: data.labels,
                datasets: [{
                    label: "Symptoms",
                    data: data.values,
                    backgroundColor: data.colors,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: Math.max(parseInt(document.getElementById("bar-data").dataset.totalSymptoms || 5), 5),
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: { display: false }
                }
            }
        });
    }
    
    // Disease Pie Chart (for single symptom view)
    // In your result-charts.js or script section
    const diseaseDataElement = document.getElementById("disease-data");
    if (diseaseDataElement) {
        try {
            const data = JSON.parse(diseaseDataElement.dataset.chartData);
            
            const ctx = document.getElementById('diseasePieChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.values,
                        backgroundColor: [
                            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
                            '#FF9F40', '#66BB6A', '#EF5350', '#BA68C8', '#FFD700'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `${context.label}: ${context.raw}%`;
                                }
                            }
                        }
                    }
                }
            });
        } catch (e) {
            console.error("Error initializing chart:", e);
        }
    }
}

// Initialize everything when DOM is loaded
document.addEventListener("DOMContentLoaded", function() {
    initProbabilityMeters();
    initCharts();
});