
const overlay = document.createElement('div');
overlay.className = 'overlay-toast';
overlay.style.position = 'fixed';
overlay.style.bottom = '10px';
overlay.style.right = '10px';   
overlay.style.zIndex = '9999';
document.body.appendChild(overlay);

const table_language_vn = {
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

function showToast(title, description, type, timeout,img="", time="Now") {
    const toast = document.createElement('div');
    toast.className = `toast mt-2`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    toast.style.display = 'block';
    toast.innerHTML = `
        <div class="toast-header">
        ${img ? `<img src="${img}" class="rounded me-2" alt="...">` : ''}
        <strong class="me-auto">${title}</strong>
        <small>${time}</small>
        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
        ${description}
        </div>
    `;
    toast.classList.add('bg-info', 'text-white');
    if (type === 'success') {
        toast.classList.add('bg-success', 'text-white');
    }
    if (type === 'error') {
        toast.classList.add('bg-danger', 'text-white');
    }
    if (type === 'warning') {
        toast.classList.add('bg-warning', 'text-dark');
    }
    toast.querySelector('.btn-close').addEventListener('click', function() {
        toast.remove();
    });
    toast.style.opacity = '0';
    toast.style.transform = 'scale(0.5) translateX(100%)';
    toast.style.transition = 'opacity 0.5s ease-in-out, transform 0.5s ease-in-out';
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'scale(1) translateX(0%)';
    });
    overlay.appendChild(toast);

    setTimeout(function() {
        toast.remove();
    }, timeout);
}
