document.addEventListener("DOMContentLoaded", function() {
    console.log("DOM loaded - initializing charts");
    
    // Debug canvas existence
    const canvas = document.getElementById('diseasePieChart');
    document.getElementById('canvas-exists').textContent = !!canvas;
    
    if (canvas) {
        console.log("Canvas element found:", canvas);
        canvas.style.border = "1px solid red"; // Temporary border to verify visibility
    } else {
        console.error("Canvas element not found!");
    }

    // Debug data
    const dataElement = document.getElementById('disease-data');
    if (dataElement) {
        const debugText = `Labels: ${dataElement.getAttribute('data-labels')}, Values: ${dataElement.getAttribute('data-values')}`;
        document.getElementById('chart-data').textContent = debugText;
        console.log("Chart data:", debugText);
    }

    // Initialize charts with more error handling
    try {
        initPieChart();
        initBarChart();
    } catch (e) {
        console.error("Chart initialization failed:", e);
    }
});

function initPieChart() {
    const element = document.getElementById('disease-data');
    if (!element) {
        console.error('Pie chart data element missing!');
        return;
    }

    const ctx = document.getElementById('diseasePieChart');
    if (!ctx) {
        console.error('Canvas element not found!');
        return;
    }

    // Visual debug
    ctx.style.border = '1px solid blue';
    
    try {
        const labels = JSON.parse(element.getAttribute('data-labels'));
        const values = JSON.parse(element.getAttribute('data-values'));
        
        new Chart(ctx.getContext('2d'), {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: {
                    onComplete: () => {
                        console.log('Chart animation complete');
                        ctx.style.border = 'none';
                    }
                }
            }
        });
        
        document.getElementById('data-loaded').textContent = 'Yes';
    } catch (e) {
        console.error('Chart error:', e);
        document.getElementById('data-loaded').textContent = 'Error: ' + e.message;
    }
}

// Initialize when ready
if (typeof Chart !== 'undefined') {
    document.addEventListener('DOMContentLoaded', initPieChart);
} else {
    console.error('Chart.js not loaded!');
}