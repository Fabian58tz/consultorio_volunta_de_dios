document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const emailError = document.getElementById('emailError');
    const passwordError = document.getElementById('passwordError');

    // IMPORTANTE: Para que esto funcione, este script DEBE estar en un archivo .html
    // que sea procesado por el motor de plantillas de Django (por ejemplo, login.html).
    // Si este script está en un archivo .js externo, Django NO procesará {% url %}.
    // En ese caso, la URL debe pasarse al script de otra manera (ver nota abajo).
   const principalPageUrl = DJANGO_URLS.principal; 
    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevenir el envío predeterminado del formulario

        let isValid = true;

        // Restablecer errores anteriores
        emailInput.classList.remove('is-invalid');
        passwordInput.classList.remove('is-invalid');
        emailError.textContent = '';
        passwordError.textContent = '';

        // 1. Validar el campo de correo electrónico
        if (emailInput.value.trim() === '') {
            emailInput.classList.add('is-invalid');
            emailError.textContent = 'El correo electrónico no puede estar vacío.';
            isValid = false;
        } else if (!isValidEmail(emailInput.value.trim())) {
            emailInput.classList.add('is-invalid');
            emailError.textContent = 'Por favor, introduce un correo electrónico válido.';
            isValid = false;
        }

        // 2. Validar el campo de contraseña
        if (passwordInput.value.trim() === '') {
            passwordInput.classList.add('is-invalid');
            passwordError.textContent = 'La contraseña no puede estar vacía.';
            isValid = false;
        }

        // Si todas las validaciones pasan, redirigir a la URL de Django
        if (isValid) {
            window.location.href = principalPageUrl; // Usa la URL de Django pre-calculada
        }
    });

    // Función para validar el formato del correo electrónico
    function isValidEmail(email) {
        // Expresión regular básica para validación de correo electrónico
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }
});