let profile = null;
let  diseases = [];
let services = [];


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
                        <span>Mỗi</span><input type="number" class="form-control hourly mx-1" placeholder="Số giờ" value="6" style="width:70px;"><span>Tiếng</span>
                    </div>
                </div>
            </td>
            <td>
                <div class="d-flex align-items-center">
                    <select name="when" class="form-control when">
                        <option value="before" selected>Trước ăn</option>
                        <option value="after">Sau ăn</option>
                        <option value="none">Không</option>
                    </select>
                </div>
            </td>
            <td>
                <input type="number" class="form-control times" placeholder="Số lần" value="1" style="width: 80px;">                            
            </td>
            <td>
                <div class="d-flex align-items-center gap-2" style="width: 100px;">
                    <input type="number" class="form-control value" placeholder="Giá trị" value="1">
                    <span class="unit">Viên</span>
                </div>
            </td>
            <td>
                <select name="day" class="form-control day" style="width: 100px;">
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
            // Fetch data
            exist_med = []
            for (let e of $rows){
                const medicine = $(e).find(".recommend-input").attr("id-medicine")
                if (medicine != "") exist_med.push(medicine)
            }
            const data = await fetch(`/api/medicine?name=${text}&exists=${exist_med.join(",")}`)
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
            data.forEach((medicine, index) => {
                $recommend.append(`<li class="recommend-item" idx="${index}" id-medicine="${medicine.id}">${medicine.ten}</li>`);
            });
            
            $('.recommend .recommend-item').click(function() {
                const d = data[$(this).attr('idx')]
                if (d === undefined) return;
                if (d.so_luong <= 0) {
                    showToast("Lỗi", "Thuốc đã hết", "error", 5000)
                    return
                }
                $(this).closest('tr').find('.recommend-input').val($(this).text());
                $(this).closest('tr').find('.recommend-input').attr('id-medicine', d.id);
                $(this).closest('tr').find('.unit').text(d.don_vi);
            });    
        });

        $(this).find('.recommend-input').on('focusout', function() {
            setTimeout(()=> {
                $(this).closest('td').find('.recommend').removeClass('show');
            },300)
        });

            
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

    $("#search-service").on("input", async function() {
        $(".service-recommend").addClass("show");
        const text = $(this).val();
        const exists = services.join(",")
        const data = await fetch(`/api/get-services?q=${text}&exists=${exists}`)
            .then(response => response.json())
            .catch(error => {
                console.error('Error:', error);
                return {"error": "Error"};
            })
        const $recommend = $('.service-recommend ul');
        $recommend.empty();
        if (data.error) {
            $recommend.append(`<li class="recommend-item" style="color: red;">Không tìm thấy dịch vụ này</li>`);
            return;
        }
        data.forEach(service => {
            $recommend.append(`<li class="recommend-item" id-service="${service.id}">${service.ten_dich_vu}</li>`);
        });
        
        $(".service-recommend ul li").click(function() {
            const service = $(this).text();
            const id = $(this).attr("id-service")
            $("#search-service").val("");
            $(".service-recommend").removeClass("show");
            $(".service-list").append(`
                <li class="d-flex justify-content-between p-3 badge bg-primary text-white rounded" id-service="${id}">
                    ${service}
                </li>
            `);
            services.push(id);

            $(".service-list li").click(function() {
                $(this).remove();
            });
        });
    });
}

// function resetSearchMedicine(){
//     $(".recommend-input").off("input")
//     $(".recommend-input").click(function() {
//         $(this).closest('td').find('.recommend').addClass('show');
//     });
// }

$(document).ready(function() {
    init();
    $('#add-medical-btn').click(addRowToTable);   
});


function savePatient(){
    $(this).attr("disabled", true)
    if (profile == null){
        showToast("Lỗi", "Chưa chọn bệnh nhân", "error", 5000)
        $(this).attr("disabled", false)
        return
    }
    const rows = $("table tbody tr")
    const medicines = []
    for (let e of rows){
        const medicine = $(e).find(".recommend-input").attr("id-medicine")
        const method = $(e).find(".method").val()
        const morning = $(e).find("input.morning").val()
        const noon = $(e).find("input.noon").val()
        const evening = $(e).find("input.evening").val()
        const hourly = $(e).find("input.hourly").val()
        const when = $(e).find("select.when").val()
        const times = $(e).find("input.times").val()
        const value = $(e).find("input.value").val()
        const unit = $(e).find(".unit").text()
        const day = $(e).find("select.day").val()
        if (medicine == ""){
            $(this).attr("disabled", false)
            showToast("Lỗi", "Chưa nhập tên thuốc", "error", 5000)
            return
        }
        const data = {
            medicine: medicine,
            method: method,
            morning: morning,
            noon: noon,
            evening: evening,
            hourly: hourly,
            when: when,
            times: times,
            value: value,
            unit: unit,
            day: day
        }
        medicines.push(data)
    }
    // console.log(medicines)
    const id_services = []
    $("ul.service-list li").each(function(){
        id_services.push($(this).attr("id-service"))
    })



    const data = {
        examination_id: profile.id,
        medicines: medicines,
        diseases: diseases,
        result: {
            bloodType: $("#blood-type").val() || "Không có",
            bloodPressure: $("#blood-pressure").val() || "Không có",
        },
        services: id_services,
        note: $("#note").val() || "Không có"
    }
    // console.log(data)

    fetch("/api/save-examination", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
    .then(data => {
        if (!data){
            $(this).attr("disabled", false)
            showToast("Lỗi", data.error, "error", 5000)
            return
        }
        $(this).attr("disabled", false)
        showToast("Thành công", "Lưu thông tin bệnh nhân thành công", "success", 5000)
        resetRow()
        addRowToTable()
        diseases = []
        services = []
        $(".disease-list").empty()
        $(".service-list").empty()
        $("#note").val("")

        setTimeout(() => {
            location.reload()
        },2000)
    }).catch(error => {
        console.error('Error:', error);
        $(this).attr("disabled", false)
        showToast("Lỗi", data.error, "error", 5000)
    });
}


$("#save-btn").click(function(){
    savePatient()
    
})

// $(".search-disease> div> .btn").click(function(){
//     const disease =$(".search-disease").val()
//     $(".disease-list").append(`
//         <li class="d-flex justify-content-between p-3 badge bg-primary text-white rounded">
//             ${disease}
//         </li>
//     `);
//     $(".search-disease").val("");
// })