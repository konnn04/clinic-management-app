function create_stat(patient_stat, healing_stat, disease_stat) {
    const ctx1 = document.querySelector("#patiens_chart")
    const ctx2 = document.querySelector("#healing_chart")
    const data1 = {
        labels: [
            'Men',
            'Women',
        ],
        datasets: [{
            label: 'Số bệnh nhân',
            data: [patient_stat['man'], patient_stat['women']],
            backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            ],
            hoverOffset: 4
        }]
    };

    const chart1 = new Chart(ctx1, {
        type: 'doughnut',
        data: data1,
    })

    const months = [];
    const data_h = []
    healing_stat.forEach((element) => {
        months.push(element['month'])
        data_h.push(element['total'])
    })
    const data2 = {        
        labels: months,
        datasets: [{
            label: 'Lượt khám',
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

    const ctx3 = document.querySelector("#disease_chart")
    const data_d = []
    const labels = []
    disease_stat.forEach((element) => {
        labels.push(element['disease'])
        data_d.push(element['total'])
    })
    const data3 = {
        labels: labels,
        datasets: [{
            label: 'Ca bệnh',
            data: data_d,
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)',
            ],
            hoverOffset: 4
        }]
    };
    const chart3 = new Chart(ctx3, {
        type: 'bar',
        data: data3,
        options: {
            indexAxis: 'y',
        }
    })
}

function initTable(){
    $('#examination_list').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/examination-list-overview",
            "type": "GET",
            "data": function(d) {
                return $.extend({}, d, d.order.length ? {
                    "sort": d.columns[d.order[0].column].data,
                    "order": d.order[0].dir
                } : {});
            }
        },
        "columns": [
            { "data": "id" },
            { "data": "ho_benh_nhanh" },
            { "data": "ten_benh_nhan" },
            { "data": "gioiTinh" },
            { "data": null, render: function(data, type, row) {
                return "KXĐ"
            }, orderable: false },
            { "data": "soDienThoai" },
            { "data": "ngayKham" },
            { "data": null, render: function(data, type, row) {
                return `${row.ho_bac_si} ${row.ten_bac_si}`
            }, orderable: false }
        ],
        "order": [[0, 'desc']],
        "language": table_language_vn
    });
}

window.onload = function() {
    fetch('/api/patient-stat')
    .then(res => res.json())
    .then(data => {
        const patient_stat = data['patient_stat'];
        const healing_stat = data['month_stat'];
        const disease_stat = data['disease_stat'];
        create_stat(patient_stat, healing_stat, disease_stat)
    })
    .catch(err => {
        console.log(err)
    })

    initTable()
}