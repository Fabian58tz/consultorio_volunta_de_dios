document.addEventListener('DOMContentLoaded', function() {
    const saveRecetaBtn = document.getElementById('saveRecetaBtn');
    const clearRecetaBtn = document.getElementById('clearRecetaBtn');
    const nombrePacienteInput = document.getElementById('nombrePaciente');
    const nombreMedicamentoInput = document.getElementById('nombreMedicamento');
    const dosisInput = document.getElementById('dosis');
    const frecuenciaInput = document.getElementById('frecuencia');
    const indicacionesTextarea = document.getElementById('indicaciones');
    const messageArea = document.getElementById('messageArea');

    // Función para mostrar mensajes de alerta de Bootstrap
    function displayMessage(message, type) {
        messageArea.innerHTML = message; // Usar innerHTML para permitir negritas
        messageArea.className = 'message-area'; // Restablecer clases
        if (type === 'success') {
            messageArea.classList.add('alert', 'alert-success');
        } else if (type === 'error') {
            messageArea.classList.add('alert', 'alert-danger');
        }
        messageArea.style.display = 'block'; // Mostrar el div
    }

    // Función para limpiar mensajes
    function clearMessage() {
        messageArea.innerHTML = '';
        messageArea.className = 'message-area'; // Restablecer clases a la base
        messageArea.style.display = 'none'; // Ocultar el div
    }

    // Función para limpiar todos los campos del formulario
    function clearFormFields() {
        nombrePacienteInput.value = '';
        nombreMedicamentoInput.value = '';
        dosisInput.value = '';
        frecuenciaInput.value = '';
        indicacionesTextarea.value = '';
        clearMessage(); // Limpiar también los mensajes al limpiar los campos
    }

    // Evento de clic para el botón Guardar
    saveRecetaBtn.addEventListener('click', function(event) {
        event.preventDefault(); // Evitar que el formulario se envíe por defecto
        clearMessage(); // Limpiar mensajes anteriores

        const nombrePaciente = nombrePacienteInput.value.trim();
        const nombreMedicamento = nombreMedicamentoInput.value.trim();
        const dosis = dosisInput.value.trim();
        const frecuencia = frecuenciaInput.value.trim();
        const indicaciones = indicacionesTextarea.value.trim();

        // Validaciones individuales para cada campo requerido
        if (!nombrePaciente) {
            displayMessage('Por favor, llene el campo **Nombre del paciente**.', 'error');
            nombrePacienteInput.focus();
            return;
        }
        if (!nombreMedicamento) {
            displayMessage('Por favor, llene el campo **Nombre del medicamento**.', 'error');
            nombreMedicamentoInput.focus();
            return;
        }
        if (!dosis) {
            displayMessage('Por favor, llene el campo **Dosis**.', 'error');
            dosisInput.focus();
            return;
        }
        if (!frecuencia) {
            displayMessage('Por favor, llene el campo **Frecuencia**.', 'error');
            frecuenciaInput.focus();
            return;
        }
        if (!indicaciones) {
            displayMessage('Por favor, llene el campo **Indicaciones**.', 'error');
            indicacionesTextarea.focus();
            return;
        }

        // Si todas las validaciones pasan, proceder a guardar (simulado)
        console.log('Datos de la receta a guardar:');
        console.log({
            nombrePaciente: nombrePaciente,
            nombreMedicamento: nombreMedicamento,
            dosis: dosis,
            frecuencia: frecuencia,
            indicaciones: indicaciones
        });

        // Simular una llamada a una API que siempre tiene éxito
        setTimeout(() => {
            displayMessage('¡Receta guardada exitosamente!', 'success');
            clearFormFields(); // Limpiar los campos después de un guardado exitoso
        }, 500); // Retraso de 500ms para simular la respuesta del servidor

        /*
        // Ejemplo de cómo harías una solicitud real con fetch (descomenta para usar)
        fetch('/api/save-receta', { // Reemplaza con la URL de tu API
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                nombrePaciente: nombrePaciente,
                nombreMedicamento: nombreMedicamento,
                dosis: dosis,
                frecuencia: frecuencia,
                indicaciones: indicaciones
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la red o en el servidor: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayMessage('¡Receta guardada exitosamente!', 'success');
                clearFormFields();
            } else {
                displayMessage('Error al guardar la receta: ' + (data.message || 'Error desconocido'), 'error');
            }
        })
        .catch((error) => {
            console.error('Error al guardar la receta:', error);
            displayMessage('Error de conexión o problema al guardar la receta.', 'error');
        });
        */
    });

    // Evento de clic para el botón Eliminar/Limpiar
    clearRecetaBtn.addEventListener('click', function() {
        clearFormFields();
        displayMessage('Los campos han sido limpiados.', 'success');
    });
});