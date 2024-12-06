
document.querySelector('#toggle-close').addEventListener('click', function() {
    document.querySelector('#left-side').classList.toggle('close');
    localStorage.setItem('left-side', document.querySelector('#left-side').classList.contains('close'));
})

if (localStorage.getItem('left-side') === 'false') {
    document.querySelector('#left-side').classList.remove('close');
}