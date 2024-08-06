/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable no-undef */
document.addEventListener("DOMContentLoaded", function() {
    const payrollData = {
        labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        datasets: [
            {
                label: "Gross Salary",
                data: [90000, 110000, 95000, 115000, 130000, 120000, 125000, 130000, 140000],
                borderColor: "#007bff",
                fill: false
            },
            {
                label: "Tax Deduction",
                data: [15000, 18000, 14000, 16000, 17000, 14000, 17500, 19500, 18000],
                borderColor: "#28a745",
                fill: false
            },
            {
                label: "Net Salary",
                data: [85000, 102000, 76000, 89000, 93000, 81000, 97500, 110500, 102000],
                borderColor: "#ffc107",
                fill: false
            }
        ]
    };

    const ctx = document.getElementById('payrollChart').getContext('2d');
    const payrollChart = new Chart(ctx, {
        type: 'line',
        data: payrollData, 
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const paymentStatusData = {
        labels: ['Successfully Paid', 'Pending', 'Unpaid'],
        datasets: [{
            data: [68, 17, 15],
            backgroundColor: ['#28a745', '#ffc107', '#dc3545']
        }]
    };

    const paymentCtx = document.getElementById('paymentStatusChart').getContext('2d');
    const paymentStatusChart = new Chart(paymentCtx, {
        type: 'pie',
        data: paymentStatusData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });
});
