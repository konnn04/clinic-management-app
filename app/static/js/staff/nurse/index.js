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

function patient_table(){
    $('#patient_table').addClass('table table-bordered table-hover');
    $('#patient_table').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/patient-list",
            "data": function(d) {
                return $.extend({}, d, {
                    "sort": d.columns[d.order[0].column].data,
                    "order": d.order[0].dir
                });
            }
        },
        "columns": [
            { "data": "id" },
            { "data": "hoTen" },
            { "data": "gioiTinh" },
            { "data": "ngaySinh" },
            { "data": "soDienThoai" },
            { "data": "lanCuoiGhe"},
        ],
        "language": {
            "paginate": {
                "first": "<i class='fas fa-angle-double-left'></i>",
                "last": "<i class='fas fa-angle-double-right'></i>",
                "next": "<i class='fas fa-angle-right'></i>",
                "previous": "<i class='fas fa-angle-left'></i>"
            },
            "search": "Tìm kiếm:",
            "lengthMenu": "Hiển thị _MENU_ bản ghi",
            "info": "Hiển thị _START_ đến _END_ của _TOTAL_ bản ghi",
            "infoEmpty": "Không có bản ghi nào",
            "infoFiltered": "(lọc từ _MAX_ bản ghi)",
            "loadingRecords": "Đang tải...",
            "processing": "Đang xử lý...",
            "zeroRecords": "Không tìm thấy bản ghi nào"
        }
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

    patient_table()

}