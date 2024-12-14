
document.querySelector('#toggle-close').addEventListener('click', function() {
    document.querySelector('main').classList.toggle('close');
    localStorage.setItem('left-side', document.querySelector('main').classList.contains('close'));
})

if (localStorage.getItem('left-side') === 'false') {
    document.querySelector('main').classList.remove('close');
}

setTimeout(function() {
    document.querySelector('#left-side').style.transition = 'all .3s';
    document.querySelectorAll('#left-side *').forEach(function(element) {
        element.style.transition = 'all .3s';
    });
}, 10);


