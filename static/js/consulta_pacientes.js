 // Listener para el envío del formulario (botón "Guardar")
            registrationForm.addEventListener('submit', function(event) {
                event.preventDefault(); // Previene el envío predeterminado

                registrationForm.classList.remove('was-validated'); // Limpia validaciones previas

                let allFieldsFilled = true;
                // Los campos marcados como 'required' en el HTML ya son validados por el navegador.
                // Aquí se puede añadir validación personalizada si se necesita.

                // Iterar sobre los campos requeridos para mostrar mensajes personalizados si no usamos Bootstrap validation feedback
                const requiredFields = registrationForm.querySelectorAll('[required]');

                for (const field of requiredFields) {
                    if (field.value.trim() === '') {
                        allFieldsFilled = false;
                        alert('Por favor, llena el campo: ' + (field.previousElementSibling ? field.previousElementSibling.textContent : field.id));
                        field.focus();
                        return; // Detiene el envío si un campo requerido está vacío
                    }
                }

                // Validar el formato del correo electrónico
                const correoInput = document.getElementById('correo');
                if (correoInput && correoInput.value.trim() !== '' && !validarEmail(correoInput.value)) {
                    allFieldsFilled = false;
                    alert('Por favor, ingresa un correo electrónico válido.');
                    correoInput.focus();
                    return; // Detiene el envío si el correo es inválido
                }

                // Si todas las validaciones pasan
                if (allFieldsFilled) {
                    const formData = new FormData(registrationForm);
                    const patientData = {};
                    formData.forEach((value, key) => {
                        patientData[key] = value;
                    });

                    console.log('Datos del paciente:', patientData);
                    alert('¡Paciente registrado correctamente!');

                    // Aquí iría tu código para enviar los datos a un servidor (fetch, XMLHttpRequest, etc.)
                    // fetch('/api/register-patient', { /* ... */ });

                    registrationForm.reset(); // Limpia el formulario después de un registro exitoso
                }
                // Si usas validación de Bootstrap, podrías agregar la clase 'was-validated' aquí para mostrar los estilos de validación
                // registrationForm.classList.add('was-validated'); 
            });

            // Listener para el botón "Cancelar" (reiniciar formulario)
            registrationForm.addEventListener('reset', function() {
                alert('Todos los campos han sido limpiados.');
                registrationForm.classList.remove('was-validated'); // Remueve la clase de validación al resetear
            });
        