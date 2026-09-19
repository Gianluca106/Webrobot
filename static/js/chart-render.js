// Configurazione comune per tutti i grafici
const chartConfig = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top',
            labels: {
                font: {
                    family: "'Segoe UI', 'Helvetica Neue', sans-serif",
                    size: 14,
                    weight: 'bold'
                },
                padding: 20,
                usePointStyle: true,
                pointStyle: 'circle'
            }
        },
        tooltip: {
            backgroundColor: 'rgba(0,0,0,0.8)',
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 12 },
            padding: 12,
            cornerRadius: 4,
            displayColors: false,
            callbacks: {
                label: function(context) {
                    return ` ${context.dataset.label}: ${context.raw}`;
                }
            }
        }
    },
    scales: {
        y: {
            beginAtZero: true,
            ticks: {
                font: { weight: 'bold' }
            }
        },
        x: {
            ticks: {
                font: { weight: 'bold' }
            }
        }
    }
};

// Colori Bootstrap per i dataset
const bootstrapColors = [
    'rgba(13, 110, 253, 0.8)',  // primary
    'rgba(25, 135, 84, 0.8)',   // success
    'rgba(220, 53, 69, 0.8)',    // danger
    'rgba(255, 193, 7, 0.8)',    // warning
    'rgba(13, 202, 240, 0.8)',   // info
    'rgba(108, 117, 125, 0.8)'   // secondary
];

const makeChart = (id, dataObj, label) => {
    const labels = Object.keys(dataObj);
    const data = Object.values(dataObj);
    
    // Scegli un colore in base all'ID del grafico
    let colorIndex;
    switch(id) {
        case 'serverChart': colorIndex = 0; break;
        case 'contentChart': colorIndex = 1; break;
        case 'encodingChart': colorIndex = 2; break;
        default: colorIndex = 0;
    }
    
    new Chart(document.getElementById(id), {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                backgroundColor: bootstrapColors[colorIndex],
                borderColor: bootstrapColors[colorIndex].replace('0.8', '1'),
                borderWidth: 2,
                borderRadius: 6,
                hoverBackgroundColor: bootstrapColors[colorIndex].replace('0.8', '0.9'),
                hoverBorderColor: '#000',
                hoverBorderWidth: 1
            }]
        },
        options: chartConfig
    });
};

// Crea i grafici
makeChart('serverChart', serverData, 'Server Types');
makeChart('contentChart', contentData, 'Content Types');
makeChart('encodingChart', encodingData, 'Encodings');