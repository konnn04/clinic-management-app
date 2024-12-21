let profile = null;
let  diseases = [];


function addRowToTable() {
    const $tbody = $('tbody');
    const rowCount = $tbody.find('tr').length + 1;

    const newRow = `
        <tr>
            <td>
                <span>${rowCount}</span>
            </td>
            <td>
                <input type="text" class="form-control recommend-input" placeholder="Tên thuốc" id-medicine="">
                <div class="recommend">
                    <ul>
                        
                    </ul>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center" style="width: 100px;">
                    <select name="method" class="form-control method">
                        <option value="stc" selected>S/T/C</option>
                        <option value="hourly">Mỗi giờ</option>
                    </select>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center">
                    <div class="stc d-flex flex-column active">
                        <div class="d-flex">
                            <div class="col-4 px-1" style="width: 70px">
                                <input type="number" class="form-control morning" placeholder="Không có" value="6">
                            </div>
                            <div class="col-4 px-1" style="width: 70px">
                                <input type="number" class="form-control noon" placeholder="Không có" value="11">
                            </div>
                            <div class="col-4 px-1" style="width: 70px">
                                <input type="number" class="form-control evening" placeholder="Không có" value="18">
                            </div>
                        </div>
                    </div>
                    <div class="hourly d-flex align-items-center w-100">
                        <span>Mỗi</span><input type="number" class="form-control mx-1" placeholder="Số giờ" value="6" style="width:70px;"><span>Tiếng</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center">
                    <select name="when" class="form-control">
                        <option value="before" selected>Trước ăn</option>
                        <option value="after">Sau ăn</option>
                        <option value="none">Không</option>
                    </select>
                </div>
            </td>
            <td>
                <input type="number" class="form-control" placeholder="Số lần" value="1" style="width: 80px;">                            
            </td>
            <td>
                <div class="d-flex align-items-center gap-2" style="width: 100px;">
                    <input type="number" class="form-control" placeholder="Giá trị" value="1">
                    <span class="unit">Viên</span>
                </div>
            </td>
            <td>
                <select name="day" class="form-control" style="width: 100px;">
                    <option value="1" selected>Mỗi ngày</option>
                    <option value="2">Mỗi 2 ngày</option>
                    <option value="3">Mỗi 3 ngày</option>
                    <option value="4">Mỗi 4 ngày</option>
                    <option value="5">Mỗi 5 ngày</option>
                </select>
            </td>
            <td>
                ${rowCount > 1 ? `<button class="btn btn-danger" onclick="removeRow(this)"><i class="fas fa-trash"></i></button>` : ''}
            </td>
        </tr>
    `;

    $tbody.append(newRow);
    updateRowNumbers();
}

function resetRow(){
    $("table tbody tr").remove()
}

function removeRow(button) {
    $(button).closest('tr').remove();
    updateRowNumbers();
}

function updateRowNumbers() {
    const $rows = $('tbody tr');
    $rows.each(function(index) {
        $(this).find('td:first-child').text(index + 1);
        $(this).find('.method').change(function() {
            const method = $(this).val();
            const $stc = $(this).closest('tr').find('.stc');
            const $hourly = $(this).closest('tr').find('.hourly');
            if (method === 'stc') {
                $stc.addClass('active');
                $hourly.removeClass('active');
            } else {
                $stc.removeClass('active');
                $hourly.addClass('active');
            }
        });
        $(this).find('.recommend-input').on('input', async function() {
            $(this).closest('td').find('.recommend').addClass('show');
            const text = $(this).val();
            const data = await fetch(`/api/medicine?name=${text}`)
                .then(response => response.json())
                .catch(error => {
                    console.error('Error:', error);
                    return {"error": "Error"};
                })
            const $recommend = $(this).closest('td').find('.recommend ul');
            $recommend.empty();
            if (data.error) {
                $recommend.append(`<li class="recommend-item" style="color: red;">Không tìm thấy thuốc</li>`);
                return;
            }
            data.forEach(medicine => {
                $recommend.append(`<li class="recommend-item" id-medicine="${medicine.id}">${medicine.name}</li>`);
            });
        });
        $(this).find('.recommend-input').on('focusout', function() {
            $(this).closest('td').find('.recommend').removeClass('show');
        });
        // $(this).find('.recommend-input').on('focusin', function() {
            
        // });
        
    });
}
    
