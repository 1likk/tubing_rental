document.addEventListener('DOMContentLoaded', function() {
    // Finance Chart
    const revenueChartEl = document.getElementById('revenueChart');
    if (revenueChartEl) {
        const labelsDataEl = document.getElementById('labels-data');
        const chartDataEl = document.getElementById('chart-data');
        
        if (labelsDataEl && chartDataEl) {
            const labelsData = JSON.parse(labelsDataEl.textContent);
            const chartData = JSON.parse(chartDataEl.textContent);
            
            const ctx = revenueChartEl.getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labelsData,
                    datasets: [{
                        label: 'Выручка',
                        data: chartData,
                        borderColor: '#3b82f6',
                        backgroundColor: 'transparent',
                        fill: false,
                        tension: 0.4,
                        borderWidth: 2,
                        pointRadius: 4,
                        pointBackgroundColor: '#3b82f6',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointHoverRadius: 6,
                        pointHoverBackgroundColor: '#3b82f6',
                        pointHoverBorderColor: '#fff',
                        pointHoverBorderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: '#fff',
                            titleColor: '#1d1d1f',
                            bodyColor: '#1d1d1f',
                            borderColor: '#e5e5e7',
                            borderWidth: 1,
                            padding: 12,
                            displayColors: false,
                            titleFont: {
                                size: 13,
                                weight: '600'
                            },
                            bodyFont: {
                                size: 13
                            },
                            callbacks: {
                                label: function(context) {
                                    return context.parsed.y.toFixed(0) + ' ₸';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: '#f0f0f0',
                                drawBorder: false
                            },
                            ticks: {
                                font: {
                                    size: 12
                                },
                                color: '#86868b',
                                padding: 10
                            }
                        },
                        x: {
                            grid: {
                                color: '#f0f0f0',
                                drawBorder: false
                            },
                            ticks: {
                                font: {
                                    size: 12
                                },
                                color: '#86868b',
                                padding: 10
                            }
                        }
                    }
                }
            });
        }
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');


document.addEventListener('DOMContentLoaded', function() {
    // Кнопки Старт
    document.querySelectorAll('.btn-start').forEach(button => {
        button.addEventListener('click', function() {
            const tubingId = this.dataset.tubingId;
            const tubingNumber = this.dataset.tubingNumber;
            openStartModal(tubingId, tubingNumber);
        });
    });
    
    // Кнопки Завершить
    document.querySelectorAll('.btn-end').forEach(button => {
        button.addEventListener('click', function() {
            const sessionId = this.dataset.sessionId;
            const tubingId = this.dataset.tubingId;
            endRental(sessionId, tubingId);
        });
    });
});

// Модальное окно для старта
function openStartModal(tubingId, tubingNumber) {
    const tubingIdInput = document.getElementById('tubingId');
    if (tubingIdInput) {
        tubingIdInput.value = tubingId;
    }
    const modalTubingNumber = document.getElementById('modalTubingNumber');
    if (modalTubingNumber) {
        modalTubingNumber.textContent = tubingNumber;
    }
    const guestNameInput = document.getElementById('guestName');
    if (guestNameInput) {
        guestNameInput.value = '';
    }
    const phoneNumberInput = document.getElementById('phoneNumber');
    if (phoneNumberInput) {
        phoneNumberInput.value = '+7 ';
    }
    const startModal = document.getElementById('startModal');
    if (startModal) {
        startModal.style.display = 'block';
    }
    if (guestNameInput) {
        guestNameInput.focus();
    }
}

function closeStartModal() {
    const startModal = document.getElementById('startModal');
    if (startModal) {
        startModal.style.display = 'none';
    }
}

// Маска для телефона
document.addEventListener('DOMContentLoaded', function() {
    const phoneInput = document.getElementById('phoneNumber');
    if (!phoneInput) return;
    
    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        
        if (!value.startsWith('7')) {
            value = '7' + value;
        }
        
        
        value = value.substring(0, 11);
        
        
        let formatted = '+7 ';
        if (value.length > 1) {
            formatted += '(' + value.substring(1, 4);
        }
        if (value.length >= 4) {
            formatted += ') ' + value.substring(4, 7);
        }
        if (value.length >= 7) {
            formatted += '-' + value.substring(7, 9);
        }
        if (value.length >= 9) {
            formatted += '-' + value.substring(9, 11);
        }
        
        e.target.value = formatted;
    });

    phoneInput.addEventListener('keydown', function(e) {
        if (e.key === 'Backspace' && e.target.value === '+7 ') {
            e.preventDefault();
        }
    });
    
    phoneInput.addEventListener('focus', function(e) {
        if (e.target.value === '') {
            e.target.value = '+7 ';
        }
    });
});

