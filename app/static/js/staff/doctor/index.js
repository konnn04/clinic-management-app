function create_stat() {
    const ctx1 = document.querySelector("#patiens_chart")
    const ctx2 = document.querySelector("#healing_chart")
    const data1 = {
        labels: [
            'Men',
            'Women',
            'Children'
        ],
        datasets: [{
            label: 'Patients',
            data: [30,50,20],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
            ],
            hoverOffset: 4
        }]
    };

    const chart1 = new Chart(ctx1, {
        type: 'doughnut',
        data: data1,
    })

    const currentDate = new Date();
    const months = [];
    const data_h = []
    for (let i = 5; i >= 0; i--) {
        const date = new Date(currentDate.getFullYear(), currentDate.getMonth() - i, 1);
        months.push(date.toLocaleString('default', { month: 'long' }));
        data_h.push(Math.floor(Math.random()*30))
    }
    const data2 = {        
        labels: months,
        datasets: [{
            label: 'Healing index',
            data: data_h,
            fill: false,
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1,

        }]
    };

    ctx1.height = 300;
    ctx2.height = 300;
    const chart2 = new Chart(ctx2, {
        type: 'line',
        data: data2,
    })
}

create_stat()