function init() {
    diseases = []
    let selected_patient = null;
    // Tìm kiếm bệnh nhân
    $(".search-box input").on("focus", function() {
        $(this).parent().addClass("show");
    });
    
    $(".search-box input").on("focusout", function() {
        setTimeout(()=>{
            $(this).parent().removeClass("show");
        },200)
    });
    
    // Tìm bệnh nhân
    $(".search-box input").on("input", async function() {
        const text = $(this).val();
        const data = await fetch(`/api/schedules-overview?q=${text}`)
            .then(response => response.json())
            .catch(error => {
                console.error('Error:', error);
                return {"error": "Error"};
            })
        const $recommend = $('.search-box .results ul');
        $recommend.empty();
        if (data.error) {
            $recommend.append(`<li class="result-item" style="color: red;">Không tìm thấy bệnh nhân</li>`);
            return;
        }

        data.forEach(patient => {
            const $item = $('<li>', { class: 'result-item', 'id-patient': patient.id });
            $item.html(`
                <div class="d-flex align-items-center justify-content-between">
                <div class="avatar">
                    <img src='/static/images/user.png' alt="avatar">
                </div>
                <div class="info">
                    <h6>${patient.ho} ${patient.ten}</h6>
                    <span>#${patient.nguoi_benh_id} | ${patient.sdt}</span>
                </div>
                </div>
            `);
            $recommend.append($item);
            selected_patient = patient;
            $item.click(function() {
                $(".profile").addClass("show");
                $(".prev-examination").addClass("show");
                $(".profile .avt #avt").attr("src", '/static/images/user.png');
                $(".profile #name").text(`${patient.ho} ${patient.ten}`);
                $(".profile #phone").text(patient.sdt);
                $(".profile #age").text(patient.tuoi);
                $(".profile #gender").text(patient.gioi_tinh);
                $(".profile #blood-type").text(patient.nhom_mau);
                $(".profile #last-examination").text("Chưa khám");
                resetRow()
                addRowToTable();  
                profile = patient;           
            });
        });
    });

    // Tìm bệnh
    $("#search-disease").on("input", async function() {
        $(".disease-recommend").addClass("show");
        const text = $(this).val();
        const exists = diseases.join(",")
        const data = await fetch(`/api/get-dieases?q=${text}&exists=${exists}`)
            .then(response => response.json())
            .catch(error => {
                console.error('Error:', error);
                return {"error": "Error"};
            })
        const $recommend = $('.disease-recommend ul');
        $recommend.empty();
        if (data.error) {
            $recommend.append(`<li class="recommend-item" style="color: red;">Không tìm thấy bệnh</li>`);
            return;
        }
        data.forEach(disease => {
            $recommend.append(`<li class="recommend-item" id-disease="">${disease}</li>`);
        });
        
        $(".disease-recommend ul li").click(function() {
            const disease = $(this).text();
            $("#search-disease").val("");
            $(".disease-recommend").removeClass("show");
            $(".disease-list").append(`
                <li class="d-flex justify-content-between p-3 badge bg-primary text-white rounded">
                    ${disease}
                </li>
            `);
            diseases.push(disease);

            $(".disease-list li").click(function() {
                $(this).remove();
            });
        });



    });
}



$(document).ready(function() {
    init();
    $('#add-medical-btn').click(addRowToTable);   
});


function savePatient(){
    if (profile == null){
        showToast("Lỗi", "Chưa chọn bệnh nhân", "error", 5000)
        return
    }
    const rows = $("table tbody tr")
    const medicines = []
    rows.each(function(index) {
        if ($(this).find('.recommend-input').val() == ""){
            showToast("Lỗi", "Chưa nhập tên thuốc", "error", 5000)
            return
        }
        if (diseases.length == 0){
            showToast("Lỗi", "Chưa chọn bệnh", "error", 5000)
            return
        }
        const medicine = {
            name: $(this).find('.recommend-input').val(),
            method: $(this).find('.method').val(),
            morning: $(this).find('.morning').val(),
            noon: $(this).find('.noon').val(),
            evening: $(this).find('.evening').val(),
            hourly: $(this).find('.hourly input').val(),
            when: $(this).find('select[name="when"]').val(),
            times: $(this).find('input[type="number"]').val(),
            value: $(this).find('input[type="number"]').val(),
            // unit: $(this).find('.unit').text(),
            day: $(this).find('select[name="day"]').val()
        }
        medicines.push(medicine)
    });
    console.log(medicines)
    const data = {
        patient: profile.id,
        medicines: medicines,
        diseases: diseases
    }
    console.log(data)
}