// Старт аренды
window.startRental = function() {
    const tubingIdInput = document.getElementById('tubingId');
    const guestNameInput = document.getElementById('guestName');
    const phoneNumberInput = document.getElementById('phoneNumber');
    
    if (!tubingIdInput || !guestNameInput || !phoneNumberInput) return;
    
    const tubingId = tubingIdInput.value;
    const guestName = guestNameInput.value.trim();
    const phoneNumber = phoneNumberInput.value.trim();
    
    if (!guestName) {
        alert('Введите имя гостя');
        return;
    }
    
    if (phoneNumber.length < 10) {
        alert('Введите корректный номер телефона');
        return;
    }
    
    fetch(`/rentals/start/${tubingId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `guest_name=${encodeURIComponent(guestName)}&phone_number=${encodeURIComponent(phoneNumber)}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeStartModal();
            location.reload();
        } else {
            alert(data.error || 'Ошибка при запуске аренды');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка при запуске аренды');
    });
}


window.endRental = function(sessionId, tubingId) {
    if (!confirm('Завершить аренду?')) {
        return;
    }
    
    fetch(`/rentals/end/${sessionId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showResult(data);
        } else {
            alert('Ошибка при завершении аренды');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка при завершении аренды');
    });
}

// Показать результат
function showResult(data) {
    const duration = data.duration;
    const timeStr = `${duration.hours}ч ${duration.minutes}м ${duration.seconds}с`;
    
    const resultHtml = `
        <p><strong>Время аренды:</strong> ${timeStr}</p>
        <div class="result-price">${data.final_cost} ₸</div>
        <p style="text-align: center; color: #86868b;">К оплате</p>
    `;
    
    const resultContent = document.getElementById('resultContent');
    if (resultContent) {
        resultContent.innerHTML = resultHtml;
    }
    
    const resultModal = document.getElementById('resultModal');
    if (resultModal) {
        resultModal.style.display = 'block';
    }
}

window.closeResultModal = function() {
    const resultModal = document.getElementById('resultModal');
    if (resultModal) {
        resultModal.style.display = 'none';
    }
    location.reload();
}

// Таймеры в реальном времени
function updateTimers() {
    const now = new Date();
    
    document.querySelectorAll('.tubing-compact-card[data-start-time]').forEach(card => {
        const startTime = new Date(card.dataset.startTime);
        const elapsed = Math.floor((now - startTime) / 1000);
        
        const hours = Math.floor(elapsed / 3600);
        const minutes = Math.floor((elapsed % 3600) / 60);
        const seconds = elapsed % 60;
        
        const timeString = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        
        const tubingId = card.dataset.tubingId;
        const timerElement = document.getElementById(`timer-${tubingId}`);
        
        if (timerElement) {
            timerElement.textContent = timeString;
            
            timerElement.classList.remove('warning', 'danger');
            if (elapsed > 3600) {
                timerElement.classList.add('danger');
            } else if (elapsed > 2700) {
                timerElement.classList.add('warning');
            }
        }
    });
}


document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelectorAll('.tubing-compact-card[data-start-time]').length > 0) {
        setInterval(updateTimers, 1000);
        updateTimers();
    }
});

window.closeStartModal = closeStartModal;


window.onclick = function(event) {
    const startModal = document.getElementById('startModal');
    const resultModal = document.getElementById('resultModal');
    if (startModal && event.target == startModal) {
        closeStartModal();
    }
    if (resultModal && event.target == resultModal) {
        closeResultModal();
    }
}
