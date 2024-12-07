function editProfileForm() {
        const inputFields = document.querySelectorAll('input[type="text"]');
        const textValues = document.querySelectorAll('.text-value');
        const submitGroup = document.getElementById('submit-group');

        inputFields.forEach(input => {
            if (input.id === 'input-id' || input.id === 'input-taiKhoan' )
                input.readOnly=true
            input.style.display = 'block';
        });

        textValues.forEach(text => {
            text.style.display = 'none';
        });

        submitGroup.style.display = 'block';
}

function viewForm() {
    document.getElementById('profile-form').reset();

        const inputs = document.querySelectorAll('#profile-form input');
        inputs.forEach(input => {
            const valueElement = document.getElementById('value-' + input.name);
            if (valueElement) {
                valueElement.style.display = 'block';
            }
            input.style.display = 'none';
        });

        document.getElementById('submit-group').style.display = 'none';
}