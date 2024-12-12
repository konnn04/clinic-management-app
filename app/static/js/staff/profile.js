
function editProfileForm() {
    const inputs = document.querySelectorAll('.modify input')
    const textareas = document.querySelectorAll('.modify textarea')
    const p = document.querySelectorAll('.modify p')
    const submitGroup = document.getElementById('submit-group')

    p.forEach(p => {
        p.style.display = 'none'
    })

    inputs.forEach(input => {
        input.style.display = 'block'
    })

    textareas.forEach(textarea => {
        textarea.style.display = 'block'
    })

    submitGroup.style.display = 'block'
}

function viewForm() {
    document.getElementById('profile-form').reset()
    const inputs = document.querySelectorAll('.modify input')
    const textareas = document.querySelectorAll('.modify textarea')
    const p = document.querySelectorAll('.modify p')
    const submitGroup = document.getElementById('submit-group')
    p.forEach(p => {
        p.style.display = 'block'
    })

    inputs.forEach(input => {
        input.style.display = 'none'
    })

    textareas.forEach(textarea => {
        textarea.style.display = 'none'
    })

    submitGroup.style.display = 'none'
}

async function processImg(imgField){
    console.log('running')
    const originalFile = imgField.files[0]
    
    const resizedFile = await resizeAndCompressImg(originalFile)

    const dataTransfer = new DataTransfer()
    dataTransfer.items.add(resizedFile)

    imgField.files = dataTransfer.files

}

function resizeAndCompressImg(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onload = function (e) {
            const img = new Image()

            img.onload = function () {
                // Tạo canvas để chỉnh sửa kích thước
                const canvas = document.createElement("canvas")
                const ctx = canvas.getContext("2d")

                canvas.width = 512
                canvas.height = 512

                ctx.drawImage(img, 0, 0, 512, 512)

                // Chuyển canvas sang Blob để xử lý file phù hợp với form
                canvas.toBlob(
                    function (blob) {
                        if (blob) {
                            const resizedFile = new File([blob], file.name, {
                                type: "image/jpeg",
                                lastModified: Date.now(),
                            })
                            resolve(resizedFile)
                        } else {
                            reject("Failed to compress image.")
                        }
                    },
                    "image/jpeg",
                    0.7
                )
            }

            img.src = e.target.result
        }
        reader.readAsDataURL(file)
    })
}