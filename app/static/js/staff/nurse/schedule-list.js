function init(){
    $("#schedule-table").addClass('table table-bordered table-hover');
    const table = $("#schedule-table").DataTable({
        serverSide: true,
        processing: true,
        ajax: {
            url: '/api/schedule-list',
            type: 'GET',
            data: function(d) {
                d.schedule_status = $("#status").val();
                d.date = $("#date").val();
                return $.extend({}, d, d.order.length ? {
                    "sort": d.columns[d.order[0].column].data,
                    "order": d.order[0].dir,
                } : {});
            }
        },
        columns: [
            {
                data:null,
                render: function(data, type, row){
                    return `<input type="checkbox" name="schedule_id" value="${row.id}">`;
                },
                orderable: false
            },
            {data: 'id'},
            {data: 'benhNhan_id'},
            {data: 'ho'},
            {data: 'ten'},
            {data: 'ngaySinh'},
            {data: 'gioiTinh'},
            {data: 'caHen'},
            {
                data:null,
                render: function(data, type, row){
                    trangThai = $('#status').val();
                    if (trangThai == 'false') {
                        return `<button class="btn btn-primary" onclick="acceptSchedule(${row.id})">Duyệt</button>`;    
                    }else{
                        return `<button class="btn btn-danger" onclick="cancelSchedule(${row.id})">Hủy</button> `;
                    }
                    
                },
                orderable: false
            }
        ],
        order: [[1, 'desc']],
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


    $("#status").change(function(){
        table.draw();
    });

    $("#date").change(function(){
        table.draw();
    });

    
}

function acceptSchedule(id){
    $.ajax({
        url: `/nurse/schedule/accept`,
        type: 'POST',
        data: {
            id: id
        },
        success: function(response){
            if(response.status){
                showToast('Thành công', response.message, 'success', 3000);
                $("#schedule-table").DataTable().draw();
            }
        }
    });
}

function cancelSchedule(id){
    $.ajax({
        url: `/nurse/schedule/cancel`,
        type: 'POST',
        data: {
            id: id
        },
        success: function(response){
            if(response.status){
                showToast('Thành công', response.message, 'success', 3000);
                $("#schedule-table").DataTable().draw();
            }
        }
    });
}

window.onload = () => {
    init();
}