// scripts.js
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('certificate-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const nameError = document.getElementById('nameError');
    const emailError = document.getElementById('emailError');

    form.addEventListener('submit', function (event) {
        let valid = true;

        // Clear previous errors
        nameError.style.display = 'none';
        emailError.style.display = 'none';

        // Validate name
        if (nameInput.value.length > 20) {
            valid = false;
            nameError.textContent = 'Name must be 20 characters or less';
            nameError.style.display = 'block';
        }

        // Validate email
        if (!validateEmail(emailInput.value)) {
            valid = false;
            emailError.textContent = 'Invalid email address';
            emailError.style.display = 'block';
        }

        if (!valid) {
            event.preventDefault();
        }
    });

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
});
