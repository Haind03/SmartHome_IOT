const client = mqtt.connect('wss://broker.hivemq.com:8000/mqtt');

function generateTimeLabels() {
    const labels = [];
    for (let i = 0; i < 24; i++) {
        const hour = i.toString().padStart(2, '0');
        labels.push(`${hour}:00`);
    }
    labels.push('current');
    return labels;
}

const satisfactionCtx = document.getElementById('satisfaction-chart').getContext('2d');
const satisfactionChart = new Chart(satisfactionCtx, {
    type: 'line',
    data: {
        labels: generateTimeLabels(),
        datasets: [
            {
                label: 'Ánh Sáng',
                data: [10, 20, 15, 25, 30, 20, 15, 20, 30, 40, 15,25,10,28,40, 30, 20, 15, 10, 5, 15, 5, 10,30, 45,50],
                borderColor: '#ffb86c',
                backgroundColor: 'rgba(255, 184, 108, 0.2)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#ffb86c',
                pointHoverRadius: 8
            },
            {
                label: 'Độ ẩm',
                data: [30, 40, 35, 5, 15 , 5, 10, 20 , 30, 20, 15, 10, 5, 20, 5, 10, 20, 30, 40, 45, 50, 55, 45, 50, 40],
                borderColor: '#50fa7b',
                backgroundColor: 'rgba(80, 250, 123, 0.2)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#50fa7b',
                pointHoverRadius: 8
            },
            {
                label: 'Nhiệt độ',
                data: [35, 30, 25, 20, 25, 10,5, 35, 30,35, 30, 25, 20, 25, 10,5, 35, 30,35, 30, 25, 20, 25, 10,5, 35, 30],
                borderColor: '#ff79c6',
                backgroundColor: 'rgba(255, 121, 198, 0.2)',
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#ff79c6',
                pointHoverRadius: 8
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: '#44475a'
                },
                ticks: {
                    color: '#f8f8f2'
                }
            },
            x: {
                grid: {
                    color: '#44475a'
                },
                ticks: {
                    color: '#f8f8f2'
                }
            }
        },
        plugins: {
            legend: {
                labels: {
                    color: '#f8f8f2'
                }
            },
            zoom: {
                pan: {
                    enabled: true,
                    mode: 'x', // Allow panning only in the x-axis
                },
                zoom: {
                    enabled: true,
                    drag: true,
                    mode: 'x', // Allow zooming only in the x-axis
                    speed: 0.1 // Speed of zooming
                }
            }
        }
    }
});
document.addEventListener('DOMContentLoaded', function() {
    // Chờ đợi trang được tải xong trước khi áp dụng hiệu ứng
    const chartContainer = document.querySelector('.chart-container');
    setTimeout(() => {
        chartContainer.classList.add('visible'); // Thêm lớp 'visible' để kích hoạt hiệu ứng fade-in
    }, 300); // Thời gian chờ để áp dụng hiệu ứng sau khi DOM đã sẵn sàng
});
document.addEventListener('DOMContentLoaded', function() {
    // Lấy tất cả các công tắc
    const switches = document.querySelectorAll('.light-switch');
    
    // Duyệt qua tất cả các công tắc và bật chúng lên
    switches.forEach(function(switchElement) {
        switchElement.checked = true; // Bật công tắc
        switchElement.dispatchEvent(new Event('change')); // Kích hoạt sự kiện thay đổi để cập nhật giao diện và nhãn
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const deviceCells = document.querySelectorAll('td:nth-child(3)'); // Chọn tất cả các ô trong cột Device

    deviceCells.forEach(cell => {
        switch(cell.textContent.trim()) {
            case 'Device 1':
                cell.textContent = 'Ánh sáng';
                break;
            case 'Device 2':
                cell.textContent = 'Độ ẩm';
                break;
            case 'Device 3':
                cell.textContent = 'Nhiệt độ';
                break;
        }
    });
});

document.querySelectorAll('.light-switch').forEach((switchElement) => {
    switchElement.addEventListener('change', function() {
        const deviceId = this.id.split('-').pop();
        const state = this.checked ? 'ON' : 'OFF';
        
        // Find the corresponding dataset in the chart
        const dataset = satisfactionChart.data.datasets[deviceId - 1]; 
        
        if (dataset) {
            // Toggle visibility of the dataset
            dataset.hidden = !this.checked;
            satisfactionChart.update(); // Update the chart to reflect changes
        }
        
        // Publish to MQTT topic only if there is a change
        client.publish(`home/switch${deviceId}`, state);
        
        // Log the action to the server
        fetch('/log_toggle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                device: `Device ${deviceId}`,
                action: state,
                timestamp: new Date().toLocaleString()
            })
        }).then(response => response.json())
          .then(data => console.log('Log saved:', data))
          .catch(error => console.error('Error logging data:', error));
    });
});

function resetZoom() {
    satisfactionChart.resetZoom();
}
