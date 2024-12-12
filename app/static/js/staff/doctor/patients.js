function init() {
    const viewTypeBtn = document.querySelector('#view-type');
    const sortBtn = document.querySelector('#sort-type');
    const main = document.querySelector('main');

    viewTypeBtn.addEventListener('click', function() {
        main.classList.toggle('list-view');
        viewTypeBtn.querySelector('i').classList.toggle('fa-th');
        viewTypeBtn.querySelector('i').classList.toggle('fa-list');
    });

    sortBtn.addEventListener('click', function() {
        main.classList.toggle('desc');
        sortBtn.querySelector('i').classList.toggle('fa-sort-amount-up');
        sortBtn.querySelector('i').classList.toggle('fa-sort-amount-down');
    });
}

init()