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

function initLagreView() {
    data = getListExamination_v1('ngay_kham', 'desc', 1)
}

function getListExamination_v1(col_sort, order, page_index){
    fetch(`/api/examination-list-v1?col_sort=${col_sort}&order=${order}&page_index=${page_index}`)
    .then(res => res.json())
    .then(data =>{
        $('#next_page').prop( "disabled", !data.next)
        $('#prev_page').prop( "disabled", !data.prev)
        $('#page_index').val(data.page_index)
        $('.examination_item').remove()
        console.log(data)
        data.data.forEach((e,i) => {
            $('.parients-container').append(`
                <div class="examination_item card p-3 card-profile shadow-sm">
                    <div class="d-flex align-items-center mb-3">
                        <div class="profile-img me-3" style="width: 50px; height: 50px;">
                            <img src="{{url_for('static', filename='images/user.png')}}" alt="" class="w-100">
                        </div>
                        <div>
                            <div class="name-header">${e.ho_benh_nhan} ${e.ten_benh_nhan}</div>
                            <div class="text-muted d-flex align-items-center">
                                <span class="hash-id me-2">#${e.id}</span>
                                <span class="text-primary">34 yrs | ${e.gioi_tinh}</span>
                            </div>
                        </div>
                        <div class="ms-auto">
                            <i class="bi bi-three-dots-vertical"></i>
                        </div>
                    </div>
                    <div class="info-item mb-2">
                        <span class="text-muted">Blood Group:</span>
                        <strong class="text-primary">O+</strong>
                    </div>
                    <div class="info-item mb-2">
                        <span class="text-muted">Phone:</span>
                        <strong class="text-primary">${e.so_dien_thoai}</strong>
                    </div>
                    <div class="info-item mb-2">
                        <span class="text-muted">Doctor Assigned:</span>
                        <strong class="text-primary">>${e.ho_bac_si} ${e.ten_bac_si}</strong>
                    </div>
                    <div class="info-item mb-2">
                        <span class="text-muted">Last Visit:</span>
                        <strong class="text-primary">${e.ngay_kham}</strong>
                    </div>
                </div>
            `)
        });
        
    })
    .catch(err => {})
}

window.onload = () =>{
    init()
    initLagreView()
}