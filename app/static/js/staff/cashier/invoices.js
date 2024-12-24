$(document).ready(function () {
    // Initialize DataTable
    $('#example').DataTable({
        "processing": true,
        "serverSide": true,
        "ajax": {
            "url": "/api/invoices",
            "data": function (d) {
                return $.extend({}, d, {
                    "sort": d.columns[d.order[0].column].data,
                    "order": d.order[0].dir
                });
            }
        },
        "columns": [
            {"data": "id"},
            {"data": "ngayLapHoaDon"},
            {"data": "hoBenhNhan"},
            {"data": "tenBenhNhan"},
            {"data": "bacSi"},
            {"data": "tongTien"},
            {"data": "trangThai"},
            {
                "data": "action",
                "orderable": false,
                "render": function (data, type, row) {
                    if (row.trangThai == true) {
                        return `
                        <button class="btn btn-primary btn-sm view-btn" data-id="${row.id}">Xem</button>
                        `;
                    } else return `
                        <button class="btn btn-primary btn-sm view-btn" data-id="${row.id}">Xem</button>
                        <button class="btn btn-success btn-sm pay-btn" data-id="${row.id}">Thanh toán</button>
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

    $(document).on('click', '.view-btn', function () {
        const invoiceId = $(this).data('id');
        handleViewInvoice(invoiceId);
    });

    $(document).on('click', '.pay-btn', function () {
        const invoiceId = $(this).data('id');
        handlePayInvoice(invoiceId);
    });

});

async function handleViewInvoice(invoiceId) {
    console.log(invoiceId);
    window.open(`/cashier/invoice/${invoiceId}`, '_blank');
}

function handlePayInvoice(invoiceId) {
    if (confirm('Bạn có chắc chắn muốn thanh toán hóa đơn này?')) {
        window.open(`/cashier/payment/${invoiceId}`, '_blank');
    }
}