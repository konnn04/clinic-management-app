function addRowToTable() {
    const $tbody = $('tbody');
    const rowCount = $tbody.find('tr').length + 1;

    const newRow = `
        <tr>
            <td>${rowCount}</td>
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
    $("table tr").remove()
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
        // const data = await fetch(`/api/patient?name=${text}`)
        //     .then(response => response.json())
        //     .catch(error => {
        //         console.error('Error:', error);
        //         return {"error": "Error"};
        //     })
        const $recommend = $('.search-box .results ul');
        $recommend.empty();
        // if (data.error) {
        //     $recommend.append(`<li class="result-item" style="color: red;">Không tìm thấy bệnh nhân</li>`);
        //     return;
        // }
        const data = [{
            "id": 1,
            "name": "Nguyễn Văn A",
            "phone": "0123456789",
            "avatar": "https://www.pngarts.com/files/5/User-Avatar-PNG-Transparent-Image.png",
            "age:": 20,
            "gender": "Nam",
            "blood_type": "A",
            "last_examination": "20/10/2021"
        }]
        data.forEach(patient => {
            const $item = $('<li>', { class: 'result-item', 'id-patient': patient.id });
            $item.html(`
                <div class="d-flex align-items-center justify-content-between">
                <div class="avatar">
                    <img src="${patient.avatar}" alt="avatar">
                </div>
                <div class="info">
                    <h6>${patient.name}</h6>
                    <span>#${patient.id} | ${patient.phone}</span>
                </div>
                </div>
            `);
            $recommend.append($item);
            $item.click(function() {
                $(".profile").addClass("show");
                $(".prev-examination").addClass("show");
                $(".profile .avt #avt").attr("src", patient.avatar);
                $(".profile #name").text(patient.name);
                $(".profile #phone").text(patient.phone);
                $(".profile #age").text(patient.age);
                $(".profile #gender").text(patient.gender);
                $(".profile #blood-type").text(patient.blood_type);
                $(".profile #last-examination").text(patient.last_examination);
                resetRow()
                addRowToTable();             
            });
        });
    });
}



$(document).ready(function() {
    init();
    $('#add-medical-btn').click(addRowToTable);   
});
