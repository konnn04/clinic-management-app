$(document).ready(function() {
    $('#example').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/invoices",
            "data": function(d) {
                console.log(d);
                return $.extend({}, d, {
                    "sort": d.columns[d.order[0].column].data,
                    "order": d.order[0].dir
                });
            }
        },
        "columns": [
            { "data": "id" },
            { "data": "ngayLapHoaDon" },
            { "data": "hoBenhNhan" },
            { "data": "tenBenhNhan" },
            { "data": "bacSi"},
            { "data": "tongTien" },
            { "data": "trangThai" },
            {"data": "action",
            orderable: false,
            "render": function(data, type, row) {
                return `
                    <button class="btn btn-primary btn-sm view-btn" data-id="${row.id}">Xem</button>
                `;
            }
        }
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
});