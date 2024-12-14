
const overlay = document.createElement('div');
overlay.className = 'overlay-toast';
overlay.style.position = 'fixed';
overlay.style.bottom = '10px';
overlay.style.right = '10px';   
overlay.style.zIndex = '9999';
document.body.appendChild(overlay);

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
    if (type === 'success') {
        toast.classList.add('bg-success', 'text-white');
    } else if (type === 'error') {
        toast.classList.add('bg-danger', 'text-white');
    } else if (type === 'warning') {
        toast.classList.add('bg-warning', 'text-dark');
    } else {
        toast.classList.add('bg-info', 'text-white');
    }
    toast.querySelector('.btn-close').addEventListener('click', function() {
        toast.remove();
    });

    overlay.appendChild(toast);
    setTimeout(function() {
        toast.remove();
    }, timeout);
}
