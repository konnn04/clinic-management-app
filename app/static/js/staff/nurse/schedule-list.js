function init(){
    const table = $("#schedule-table").DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/api/schedule-list',
            type: 'GET',
            data: function(d) {
                // Add custom parameters
                d.status = $('.nav-link.active').attr('href') === '#scheduled' ? 'scheduled' : 'waiting';
            }
        },
        columns: [
            {data: 'id'},
            {data: 'nguoiBenh_id'},
            {data: 'hoTen'},
            {data: 'ngaySinh'},
            {data: 'gioiTinh'},
            {data: 'gioKham'},
            {data: 'bacSi'},
            {
                data:null,
                render: function(data, type, row){
                    return `<button class="btn btn-danger" onclick="cancelSchedule(${row.id})">Hủy</button>`;
                },
                orderable: false
            }
        ],
        order: [[0, 'desc']]
    });    
}